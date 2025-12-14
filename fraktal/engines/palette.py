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
    # intensity = k * (color_index - u0)
    # intensity = max(0.0, min(1.0, intensity))  # Clamp to [0, 1]
    intensity = int(color_index * 255)
    return (intensity, intensity, intensity)


@njit
def hot_palette(color_index: float, k: float = 2.5, u0: float = 0) -> tuple:
    """
    Hot palette function mapping color index to an RGB "hot" color in [0, 1]^3.
    Args:
        color_index: float, color index value
        k: float, scaling factor for color intensity (default is 2.5)
        u0: float, offset for color index (default is 0)
    Returns:
        tuple of (r, g, b), each in [0, 1]
    """
    intensity = k * (color_index - u0)
    intensity = max(0.0, min(1.0, intensity))  # Clamp to [0, 1]
    
    if intensity < 1/3:
        r = intensity * 3
        g = 0.0
        b = 0.0
    elif intensity < 2/3:
        r = 1.0
        g = (intensity - 1/3) * 3
        b = 0.0
    else:
        r = 1.0
        g = 1.0
        b = (intensity - 2/3) * 3
    
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    
    return (r, g, b)

@njit
def cool_palette(color_index: float, k: float = 2.5, u0: float = 0) -> tuple:
    """
    Cool palette function mapping color index to an RGB "cool" color in [0, 1]^3.
    Args:
        color_index: float, color index value
        k: float, scaling factor for color intensity (default is 2.5)
        u0: float, offset for color index (default is 0)
    Returns:
        tuple of (r, g, b), each in [0, 1]
    """
    intensity = k * (color_index - u0)
    intensity = max(0.0, min(1.0, intensity))  # Clamp to [0, 1]
    
    if intensity < 1/3:
        r = 0.0
        g = intensity * 3
        b = 1.0
    elif intensity < 2/3:
        r = 0.0
        g = 1.0
        b = 1.0 - (intensity - 1/3) * 3
    else:
        r = (intensity - 2/3) * 3
        g = 1.0
        b = 0.0
    
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    
    return (r, g, b)