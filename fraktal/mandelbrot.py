from numba import njit, prange
import numpy as np

@njit(parallel=True, fastmath=True)
def mandelbrot_set_numba(xmin, xmax, ymin, ymax, width, height, max_iter):
    """
    Numba-accelerated Mandelbrot set generator (returns same output as mandelbrot_set).
    Much faster for large images and high iteration counts.
    """
    result = np.full((height, width), max_iter, dtype=np.int32)
    for i in prange(height):
        for j in prange(width):
            x0 = xmin + j * (xmax - xmin) / (width - 1)
            y0 = ymin + i * (ymax - ymin) / (height - 1)
            x, y = 0.0, 0.0
            for iter in range(max_iter):
                xtemp = x*x - y*y + x0
                y = 2*x*y + y0
                x = xtemp
                if x*x + y*y > 4.0:
                    result[i, j] = iter
                    break
            # If never diverged, value remains max_iter
    return result

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
