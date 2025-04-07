import json
import re
from typing import Optional

import pytest

from cmake_presets_exploder import explode_presets


def get_md_json_blocks(text: str) -> list[str]:
    return [
        match[1]
        for match in re.finditer(
            r"^```json$(.*?)^```",
            text,
            re.MULTILINE | re.DOTALL,
        )
    ]


def test_readme_example_matches() -> None:
    with open("README.md") as f:
        readme = f.read()
    json_blocks = get_md_json_blocks(readme)
    template = json.loads(json_blocks[1])
    output = json_blocks[2]
    expected = json.dumps(explode_presets(template), indent=2)
    assert f"\n{expected}\n" == output


def assert_json_eq(a: dict, b: dict, msg: Optional[str] = None) -> None:
    """
    Assert that two JSON objects are equal, including ordering of properties.
    """
    __tracebackhide__ = True
    assert json.dumps(a, indent=2) == json.dumps(b, indent=2), msg


def template_dict(
    vendor: dict,
    presets_template: Optional[dict] = None,
    *,
    vendor_name: str = "exploder",
) -> dict:
    template = presets_template or {}
    template.setdefault("vendor", {})[vendor_name] = vendor
    return template


def test_fails_with_empty_preset_groups_list() -> None:
    vendor = {"vendor": 0, "presetGroups": {}}
    with pytest.raises(ValueError):
        explode_presets(template_dict(vendor))


def test_fails_with_no_preset_groups() -> None:
    vendor = {"vendor": 0}
    with pytest.raises(ValueError):
        explode_presets(template_dict(vendor))


def test_fails_with_no_version() -> None:
    vendor = {
        "presetGroups": {
            "configure": {"type": "configure", "parameters": {"param": ["a"]}}
        }
    }
    with pytest.raises(ValueError):
        explode_presets(template_dict(vendor))


def test_fails_with_invalid_version() -> None:
    vendor = {
        "version": 1,
        "presetGroups": {
            "configure": {"type": "configure", "parameters": {"param": ["a"]}}
        },
    }
    with pytest.raises(ValueError):
        explode_presets(template_dict(vendor))


def test_fails_if_template_not_an_object() -> None:
    with pytest.raises(ValueError, match=r"^template must be a JSON object$"):
        explode_presets(["Not an object"])


def test_fails_if_missing_vendor_object() -> None:
    with pytest.raises(
        ValueError,
        match=r"^template missing 'vendor' property$",
    ):
        explode_presets({"Vendor": {}})


@pytest.mark.parametrize("vendor_name", (None, "custom"))
def test_fails_if_vendor_object_missing_exploder_field(
    vendor_name: Optional[str],
) -> None:
    kw: dict = {} if vendor_name is None else {"vendor_name": vendor_name}
    if not vendor_name:
        vendor_name = "exploder"
    with pytest.raises(
        ValueError,
        match=rf"^vendor object missing '{vendor_name}' property$",
    ):
        explode_presets({"vendor": {vendor_name: {}}}, **kw)


def test_fails_if_vendor_not_an_object() -> None:
    with pytest.raises(ValueError, match=r"^'vendor' must be a JSON object$"):
        explode_presets({"vendor": ["Not an object"]})


def test_empty_param_does_not_generate_presets() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param1": [],
                    "param2": [],
                },
            }
        },
    }
    assert_json_eq(explode_presets(template_dict(vendor)), {})


