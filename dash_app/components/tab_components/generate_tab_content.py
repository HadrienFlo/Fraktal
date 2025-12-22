"""Generate tab content with fractal visualization."""

import numpy as np
import dash_mantine_components as dmc
from dash import dcc
import plotly.graph_objects as go
from PIL import Image
import io
import base64

from fraktal.engines.mandelbrot import mandelbrot_set_numba
from fraktal.mapping import FRAKTAL_MODELS


def _image_array_to_base64(img_array: np.ndarray) -> str:
    """Convert a numpy RGB image array to base64 PNG data URL."""
    img = Image.fromarray(img_array.astype(np.uint8), "RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{data}"


def generate_fractal_tab_content(tab_id: str, tab_name: str, inputs_data: dict) -> dmc.Container:
    """Generate tab content displaying the rendered Mandelbrot fractal.
    
    Args:
        tab_id: Unique identifier for the tab
        tab_name: Display name for the tab
        inputs_data: Dictionary containing fractal parameters:
            - center_x: float, center X coordinate
            - center_y: float, center Y coordinate
            - zoom: float, zoom level
            - width: int, image width in pixels
            - height: int, image height in pixels
            - max_iter: int, maximum iterations
    
    Returns:
        dmc.Container with the fractal image
    """
    # Extract parameters
    center_x = inputs_data.get('center_x', -0.5)
    center_y = inputs_data.get('center_y', 0.0)
    zoom = inputs_data.get('zoom', 1.0)
    width = int(inputs_data.get('width', 800))
    height = int(inputs_data.get('height', 600))
    max_iter = int(inputs_data.get('max_iter', 256))
    
    # Calculate the complex plane bounds based on zoom and center
    # Standard Mandelbrot view is roughly from -2 to 1 on x, -1.5 to 1.5 on y
    base_width = 3.0  # x range: -2 to 1
    base_height = 3.0  # y range: -1.5 to 1.5
    
    # Apply zoom
    view_width = base_width / zoom
    view_height = base_height / zoom
    
    xmin = center_x - view_width / 2
    xmax = center_x + view_width / 2
    ymin = center_y - view_height / 2
    ymax = center_y + view_height / 2
    
    # Get selected functions from inputs_data
    coloring_key = inputs_data.get('coloring_function', 'smooth-iteration-count')
    color_index_key = inputs_data.get('color_index_function', 'simple-index')
    palette_key = inputs_data.get('palette_function', 'simple-palette')
    
    # Get coloring, color index, and palette functions from mapping
    coloring_fn = FRAKTAL_MODELS['coloring'][coloring_key]['function']
    color_index_fn = FRAKTAL_MODELS['color_index'][color_index_key]['function']
    palette_fn = FRAKTAL_MODELS['palette'][palette_key]['function']
    
    # Generate the Mandelbrot set image
    img_array = mandelbrot_set_numba(
        xmin, xmax, ymin, ymax, 
        width, height, max_iter,
        coloring_fn, color_index_fn, palette_fn,
        bailout=2.0, p=2
    )
    
    # Convert to base64
    img_data_url = _image_array_to_base64(img_array)
    
    # Create tab content with image
    return dmc.Container(
        [
            dmc.Title(tab_name, order=3, mb="md"),
            dmc.Stack([
                dmc.Image(
                    src=img_data_url,
                    alt=f"Mandelbrot fractal: {tab_name}",
                    radius="md",
                    style={"maxWidth": "100%"},
                ),
                dmc.Text(
                    f"Center: ({center_x:.6f}, {center_y:.6f}) | Zoom: {zoom:.2f}x | Iterations: {max_iter}",
                    size="sm",
                    c="dimmed",
                ),
            ], gap="sm"),
        ],
        id=f"{tab_id}-container",
        size="lg",
        py="lg"
    )
