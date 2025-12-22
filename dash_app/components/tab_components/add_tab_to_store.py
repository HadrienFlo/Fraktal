import uuid
import json
from pathlib import Path
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, no_update
from fraktal.config import load_default_config
from components.tab_components.generate_tab_content import generate_fractal_tab_content


def _get_tabs_base_dir():
    """Get the base tabs directory."""
    # This file is at dash_app/components/tab_components/add_tab_to_store.py
    return Path(__file__).parents[2] / "tabs"


@callback(
    Output("tabs-store", "data", allow_duplicate=True),
    Output("tabs", "value", allow_duplicate=True),
    Input("add-tab-button", "n_clicks"),
    State("tabs-store", "data"),
    State("tab-name-input", "value"),
    State("center-x-input", "value"),
    State("center-y-input", "value"),
    State("zoom-input", "value"),
    State("width-input", "value"),
    State("height-input", "value"),
    State("max-iter-input", "value"),
    State("coloring-function-input", "value"),
    State("color-index-function-input", "value"),
    State("palette-function-input", "value"),
    State("use-cython-switch", "checked"),
    prevent_initial_call=True,
)
def add_tab_to_store(n_clicks, tabs_data, tab_name, center_x, center_y, zoom, width, height, max_iter, coloring_function, color_index_function, palette_function, use_cython):
    if not n_clicks or not tabs_data:
        return no_update
    
    # Load default configuration
    config = load_default_config()
    mandelbrot_defaults = config.get('mandelbrot', {})
    
    # Create a new tab ID
    new_tab_id = str(uuid.uuid4())
    
    # Create folder for this tab
    tab_folder = _get_tabs_base_dir() / new_tab_id
    tab_folder.mkdir(parents=True, exist_ok=True)
    
    # Save input data to JSON file
    inputs_data = {
        "tab_id": new_tab_id,
        "tab_name": tab_name or mandelbrot_defaults.get('tab_name', 'Untitled'),
        "center_x": center_x if center_x is not None else mandelbrot_defaults.get('center_x', -0.5),
        "center_y": center_y if center_y is not None else mandelbrot_defaults.get('center_y', 0.0),
        "zoom": zoom if zoom is not None else mandelbrot_defaults.get('zoom', 1.0),
        "width": width if width is not None else mandelbrot_defaults.get('width', 800),
        "height": height if height is not None else mandelbrot_defaults.get('height', 600),
        "max_iter": max_iter if max_iter is not None else mandelbrot_defaults.get('max_iter', 256),
        "fractal_type": mandelbrot_defaults.get('fractal_type', 'mandelbrot'),
        "coloring_function": coloring_function or mandelbrot_defaults.get('coloring_function', 'smooth-iteration-count'),
        "color_index_function": color_index_function or mandelbrot_defaults.get('color_index_function', 'simple-index'),
        "palette_function": palette_function or mandelbrot_defaults.get('palette_function', 'simple-palette'),
        "use_cython": use_cython if use_cython is not None else mandelbrot_defaults.get('use_cython', False),
    }
    
    json_file = tab_folder / f"{new_tab_id}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(inputs_data, f, indent=2)
    
    # Generate tab content with fractal image
    new_tab_content = generate_fractal_tab_content(
        new_tab_id,
        inputs_data["tab_name"],
        inputs_data
    )
    
    # Add new tab to the store
    tabs_data[new_tab_id] = new_tab_content
    
    print(f"Added new tab: {new_tab_id}")
    print(f"Created folder: {tab_folder}")
    print(f"Saved inputs to: {json_file}")
    print(f"Current tabs data keys: {list(tabs_data.keys())}")
    return tabs_data, new_tab_id