def test_single_param_with_single_list_value() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a"]},
            }
        },
    }
    expected = {"configurePresets": [{"name": "configure-a", "param": "a"}]}
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_preset_groups_different_types() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {"type": "configure", "parameters": {"param": ["a"]}},
            "build": {"type": "build", "parameters": {"param": ["a"]}},
        },
    }
    expected = {
        "configurePresets": [
            {"name": "configure-a", "param": "a"},
        ],
        "buildPresets": [
            {"name": "build-a", "param": "a"},
        ],
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_single_param_with_multi_list_values() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a", "b"]},
            }
        },
    }
    expected = {
        "configurePresets": [
            {"name": "configure-a", "param": "a"},
            {"name": "configure-b", "param": "b"},
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_multiple_params_list_values() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param1": ["a"],
                    "param2": ["a", "b"],
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-param1-a",
                "hidden": True,
                "param1": "a",
            },
            {
                "name": "configure-param2-a",
                "hidden": True,
                "param2": "a",
            },
            {
                "name": "configure-param2-b",
                "hidden": True,
                "param2": "b",
            },
            {
                "name": "configure-a-a",
                "inherits": ["configure-param1-a", "configure-param2-a"],
            },
            {
                "name": "configure-a-b",
                "inherits": ["configure-param1-a", "configure-param2-b"],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_multiple_params_dict_values() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param1": {
                        "w": "W Value",
                        "x": "X Value",
                    },
                    "param2": {
                        "y": "Y Value",
                        "z": "Z Value",
                    },
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-param1-w",
                "hidden": True,
                "param1": "W Value",
            },
            {
                "name": "configure-param1-x",
                "hidden": True,
                "param1": "X Value",
            },
            {
                "name": "configure-param2-y",
                "hidden": True,
                "param2": "Y Value",
            },
            {
                "name": "configure-param2-z",
                "hidden": True,
                "param2": "Z Value",
            },
            {
                "name": "configure-w-y",
                "inherits": ["configure-param1-w", "configure-param2-y"],
            },
            {
                "name": "configure-w-z",
                "inherits": ["configure-param1-w", "configure-param2-z"],
            },
            {
                "name": "configure-x-y",
                "inherits": ["configure-param1-x", "configure-param2-y"],
            },
            {
                "name": "configure-x-z",
                "inherits": ["configure-param1-x", "configure-param2-z"],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_param_list_dict_values() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": [
                        {
                            "name": "name1",
                            "value": "value1",
                        },
                        {
                            "name": "name2",
                            "value": "value2",
                        },
                    ]
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-name1",
                "param": "value1",
            },
            {
                "name": "configure-name2",
                "param": "value2",
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_param_list_with_duplicate_fails() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": ["a", "b", "b", "c"],
                },
            }
        },
    }
    with pytest.raises(ValueError, match=r"duplicate parameter name 'b'"):
        explode_presets(template_dict(vendor))


def test_param_list_dict_with_duplicate_names_fails() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": [
                        {
                            "name": "a",
                            "value": "a-value",
                        },
                        {
                            "name": "b",
                            "value": "b-value",
                        },
                        {
                            "name": "c",
                            "value": "c-value",
                        },
                        {
                            "name": "b",
                            "value": "b-value-2",
                        },
                    ],
                },
            }
        },
    }
    with pytest.raises(ValueError, match=r"duplicate parameter name 'b'"):
        explode_presets(template_dict(vendor))


def test_common_inherits() -> None:
    template = {
        "configurePresets": [
            {
                "name": "base",
                "base-param": "base-value",
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
                            "param1": ["a"],
                            "param2": ["a", "b"],
                        },
                    }
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "base",
                "base-param": "base-value",
            },
            {
                "name": "configure-param1-a",
                "hidden": True,
                "param1": "a",
            },
            {
                "name": "configure-param2-a",
                "hidden": True,
                "param2": "a",
            },
            {
                "name": "configure-param2-b",
                "hidden": True,
                "param2": "b",
            },
            {
                "name": "configure-a-a",
                "inherits": [
                    "base",
                    "configure-param1-a",
                    "configure-param2-a",
                ],
            },
            {
                "name": "configure-a-b",
                "inherits": [
                    "base",
                    "configure-param1-a",
                    "configure-param2-b",
                ],
            },
        ]
    }
    assert_json_eq(explode_presets(template), expected)


