"""Home / landing page for Fraktal Dash app.

This POC includes LaTeX equations rendered via MathJax and a small Mandelbrot
thumbnail generated from the project's engines to show a preview.
"""

import dash
from dash import html, dcc
import dash_mantine_components as dmc
import numpy as np
from PIL import Image
import io
import base64

from fraktal.engines.mandelbrot import mandelbrot_set
from fraktal.engines.palette import simple_palette

# register page as root
dash.register_page(__name__, path="/", name="Home")


def _image_to_base64(img_array: np.ndarray) -> str:
    """Convert a numpy RGB image array to base64 PNG data URL."""
    img = Image.fromarray(img_array.astype(np.uint8), "RGB")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode()
    return f"data:image/png;base64,{data}"


def generate_thumbnail(width: int = 200, height: int = 150, max_iter: int = 80):
    """Generate a small Mandelbrot thumbnail (RGB) and return a data URL.

    Uses the project's NumPy implementation (`mandelbrot_set`) for quick generation.
    """
    xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
    data = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iter)
    # Normalize to [0, 1]
    norm = data.astype(float) / float(max_iter)
    img = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            r, g, b = simple_palette(norm[i, j], k=2.5, u0=0)
            img[i, j, 0] = r
            img[i, j, 1] = g
            img[i, j, 2] = b
    return _image_to_base64(img)


layout = dmc.Container(
    [
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

                        dcc.Markdown(r"""
### A quick mathematical definition

The Mandelbrot iteration is given by:

$$
z_{0} = 0, \quad z_{n+1} = z_n^2 + c
$$

The Mandelbrot set is the set of complex parameters $c$ for which the orbit of $z_0$ stays bounded:

$$
\mathcal{M} = \{ c \in \mathbb{C} : \sup_n |z_n| \le 2 \}\,.
$$

We color each point by the number of iterations needed to escape the bailout radius (or the maximum iteration count if it does not escape).

""",
                            mathjax=True,
                        ),

                        dmc.Text("Try the interactive Mandelbrot page to generate higher-resolution images and explore zoomed regions."),

                        dmc.Anchor("Open Mandelbrot page", href="/mandelbrot", target="_self", style={"marginTop": "6px"}),
                    ],
                    gap="sm",
                ),

                # thumbnail
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
            ],
            align="flex-start",
            gap="xl",
        ),
    ],
    size="lg",
    py="lg",
)
