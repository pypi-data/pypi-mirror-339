import io
import json
import os.path
import re
from collections.abc import Callable
from typing import IO, Optional

import click

from cmake_presets_exploder import Exploder, explode_presets


def _generate_schema(ctx: click.Context, _, value):
    if not value or ctx.resilient_parsing:
        return

    indent = ctx.params.get("indent", 2)
    if indent < 0:
        indent = None
    click.echo(json.dumps(Exploder.model_json_schema(), indent=indent))
    ctx.exit(0)


@click.command()
@click.argument(
    "template_path",
    type=click.Path(
        dir_okay=False,
        exists=True,
        readable=True,
        allow_dash=True,
    ),
    required=False,
)
@click.option(
    "--loader",
    "-l",
    type=click.Choice(("json", "toml", "yaml")),
    default="json",
    show_default=True,
    help="""Template file format. Parsing YAML requires that the package was
    installed with optional [yaml] extra. Parsing TOML requires Python >=3.11
    or that the package was installed with the [toml] extra.""",
)
@click.option(
    "-o",
    "--output",
    default="-",
    type=click.Path(dir_okay=False, writable=True, allow_dash=True),
    help="""File to write to; use '-' for stdout (the default).""",
)
@click.option(
    "--indent",
    "-i",
    type=int,
    is_eager=True,
    default=2,
    show_default=True,
    help="""JSON indent size in spaces; pass negative number for no
    indent.""",
)
@click.option(
    "--ignore-formatting",
    is_flag=True,
    help="""Do not write to output file if it would only change formatting of
    the JSON, including ordering of object properties.""",
)
@click.option(
    "--verify",
    is_flag=True,
    help="""Instead of writing to output, verify that output file would not be
    changed (applying same logic if --ignore-formatting is passed), and exit
    with non-zero code if it would.""",
)
@click.option(
    "--include-vendor",
    is_flag=True,
    help="""Include the 'exploder' object (or whatever name is passed to
    --vendor-name option) in the 'vendor' section of output presets JSON.""",
)
@click.option(
    "--vendor-name",
    default="exploder",
    show_default=True,
    help="""Name of the property in the 'vendor' object of the template to
    look for matrix configuration.""",
)
@click.option(
    "--generate-schema",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=_generate_schema,
    help="""Print JSON schema for the vendor object and exit.""",
)
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    template_path: Optional[str],
    loader: str,
    output: str,
    indent: int,
    ignore_formatting: bool,
    verify: bool,
    include_vendor: bool,
    vendor_name: str,
) -> None:
    """
    Generate CMake presets JSON from template specified in TEMPLATE_PATH.

    If TEMPLATE_PATH not provided, defaults to CMakePresetsMatrixTemplate.json
    or CMakePresetsMatrixTemplate.{type} if a different type is passed to
    --loader. If -, reads from stdin.
    """

    if template_path is None:
        template_path = f"CMakePresetsMatrixTemplate.{loader}"
        click.Path(exists=True, readable=True, dir_okay=False).convert(
            template_path, None, ctx
        )

    if verify or ignore_formatting:
        if output == "-":
            raise click.UsageError(
                "cannot use --verify/--ignore-formatting with stdout output "
                "(did you specify a path with --output?)"
            )
        if not os.path.exists(output):
            raise click.ClickException(f"path does not exist: {output}")

    if output == template_path and not output == "-":
        raise click.ClickException(
            "output file cannot be the same as input file"
        )

    template = _read_template_json(template_path, loader)
    try:
        presets = explode_presets(
            template,
            include_vendor=include_vendor,
            vendor_name=vendor_name,
        )
    except ValueError as e:
        raise click.ClickException(str(e)) from None

    if verify:
        if _would_change_output(presets, output, indent, ignore_formatting):
            raise click.ClickException(f"{output} would be changed")
        click.echo(f"No changes to {output}", err=True)
    elif not ignore_formatting or _would_change_output(
        presets, output, indent, ignore_formatting
    ):
        with click.open_file(output, "w") as f:
            _write_json(f, presets, indent)


def _read_template_json(path: str, loader_type: str) -> dict:
    with click.open_file(path) as f:
        text = f.read()

    loader: Callable[[str, str], object] = {
        "json": _load_json,
        "toml": _load_toml,
        "yaml": _load_yaml,
    }[loader_type]
    data = loader(text, "<stdin>" if path == "-" else path)
    if not isinstance(data, dict):
        raise click.ClickException(
            "template file must contain an object at top-level, "
            f"got {type(data).__name__}"
        )

    return data


def _load_json(text: str, path: str) -> object:
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        msg = _format_parse_error(
            text=text,
            path=path,
            error=error.msg,
            pos=(error.lineno - 1, error.colno - 1),
        )
        raise click.ClickException(f"JSON parse error: {msg}") from None