def test_include_vendor() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a", "b"]},
            }
        },
    }
    expected = {
        "vendor": {"exploder": vendor},
        "configurePresets": [
            {"name": "configure-a", "param": "a"},
            {"name": "configure-b", "param": "b"},
        ],
    }
    assert_json_eq(
        explode_presets(template_dict(vendor), include_vendor=True),
        expected,
    )


def test_other_vendor_objects_kept() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a", "b"]},
            }
        },
    }
    template = {
        "vendor": {
            "other_vendor1": "hello, world!",
            "exploder": vendor,
            "other_vendor2": ["hello", "world"],
        }
    }
    expected = {
        "vendor": {
            "other_vendor1": "hello, world!",
            "other_vendor2": ["hello", "world"],
        },
        "configurePresets": [
            {"name": "configure-a", "param": "a"},
            {"name": "configure-b", "param": "b"},
        ],
    }
    assert_json_eq(explode_presets(template), expected)


def test_different_vendor_name() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a", "b"]},
            }
        },
    }
    template = {
        "vendor": {
            "other_vendor1": "hello, world!",
            "alternate_name": vendor,
            "exploder": vendor,
            "other_vendor2": ["hello", "world"],
        }
    }
    expected = {
        "vendor": {
            "other_vendor1": "hello, world!",
            "exploder": vendor,
            "other_vendor2": ["hello", "world"],
        },
        "configurePresets": [
            {"name": "configure-a", "param": "a"},
            {"name": "configure-b", "param": "b"},
        ],
    }
    assert_json_eq(
        explode_presets(template, vendor_name="alternate_name"),
        expected,
    )


def test_template_dict_is_copied() -> None:
    template = {
        "other": "hello, world",
        "vendor": {
            "exploder": {
                "version": 0,
                "presetGroups": {
                    "configure": {
                        "type": "configure",
                        "parameters": {"param": ["a"]},
                    }
                },
            }
        },
    }
    template_copy = template.copy()
    expected = {
        "other": "hello, world",
        "configurePresets": [{"name": "configure-a", "param": "a"}],
    }
    assert_json_eq(explode_presets(template), expected)
    assert_json_eq(template_copy, template)


def test_template_dict_with_no_copy_is_modified() -> None:
    template = {
        "other": "hello, world",
        "vendor": {
            "exploder": {
                "version": 0,
                "presetGroups": {
                    "configure": {
                        "type": "configure",
                        "parameters": {"param": ["a"]},
                    }
                },
            }
        },
    }
    expected = {
        "other": "hello, world",
        "configurePresets": [{"name": "configure-a", "param": "a"}],
    }
    assert_json_eq(explode_presets(template, copy=False), expected)
    assert_json_eq(template, expected)


