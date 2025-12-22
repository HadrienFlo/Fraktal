"""Type stub for mandelbrot_cy module."""

import numpy as np
from typing import Callable

def mandelbrot_set_cython(
    xmin: float, xmax: float, ymin: float, ymax: float,
    width: int, height: int, max_iter: int,
    coloring_function: Callable, color_index_function: Callable, palette_function: Callable,
    bailout: float = 2.0, p: int = 2
) -> np.ndarray:
    """Cython-optimized Mandelbrot set generator."""
    ...
