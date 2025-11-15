"""We define here coloring functions "u" related to the iteration count of truncated orbits.
To be used in conjunction with color index functions and palette functions.
A coloring function u: C_{max_iterations} -> R maps truncated orbits to the real line.
"""

from numba import njit
import numpy as np

@njit
def truncated_orbit_length(truncated_orbit: np.ndarray) -> int:
    """
    Numba-compatible function to get the length of a truncated orbit divided by 20.
    
    Args:
        truncated_orbit: np.ndarray of complex numbers, the truncated orbit
    Returns:
        int, length of the truncated orbit divided by 20
    """
    return len(truncated_orbit)/20