"""Palette functions mapping color index values to RGB colors.
To be used in conjunction with coloring functions and color index functions.
A palette function P: R -> [0, 1]^3 maps color index values to RGB colors.
"""

from numba import njit
import numpy as np

@njit
def simple_palette(color_index: float, k: float = 2.5, u0: float = 0) -> tuple:
    """
    Simple palette function mapping color index to an RGB grayscale in [0, 1]^3.
    Args:
        color_index: float, color index value
        k: float, scaling factor for color intensity (default is 2.5)
        u0: float, offset for color index (default is 0)
    Returns:
        tuple of (r, g, b), each in [0, 1]
    """
    intensity = k * (color_index - u0)
    intensity = max(0.0, min(1.0, intensity))  # Clamp to [0, 1]
    return (intensity, intensity, intensity)