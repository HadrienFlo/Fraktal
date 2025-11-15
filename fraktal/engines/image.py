"""Image engine module for Fraktal library. Set the image setting parameters and pass them to the set generation functions.
This module is compatible with Numba for performance optimization.
The following operations are carried out for each pixel in the m x n matrix representing the image:
1. Set z0 to correspond to the position of the pixel in the complex plane.
2. Compute the truncated orbit O_T(z0) by iterating z_{n} = f(z_{n-1}) with f the seed function starting from z0 until either
    the escape condition is met (abs(z_n) > bailout) or n=max_iterations.
3. Using the coloring function and color index functions, map the resulting truncated orbit to a color index value for the pixel.
4. Determine an RGB color of the pixel by using the palette function.
"""

from numba import njit
import numpy as np

@njit
def set_image_parameters(xmin, xmax, ymin, ymax, width, height):
    """
    Numba-compatible function to set image parameters for fractal generation.
    
    Args:
        xmin, xmax: float, real axis range
        ymin, ymax: float, imaginary axis range
        width, height: int, output image size
    Returns:
        tuple of (x values array, y values array)
    """
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    return x, y

def generate_fractal_image(xmin, xmax, ymin, ymax, width, height, max_iter, engine_function, **kwargs):
    """
    Generate a fractal image using the specified engine function.
    
    Args:
        xmin, xmax: float, real axis range
        ymin, ymax: float, imaginary axis range
        width, height: int, output image size
        max_iter: int, maximum iterations
        engine_function: callable, function to generate the fractal set
        **kwargs: additional parameters for the engine function
    Returns:
        np.ndarray of shape (height, width), dtype=int
        Each value is the iteration count at which the point diverged (or max_iter if not diverged)
    """
    return engine_function(xmin, xmax, ymin, ymax, width, height, max_iter, **kwargs)

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from fraktal.engines.mandelbrot import mandelbrot_set_numba, mandelbrot_set

    # Example usage with Numba-accelerated Mandelbrot set
    img_numba = generate_fractal_image(-2, 1, -1.5, 1.5, 800, 600, 100, mandelbrot_set_numba)
    plt.imshow(img_numba)
    plt.title("Mandelbrot Set (Numba)")
    plt.show()

    # Example usage with NumPy vectorized Mandelbrot set
    img_numpy = generate_fractal_image(-2, 1, -1.5, 1.5, 800, 600, 100, mandelbrot_set)
    plt.imshow(img_numpy)
    plt.title("Mandelbrot Set (NumPy)")
    plt.show()
