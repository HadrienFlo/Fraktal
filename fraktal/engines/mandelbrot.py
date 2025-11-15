
from numba import njit, prange
import numpy as np
from fraktal.engines.seed import f_numba
from fraktal.engines.orbit import truncated_orbit_numba


@njit(parallel=True, fastmath=True)
def mandelbrot_set_numba(xmin, xmax, ymin, ymax, width, height, max_iter, p=2):
    """
    Numba-accelerated Mandelbrot set generator using truncated_orbit_numba and f_numba.
    """
    result = np.full((height, width), max_iter, dtype=np.int32)
    for i in prange(height):
        for j in prange(width):
            c_real = xmin + j * (xmax - xmin) / (width - 1)
            c_imag = ymin + i * (ymax - ymin) / (height - 1)
            c = np.complex128(c_real + 1j * c_imag)
            z0 = np.complex128(0.0 + 0.0j)
            _, length = truncated_orbit_numba(z0, c, max_iter, bailout=2.0, p=p)
            result[i, j] = length
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


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    plt.imshow(mandelbrot_set_numba(-2, 1, -1.5, 1.5, 800, 600, 100))
    plt.show()
    plt.imshow(mandelbrot_set(-2, 1, -1.5, 1.5, 800, 600, 100))
    plt.show()