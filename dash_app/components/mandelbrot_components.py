"""UI Components for Mandelbrot page"""

from dash import html
import dash_mantine_components as dmc

from fraktal.mapping import FRAKTAL_MODELS


def create_image_panel_content(
    image_id, image_src, max_iter, bailout, image_size, region,
    coloring_model, color_index_model, palette_model
):
    """Helper function to create the content for an image tab panel."""
    return dmc.Grid([
        # Left column - Image and description
        dmc.GridCol([
            dmc.Paper([
                dmc.Center(
                    html.Img(
                        id={"type": "image-display", "index": image_id},
                        src=image_src,
                        style={
                            "maxWidth": "100%",
                            "height": "auto",
                            "borderRadius": "8px",
                        },
                    ),
                ),
            ], p="md", radius="md", withBorder=True),
            dmc.Text(
                id={"type": "image-description", "index": image_id},
                children=f"Max iterations: {max_iter} | Size: {image_size}x{image_size} | Region: {region} | Bailout: {bailout}",
                size="sm",
                c="dimmed",
                ta="center",
                mt="sm",
            ),
        ], span={"base": 12, "md": 8}),
        
        # Right column - Controls
        dmc.GridCol([
            dmc.Paper([
                dmc.Title("Update Image", order=4, mb="md"),
                dmc.Stack([
                    dmc.Group([
                        dmc.Text("Max Iterations:", fw=500),
                        dmc.NumberInput(
                            id={"type": "update-max-iter", "index": image_id},
                            value=max_iter,
                            min=10,
                            max=10000,
                            step=10,
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="sm"),
                    
                    dmc.Group([
                        dmc.Text("Bailout:", fw=500),
                        dmc.NumberInput(
                            id={"type": "update-bailout", "index": image_id},
                            value=bailout,
                            min=1,
                            max=10,
                            step=0.1,
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="sm"),
                    
                    dmc.Group([
                        dmc.Text("Image Size:", fw=500),
                        dmc.Select(
                            id={"type": "update-image-size", "index": image_id},
                            value=str(image_size),
                            data=[
                                {"value": "200", "label": "Small (200x200)"},
                                {"value": "400", "label": "Medium (400x400)"},
                                {"value": "600", "label": "Large (600x600)"},
                                {"value": "800", "label": "XLarge (800x800)"},
                            ],
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="sm"),
                    
                    dmc.Group([
                        dmc.Text("Region:", fw=500),
                        dmc.Select(
                            id={"type": "update-region", "index": image_id},
                            value=region,
                            data=[
                                {"value": "full", "label": "Full Set"},
                                {"value": "zoom1", "label": "Zoom 1x"},
                                {"value": "zoom2", "label": "Zoom 2x"},
                                {"value": "zoom3", "label": "Zoom 3x"},
                            ],
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="sm"),
                    
                    dmc.Group([
                        dmc.Text("Coloring model:", fw=500),
                        dmc.Select(
                            id={"type": "update-coloring-model", "index": image_id},
                            value=coloring_model,
                            data=[
                                {"value": k, "label": FRAKTAL_MODELS["coloring"][k]["name"]}
                                for k in FRAKTAL_MODELS["coloring"].keys()
                            ],
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="sm"),
                    
                    dmc.Group([
                        dmc.Text("Color index model:", fw=500),
                        dmc.Select(
                            id={"type": "update-color-index-model", "index": image_id},
                            value=color_index_model,
                            data=[
                                {"value": k, "label": FRAKTAL_MODELS["color_index"][k]["name"]}
                                for k in FRAKTAL_MODELS["color_index"].keys()
                            ],
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="sm"),
                    
                    dmc.Group([
                        dmc.Text("Palette model:", fw=500),
                        dmc.Select(
                            id={"type": "update-palette-model", "index": image_id},
                            value=palette_model,
                            data=[
                                {"value": k, "label": FRAKTAL_MODELS["palette"][k]["name"]}
                                for k in FRAKTAL_MODELS["palette"].keys()
                            ],
                            style={"flex": 1},
                        ),
                    ], grow=True, mb="md"),
                    
                    dmc.Button(
                        "Update Image",
                        id={"type": "update-image-btn", "index": image_id},
                        fullWidth=True,
                        color="blue",
                        size="sm",
                    ),
                ], gap="xs"),
            ], p="md", radius="md", withBorder=True),
        ], span={"base": 12, "md": 4}),
    ], gutter="md")


def create_form_panel():
    """Create the main form panel for generating Mandelbrot images."""
    return dmc.TabsPanel(
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
                                                dmc.Text("Bailout:", fw=500),
                                                dmc.NumberInput(
                                                    id="bailout-input",
                                                    value=2,
                                                    min=1,
                                                    max=10,
                                                    step=0.1,
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

                                        dmc.Group(
                                            [
                                                dmc.Text("Coloring model:", fw=500),
                                                dmc.Select(
                                                    id="coloring-model-select",
                                                    value="iteration-count",
                                                    data=[
                                                        {"value": k, "label": FRAKTAL_MODELS["coloring"][k]["name"]}
                                                        for k in FRAKTAL_MODELS["coloring"].keys()
                                                    ],
                                                    style={"flex": 1},
                                                ),
                                            ],
                                            grow=True,
                                            mb="md",
                                        ),

                                        dmc.Group(
                                            [
                                                dmc.Text("Color index model:", fw=500),
                                                dmc.Select(
                                                    id="color-index-model-select",
                                                    value="simple-index",
                                                    data=[
                                                        {"value": k, "label": FRAKTAL_MODELS["color_index"][k]["name"]}
                                                        for k in FRAKTAL_MODELS["color_index"].keys()
                                                    ],
                                                    style={"flex": 1},
                                                ),
                                            ],
                                            grow=True,
                                            mb="md",
                                        ),

                                        dmc.Group(
                                            [
                                                dmc.Text("Palette model:", fw=500),
                                                dmc.Select(
                                                    id="palette-model-select",
                                                    value="simple-palette",
                                                    data=[
                                                        {"value": k, "label": FRAKTAL_MODELS["palette"][k]["name"]}
                                                        for k in FRAKTAL_MODELS["palette"].keys()
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
                                            size="lg",
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
                    span={"base": 12, "sm": 6},
                ),
                dmc.GridCol(
                    [
                        dmc.Paper(
                            [
                                dmc.Text(
                                    "Click 'Generate' to create a new Mandelbrot image in a new tab.",
                                    size="lg",
                                    ta="center",
                                    c="dimmed",
                                    p="xl",
                                ),
                            ],
                            p="md",
                            radius="md",
                            withBorder=True,
                            style={"minHeight": "400px", "display": "flex", "alignItems": "center", "justifyContent": "center"},
                        ),
                    ],
                    span={"base": 12, "sm": 6},
                ),
            ],
            gutter="lg",
        ),
        value="form-tab",
    )
