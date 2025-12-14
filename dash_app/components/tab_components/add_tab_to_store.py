import uuid
import json
from pathlib import Path
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, no_update


def _get_tabs_base_dir():
    """Get the base tabs directory."""
    # This file is at dash_app/components/tab_components/add_tab_to_store.py
    return Path(__file__).parents[2] / "tabs"


@callback(
    Output("tabs-store", "data", allow_duplicate=True),
    Output("tabs", "value", allow_duplicate=True),
    Input("add-tab-button", "n_clicks"),
    State("tabs-store", "data"),
    prevent_initial_call=True,
)
def add_tab_to_store(n_clicks, tabs_data):
    if not n_clicks or not tabs_data:
        return no_update
    
    # Create a new tab ID
    new_tab_id = str(uuid.uuid4())
    
    # Create folder for this tab
    tab_folder = _get_tabs_base_dir() / new_tab_id
    tab_folder.mkdir(parents=True, exist_ok=True)
    
    # Save input data to JSON file
    inputs_data = {
        "tab_id": new_tab_id,
        "created_at": str(uuid.uuid4()),  # Placeholder - you can add timestamp or actual inputs
        # Add your actual input parameters here when you have them
        # e.g., "max_iter": 100, "bailout": 2, etc.
    }
    
    json_file = tab_folder / f"{new_tab_id}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(inputs_data, f, indent=2)
    
    # Create tab content
    new_tab_content = dmc.Container(
        [
            dmc.Text(f"This is the content of {new_tab_id}.", my=10),
        ],
        id=f"{new_tab_id}-container",
        size="sm", py="lg"
    )
    
    # Add new tab to the store
    tabs_data[new_tab_id] = new_tab_content
    
    print(f"Added new tab: {new_tab_id}")
    print(f"Created folder: {tab_folder}")
    print(f"Saved inputs to: {json_file}")
    print(f"Current tabs data keys: {list(tabs_data.keys())}")
    return tabs_data, new_tab_id