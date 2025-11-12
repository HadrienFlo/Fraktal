from numba import njit, prange
import numpy as np


def window(shape: tuple[int, int, int, int], width: int, height: int) -> np.ndarray:
    """
    Generate a 2D grid of complex numbers representing a window in the complex plane.
    Args:
        shape: tuple of (x_min, x_max, y_min, y_max) defining the window in the complex plane
        width: int, number of points along the real axis
        height: int, number of points along the imaginary axis
    Returns:
        np.ndarray of shape (height, width) with complex numbers
    """
    x_m, x_M, y_m, y_M = shape
    delta_x = (x_M - x_m) / width
    delta_y = (y_M - y_m) / height
    x = np.linspace(x_m, x_M - delta_x, width)
    y = np.linspace(y_m, y_M - delta_y, height)
    X, Y = np.meshgrid(x, y)
    return X + 1j * Y


def window_from_center(
    center: complex, span: float, width: int, height: int
) -> np.ndarray:
    """
    Generate a 2D grid of complex numbers representing a window in the complex plane,
    centered around a given point with a specified span.
    Args:
        center: complex, center point of the window
        span: float, total width and height of the window
        width: int, number of points along the real axis
        height: int, number of points along the imaginary axis
    Returns:
        np.ndarray of shape (height, width) with complex numbers
    """
    half_span = span / 2
    x_m = center.real - half_span
    x_M = center.real + half_span
    y_m = center.imag - half_span
    y_M = center.imag + half_span
    return window((x_m, x_M, y_m, y_M), width, height)


def window_to_screen(
    data_array: np.ndarray,
    pixel_model: str | None = None,
) -> np.ndarray:
    """
    Map a Mandelbrot set array to a specific window in the complex plane.
    Args:
        mandelbrot_array: np.ndarray, 2D array representing the Mandelbrot set
    Returns:
        np.ndarray of shape (height, width) with pixel model applied if specified (RGB by default).
    """
    if pixel_model is not None:
        pixel_model = 'rgb'
    height, width = data_array.shape
    if pixel_model == 'rgbx':
        # rgbx
        rgba_image = np.zeros((height, width, 4), dtype=np.uint8)
        max_iter = data_array.max()
        norm = (data_array / max_iter * 255).astype(np.uint8)
        rgba_image[..., 0] = norm  # Red channel
        rgba_image[..., 1] = norm  # Green channel
        rgba_image[..., 2] = norm  # Blue channel
        rgba_image[..., 3] = 255   # Alpha channel
        return rgba_image
    elif pixel_model == 'grayscale':
        grayscale_image = (data_array / data_array.max() * 255).astype(np.uint8)
        return grayscale_image
    else:
        rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
        max_iter = data_array.max()
        norm = (data_array / max_iter * 255).astype(np.uint8)
        rgb_image[..., 0] = norm  # Red channel
        rgb_image[..., 1] = norm  # Green channel
        rgb_image[..., 2] = norm  # Blue channel
        return rgb_image