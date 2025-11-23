"""Define the orbit engine for fractal generation.
An Orbit of z in C under f is the sequence O(z) = (z_0, z_1, ..., z_N, ...), where z_0 = z and z_{n+1} = f(z_n).
On a computed an Orbit length is limited by max_iterations.
If we note N* the smallest integer where abs(z_{N*}) > bailout, then N = min(N*, max_iterations). We can define truncated orbits as follows:
The Truncated Orbit O_T(z) is the finite sequence (z_0, z_1, ..., z_N), where N <= max_iterations is the first index such that abs(z_N) > bailout (escape condition).
"""

import numpy as np
from numba import njit

def orbit(z: complex, f: callable, max_iterations: int, **kwargs) -> int:
    """Compute the orbit of a point z under the function f until it reaches max_iterations.

    Args:
        z: complex, initial point in the complex plane
        f: callable, function defining the fractal iteration
        max_iterations: int, maximum number of iterations to perform

    Returns:
        list[complex] of size max_iterations + 1.
    """
    res = []
    for _ in range(max_iterations + 1):
        res.append(z)
        z = f(z, **kwargs)
    return res

@njit
def truncated_orbit_numba(z, c, max_iterations, bailout=2.0, p=2):
    """
    Numba-compatible: returns the full orbit as a preallocated array and the valid length.
    Returns the iteration count at which escape occurs (matching NumPy mandelbrot_set behavior).
    """
    orbit = np.empty(max_iterations + 1, dtype=np.complex128)
    for n in range(max_iterations + 1):
        orbit[n] = z
        z = z**p + c  # Compute next iteration first
        if (z.real*z.real + z.imag*z.imag) > bailout**2:
            return orbit, n  # Return the iteration index where escape happens
    return orbit, max_iterations


@njit
def bailout_inequality(truncated_orbit: np.ndarray, N: int) -> int:
    """
    Numba-compatible: Given a truncated orbit and an index N, return the values satisfying the bailout inequality.
    The bailout inequality states that:
    abs(z_{N-1}) <= bailout < abs(z_N)
    Args:
        truncated_orbit: np.ndarray of complex numbers, the truncated orbit
        N: int, index to check the bailout inequality
    Returns:
        tuple (abs(z_{N-1}), abs(z_N)) if N is valid, else None
    """
    if N <= 0 or N >= len(truncated_orbit):
        return None
    abs_prev = np.sqrt(truncated_orbit[N-1].real**2 + truncated_orbit[N-1].imag**2)
    abs_curr = np.sqrt(truncated_orbit[N].real**2 + truncated_orbit[N].imag**2)
    return abs_prev, abs_curr

