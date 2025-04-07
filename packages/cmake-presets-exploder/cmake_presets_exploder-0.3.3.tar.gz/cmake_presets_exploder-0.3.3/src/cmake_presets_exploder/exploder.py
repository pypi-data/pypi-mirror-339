from collections.abc import Iterable, Mapping, Sequence
from itertools import product
from string import Template as _BaseStringTemplate
from typing import Annotated, Any, Literal, Optional, TypeVar, Union, cast

from pydantic import (
    BaseModel,
    ConfigDict,
    Discriminator,
    Field,
    Tag,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_camel

T = TypeVar("T")


def _expand_jinja(s: str, env: Mapping[str, Any]) -> str:
    try:
        import jinja2  # type: ignore
    except ImportError as e:
        msg = (
            "jinja2 is required for jinja strings templates. "
            "Did you install with [jinja2] extra?"
        )
        raise RuntimeError(msg) from e

    return jinja2.Template(s).render(env)


class _StringTemplate(_BaseStringTemplate):
    __ident = r"[_a-z][_a-z0-9]*"
    braceidpattern = rf"(?a:{__ident}(?:\.{__ident})*)"


def _expand_string_template(
    s: str,
    mapping: Mapping[str, Any],
    *,
    jinja_env: Optional[Mapping[str, Any]] = None,
) -> str:
    jinja_prefix = "{jinja}"
    if s.startswith(jinja_prefix):
        return _expand_jinja(
            s.removeprefix(jinja_prefix),
            mapping if jinja_env is None else jinja_env,
        )

    try:
        return _StringTemplate(s).substitute(mapping)
    except ValueError as e:
        msg = f"invalid template string: {s}"
        raise ValueError(msg) from e
    except KeyError as e:
        msg = f"unknown key {e} in template string: {s}"
        raise ValueError(msg) from None


def _format_json_strings(obj: T, mapping: Mapping[str, Any]) -> T:
    r: Any

    if isinstance(obj, str):
        r = _expand_string_template(obj, mapping)
        return r

    if isinstance(obj, Sequence):
        r = [_format_json_strings(v, mapping) for v in obj]
        return r

    if isinstance(obj, Mapping):
        r = {}
        for k, v in obj.items():
            if isinstance(k, str):
                k = _expand_string_template(k, mapping)
            r[k] = _format_json_strings(v, mapping)
        return r

    # obj is another type, return as-is
    return obj


class _Model(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)


class ParameterValue(_Model):
    name: str
    value: str


def _expand_param_template(
    template: dict, param_value: ParameterValue
) -> dict:
    return _format_json_strings(
        template,
        {
            "value": param_value.value,
            "name": param_value.name,
        },
    )


def _base_preset_name(
    prefix: str,
    sep: str,
    param_name: str,
    param_value: ParameterValue,
) -> str:
    return sep.join((prefix, param_name, param_value.name))


def _parameter_values_discriminator(
    values: "ParameterValues",
) -> Optional[str]:
    # The types of dict keys/values or list values do not actually have to be
    # strings (e.g. as in dict[str, str]), as Pydantic will check this. The
    # checks for dict and list are just to guide Pydantic to give a more
    # specific error message.

    if isinstance(values, Mapping):
        return "dict[str, str]"

    if isinstance(values, Sequence):
        if values and isinstance(values[0], dict):
            return "list[dict]"
        return "list[str]"

    return None


# Using an explicit discriminator improves the error message: without one
# Pydantic would give a separate validation error for each type in the union,
# leading to verbose errors.
ParameterValues = Annotated[
    Union[
        Annotated[dict[str, str], Tag("dict[str, str]")],
        Annotated[list[str], Tag("list[str]")],
        Annotated[list[ParameterValue], Tag("list[dict]")],
    ],
    Discriminator(
        _parameter_values_discriminator,
        custom_error_type="invalid_parameter_values",
        custom_error_message="Invalid parameter values",
    ),
]


def _validate_parameter_value_list(
    parameters: ParameterValues,
) -> list[ParameterValue]:
    """
    Convert parameter to a list of ParameterValues, checking that the
    parameter names are unique.

    Each parameter has a 'name' and a 'value'. The name is used for generating
    preset names and prefixes, and the value is used for generating the actual
    configuration value. It may be useful to have a separate name and value if,
    for example, the parameter value is long or contains special characters.

    Parameters may be specified in JSON as either:

    - An object mapping parameter name to value.
    - An array of strings, where each string doubles as the parameter name and
      value.
    - An array of ParameterValue objects.
    """

    if isinstance(parameters, dict):
        return [ParameterValue(name=k, value=v) for k, v in parameters.items()]

    unique_names = set()
    converted: list[ParameterValue] = []
    for val in parameters:
        if isinstance(val, str):
            val = ParameterValue(name=val, value=val)
        if val.name in unique_names:
            raise ValueError(f"duplicate parameter name '{val.name}'")
        unique_names.add(val.name)
        converted.append(val)
    return converted


def _validate_preset_names(names: Iterable[str]) -> None:
    unique = set()
    for name in names:
        if name in unique:
            msg = (
                f"duplicate preset name '{name}' "
                "(did you include all parameters in name template?)"
            )
            raise ValueError(msg)
        unique.add(name)


class _JinjaParameterValue:
    """
    Wraps ParameterValue so that "{{ value }}" is equivalent to
    "{{ value.name }}" in Jinja templates.
    """

    def __init__(self, value: ParameterValue):
        self.name = value.name
        self.value = value.value

    def __str__(self) -> str:
        return self.name


class PresetGroup(_Model):
    type: str = Field(
        ...,
        min_length=1,
        description="Type of configuration preset, "
        "e.g. configure, build, test.",
    )
    name_template: Optional[str] = Field(
        None,
        min_length=1,
        description="Template string for constructing preset names. "
        "By default, preset names are the group name followed by the "
        "parameter value names, separated by '-'.",
    )
    inherits: list[str] = Field(
        [],
        description="Name of pre-existing configuration presets to inherit "
        "in all generated presets.",
    )
    parameters: dict[str, ParameterValues] = Field(
        ...,
        min_length=1,
        description="Parameters to generate presets from.",
    )
    templates: dict[str, Any] = Field(
        {},
        description="Template for generating configuration options.",
    )

    _sep = "-"

    @field_validator("parameters", mode="after")
    @classmethod
    def _validate_parameters(
        cls,
        parameters: dict[str, ParameterValues],
    ) -> dict[str, list[ParameterValue]]:
        """
        Narrow the type of the `parameters` member to
        `dict[str, list[ParameterValue]]`. We keep the `ParameterValues`
        in the type annotation so that the JSON schema type is correctly
        specified.
        """
        return {
            k: _validate_parameter_value_list(v) for k, v in parameters.items()
        }

    def _parameters_dict(self) -> dict[str, list[ParameterValue]]:
        """
        Returns `self.parameters`, casted to `dict[str, list[ParameterValue]]`.
        The `parameters` attribute will have already been narrowed to this type
        by `_validate_parameters`, so safe to cast.
        """
        return cast(dict[str, list[ParameterValue]], self.parameters)

    @model_validator(mode="after")
    def _validate_template_parameters(self) -> "PresetGroup":
        missing = []
        for param_name in self.templates:
            if param_name not in self.parameters:
                missing.append(param_name)

        if missing:
            s = "" if len(missing) == 1 else "s"
            missing_str = ", ".join(missing)
            msg = f"Missing parameter{s} for template keys: {missing_str}"
            raise ValueError(msg)

        return self

    def _get_template(self, param_name: str) -> dict:
        template = self.templates.get(param_name)
        if isinstance(template, dict):
            return template

        param_name = param_name.replace("$", "$$")
        if template is None:
            return {param_name: "$value"}
        return {param_name: template}

    def _preset_name(
        self,
        prefix: str,
        param_values: dict[str, ParameterValue],
    ) -> str:
        if self.name_template is None:
            return "-".join([prefix, *(v.name for v in param_values.values())])

        mapping = {}
        jinja_env = {}
        for param_name, param_value in param_values.items():
            mapping.update(
                {
                    param_name: param_value.name,
                    f"{param_name}.name": param_value.name,
                    f"{param_name}.value": param_value.value,
                }
            )
            jinja_env[param_name] = _JinjaParameterValue(param_value)

        return _expand_string_template(
            self.name_template,
            mapping,
            jinja_env=jinja_env,
        )

    def _generate_presets_for_single_parameter(self, prefix: str) -> list:
        param_name, param_values = self._parameters_dict().popitem()
        template = self._get_template(param_name)
        presets = [
            {
                "name": self._preset_name(prefix, {param_name: param_value}),
                **({"inherits": self.inherits} if self.inherits else {}),
                **_expand_param_template(template, param_value),
            }
            for param_value in param_values
        ]
        _validate_preset_names(preset["name"] for preset in presets)
        return presets

    def _generate_base_presets(self, prefix: str) -> list:
        """
        Generate base presets for all individual parameters.
        """
        presets: list[dict] = []
        for param_name, param_values in self._parameters_dict().items():
            template = self._get_template(param_name)
            presets.extend(
                {
                    "name": _base_preset_name(
                        prefix,
                        self._sep,
                        param_name,
                        param_value,
                    ),
                    "hidden": True,
                    **_expand_param_template(template, param_value),
                }
                for param_value in param_values
            )

        return presets

    def generate_presets(self, prefix: str) -> list:
        if len(self.parameters) == 1:
            return self._generate_presets_for_single_parameter(prefix)

        presets = self._generate_base_presets(prefix)
        parameters = self._parameters_dict()
        for param_values in product(*parameters.values()):
            bases = (
                _base_preset_name(prefix, self._sep, param_name, param_value)
                for param_name, param_value in zip(
                    parameters.keys(), param_values
                )
            )
            preset = {
                "name": self._preset_name(
                    prefix,
                    {n: v for n, v in zip(parameters.keys(), param_values)},
                ),
                "inherits": [*self.inherits, *bases],
            }
            presets.append(preset)

        _validate_preset_names(preset["name"] for preset in presets)
        return presets


class Exploder(_Model):
    version: Literal[0]
    preset_groups: dict[str, PresetGroup] = Field(
        ...,
        description="Preset groups. Presets are generated from the Cartesian "
        "product of the parameters in each group.",
    )


def explode_presets(
    template_json: object,
    *,
    vendor_name: str = "exploder",
    include_vendor: bool = False,
    copy: bool = True,
) -> dict:
    if not isinstance(template_json, dict):
        raise ValueError("template must be a JSON object")

    if copy:
        template_json = template_json.copy()

    vendor_json: object = template_json.get("vendor")
    if not vendor_json:
        raise ValueError("template missing 'vendor' property")

    if not isinstance(vendor_json, dict):
        raise ValueError("'vendor' must be a JSON object")
    exploder_json = vendor_json.get(vendor_name)
    if not exploder_json:
        raise ValueError(f"vendor object missing '{vendor_name}' property")

    try:
        exploder = Exploder.model_validate(exploder_json)
    except ValueError as e:
        raise ValueError(f"invalid '{vendor_name}' object: {e}") from e

    for name, group in exploder.preset_groups.items():
        presets = group.generate_presets(name)
        if presets:
            template_json.setdefault(f"{group.type}Presets", []).extend(
                presets
            )

    if not include_vendor:
        del template_json["vendor"][vendor_name]
        if not template_json["vendor"]:
            del template_json["vendor"]

    return template_json
