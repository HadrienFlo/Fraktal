import uuid
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, no_update



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
    
    # Create a new tab content
    new_tab_id = str(uuid.uuid4())
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
    print(f"Current tabs data keys: {list(tabs_data.keys())}")
    return tabs_data, new_tab_id