def _load_yaml(text: str, path: str) -> object:
    try:
        import yaml  # type: ignore
    except ImportError as e:
        msg = (
            "PyYAML is required to parse YAML files. "
            "Did you install with [yaml] extra?"
        )
        raise click.ClickException(msg) from e

    from yaml.error import MarkedYAMLError, YAMLError  # type: ignore

    try:
        return yaml.safe_load(text)
    except YAMLError as err:
        if isinstance(err, MarkedYAMLError):
            pos = err.problem_mark
            if pos is None:
                msg = str(err)
            else:
                msg = _format_parse_error(
                    text=text,
                    path=path,
                    error=err.problem or str(err),
                    pos=(pos.line, pos.column),
                )
        else:
            msg = str(err)
        raise click.ClickException(f"YAML parse error: {msg}") from None


def _parse_toml_err_msg(
    msg: str,
) -> Optional[tuple[str, Optional[int], Optional[int]]]:
    loc = r"(?:line\ (?P<lineno>\d+),\ col(?:umn)?\ (?P<colno>\d+))"
    match = re.match(
        rf"^(?P<msg>.+?) \(at (?:(?P<end>end of document)|{loc})\)",
        msg,
    )
    if not match:
        return None

    if match.group("end"):
        lineno = colno = None
    else:
        lineno = int(match.group("lineno"))
        colno = int(match.group("colno"))

    return match.group("msg"), lineno, colno


def _format_toml_parse_error(err: Exception, text: str, path: str) -> str:
    lineno: Optional[int] = getattr(err, "lineno", None)
    colno: Optional[int] = getattr(err, "colno", None)
    if lineno is None or colno is None:
        err_info = _parse_toml_err_msg(str(err))
        if not err_info:
            return str(err)
        msg, lineno, colno = err_info
    else:
        msg = getattr(err, "msg", str(err))

    if lineno is None or colno is None:
        pos = None
    else:
        pos = (lineno - 1, colno - 1)

    return _format_parse_error(
        text=text,
        path=path,
        error=msg,
        pos=pos,
    )


def _load_toml(text: str, path: str) -> dict:
    import sys

    if sys.version_info >= (3, 11):
        import tomllib
    else:
        try:
            import tomli as tomllib
        except ImportError:
            msg = (
                "tomli is required to parse TOML files on Python < 3.11. "
                "Did you install with [toml] extra?"
            )
            raise click.ClickException(msg) from None

    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as err:
        msg = _format_toml_parse_error(err, text, path)
        raise click.ClickException(f"TOML parse error: {msg}") from None


def _format_parse_error(
    *,
    text: str,
    path: str,
    error: str,
    pos: Optional[tuple[int, int]],
    lines_before: int = 2,
) -> str:
    """
    Argument `pos` is a tuple of 0-index (lineno, colno) or `None`; if `None`,
    position is assumed to be end.
    """
    if lines_before < 0:
        raise ValueError("lines_before must be >= 0")

    lines = text.splitlines()
    if pos:
        lineno, colno = pos
        if lineno < 0:
            raise ValueError("lineno must be >= 0")
        if colno < 0:
            raise ValueError("colno must be >= 0")
    else:
        lineno = len(lines) - 1
        colno = len(lines[-1])

    start_line = max(0, lineno - lines_before)
    lineno_str_width = len(str(lineno + 1))
    lines = lines[start_line : lineno + 1]
    msg = [f"{path}, line {lineno + 1}, col {colno + 1}: {error}"]
    for n, line in enumerate(lines, start=start_line):
        margin = f" {n + 1:>{lineno_str_width}}"
        if n == lineno and len(line) > colno:
            # Color the offending character bold red
            line = "".join(
                (
                    line[:colno],
                    click.style(line[colno], fg="red", bold=True),
                    line[colno + 1 :],
                )
            )

        msg.append(f"{margin} | {line}")
        if n == lineno:
            indicator = click.style("^", fg="red", bold=True)
            msg.append(f"{' ' * len(margin)} | {' ' * colno}{indicator}")

    return "\n".join(msg)


def _would_change_output(
    presets: dict,
    output_path: str,
    indent: int,
    ignore_formatting: bool,
) -> bool:
    if ignore_formatting:
        with open(output_path) as f:
            return presets != json.load(f)

    with io.StringIO() as buf:
        _write_json(buf, presets, indent)
        buf.seek(0)
        with open(output_path) as f:
            return not _file_cmp(buf, f)


def _file_cmp(f1: IO[str], f2: IO[str], chunksize: int = 1024) -> bool:
    while True:
        data = f1.read(chunksize)
        if data != f2.read(chunksize):
            return False
        if not data:
            return True


def _write_json(f: IO[str], obj: dict, indent: int):
    json.dump(obj, f, indent=indent if indent >= 0 else None)
    f.write("\n")
