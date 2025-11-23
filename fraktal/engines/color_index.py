"""We define here color index functions that map the output of coloring functions "I" to color index values.
To be used in conjunction with coloring function and palette functions.
I(u) maps the value u of the coloring function to a color index.
"""

from numba import njit
import numpy as np


@njit
def simple_index(u: float, m: float) -> float:
    """
    Simple color index function mapping the input value to a color index in R.
    Args:
        u: float, input value from the coloring function
        m: float, maximum value for normalization (default is max_iterations)
    Returns:
        float, color index I(u)
    """
    return u / m


@njit
def simple_index2(u: float, k: float = 2.5, u0: float = 0.0) -> float:
    """
    Simple color index function mapping the input value to a color index in R.
    Args:
        u: float, input value from the coloring function
        k: float, scaling factor for color index (default is 2.5)
        u0: float, offset for color index (default is 0.0)
    Returns:
        float, color index I(u)
    """
    return k*(u - u0)