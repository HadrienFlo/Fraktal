"""Mandelbrot Set Visualization Page"""

import dash
from dash import dcc, html, Input, Output, State, callback, ALL, MATCH
import dash_mantine_components as dmc
import uuid
import sys
from pathlib import Path

# Add parent directory to path to import components
sys.path.insert(0, str(Path(__file__).parent.parent))

from components import generate_mandelbrot_image, ZOOM_REGIONS, create_image_panel_content, create_form_panel
from fraktal.mapping import FRAKTAL_MODELS

dash.register_page(__name__, name="Mandelbrot")


layout = dmc.Container(
    [
        dmc.Title("Mandelbrot Set", order=1, mt="lg", mb="lg"),
        
        # Store for image counter
        dcc.Store(id="image-counter-store", data={"count": 1}, storage_type="session"),
        
        # Store for tabs metadata (just IDs and labels, not the full component tree)
        dcc.Store(id="mandelbrot-tabs-metadata-store", storage_type="session"),
        
        # Centralized store for ALL image data (keyed by image_id)
        dcc.Store(id="all-images-store", storage_type="session", data={}),
        
        # Container for tabs
        html.Div(id="mandelbrot-tabs-container", children=[
            dmc.Tabs(
                id="mandelbrot-tabs",
                value="form-tab",
                children=[
                    dmc.TabsList([
                        dmc.TabsTab("Generate", value="form-tab"),
                    ]),
                    create_form_panel(),
                ],
            )
        ]),
    ],
    size="xl",
    py="lg",
)