def test_single_param_template_single_value_string() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": {"a": "A Value", "b": "B Value"},
                },
                "templates": {
                    "param": "param-$name = $value",
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-a",
                "param": "param-a = A Value",
            },
            {
                "name": "configure-b",
                "param": "param-b = B Value",
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_single_param_template_single_value_list() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": {"a": "A Value", "b": "B Value"},
                },
                "templates": {
                    "param": ["param-$name = $value", 1, 2],
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-a",
                "param": ["param-a = A Value", 1, 2],
            },
            {
                "name": "configure-b",
                "param": ["param-b = B Value", 1, 2],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_multiple_params_template_single_value_string() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": {"a": "A Value", "b": "B Value"},
                    "num": ["1", "2"],
                },
                "templates": {
                    "alpha": "alpha-$name = ${value}value",
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-alpha-a",
                "hidden": True,
                "alpha": "alpha-a = A Valuevalue",
            },
            {
                "name": "configure-alpha-b",
                "hidden": True,
                "alpha": "alpha-b = B Valuevalue",
            },
            {
                "name": "configure-num-1",
                "hidden": True,
                "num": "1",
            },
            {
                "name": "configure-num-2",
                "hidden": True,
                "num": "2",
            },
            {
                "name": "configure-a-1",
                "inherits": ["configure-alpha-a", "configure-num-1"],
            },
            {
                "name": "configure-a-2",
                "inherits": ["configure-alpha-a", "configure-num-2"],
            },
            {
                "name": "configure-b-1",
                "inherits": ["configure-alpha-b", "configure-num-1"],
            },
            {
                "name": "configure-b-2",
                "inherits": ["configure-alpha-b", "configure-num-2"],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_multiple_params_template_single_value_list() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": {"a": "A Value", "b": "B Value"},
                    "num": ["1", "2"],
                },
                "templates": {
                    "alpha": [1, 2, "alpha-$name = ${value}value", "${name}"],
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-alpha-a",
                "hidden": True,
                "alpha": [1, 2, "alpha-a = A Valuevalue", "a"],
            },
            {
                "name": "configure-alpha-b",
                "hidden": True,
                "alpha": [1, 2, "alpha-b = B Valuevalue", "b"],
            },
            {
                "name": "configure-num-1",
                "hidden": True,
                "num": "1",
            },
            {
                "name": "configure-num-2",
                "hidden": True,
                "num": "2",
            },
            {
                "name": "configure-a-1",
                "inherits": ["configure-alpha-a", "configure-num-1"],
            },
            {
                "name": "configure-a-2",
                "inherits": ["configure-alpha-a", "configure-num-2"],
            },
            {
                "name": "configure-b-1",
                "inherits": ["configure-alpha-b", "configure-num-1"],
            },
            {
                "name": "configure-b-2",
                "inherits": ["configure-alpha-b", "configure-num-2"],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_multiple_params_template_dict() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": {"a": "A Value", "b": "B Value"},
                    "num": ["1", "2"],
                },
                "templates": {
                    "alpha": {
                        "cacheVariables_$name": {
                            "ALPHA": "$value",
                        },
                    },
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-alpha-a",
                "hidden": True,
                "cacheVariables_a": {
                    "ALPHA": "A Value",
                },
            },
            {
                "name": "configure-alpha-b",
                "hidden": True,
                "cacheVariables_b": {
                    "ALPHA": "B Value",
                },
            },
            {
                "name": "configure-num-1",
                "hidden": True,
                "num": "1",
            },
            {
                "name": "configure-num-2",
                "hidden": True,
                "num": "2",
            },
            {
                "name": "configure-a-1",
                "inherits": ["configure-alpha-a", "configure-num-1"],
            },
            {
                "name": "configure-a-2",
                "inherits": ["configure-alpha-a", "configure-num-2"],
            },
            {
                "name": "configure-b-1",
                "inherits": ["configure-alpha-b", "configure-num-1"],
            },
            {
                "name": "configure-b-2",
                "inherits": ["configure-alpha-b", "configure-num-2"],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_single_param_template_dict() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": {"a": "A Value", "b": "B Value"},
                },
                "templates": {
                    "param": {
                        "cacheVariables_$name": {
                            "VALUE": "$value",
                            "NAME": "$name",
                        }
                    },
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-a",
                "cacheVariables_a": {
                    "VALUE": "A Value",
                    "NAME": "a",
                },
            },
            {
                "name": "configure-b",
                "cacheVariables_b": {
                    "VALUE": "B Value",
                    "NAME": "b",
                },
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_template_string_escape() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": ["a", "b", "c"],
                },
                "templates": {
                    "param": "$value = $$value = $${value}",
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {"name": "configure-a", "param": "a = $value = ${value}"},
            {"name": "configure-b", "param": "b = $value = ${value}"},
            {"name": "configure-c", "param": "c = $value = ${value}"},
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_template_string_in_single_param_dict_not_expanded() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "$param": {
                        "a$name": "a$value",
                        "b$$name": "b$$value",
                    },
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-a$name",
                "$param": "a$value",
            },
            {
                "name": "configure-b$$name",
                "$param": "b$$value",
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_template_string_in_single_param_string_not_expanded() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "$param": ["a$name", "b$$name"],
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-a$name",
                "$param": "a$name",
            },
            {
                "name": "configure-b$$name",
                "$param": "b$$name",
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_template_string_in_multi_params_dict_not_expanded() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "$alpha": {
                        "a$name": "a$value",
                        "b$$name": "b$$value",
                    },
                    "$num": {
                        "1$name": "1$value",
                        "2$$name": "2$$value",
                    },
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-$alpha-a$name",
                "hidden": True,
                "$alpha": "a$value",
            },
            {
                "name": "configure-$alpha-b$$name",
                "hidden": True,
                "$alpha": "b$$value",
            },
            {
                "name": "configure-$num-1$name",
                "hidden": True,
                "$num": "1$value",
            },
            {
                "name": "configure-$num-2$$name",
                "hidden": True,
                "$num": "2$$value",
            },
            {
                "name": "configure-a$name-1$name",
                "inherits": [
                    "configure-$alpha-a$name",
                    "configure-$num-1$name",
                ],
            },
            {
                "name": "configure-a$name-2$$name",
                "inherits": [
                    "configure-$alpha-a$name",
                    "configure-$num-2$$name",
                ],
            },
            {
                "name": "configure-b$$name-1$name",
                "inherits": [
                    "configure-$alpha-b$$name",
                    "configure-$num-1$name",
                ],
            },
            {
                "name": "configure-b$$name-2$$name",
                "inherits": [
                    "configure-$alpha-b$$name",
                    "configure-$num-2$$name",
                ],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_template_string_in_multi_params_string_not_expanded() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "$alpha": ["a$name", "b$$name"],
                    "$num": ["1$name", "2$$name"],
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-$alpha-a$name",
                "hidden": True,
                "$alpha": "a$name",
            },
            {
                "name": "configure-$alpha-b$$name",
                "hidden": True,
                "$alpha": "b$$name",
            },
            {
                "name": "configure-$num-1$name",
                "hidden": True,
                "$num": "1$name",
            },
            {
                "name": "configure-$num-2$$name",
                "hidden": True,
                "$num": "2$$name",
            },
            {
                "name": "configure-a$name-1$name",
                "inherits": [
                    "configure-$alpha-a$name",
                    "configure-$num-1$name",
                ],
            },
            {
                "name": "configure-a$name-2$$name",
                "inherits": [
                    "configure-$alpha-a$name",
                    "configure-$num-2$$name",
                ],
            },
            {
                "name": "configure-b$$name-1$name",
                "inherits": [
                    "configure-$alpha-b$$name",
                    "configure-$num-1$name",
                ],
            },
            {
                "name": "configure-b$$name-2$$name",
                "inherits": [
                    "configure-$alpha-b$$name",
                    "configure-$num-2$$name",
                ],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_unknown_parameter_in_template_fails() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"alpha": ["a", "b", "c"]},
                "templates": {
                    "numeric": "$value",
                },
            }
        },
    }
    with pytest.raises(ValueError):  # TODO: match on error message
        explode_presets(template_dict(vendor))


