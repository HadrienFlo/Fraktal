"""Mandelbrot Set Visualization Page"""

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_mantine_components as dmc
import numpy as np
from PIL import Image
import io
import base64

from fraktal.engines.mandelbrot import mandelbrot_set_numba
from fraktal.models.iteration_count import iteration_count
from fraktal.engines.color_index import simple_index
from fraktal.engines.palette import simple_palette

dash.register_page(__name__, name="Mandelbrot")


def generate_mandelbrot_image(xmin, xmax, ymin, ymax, width, height, max_iter, coloring_function=iteration_count, color_index_function=simple_index, palette_function=simple_palette):
    """Generate a Mandelbrot set image and return as base64 encoded PNG."""
    # Generate the Mandelbrot set
    image_array = mandelbrot_set_numba(xmin, xmax, ymin, ymax, width, height, max_iter, coloring_function, color_index_function, palette_function, bailout=2, p=2)
    
    # Convert to PIL Image
    img = Image.fromarray(image_array, 'RGB')
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    
    return f"data:image/png;base64,{image_base64}"


layout = dmc.Container(
    [
        dmc.Title("Mandelbrot Set", order=1, mt="lg", mb="lg"),
        
        dmc.Grid(
            [
                dmc.GridCol(
                    [
                        dmc.Paper(
                            [
                                dmc.Title("Controls", order=3, mb="md"),
                                
                                dmc.Stack(
                                    [
                                        dmc.Group(
                                            [
                                                dmc.Text("Max Iterations:", fw=500),
                                                dmc.NumberInput(
                                                    id="max-iter-input",
                                                    value=100,
                                                    min=10,
                                                    max=10000,
                                                    step=10,
                                                    style={"flex": 1},
                                                ),
                                            ],
                                            grow=True,
                                            mb="md",
                                        ),
                                        
                                        dmc.Group(
                                            [
                                                dmc.Text("Image Size:", fw=500),
                                                dmc.Select(
                                                    id="image-size-select",
                                                    value="400",
                                                    data=[
                                                        {"value": "200", "label": "Small (200x200)"},
                                                        {"value": "400", "label": "Medium (400x400)"},
                                                        {"value": "600", "label": "Large (600x600)"},
                                                        {"value": "800", "label": "XLarge (800x800)"},
                                                    ],
                                                    style={"flex": 1},
                                                ),
                                            ],
                                            grow=True,
                                            mb="md",
                                        ),
                                        
                                        dmc.Group(
                                            [
                                                dmc.Text("Region:", fw=500),
                                                dmc.Select(
                                                    id="region-select",
                                                    value="full",
                                                    data=[
                                                        {"value": "full", "label": "Full Set"},
                                                        {"value": "zoom1", "label": "Zoom 1x"},
                                                        {"value": "zoom2", "label": "Zoom 2x"},
                                                        {"value": "zoom3", "label": "Zoom 3x"},
                                                    ],
                                                    style={"flex": 1},
                                                ),
                                            ],
                                            grow=True,
                                            mb="md",
                                        ),
                                        
                                        dmc.Button(
                                            "Generate",
                                            id="generate-btn",
                                            fullWidth=True,
                                            color="blue",
                                            size="md",
                                        ),
                                    ],
                                    gap="md",
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                        ),
                    ],
                    span={"base": 12, "sm": 4},
                ),
                
                dmc.GridCol(
                    [
                        dmc.Paper(
                            [
                                html.Div(
                                    id="mandelbrot-container",
                                    children=[
                                        dmc.Center(
                                            [
                                                dmc.Loader(
                                                    size="lg",
                                                    color="blue",
                                                ),
                                                dmc.Text("Generating initial image...", mt="md"),
                                            ],
                                            style={"height": "400px"},
                                        ),
                                    ],
                                    style={"minHeight": "400px", "display": "flex", "alignItems": "center", "justifyContent": "center"},
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                        ),
                        html.Div(id="mandelbrot-description", style={"marginTop": "1rem"}),
                    ],
                    span={"base": 12, "sm": 8},
                ),
            ],
            gutter="lg",
        ),
    ],
    size="lg",
    py="lg",
)


# Define zoom regions
ZOOM_REGIONS = {
    "full": (-2, 1, -1.5, 1.5),
    "zoom1": (-0.8, -0.4, -0.2, 0.2),
    "zoom2": (-0.748, -0.746, 0.099, 0.101),
    "zoom3": (-0.7485, -0.7465, 0.0995, 0.1005),
}


@callback(
    Output("mandelbrot-container", "children"),
    Output("mandelbrot-description", "children"),
    Input("generate-btn", "n_clicks"),
    State("max-iter-input", "value"),
    State("image-size-select", "value"),
    State("region-select", "value"),
    prevent_initial_call=False,
)
def update_mandelbrot(n_clicks, max_iter, size, region):
    """Generate and display the Mandelbrot set."""
    if max_iter is None or size is None or region is None:
        error = dmc.Alert("Please fill in all parameters", color="red", title="Error")
        return error, ""
    
    try:
        # Get image size
        image_size = int(size)
        
        # Get region bounds
        xmin, xmax, ymin, ymax = ZOOM_REGIONS.get(region, ZOOM_REGIONS["full"])
        
        # Generate image
        image_src = generate_mandelbrot_image(xmin, xmax, ymin, ymax, image_size, image_size, max_iter, coloring_function=iteration_count, color_index_function=simple_index, palette_function=simple_palette)
        
        image_element = html.Img(
            src=image_src,
            style={
                "maxWidth": "100%",
                "height": "auto",
                "borderRadius": "8px",
            },
        )
        
        description = dmc.Text(
            f"Max iterations: {max_iter} | Size: {image_size}x{image_size} | Region: {region}",
            size="sm",
            c="dimmed",
            ta="center",
        )
        
        return image_element, description
    
    except Exception as e:
        error = dmc.Alert(
            f"Error generating image: {str(e)}",
            color="red",
            title="Error",
        )
        return error, ""
