"""Components for Dash app"""

from .mandelbrot_helpers import generate_mandelbrot_image, ZOOM_REGIONS
from .mandelbrot_components import create_image_panel_content, create_form_panel

__all__ = [
    "generate_mandelbrot_image",
    "ZOOM_REGIONS",
    "create_image_panel_content",
    "create_form_panel",
]
