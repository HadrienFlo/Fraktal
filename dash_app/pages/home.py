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

                        dmc.Divider(my="lg"),

                        dmc.Title("Interactive Tabs Example", order=3, mb="md"),
                        dmc.Text("Example of closable tabs with dynamic content:", size="sm", c="dimmed", mb="sm"),

                        html.Div(id="tabs-container", children=[
                            dmc.Tabs(
                                id="closable-tabs",
                                value="tab-1",
                                children=[
                                    dmc.TabsList([
                                        dmc.TabsTab("Tab 1", value="tab-1"),  # First tab - no close button
                                        dmc.TabsTab("Tab 2", value="tab-2", rightSection=dmc.ActionIcon(
                                            "×",
                                            id={"type": "close-tab", "index": "tab-2"},
                                            size="xs",
                                            variant="subtle",
                                            c="gray",
                                        )),
                                        dmc.TabsTab("Tab 3", value="tab-3", rightSection=dmc.ActionIcon(
                                            "×",
                                            id={"type": "close-tab", "index": "tab-3"},
                                            size="xs",
                                            variant="subtle",
                                            c="gray",
                                        )),
                                    ]),
                                    dmc.TabsPanel(
                                        dmc.Stack([
                                            dmc.Text("Content for Tab 1 (this tab cannot be closed)", mt="sm"),
                                            dmc.TextInput(
                                                id="new-tab-name-input",
                                                label="New tab name",
                                                placeholder="Tab 4",
                                                value="Tab 4",
                                                style={"maxWidth": "300px"},
                                            ),
                                            dmc.Button("Add New Tab", id="add-tab-btn", size="sm", variant="light"),
                                        ], gap="sm"),
                                        value="tab-1"
                                    ),
                                    dmc.TabsPanel(
                                        dmc.Text("Content for Tab 2", mt="sm"),
                                        value="tab-2"
                                    ),
                                    dmc.TabsPanel(
                                        dmc.Text("Content for Tab 3", mt="sm"),
                                        value="tab-3"
                                    ),
                                ],
                            )
                        ]),

                        dmc.Anchor("Open Mandelbrot page", href="/mandelbrot", target="_self", style={"marginTop": "1rem"}),
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


# Callback to restore tabs from storage on page load
@callback(
    Output("tabs-container", "children", allow_duplicate=True),
    Output("closable-tabs", "value", allow_duplicate=True),
    Input("tabs-state-store", "data"),
    prevent_initial_call='initial_duplicate',
)
def restore_tabs(stored_tabs_data):
    """Restore tabs from session storage when page loads."""
    if stored_tabs_data is not None:
        # Stored data contains the tabs structure and active tab
        return stored_tabs_data.get("tabs"), stored_tabs_data.get("active_tab")
    return dash.no_update, dash.no_update


# Callback to restore input values from storage on page load
@callback(
    Output("new-tab-name-input", "value", allow_duplicate=True),
    Output("new-tab-name-input", "placeholder", allow_duplicate=True),
    Input("input-suggestion-store", "data"),
    prevent_initial_call='initial_duplicate',
)
def restore_input_values(stored_input_data):
    """Restore input value and placeholder from session storage when page loads."""
    if stored_input_data is not None:
        return stored_input_data.get("value"), stored_input_data.get("placeholder")
    return dash.no_update, dash.no_update


@callback(
    Output("tabs-container", "children"),
    Output("closable-tabs", "value"),
    Output("new-tab-name-input", "value"),
    Output("new-tab-name-input", "placeholder"),
    Output("tab-counter-store", "data"),
    Output("tabs-state-store", "data"),
    Output("input-suggestion-store", "data"),
    Input({"type": "close-tab", "index": ALL}, "n_clicks"),
    Input("add-tab-btn", "n_clicks"),
    State("closable-tabs", "value"),
    State("tabs-container", "children"),
    State("new-tab-name-input", "value"),
    State("tab-counter-store", "data"),
    prevent_initial_call=True,
)
def manage_tabs(close_clicks, add_clicks, current_tab, tabs_container, new_tab_name, counter_data):
    """Handle closing and adding tabs."""
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    trigger_id = ctx.triggered[0]["prop_id"]
    
    # Get current tabs structure
    current_tabs = tabs_container[0] if tabs_container else None
    if not current_tabs or "props" not in current_tabs:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    tab_list = current_tabs["props"]["children"][0]["props"]["children"]
    tab_panels = current_tabs["props"]["children"][1:]
    
    # Handle closing a tab
    if "close-tab" in trigger_id:
        # Find which close button was clicked
        for i, clicks in enumerate(close_clicks):
            if clicks:
                # Account for the first tab not having a close button (offset by 1)
                actual_tab_index = i + 1  # Skip tab-1 which has no close button
                tab_to_remove = tab_list[actual_tab_index]["props"]["value"]
                
                # Remove the tab and its panel
                tab_list.pop(actual_tab_index)
                tab_panels = [p for p in tab_panels if p["props"]["value"] != tab_to_remove]
                
                # If we removed the active tab, switch to first tab
                new_active = current_tab
                if tab_to_remove == current_tab:
                    new_active = "tab-1"  # Always fall back to the permanent first tab
                
                # Rebuild tabs component
                new_tabs = dmc.Tabs(
                    id="closable-tabs",
                    value=new_active,
                    children=[
                        dmc.TabsList(tab_list),
                        *tab_panels
                    ]
                )
                # Keep the input and counter as is when closing tabs, but update tabs state
                tabs_state = {"tabs": [new_tabs], "active_tab": new_active}
                return [new_tabs], new_active, dash.no_update, dash.no_update, dash.no_update, tabs_state, dash.no_update
    
    # Handle adding a new tab
    if "add-tab-btn" in trigger_id:
        current_count = counter_data['count']
        new_tab_id = f"tab-{current_count}"
        
        # Use the custom name from input, or default to "Tab X"
        tab_name = new_tab_name.strip() if new_tab_name and new_tab_name.strip() else f"Tab {current_count}"
        
        # Always increment counter for next tab
        new_count = current_count + 1
        
        # Create new tab with close button
        new_tab = dmc.TabsTab(
            tab_name,
            value=new_tab_id,
            rightSection=dmc.ActionIcon(
                "×",
                id={"type": "close-tab", "index": new_tab_id},
                size="xs",
                variant="subtle",
                c="gray",
            )
        )
        
        # Create new panel
        new_panel = dmc.TabsPanel(
            dmc.Text(f"Content for {tab_name}", mt="sm"),
            value=new_tab_id
        )
        
        # Add to lists
        tab_list.append(new_tab)
        tab_panels.append(new_panel)
        
        # Rebuild tabs component
        new_tabs = dmc.Tabs(
            id="closable-tabs",
            value=new_tab_id,  # Switch to newly created tab
            children=[
                dmc.TabsList(tab_list),
                *tab_panels
            ]
        )
        
        # Update input with next default value, increment counter, and save all states
        next_tab_name = f"Tab {new_count}"
        tabs_state = {"tabs": [new_tabs], "active_tab": new_tab_id}
        input_state = {"value": next_tab_name, "placeholder": next_tab_name}
        return [new_tabs], new_tab_id, next_tab_name, next_tab_name, {"count": new_count}, tabs_state, input_state
    
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
