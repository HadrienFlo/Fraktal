import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, callback, callback_context, no_update, ctx


def create_simple_tab(tab_id):
    return dmc.TabsTab(tab_id, value=tab_id)


def create_closable_tab(tab_id):
    return dmc.TabsTab(
        children=[
            tab_id,
            dmc.ActionIcon(
                "x",
                id={"type": "delete-tab-btn", "index": tab_id},
                size="sm",
                variant="transparent",
                ml=5,
            ),
        ],
        value=tab_id
    )


@callback(
    Output("tabs", "children", allow_duplicate=True),
    Input("tabs-store", "data"),
    prevent_initial_call=True,
)
def sync_tabs_to_store(tabs_data):
    if not tabs_data:
        return no_update
    
    tabs_list = []
    for tab_id in tabs_data.keys():
        if tab_id == "form-tab":
            tabs_list.append(create_simple_tab(tab_id))
        else:
            tabs_list.append(create_closable_tab(tab_id))

    return dmc.TabsList(tabs_list)


@callback(
    Output("tabs-store", "data", allow_duplicate=True),
    Input({"type": "delete-tab-btn", "index": ALL}, "n_clicks"),
    State("tabs-store", "data"),
    prevent_initial_call=True,
)
def delete_tab(n_clicks_list, tabs_data):
    if not ctx.triggered or not tabs_data:
        return no_update

    # Check if any button was actually clicked (not just added)
    if not any(n_clicks_list) or all(n is None or n == 0 for n in n_clicks_list):
        return no_update

    # Safely get the triggered component ID
    triggered_id = ctx.triggered_id
    if not triggered_id or "index" not in triggered_id:
        return no_update
    
    tab_id = triggered_id["index"]

    if tab_id in tabs_data:
        print(f"Deleting tab: {tab_id}")
        del tabs_data[tab_id]

    return tabs_data