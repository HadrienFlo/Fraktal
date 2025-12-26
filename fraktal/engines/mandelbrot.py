
from numba import njit, prange
import numpy as np
from fraktal.engines.seed import f_numba
from fraktal.engines.orbit import truncated_orbit_numba


def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter):
    """
    Generate a matrix representing the Mandelbrot set using NumPy vectorization.

    Args:
        xmin, xmax: float, real axis range
        ymin, ymax: float, imaginary axis range
        width, height: int, output image size
        max_iter: int, maximum iterations
    Returns:
        np.ndarray of shape (height, width), dtype=int
        Each value is the iteration count at which the point diverged (or max_iter if not diverged)
    """
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    Z = np.zeros_like(C)
    div_time = np.full(C.shape, max_iter, dtype=int)
    mask = np.full(C.shape, True, dtype=bool)
    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + C[mask]
        diverged = np.abs(Z) > 2
        div_now = diverged & mask
        div_time[div_now] = i
        mask &= ~diverged
        if not mask.any():
            break
    return div_time


@njit(parallel=True, fastmath=True)
def mandelbrot_set_numba(xmin, xmax, ymin, ymax, width, height, max_iter, coloring_function, color_index_function, palette_function, bailout=2, p=2):
    """
    Numba-accelerated Mandelbrot set generator using a given coloring function, color index function and palette_function.
    """
    result = np.full((height, width, 3), max_iter, dtype=np.uint8)
    for i in prange(height):
        for j in prange(width):
            c_real = xmin + j * (xmax - xmin) / (width - 1)
            c_imag = ymin + i * (ymax - ymin) / (height - 1)
            c = np.complex128(c_real + 1j * c_imag)
            z0 = np.complex128(0.0 + 0.0j)
            o_T, escape_time = truncated_orbit_numba(z0, c, max_iter, bailout=bailout, p=p)
            u = coloring_function(o_T, escape_time, bailout=bailout, p=p)
            I = color_index_function(u, max_iter)
            r, g, b = palette_function(I)
            result[i, j, 0] = r
            result[i, j, 1] = g
            result[i, j, 2] = b    
    return result    
    return result
