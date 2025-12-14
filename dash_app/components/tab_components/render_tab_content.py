import dash_mantine_components as dmc
from dash import Input, Output, State, callback, no_update

@callback(
    Output("tabs-content", "children"), 
    Input("tabs", "value"),
    State("tabs-store", "data")
)
def render_content(active, tabs_data):
    if not tabs_data or active not in tabs_data:
        return no_update
    return tabs_data[active]
    