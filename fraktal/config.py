"""Configuration loader for fraktal.

Loads a default YAML configuration shipped with the package.
"""
from __future__ import annotations

import yaml
from typing import Any, Dict
try:
    # Python 3.9+: importlib.resources.files
    from importlib import resources
except Exception:
    import importlib_resources as resources  # type: ignore

DEFAULT_CONFIG_YAML = "config/default.yaml"


def load_default_config() -> Dict[str, Any]:
    """Load and return the default configuration dict shipped in `config/default.yaml`.

    Returns:
        dict: Configuration loaded from YAML. If YAML parse fails, returns an empty dict.
    """
    # Try multiple ways to open the config file to be robust in different environments
    try:
        # Try importlib.resources files() API (modern approach)
        data_file = resources.files(__package__).joinpath("..").joinpath("config").joinpath("default.yaml")
        text = data_file.read_text(encoding="utf-8")
    except Exception:
        try:
            # Fallback: try relative path from package directory
            import os
            here = os.path.dirname(os.path.dirname(__file__))
            path = os.path.join(here, "config", "default.yaml")
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            # Last fallback: assume config/ is a sibling to package directory
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "default.yaml")
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()

    try:
        cfg = yaml.safe_load(text)
        if cfg is None:
            cfg = {}
    except Exception:
        cfg = {}
    return cfg
