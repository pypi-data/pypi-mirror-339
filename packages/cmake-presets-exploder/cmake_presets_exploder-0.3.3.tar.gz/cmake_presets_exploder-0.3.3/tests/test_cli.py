import json
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Optional

import pytest
from click.testing import CliRunner

from cmake_presets_exploder.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@dataclass
class PresetsPaths:
    template: Path
    presets: Path


EXAMPLE_TEMPLATE = {
    "version": 5,
    "configurePresets": [
        {
            "name": "base",
            "toolchainFile": "toolchain",
        },
    ],
    "vendor": {
        "exploder": {
            "version": 0,
            "presetGroups": {
                "configure": {
                    "type": "configure",
                    "inherits": ["base"],
                    "parameters": {
                        "alpha": {"a": "A Value", "b": "B Value"},
                        "num": ["1", "2"],
                    },
                    "templates": {
                        "alpha": {
                            "cacheVariables_{name}": {
                                "ALPHA": "{value}",
                            },
                        },
                    },
                }
            },
        }
    },
}


@pytest.fixture
def generated_presets(runner: CliRunner, tmp_path: Path) -> PresetsPaths:
    template_path = tmp_path / "template.json"
    with template_path.open("w") as f:
        json.dump(EXAMPLE_TEMPLATE, f, indent=2)

    presets_path = tmp_path / "presets.json"
    res = runner.invoke(
        cli,
        [f"--output={presets_path}", str(template_path)],
    )
    assert res.exit_code == 0
    return PresetsPaths(template=template_path, presets=presets_path)


@pytest.mark.parametrize("indent", (None, -1, 0, 4))
def test_output_file_has_newline(
    runner: CliRunner,
    tmp_path: Path,
    indent: Optional[int],
) -> None:
    output = tmp_path / "presets.json"
    res = runner.invoke(
        cli,
        [
            f"--output={output}",
            *(("--indent", str(indent)) if indent is not None else ()),
            "-",
        ],
        input=json.dumps(EXAMPLE_TEMPLATE),
    )
    assert res.exit_code == 0
    assert output.read_text().endswith("\n")


@pytest.mark.parametrize("indent", (None, -1, 0, 4))
def test_output_to_stdout_has_newline(
    runner: CliRunner,
    indent: Optional[int],
) -> None:
    res = runner.invoke(
        cli,
        [
            *(("--indent", str(indent)) if indent is not None else ()),
            "-",
        ],
        input=json.dumps(EXAMPLE_TEMPLATE),
    )
    assert res.exit_code == 0
    assert res.output.endswith("\n")


def test_file_unchanged_with_same_template(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            f"--output={generated_presets.presets}",
            str(generated_presets.template),
        ],
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text()


def test_verify_with_unchanged_file_succeeds(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            "--verify",
            f"--output={generated_presets.presets}",
            str(generated_presets.template),
        ],
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text()


@pytest.mark.parametrize("ignore_formatting", (True, False))
def test_output_always_overwritten_if_structure_changed(
    runner: CliRunner,
    generated_presets: PresetsPaths,
    ignore_formatting: bool,
):
    original_presets = generated_presets.presets.read_text()
    generated_presets.presets.write_text("{}\n")
    res = runner.invoke(
        cli,
        [
            "--ignore-formatting",
            f"--output={generated_presets.presets}",
            *(("--ignore-formatting",) if ignore_formatting else ()),
            str(generated_presets.template),
        ],
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text(), (
        "File not overwritten"
    )


@pytest.mark.parametrize("ignore_formatting", (True, False))
def test_verify_always_fails_if_structure_changed(
    runner: CliRunner,
    generated_presets: PresetsPaths,
    ignore_formatting: bool,
) -> None:
    new_file_content = "{}\n"
    generated_presets.presets.write_text(new_file_content)
    res = runner.invoke(
        cli,
        [
            "--ignore-formatting",
            "--verify",
            f"--output={generated_presets.presets}",
            *(("--ignore-formatting",) if ignore_formatting else ()),
            str(generated_presets.template),
        ],
    )
    assert res.exit_code != 0, res.output
    assert new_file_content == generated_presets.presets.read_text(), (
        "Files changed"
    )


def test_verify_with_changed_file_formatting_fails(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            "--verify",
            "--indent=4",  # different file indent
            f"--output={generated_presets.presets}",
            str(generated_presets.template),
        ],
    )
    assert res.exit_code != 0, res.output
    assert original_presets == generated_presets.presets.read_text()


def test_fails_with_ignore_formatting_and_stdout(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    res = runner.invoke(
        cli,
        [
            "--ignore-formatting",
            "--output=-",
            str(generated_presets.template),
        ],
    )
    assert res.exit_code != 0


def test_ignore_formatting_does_not_change_output_with_different_whitespace(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            "--indent=4",  # different file indent
            "--ignore-formatting",
            f"--output={generated_presets.presets}",
            str(generated_presets.template),
        ],
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text(), (
        "File changed"
    )


def test_verify_with_ignore_formatting_does_not_fail_with_different_whitespace(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            "--indent=4",  # different file indent
            "--ignore-formatting",
            "--verify",
            f"--output={generated_presets.presets}",
            str(generated_presets.template),
        ],
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text(), (
        "File changed"
    )


def test_ignore_formatting_does_not_change_output_with_different_prop_order(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    with open(generated_presets.template) as f:
        old_template = json.load(f)

    # Move the 'version' property to end of object
    template = old_template.copy()
    template["version"] = template.pop("version")
    template_json = json.dumps(template)
    assert template_json != json.dumps(old_template)

    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            "--ignore-formatting",
            f"--output={generated_presets.presets}",
            "-",
        ],
        input=template_json,
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text(), (
        "File changed"
    )


def test_verify_with_ignore_formatting_does_not_fail_with_different_prop_order(
    runner: CliRunner, generated_presets: PresetsPaths
) -> None:
    with open(generated_presets.template) as f:
        old_template = json.load(f)

    # Move the 'version' property to end of object
    template = old_template.copy()
    template["version"] = template.pop("version")
    template_json = json.dumps(template)
    assert template_json != json.dumps(old_template)

    original_presets = generated_presets.presets.read_text()
    res = runner.invoke(
        cli,
        [
            "--ignore-formatting",
            "--verify",
            f"--output={generated_presets.presets}",
            "-",
        ],
        input=template_json,
    )
    assert res.exit_code == 0, res.output
    assert original_presets == generated_presets.presets.read_text(), (
        "File changed"
    )


def test_toml_error(runner: CliRunner) -> None:
    res = runner.invoke(
        cli,
        ["--loader=toml", "-"],
        input='no-val" =\n',
    )
    assert res.exit_code != 0
    expected_error = "Expected '=' after a key in a key/value pair"
    assert res.output == dedent(
        f"""\
        Error: TOML parse error: <stdin>, line 1, col 7: {expected_error}
         1 | no-val" =
           |       ^
        """
    )


def test_toml_error_at_end_of_document(runner: CliRunner) -> None:
    res = runner.invoke(
        cli,
        ["--loader=toml", "-"],
        input='"unterminated string',
    )
    assert res.exit_code != 0
    assert res.output == dedent(
        """\
        Error: TOML parse error: <stdin>, line 1, col 21: Unterminated string
         1 | "unterminated string
           |                     ^
        """
    )
