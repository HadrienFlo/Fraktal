"""We define here coloring functions "u" related to the iteration count of truncated orbits.
To be used in conjunction with color index functions and palette functions.
A coloring function u: C_{max_iterations} -> R maps truncated orbits to the real line.
"""

from numba import njit
import numpy as np

@njit
def iteration_count(truncated_orbit: np.ndarray, escape_time: int) -> int:
    """
    Numba-compatible function to get the length of a truncated orbit.
    
    Args:
        truncated_orbit: np.ndarray of complex numbers, the truncated orbit
    Returns:
        int, length of the truncated orbit
    """
    return escape_time

@njit
def continuous_iteration_count(truncated_orbit: np.ndarray, escape_time: int, bailout: float, p: float = 2.0) -> float:
    """
    Numba-compatible function to compute a continuous iteration count for smooth coloring.
    
    Args:
        truncated_orbit: np.ndarray of complex numbers, the truncated orbit
        bailout: float, the bailout radius
        p: float, the power used in the fractal iteration (default is 2 for Mandelbrot)
    Returns:
        float, continuous iteration count
    """
    N = escape_time
    rN = abs(truncated_orbit[-1])
    return N + (bailout**p - abs(rN))/(bailout**p - bailout)

@njit
def smooth_iteration_count(truncated_orbit: np.ndarray, escape_time: int, bailout: float, p: float = 2.0) -> float:
    """
    Numba-compatible function to compute a smooth iteration count using logarithmic scaling.
    
    Args:
        truncated_orbit: np.ndarray of complex numbers, the truncated orbit
        bailout: float, the bailout radius
        p: float, the power used in the fractal iteration (default is 2 for Mandelbrot)
    Returns:
        float, smooth iteration count
    """
    N = escape_time
    rN = abs(truncated_orbit[-1])
    return N + 1 + np.log(np.log(rN)/np.log(bailout))/np.log(p)