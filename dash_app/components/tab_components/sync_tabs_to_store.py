import shutil
import json
from pathlib import Path
import dash_mantine_components as dmc
from dash import ALL, Input, Output, State, callback, callback_context, no_update, ctx


def _get_tabs_base_dir():
    """Get the base tabs directory."""
    # This file is at dash_app/components/tab_components/sync_tabs_to_store.py
    return Path(__file__).parents[2] / "tabs"


def _get_tab_name(tab_id):
    """Get the display name for a tab from its JSON file."""
    if tab_id == "form-tab":
        return "Form tab"
    
    tab_folder = _get_tabs_base_dir() / tab_id
    json_file = tab_folder / f"{tab_id}.json"
    
    if json_file.exists():
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('tab_name', tab_id)
        except Exception:
            return tab_id
    return tab_id


def create_simple_tab(tab_id):
    return dmc.TabsTab(_get_tab_name(tab_id), value=tab_id)


def create_closable_tab(tab_id):
    return dmc.TabsTab(
        children=[
            _get_tab_name(tab_id),
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
    Output("tabs", "value", allow_duplicate=True),
    Input({"type": "delete-tab-btn", "index": ALL}, "n_clicks"),
    State("tabs-store", "data"),
    State("tabs", "value"),
    prevent_initial_call=True,
)
def delete_tab(n_clicks_list, tabs_data, current_tab):
    if not ctx.triggered or not tabs_data:
        return no_update, no_update

    # Check if any button was actually clicked (not just added)
    if not any(n_clicks_list) or all(n is None or n == 0 for n in n_clicks_list):
        return no_update, no_update

    # Safely get the triggered component ID
    triggered_id = ctx.triggered_id
    if not triggered_id or "index" not in triggered_id:
        return no_update, no_update
    
    tab_id = triggered_id["index"]

    if tab_id in tabs_data:
        print(f"Deleting tab: {tab_id}")
        
        # Delete the tab folder and all its contents
        tab_folder = _get_tabs_base_dir() / tab_id
        if tab_folder.exists():
            shutil.rmtree(tab_folder)
            print(f"Deleted folder: {tab_folder}")
        
        # Remove from store
        del tabs_data[tab_id]
        
        # Determine which tab to activate after deletion
        new_active_tab = current_tab
        if current_tab == tab_id:
            # If we're deleting the active tab, switch to another
            remaining_tabs = list(tabs_data.keys())
            if remaining_tabs:
                # Prefer form-tab if available, otherwise use the first remaining tab
                new_active_tab = "form-tab" if "form-tab" in remaining_tabs else remaining_tabs[0]
            else:
                new_active_tab = None
        
        return tabs_data, new_active_tab

    return no_update, no_update