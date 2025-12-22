import dash_mantine_components as dmc
from fraktal.config import load_default_config
from fraktal.mapping import FRAKTAL_MODELS

# Load default configuration
config = load_default_config()
mandelbrot_defaults = config.get('mandelbrot', {})

# Define the form with Mandelbrot parameters
form = dmc.Container(
    [
        dmc.TextInput(
            label="Tab Name",
            id="tab-name-input",
            placeholder="My Mandelbrot",
            required=True,
            my=10
        ),
        dmc.NumberInput(
            label="Center X",
            id="center-x-input",
            value=mandelbrot_defaults.get('center_x', -0.5),
            step=0.1,
            decimalScale=10,
            my=10
        ),
        dmc.NumberInput(
            label="Center Y",
            id="center-y-input",
            value=mandelbrot_defaults.get('center_y', 0.0),
            step=0.1,
            decimalScale=10,
            my=10
        ),
        dmc.NumberInput(
            label="Zoom",
            id="zoom-input",
            value=mandelbrot_defaults.get('zoom', 1.0),
            min=0.1,
            step=0.1,
            my=10
        ),
        dmc.NumberInput(
            label="Width (pixels)",
            id="width-input",
            value=mandelbrot_defaults.get('width', 800),
            min=100,
            step=50,
            my=10
        ),
        dmc.NumberInput(
            label="Height (pixels)",
            id="height-input",
            value=mandelbrot_defaults.get('height', 600),
            min=100,
            step=50,
            my=10
        ),
        dmc.NumberInput(
            label="Max Iterations",
            id="max-iter-input",
            value=mandelbrot_defaults.get('max_iter', 256),
            min=10,
            max=10000,
            step=10,
            my=10
        ),
        dmc.Select(
            label="Coloring Function",
            id="coloring-function-input",
            value=mandelbrot_defaults.get('coloring_function', 'smooth-iteration-count'),
            data=[
                {"value": key, "label": val["name"]}
                for key, val in FRAKTAL_MODELS["coloring"].items()
            ],
            my=10
        ),
        dmc.Select(
            label="Color Index Function",
            id="color-index-function-input",
            value=mandelbrot_defaults.get('color_index_function', 'simple-index'),
            data=[
                {"value": key, "label": val["name"]}
                for key, val in FRAKTAL_MODELS["color_index"].items()
            ],
            my=10
        ),
        dmc.Select(
            label="Palette Function",
            id="palette-function-input",
            value=mandelbrot_defaults.get('palette_function', 'simple-palette'),
            data=[
                {"value": key, "label": val["name"]}
                for key, val in FRAKTAL_MODELS["palette"].items()
            ],
            my=10
        ),
        dmc.Group([
            dmc.Button("Add Tab", id="add-tab-button", variant="outline", my=10),
        ]),
    ],
    id="form-container",
    size="sm",
    py="lg"
)