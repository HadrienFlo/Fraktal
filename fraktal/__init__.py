"""fraktal package - small library for fractal computations and utilities.

Expose config loader and decorators.
"""

from .config import load_default_config
from .decorators import time_and_memory

__all__ = ["load_default_config", "time_and_memory"]