# Callback to restore tabs from metadata and image stores on page load
@callback(
    Output("mandelbrot-tabs-container", "children", allow_duplicate=True),
    Output("mandelbrot-tabs", "value", allow_duplicate=True),
    Input("mandelbrot-tabs-metadata-store", "data"),
    State("all-images-store", "data"),
    prevent_initial_call='initial_duplicate',
)
def restore_mandelbrot_tabs(tabs_metadata, all_images):
    """Restore tabs from metadata and centralized image store when page loads."""
    print(f"Restoring tabs with metadata: {tabs_metadata}")  # Debug
    print(f"All images keys: {list(all_images.keys()) if all_images else []}")  # Debug
    
    if not tabs_metadata or not all_images:
        return dash.no_update, dash.no_update
    
    # Get tab info from metadata
    tab_list_data = tabs_metadata.get("tab_list", [])
    active_tab = tabs_metadata.get("active_tab", "form-tab")
    
    print(f"Tab list data: {tab_list_data}")  # Debug
    
    if not tab_list_data:
        return dash.no_update, dash.no_update
    
    # Build tab list
    tab_list = [dmc.TabsTab("Generate", value="form-tab")]  # Always include form tab
    
    # Build panels list - start with form panel (from layout)
    form_panel = dmc.TabsPanel(
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
                                            size="md",
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
    
    tab_panels = [form_panel]
    
    # Rebuild image tabs from centralized store
    for i, tab_data in enumerate(tab_list_data):
        tab_value = tab_data.get("value")
        if not tab_value or tab_value == "form-tab":
            continue  # Skip form tab and invalid values
        
        # Extract image_id from tab_value (format: "image-<uuid>")
        image_id = tab_value.replace("image-", "")
        store_data = all_images.get(image_id)
        
        if store_data and "image_id" in store_data:
            tab_id = tab_value
            # Derive label from value (e.g., "image-uuid" -> "Image N")
            label = f"Image {tab_data.get('index', i)}"
            
            print(f"Recreating tab {i}: value={tab_id}, label={label}, image_id={image_id}")  # Debug
            
            # Recreate tab
            new_tab = dmc.TabsTab(
                label,
                value=tab_id,
                rightSection=dmc.ActionIcon(
                    "×",
                    id={"type": "close-image-tab", "index": image_id},
                    size="xs",
                    variant="subtle",
                    c="gray",
                )
            )
            tab_list.append(new_tab)
            
            # Recreate panel (no individual store needed)
            new_panel = dmc.TabsPanel(
                dmc.Stack([
                    create_image_panel_content(
                        image_id,
                        store_data.get("image_src", ""),
                        store_data.get("max_iter", 100),
                        store_data.get("bailout", 2),
                        store_data.get("width", 400),
                        store_data.get("region", "full"),
                        store_data.get("coloring_model", "iteration-count"),
                        store_data.get("color_index_model", "simple-index"),
                        store_data.get("palette_model", "simple-palette"),
                    ),
                ], gap="md"),
                value=tab_id,
            )
            tab_panels.append(new_panel)
    
    # Rebuild tabs component
    new_tabs = dmc.Tabs(
        id="mandelbrot-tabs",
        value=active_tab,
        children=[
            dmc.TabsList(tab_list),
            *tab_panels
        ]
    )
    
    return [new_tabs], active_tab


# Callback to restore images from their stores - this now only updates existing components
@callback(
    Output({"type": "image-display", "index": ALL}, "src", allow_duplicate=True),
    Output({"type": "image-description", "index": ALL}, "children", allow_duplicate=True),
    Output({"type": "update-max-iter", "index": ALL}, "value", allow_duplicate=True),
    Output({"type": "update-bailout", "index": ALL}, "value", allow_duplicate=True),
    Output({"type": "update-image-size", "index": ALL}, "value", allow_duplicate=True),
    Output({"type": "update-region", "index": ALL}, "value", allow_duplicate=True),
    Output({"type": "update-coloring-model", "index": ALL}, "value", allow_duplicate=True),
    Output({"type": "update-color-index-model", "index": ALL}, "value", allow_duplicate=True),
    Output({"type": "update-palette-model", "index": ALL}, "value", allow_duplicate=True),
    Input("mandelbrot-tabs-container", "children"),
    State("all-images-store", "data"),
    State("mandelbrot-tabs-metadata-store", "data"),
    prevent_initial_call='initial_duplicate',
)
def restore_image_form_values(tabs_container, all_images, tabs_metadata):
    """Restore form values after tabs are rebuilt."""
    if not all_images or not tabs_metadata:
        return [dash.no_update] * 9
    
    # Get ordered list of image IDs from tab metadata
    tab_list_data = tabs_metadata.get("tab_list", [])
    
    # Extract data from centralized store in correct order
    image_sources = []
    descriptions = []
    max_iters = []
    bailouts = []
    image_sizes = []
    regions = []
    coloring_models = []
    color_index_models = []
    palette_models = []
    
    for tab_data in tab_list_data:
        tab_value = tab_data.get("value")
        if tab_value == "form-tab":
            continue
        
        # Extract image_id from tab_value
        image_id = tab_value.replace("image-", "")
        store_data = all_images.get(image_id)
        
        if store_data and "image_src" in store_data:
            image_sources.append(store_data["image_src"])
            max_iter = store_data["max_iter"]
            size = store_data["width"]
            region = store_data["region"]
            bailout = store_data["bailout"]
            descriptions.append(
                f"Max iterations: {max_iter} | Size: {size}x{size} | Region: {region} | Bailout: {bailout}"
            )
            
            # Restore form values
            max_iters.append(max_iter)
            bailouts.append(bailout)
            image_sizes.append(str(size))
            regions.append(region)
            coloring_models.append(store_data["coloring_model"])
            color_index_models.append(store_data["color_index_model"])
            palette_models.append(store_data["palette_model"])
        else:
            image_sources.append(dash.no_update)
            descriptions.append(dash.no_update)
            max_iters.append(dash.no_update)
            bailouts.append(dash.no_update)
            image_sizes.append(dash.no_update)
            regions.append(dash.no_update)
            coloring_models.append(dash.no_update)
            color_index_models.append(dash.no_update)
            palette_models.append(dash.no_update)
    
    return (
        image_sources, descriptions, max_iters, bailouts, image_sizes,
        regions, coloring_models, color_index_models, palette_models
    )


@callback(
    Output("mandelbrot-tabs-container", "children"),
    Output("mandelbrot-tabs", "value"),
    Output("image-counter-store", "data"),
    Output("mandelbrot-tabs-metadata-store", "data"),
    Output("all-images-store", "data"),
    Input("generate-btn", "n_clicks"),
    Input({"type": "close-image-tab", "index": ALL}, "n_clicks"),
    State("max-iter-input", "value"),
    State("bailout-input", "value"),
    State("image-size-select", "value"),
    State("region-select", "value"),
    State("coloring-model-select", "value"),
    State("color-index-model-select", "value"),
    State("palette-model-select", "value"),
    State("mandelbrot-tabs-container", "children"),
    State("image-counter-store", "data"),
    State("all-images-store", "data"),
    prevent_initial_call=True,
)
def manage_mandelbrot_tabs(
    generate_clicks, close_clicks, max_iter, bailout, size, region,
    coloring_model, color_index_model, palette_model, tabs_container, counter_data, all_images
):
    """Generate new images in new tabs or close tabs."""
    ctx = dash.callback_context
    
    if all_images is None:
        all_images = {}
    
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    trigger_id = ctx.triggered[0]["prop_id"]
    
    # Get current tabs structure
    current_tabs = tabs_container[0] if tabs_container else None
    if not current_tabs or "props" not in current_tabs:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    tab_list = current_tabs["props"]["children"][0]["props"]["children"]
    tab_panels = current_tabs["props"]["children"][1:]
    
    # Handle closing a tab
    if "close-image-tab" in trigger_id:
        # Find which close button was clicked
        for i, clicks in enumerate(close_clicks):
            if clicks:
                # Account for the first tab (form tab) not having a close button (offset by 1)
                actual_tab_index = i + 1
                tab_to_remove = tab_list[actual_tab_index]["props"]["value"]
                
                # Remove the tab and its panel
                tab_list.pop(actual_tab_index)
                tab_panels = [p for p in tab_panels if p["props"]["value"] != tab_to_remove]
                
                # Always stay on or return to form tab when closing
                new_active = "form-tab"
                
                # Remove from centralized store
                all_images_copy = all_images.copy()
                image_id_to_delete = tab_to_remove.replace("image-", "")
                if image_id_to_delete in all_images_copy:
                    del all_images_copy[image_id_to_delete]
                
                # Rebuild tabs component
                new_tabs = dmc.Tabs(
                    id="mandelbrot-tabs",
                    value=new_active,
                    children=[
                        dmc.TabsList(tab_list),
                        *tab_panels
                    ]
                )
                # Save metadata instead of full component tree
                # At this point tab_list contains dict representations from serialized component
                tabs_metadata = {
                    "tab_list": [
                        {"value": tab["props"]["value"], "index": i}
                        for i, tab in enumerate(tab_list)
                    ],
                    "active_tab": new_active
                }
                return [new_tabs], new_active, dash.no_update, tabs_metadata, all_images_copy
    
    # Handle generating a new image
    if "generate-btn" in trigger_id:
        if max_iter is None or bailout is None or size is None or region is None:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update
        
        try:
            # Generate unique image ID
            image_id = str(uuid.uuid4())
            current_count = counter_data['count']
            new_count = current_count + 1
            tab_id = f"image-{image_id}"
            
            # Get image size
            image_size = int(size)
            
            # Get region bounds
            xmin, xmax, ymin, ymax = ZOOM_REGIONS.get(region, ZOOM_REGIONS["full"])
            
            # Select functions
            coloring_function = FRAKTAL_MODELS["coloring"][coloring_model]["function"]
            color_index_function = FRAKTAL_MODELS["color_index"][color_index_model]["function"]
            palette_function = FRAKTAL_MODELS["palette"][palette_model]["function"]
            
            # Generate image
            image_src = generate_mandelbrot_image(
                xmin, xmax, ymin, ymax, image_size, image_size, max_iter,
                bailout=bailout, coloring_function=coloring_function,
                color_index_function=color_index_function, palette_function=palette_function
            )
            
            # Store image data in centralized store
            all_images_copy = all_images.copy()
            all_images_copy[image_id] = {
                "image_id": image_id,
                "image_src": image_src,
                "width": image_size,
                "height": image_size,
                "max_iter": max_iter,
                "bailout": bailout,
                "xmin": xmin,
                "xmax": xmax,
                "ymin": ymin,
                "ymax": ymax,
                "region": region,
                "coloring_model": coloring_model,
                "color_index_model": color_index_model,
                "palette_model": palette_model,
            }
            
            # Create new tab
            new_tab = dmc.TabsTab(
                f"Image {current_count}",
                value=tab_id,
                rightSection=dmc.ActionIcon(
                    "×",
                    id={"type": "close-image-tab", "index": image_id},
                    size="xs",
                    variant="subtle",
                    c="gray",
                )
            )
            
            # Create new panel with image and controls
            new_panel = dmc.TabsPanel(
                dmc.Stack([
                    create_image_panel_content(
                        image_id, image_src, max_iter, bailout, image_size, region,
                        coloring_model, color_index_model, palette_model
                    ),
                ], gap="md"),
                value=tab_id,
            )
            
            # Add to lists
            tab_list.append(new_tab)
            tab_panels.append(new_panel)
            
            # Rebuild tabs component
            new_tabs = dmc.Tabs(
                id="mandelbrot-tabs",
                value=tab_id,  # Switch to newly created tab
                children=[
                    dmc.TabsList(tab_list),
                    *tab_panels
                ]
            )
            
            # Save metadata instead of full component tree
            # tab_list can contain either component objects or dict representations
            tabs_metadata = {
                "tab_list": [
                    {
                        "value": (tab.value if hasattr(tab, 'value') else tab.get("props", {}).get("value", f"tab-{i}")),
                        "index": i
                    }
                    for i, tab in enumerate(tab_list)
                ],
                "active_tab": tab_id
            }
            print(f"Saving tabs_metadata: {tabs_metadata}")  # Debug
            return [new_tabs], tab_id, {"count": new_count}, tabs_metadata, all_images_copy
        
        except Exception as e:
            # On error, just show alert in current state
            import traceback
            print(f"Error generating image: {str(e)}")
            print(traceback.format_exc())
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


@callback(
    Output({"type": "image-display", "index": MATCH}, "src"),
    Output({"type": "image-description", "index": MATCH}, "children"),
    Input({"type": "update-image-btn", "index": MATCH}, "n_clicks"),
    State({"type": "update-max-iter", "index": MATCH}, "value"),
    State({"type": "update-bailout", "index": MATCH}, "value"),
    State({"type": "update-image-size", "index": MATCH}, "value"),
    State({"type": "update-region", "index": MATCH}, "value"),
    State({"type": "update-coloring-model", "index": MATCH}, "value"),
    State({"type": "update-color-index-model", "index": MATCH}, "value"),
    State({"type": "update-palette-model", "index": MATCH}, "value"),
    prevent_initial_call=True,
)
def update_existing_image(
    n_clicks, max_iter, bailout, size, region,
    coloring_model, color_index_model, palette_model
):
    """Update an existing image with new parameters."""
    if not n_clicks or max_iter is None or bailout is None or size is None or region is None:
        return dash.no_update, dash.no_update
    
    try:
        # Get image size
        image_size = int(size)
        
        # Get region bounds
        xmin, xmax, ymin, ymax = ZOOM_REGIONS.get(region, ZOOM_REGIONS["full"])
        
        # Select functions
        coloring_function = FRAKTAL_MODELS["coloring"][coloring_model]["function"]
        color_index_function = FRAKTAL_MODELS["color_index"][color_index_model]["function"]
        palette_function = FRAKTAL_MODELS["palette"][palette_model]["function"]
        
        # Generate updated image
        image_src = generate_mandelbrot_image(
            xmin, xmax, ymin, ymax, image_size, image_size, max_iter,
            bailout=bailout, coloring_function=coloring_function,
            color_index_function=color_index_function, palette_function=palette_function
        )
        
        # Update description
        description = f"Max iterations: {max_iter} | Size: {image_size}x{image_size} | Region: {region} | Bailout: {bailout}"
        
        return image_src, description
    
    except Exception as e:
        print(f"Error updating image: {str(e)}")
        return dash.no_update, dash.no_update


# Separate callback to update the centralized store when images are updated
@callback(
    Output("all-images-store", "data", allow_duplicate=True),
    Input({"type": "update-image-btn", "index": ALL}, "n_clicks"),
    State({"type": "update-max-iter", "index": ALL}, "value"),
    State({"type": "update-bailout", "index": ALL}, "value"),
    State({"type": "update-image-size", "index": ALL}, "value"),
    State({"type": "update-region", "index": ALL}, "value"),
    State({"type": "update-coloring-model", "index": ALL}, "value"),
    State({"type": "update-color-index-model", "index": ALL}, "value"),
    State({"type": "update-palette-model", "index": ALL}, "value"),
    State("all-images-store", "data"),
    State("mandelbrot-tabs-metadata-store", "data"),
    prevent_initial_call=True,
)
def sync_store_on_image_update(
    n_clicks_list, max_iters, bailouts, sizes, regions,
    coloring_models, color_index_models, palette_models, all_images, tabs_metadata
):
    """Synchronize the centralized store when any image is updated."""
    ctx = dash.callback_context
    
    if not ctx.triggered or not tabs_metadata:
        return dash.no_update
    
    # Find which button was clicked
    triggered_id = ctx.triggered_id
    if not triggered_id or "index" not in triggered_id:
        return dash.no_update
    
    image_id = triggered_id["index"]
    
    # Find the index in the lists
    tab_list_data = tabs_metadata.get("tab_list", [])
    image_index = None
    for i, tab_data in enumerate(tab_list_data):
        tab_value = tab_data.get("value")
        if tab_value != "form-tab":
            extracted_id = tab_value.replace("image-", "")
            if extracted_id == image_id:
                # Adjust for form tab at index 0
                image_index = i - 1
                break
    
    if image_index is None or image_index < 0 or image_index >= len(max_iters):
        return dash.no_update
    
    # Get the new values for this image
    max_iter = max_iters[image_index]
    bailout = bailouts[image_index]
    size = sizes[image_index]
    region = regions[image_index]
    coloring_model = coloring_models[image_index]
    color_index_model = color_index_models[image_index]
    palette_model = palette_models[image_index]
    
    if max_iter is None or bailout is None or size is None or region is None:
        return dash.no_update
    
    try:
        # Get image size
        image_size = int(size)
        
        # Get region bounds
        xmin, xmax, ymin, ymax = ZOOM_REGIONS.get(region, ZOOM_REGIONS["full"])
        
        # Select functions
        coloring_function = FRAKTAL_MODELS["coloring"][coloring_model]["function"]
        color_index_function = FRAKTAL_MODELS["color_index"][color_index_model]["function"]
        palette_function = FRAKTAL_MODELS["palette"][palette_model]["function"]
        
        # Generate updated image
        image_src = generate_mandelbrot_image(
            xmin, xmax, ymin, ymax, image_size, image_size, max_iter,
            bailout=bailout, coloring_function=coloring_function,
            color_index_function=color_index_function, palette_function=palette_function
        )
        
        # Update centralized store
        all_images_copy = all_images.copy() if all_images else {}
        all_images_copy[image_id] = {
            "image_id": image_id,
            "image_src": image_src,
            "width": image_size,
            "height": image_size,
            "max_iter": max_iter,
            "bailout": bailout,
            "xmin": xmin,
            "xmax": xmax,
            "ymin": ymin,
            "ymax": ymax,
            "region": region,
            "coloring_model": coloring_model,
            "color_index_model": color_index_model,
            "palette_model": palette_model,
        }
        
        return all_images_copy
    
    except Exception as e:
        print(f"Error syncing store: {str(e)}")
        return dash.no_update
