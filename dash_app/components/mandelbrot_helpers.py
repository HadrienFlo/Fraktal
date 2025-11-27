"""Helper functions for Mandelbrot page"""

from PIL import Image
import io
import base64

from fraktal.engines.mandelbrot import mandelbrot_set_numba
from fraktal.models.iteration_count import iteration_count
from fraktal.engines.color_index import simple_index
from fraktal.engines.palette import simple_palette


# Define zoom regions
ZOOM_REGIONS = {
    "full": (-2, 1, -1.5, 1.5),
    "zoom1": (-0.8, -0.4, -0.2, 0.2),
    "zoom2": (-0.748, -0.746, 0.099, 0.101),
    "zoom3": (-0.7485, -0.7465, 0.0995, 0.1005),
}


def generate_mandelbrot_image(
    xmin, xmax, ymin, ymax, width, height, max_iter,
    bailout=2,
    coloring_function=iteration_count,
    color_index_function=simple_index,
    palette_function=simple_palette
):
    """Generate a Mandelbrot set image and return as base64 encoded PNG."""
    # Generate the Mandelbrot set
    image_array = mandelbrot_set_numba(
        xmin, xmax, ymin, ymax, width, height, max_iter,
        coloring_function, color_index_function, palette_function,
        bailout=bailout, p=2
    )
    
    # Convert to PIL Image
    img = Image.fromarray(image_array, 'RGB')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    
    return f"data:image/png;base64,{image_base64}"