def test_unknown_template_string_fails() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a"]},
                "templates": {"param": "param-$unknown = $value"},
            }
        },
    }
    with pytest.raises(
        ValueError,
        match=(
            r"^unknown key 'unknown' in template string: "
            r"param-\$unknown = \$value$"
        ),
    ):
        explode_presets(template_dict(vendor))


@pytest.mark.parametrize(
    "invalid_template",
    (
        "$",
        "${param!name}",
        "${{param}}",
        "$(param.name)",
    ),
)
def test_invalid_template_string_fails(invalid_template: str) -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"param": ["a"]},
                "templates": {"param": invalid_template},
            }
        },
    }
    with pytest.raises(
        ValueError,
        match=rf"^invalid template string: {re.escape(invalid_template)}$",
    ):
        explode_presets(template_dict(vendor))


def test_jinja_template_expansion() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "param": {"a": "A Value", "b": "B Value"},
                },
                "templates": {
                    "param": (
                        "{jinja}param-{{ name * 3 }} = {{ value | upper }} "
                        "${name} $name $$name"
                    ),
                },
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-a",
                "param": "param-aaa = A VALUE ${name} $name $$name",
            },
            {
                "name": "configure-b",
                "param": "param-bbb = B VALUE ${name} $name $$name",
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_preset_name_template_expansion_with_single_param() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": {"a": "a-value", "b": "b-value"},
                },
                "nameTemplate": (
                    "template $alpha ${alpha.name} ${alpha.value} "
                    "$$alpha $$$alpha"
                ),
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "template a a a-value $alpha $a",
                "alpha": "a-value",
            },
            {
                "name": "template b b b-value $alpha $b",
                "alpha": "b-value",
            },
        ],
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_preset_name_template_expansion_with_multiple_params() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": ["a", "b"],
                    "num": {
                        "1": "numeric-value-1",
                        "2": "numeric-value-2",
                    },
                },
                "nameTemplate": (
                    "template $alpha $num ${alpha.name} "
                    "${num.name} ${alpha.value} ${num.value} "
                    "$$alpha $$$alpha"
                ),
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "configure-alpha-a",
                "hidden": True,
                "alpha": "a",
            },
            {
                "name": "configure-alpha-b",
                "hidden": True,
                "alpha": "b",
            },
            {
                "name": "configure-num-1",
                "hidden": True,
                "num": "numeric-value-1",
            },
            {
                "name": "configure-num-2",
                "hidden": True,
                "num": "numeric-value-2",
            },
            {
                "name": "template a 1 a 1 a numeric-value-1 $alpha $a",
                "inherits": ["configure-alpha-a", "configure-num-1"],
            },
            {
                "name": "template a 2 a 2 a numeric-value-2 $alpha $a",
                "inherits": ["configure-alpha-a", "configure-num-2"],
            },
            {
                "name": "template b 1 b 1 b numeric-value-1 $alpha $b",
                "inherits": ["configure-alpha-b", "configure-num-1"],
            },
            {
                "name": "template b 2 b 2 b numeric-value-2 $alpha $b",
                "inherits": ["configure-alpha-b", "configure-num-2"],
            },
        ]
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_preset_name_jinja_template() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": {"a": "A value", "b": "B value"},
                },
                # Parameter by itself is equivalent to parameter.name
                "nameTemplate": (
                    "{jinja}{{ alpha | upper }} == {{ alpha.name | upper }}, "
                    "{{ alpha.value | lower }}"
                ),
            }
        },
    }
    expected = {
        "configurePresets": [
            {
                "name": "A == A, a value",
                "alpha": "A value",
            },
            {
                "name": "B == B, b value",
                "alpha": "B value",
            },
        ],
    }
    assert_json_eq(explode_presets(template_dict(vendor)), expected)


def test_single_param_preset_name_template_fails_with_duplicate() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {"alpha": ["a", "b"]},
                "nameTemplate": "configure",
            }
        },
    }
    with pytest.raises(
        ValueError,
        match=r"^duplicate preset name 'configure'",
    ):
        explode_presets(template_dict(vendor))


def test_multi_param_preset_name_template_fails_with_duplicate() -> None:
    vendor = {
        "version": 0,
        "presetGroups": {
            "configure": {
                "type": "configure",
                "parameters": {
                    "alpha": ["a", "b"],
                    "num": ["1", "2"],
                },
                "nameTemplate": "configure $alpha",
            }
        },
    }
    with pytest.raises(
        ValueError,
        match=r"^duplicate preset name 'configure a'",
    ):
        explode_presets(template_dict(vendor))
