import numpy as np
from numba import njit

@njit
def f_numba(z, c, p=2):
    return z**p + c

def f(z, c, p: int = 2):
    """Compute the next iteration of the seed function f(z) = z^p + c.

    Args:
        z: complex, current value
        c: complex, constant value
        p: int, power to raise z to (default is 2)
    Returns:
        return next iteration of f(z) = z**p + c
    """
    return z**p + c