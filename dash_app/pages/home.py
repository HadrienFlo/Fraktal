"""Home / landing page for Fraktal Dash app.

This POC includes LaTeX equations rendered via MathJax and a small Mandelbrot
thumbnail generated from the project's engines to show a preview.
"""

import dash
from dash import html, dcc, Input, Output, State, callback, MATCH, ALL
import dash_mantine_components as dmc
import numpy as np
from PIL import Image
import io
import base64
from pathlib import Path

from fraktal.engines.mandelbrot import mandelbrot_set
from fraktal.engines.palette import simple_palette, hot_palette, cool_palette

# register page as root
dash.register_page(__name__, path="/", name="Home")

# palette mapping
def get_palette_function(name: str):
    """Return a palette function by name."""
    if name == "hot":
        return hot_palette
    elif name == "cool":
        return cool_palette
    else:
        return simple_palette

def _image_to_base64(img_array: np.ndarray) -> str:
    """Convert a numpy RGB image array to base64 PNG data URL."""
    img = Image.fromarray(img_array.astype(np.uint8), "RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{data}"


def load_markdown_content(filename: str) -> str:
    """Load markdown content from the assets/content directory."""
    content_path = Path(__file__).parent.parent / "assets" / "content" / filename
    return content_path.read_text(encoding="utf-8")


def generate_thumbnail(
    width: int = 200,
    height: int = 150,
    max_iter: int = 80,
    coloring_function=None,
    palette: str = "simple",
) -> str:
    """Generate a small Mandelbrot thumbnail (RGB) and return a data URL.

    Uses the project's NumPy implementation (`mandelbrot_set`) for quick generation.
    """
    xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
    data = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    # Normalize to [0, 1]
    norm = data.astype(float) / float(max_iter)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    # Select palette function
    palette_fn = get_palette_function(palette)

    for i in range(height):
        for j in range(width):
            if coloring_function is not None:
                I = coloring_function(norm[i, j], max_iter)
            else:
                I = norm[i, j]
            # Use selected palette (expects normalized index in [0,1] for hot,
            # simple_palette clamps internally when converting to 0-255)
            r, g, b = palette_fn(I)
            img[i, j, 0] = r
            img[i, j, 1] = g
            img[i, j, 2] = b
    return _image_to_base64(img)


layout = dmc.Container(
    [
        # Store for tab counter with session storage (persists across page refreshes)
        dcc.Store(id="tab-counter-store", data={"count": 4}, storage_type="session"),
        
        # Store for tabs state (persists the actual tabs structure)
        dcc.Store(id="tabs-state-store", storage_type="session"),
        
        # Store for the input value/placeholder (persists across page navigation)
        dcc.Store(id="input-suggestion-store", data={"value": "Tab 4", "placeholder": "Tab 4"}, storage_type="session"),
        
        # MathJax script for LaTeX rendering on this page
        html.Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),

        dmc.Title("Fraktal — interactive fractal explorer", order=1, mt="lg", mb="md"),

        dmc.Group(
            [
                dmc.Stack(
                    [
                        dmc.Text(
                            "Fraktal is a lightweight exploratory app for generating and visualizing mathematical \n" \
                            "fractals such as the Mandelbrot set. Use the Mandelbrot page to interactively tune \n" \
                            "parameters and render images.",
                            style={"whiteSpace": "pre-line"},
                        ),

                        dcc.Markdown(
                            load_markdown_content("mandelbrot_definition.md"),
                            mathjax=True,
                        ),

                        dmc.Text("Try the interactive Mandelbrot page to generate higher-resolution images and explore zoomed regions."),

                        dmc.Divider(my="lg"),

                    ],
                    gap="sm",
                ),

                dmc.Grid(
                    gutter="lg",
                    children=[
                        # thumbnail 1
                        dmc.GridCol([
                            dmc.Card(
                                [
                                    dmc.CardSection(
                                        html.Img(src=generate_thumbnail(), style={"width": "100%", "borderRadius": "6px"})
                                    ),
                                    dmc.Text("Rendered with project's engine — click through to generate larger images.", size="sm", c="dimmed", mt="sm"),
                                ],
                                shadow="sm",
                                radius="md",
                                style={"maxWidth": "360px"},
                            ),
                        ], span={"base": 12, "md": 6, "lg": 4}),
                        # thumbnail 2
                        dmc.GridCol([
                            dmc.Card(
                                [
                                    dmc.CardSection(
                                        html.Img(src=generate_thumbnail(palette="hot"), style={"width": "100%", "borderRadius": "6px"})
                                    ),
                                    dmc.Text("Rendered with project's engine — click through to generate larger images.", size="sm", c="dimmed", mt="sm"),
                                ],
                                shadow="sm",
                                radius="md",
                                style={"maxWidth": "360px"},
                            ),
                        ], span={"base": 12, "md": 6, "lg": 4}),
                        # thumbnail 3
                        dmc.GridCol([
                            dmc.Card(
                                [
                                    dmc.CardSection(
                                        html.Img(src=generate_thumbnail(palette="cool"), style={"width": "100%", "borderRadius": "6px"})
                                    ),
                                    dmc.Text("Rendered with project's engine — click through to generate larger images.", size="sm", c="dimmed", mt="sm"),
                                ],
                                shadow="sm",
                                radius="md",
                                style={"maxWidth": "360px"},
                            ),
                        ], span={"base": 12, "md": 6, "lg": 4}),
                    ],
                ),

            ],
            align="flex-start",
            gap="xl",
        ),
    ],
    size="lg",
    py="lg",
)
