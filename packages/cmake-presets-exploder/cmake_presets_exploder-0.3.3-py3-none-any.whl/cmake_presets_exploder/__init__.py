from importlib import metadata

from cmake_presets_exploder.exploder import (
    Exploder,
    PresetGroup,
    explode_presets,
)

__version__ = metadata.version(__package__)

__all__ = [
    "Exploder",
    "PresetGroup",
    "__version__",
    "explode_presets",
]
