import numpy as np
from numba import njit
import os

@njit
def f_numba(z, c, p=2):
    """Numba-compatible version of the seed function f(z) = z^p + c.
    Args:
        z: complex, current value
        c: complex, constant value
        p: int, power to raise z to (default is 2)
    Returns:
        return next iteration of f(z) = z**p + c
    """
    return z**p + c

# Try to import Cython version
try:
    from fraktal.engines.seed_cy import f_cython
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False
    f_cython = None

# Select implementation based on environment variable
USE_CYTHON = os.getenv('FRAKTAL_USE_CYTHON', 'false').lower() == 'true' and CYTHON_AVAILABLE

# Export the selected implementation
if USE_CYTHON:
    f = f_cython
else:
    f = f_numba