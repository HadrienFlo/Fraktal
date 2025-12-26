"""Dynamic Fractal Explorer using Leaflet for smooth pan/zoom interaction."""

import dash
from dash import html, dcc, Input, Output, State, callback, callback_context, no_update
from dash.exceptions import PreventUpdate
import dash_leaflet as dl
import dash_mantine_components as dmc
from flask import send_file
from io import BytesIO
import numpy as np
from PIL import Image

from fraktal.engines.mandelbrot import mandelbrot_set_numba
from fraktal.engines.palette import hot_palette, cool_palette, simple_palette
from fraktal.engines.color_index import simple_index
from fraktal.models.iteration_count import smooth_iteration_count, continuous_iteration_count, iteration_count

dash.register_page(__name__, name="Explorer", path="/explorer")

# In-memory tile cache (in production, consider Redis)
TILE_CACHE = {}

# Track current zoom level from tile requests
CURRENT_ZOOM_LEVEL = 2

# Current parameters (will be improved with proper state management)
CURRENT_PARAMS = {
    'max_iter': 256,
    'palette': 'hot',
    'use_cython': False,
    'auto_iter': True,
    'coloring_method': 'smooth'
}

PALETTE_FUNCTIONS = {
    'hot': hot_palette,
    'cool': cool_palette,
    'simple': simple_palette
}

COLORING_FUNCTIONS = {
    'iteration': iteration_count,
    'continuous': continuous_iteration_count,
    'smooth': smooth_iteration_count
}


def tile_to_bounds(x, y, z):
    """Convert Leaflet tile coordinates to complex plane bounds.
    
    Args:
        x: Tile x coordinate
        y: Tile y coordinate  
        z: Zoom level
        
    Returns:
        Tuple of (xmin, xmax, ymin, ymax) in complex plane
    """
    n = 2.0 ** z
    
    # Use square aspect ratio for proper tile alignment
    # Center on the interesting part of the Mandelbrot set
    center_real = -0.5
    center_imag = 0.0
    total_range = 4.0  # Total view range (square)
    
    # Calculate bounds for this tile
    xmin = center_real - total_range/2 + (x / n) * total_range
    xmax = center_real - total_range/2 + ((x + 1) / n) * total_range
    ymin = center_imag - total_range/2 + (y / n) * total_range
    ymax = center_imag - total_range/2 + ((y + 1) / n) * total_range
    
    return xmin, xmax, ymin, ymax


# Page layout
layout = dmc.Container([
    dmc.Title("Fractal Explorer", order=1, mt="md", mb="lg"),
    
    dmc.Text(
        "Pan and zoom to explore the Mandelbrot set. Use mouse wheel to zoom, drag to pan.",
        c="dimmed",
        mb="md"
    ),
    
    # Hidden interval component to update cache info
    dcc.Interval(id='cache-update-interval', interval=1000, n_intervals=0),
    
    # Store to track current zoom level
    dcc.Store(id='zoom-level-store', data=2),
    
    dmc.Grid([
        # Left sidebar: Controls
        dmc.GridCol([
            dmc.Stack([
                dmc.Card([
                    dmc.CardSection([
                        dmc.Text("Parameters", fw=500, mb="sm"),
                    ]),
                    dmc.Stack([
                        dmc.Switch(
                            id='explorer-auto-iter',
                            label="Auto-adjust iterations on zoom",
                            checked=True,
                            mb="sm"
                        ),
                        
                        dmc.Badge(
                            id='explorer-iter-display',
                            children="256 iterations",
                            color="grape",
                            variant="light",
                            size="lg",
                            mb="xs"
                        ),
                        
                        dmc.Slider(
                            id='explorer-max-iter',
                            min=50,
                            max=5000,
                            step=50,
                            value=256,
                            label="Max Iterations",
                            disabled=True,  # Disabled when auto mode is on
                            marks=[
                                {"value": 50, "label": "50"},
                                {"value": 1000, "label": "1K"},
                                {"value": 2500, "label": "2.5K"},
                                {"value": 5000, "label": "5K"}
                            ]
                        ),
                        
                        dmc.Select(
                            id='explorer-palette',
                            label="Color Palette",
                            data=[
                                {"value": "hot", "label": "Hot"},
                                {"value": "cool", "label": "Cool"},
                                {"value": "simple", "label": "Simple"},
                            ],
                            value="hot"
                        ),
                        
                        dmc.Select(
                            id='explorer-coloring',
                            label="Coloring Method",
                            data=[
                                {"value": "smooth", "label": "Smooth (recommended)"},
                                {"value": "continuous", "label": "Continuous"},
                                {"value": "iteration", "label": "Basic Iteration"},
                            ],
                            value="smooth",
                            description="Affects color gradient smoothness"
                        ),
                        
                        dmc.Switch(
                            id='explorer-use-cython',
                            label="Use Cython (experimental - slower)",
                            checked=False
                        ),
                    ], gap="md")
                ], withBorder=True, p="md"),
                
                dmc.Card([
                    dmc.CardSection([
                        dmc.Text("Cache Info", fw=500, mb="sm"),
                    ]),
                    dmc.Stack([
                        dmc.Badge(id='explorer-cache-size', color="blue", variant="light", size="lg"),
                        dmc.Text("Use mouse wheel to zoom, drag to pan", size="xs", c="dimmed"),
                    ], gap="xs")
                ], withBorder=True, p="md"),
                
                dmc.Alert(
                    "Tiles are cached for better performance. Change parameters to regenerate.",
                    title="Tip",
                    color="blue",
                    icon=True
                )
            ], gap="md")
        ], span={"base": 12, "md": 3}),
        
        # Right: Leaflet map
        dmc.GridCol([
            dmc.Card([
                dl.Map(
                    center=[0, 0],
                    zoom=2,
                    viewport={'center': [0, 0], 'zoom': 2},
                    children=[
                        dl.TileLayer(
                            id='fractal-tiles',
                            url='/api/fractal-tiles/{z}/{x}/{y}',
                            minZoom=0,
                            maxZoom=60,
                            tileSize=256,
                        ),
                    ],
                    style={'width': '100%', 'height': '75vh'},
                    id='explorer-map',
                    zoomControl=True,
                    scrollWheelZoom=True,
                )
            ], withBorder=True, p=0)
        ], span={"base": 12, "md": 9}),
    ])
], fluid=True, size="xl")


# Clientside callback to track zoom level changes
dash.clientside_callback(
    """
    function(viewport) {
        if (viewport && viewport.zoom !== undefined) {
            return viewport.zoom;
        }
        return window.dash_clientside.no_update;
    }
    """,
    Output('zoom-level-store', 'data'),
    Input('explorer-map', 'viewport')
)


# Callback to calculate max_iter based on zoom level
@callback(
    Output('explorer-max-iter', 'value'),
    Output('explorer-max-iter', 'disabled'),
    Input('zoom-level-store', 'data'),
    Input('explorer-auto-iter', 'checked'),
)
def update_max_iter_from_zoom(zoom_level, auto_enabled):
    """Calculate max_iter based on zoom level when auto mode is enabled.
    
    Formula: max_iter = 100 * (1.3 ^ zoom_level)
    
    This exponential relationship ensures:
    - Zoom 0: ~100 iterations (whole Mandelbrot set)
    - Zoom 3: ~220 iterations
    - Zoom 6: ~470 iterations
    - Zoom 9: ~1000 iterations
    - Zoom 12: ~2200 iterations
    """
    print(f"update_max_iter_from_zoom called: zoom_level={zoom_level}, auto_enabled={auto_enabled}")
    
    if zoom_level is None:
        zoom_level = 2
    
    # Exponential formula: max_iter = base * (growth_rate ^ zoom)
    base_iter = 100
    growth_rate = 1.3
    calculated_iter = int(base_iter * (growth_rate ** zoom_level))
    
    # Clamp to slider range
    calculated_iter = max(50, min(5000, calculated_iter))
    
    print(f"Calculated max_iter: {calculated_iter}")
    
    if not auto_enabled:
        return calculated_iter, False  # Enable manual slider
    
    return calculated_iter, True  # Disable slider, the badge will update via the next callback


# Update callback to handle parameter changes and badge display
@callback(
    Output('explorer-cache-size', 'children'),
    Output('explorer-iter-display', 'children'),
    Output('explorer-max-iter', 'value', allow_duplicate=True),
    Input('cache-update-interval', 'n_intervals'),
    Input('explorer-max-iter', 'value'),
    Input('explorer-palette', 'value'),
    Input('explorer-coloring', 'value'),
    Input('explorer-use-cython', 'checked'),
    Input('explorer-auto-iter', 'checked'),
    prevent_initial_call=True
)
def update_info_and_params(n_intervals, max_iter, palette, coloring_method, use_cython, auto_iter):
    """Update cache display and handle parameter changes."""
    global CURRENT_PARAMS, TILE_CACHE, CURRENT_ZOOM_LEVEL
    
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0] if callback_context.triggered else None
    
    # Use CURRENT_ZOOM_LEVEL which is updated by serve_tile
    actual_zoom = CURRENT_ZOOM_LEVEL if CURRENT_ZOOM_LEVEL is not None else 2
    
    # Update parameters if they changed (but not on interval trigger)
    if triggered_id in ['explorer-max-iter', 'explorer-palette', 'explorer-coloring', 'explorer-use-cython', 'explorer-auto-iter']:
        CURRENT_PARAMS['palette'] = palette
        CURRENT_PARAMS['coloring_method'] = coloring_method
        CURRENT_PARAMS['use_cython'] = use_cython
        CURRENT_PARAMS['auto_iter'] = auto_iter
        # Only update max_iter if not in auto mode
        if not auto_iter:
            CURRENT_PARAMS['max_iter'] = max_iter
        TILE_CACHE.clear()
    
    # Calculate the actual max_iter being used (same logic as serve_tile)
    if CURRENT_PARAMS.get('auto_iter', True):
        base_iter = 100
        growth_rate = 1.3
        actual_max_iter = int(base_iter * (growth_rate ** actual_zoom))
        actual_max_iter = max(50, min(5000, actual_max_iter))
        # Update CURRENT_PARAMS with the calculated value
        CURRENT_PARAMS['max_iter'] = actual_max_iter
    else:
        actual_max_iter = CURRENT_PARAMS['max_iter']
    
    cache_size = len(TILE_CACHE)
    
    return f"{cache_size} tiles cached", f"{actual_max_iter} iterations", actual_max_iter


# Flask route handler function (will be registered by app.py)
def serve_tile(z, x, y):
    """Serve a 256x256 fractal tile as PNG."""
    
    global CURRENT_ZOOM_LEVEL, CURRENT_PARAMS
    
    try:
        import time
        start_time = time.perf_counter()
        
        # Track zoom level
        CURRENT_ZOOM_LEVEL = z
        
        # Calculate max_iter based on zoom if auto mode is enabled
        if CURRENT_PARAMS.get('auto_iter', True):
            base_iter = 100
            growth_rate = 1.3
            max_iter = int(base_iter * (growth_rate ** z))
            max_iter = max(50, min(5000, max_iter))
            # Update CURRENT_PARAMS so the badge callback can read it
            CURRENT_PARAMS['max_iter'] = max_iter
        else:
            max_iter = CURRENT_PARAMS['max_iter']
        
        palette = CURRENT_PARAMS['palette']
        use_cython = CURRENT_PARAMS['use_cython']
        coloring_method = CURRENT_PARAMS.get('coloring_method', 'smooth')
        
        # Create cache key
        cache_key = f"{z}:{x}:{y}:{max_iter}:{palette}:{coloring_method}:{use_cython}"
        
        # Return cached tile if available
        if cache_key in TILE_CACHE:
            return send_file(BytesIO(TILE_CACHE[cache_key]), mimetype='image/png')
        
        # Generate tile bounds
        xmin, xmax, ymin, ymax = tile_to_bounds(x, y, z)
        
        # Get palette and coloring functions
        palette_fn = PALETTE_FUNCTIONS[palette]
        coloring_fn = COLORING_FUNCTIONS[coloring_method]
        
        # Choose implementation and time it
        compute_start = time.perf_counter()
        if use_cython:
            try:
                # Try optimized Cython first (no Python callbacks, ~20-50x faster)
                from fraktal.engines.mandelbrot_cy_optimized import mandelbrot_set_cython_optimized
                
                # Map palette name to index
                palette_map = {'simple': 0, 'hot': 1, 'cool': 2}
                palette_idx = palette_map.get(palette, 0)
                
                img_array = mandelbrot_set_cython_optimized(
                    xmin, xmax, ymin, ymax, 256, 256, max_iter,
                    palette_choice=palette_idx, bailout=2, p=2
                )
                compute_time = time.perf_counter() - compute_start
                print(f"CYTHON-OPT tile z={z}, iter={max_iter}: {compute_time:.3f}s")
            except ImportError:
                try:
                    # Fallback to old Cython (slow, Python callbacks)
                    from fraktal.engines.mandelbrot_cy import mandelbrot_set_cython
                    img_array = mandelbrot_set_cython(
                        xmin, xmax, ymin, ymax, 256, 256, max_iter,
                        coloring_fn, simple_index, palette_fn
                    )
                    compute_time = time.perf_counter() - compute_start
                    print(f"CYTHON-OLD tile z={z}, iter={max_iter}: {compute_time:.3f}s")
                except ImportError:
                    # Fallback to Numba if no Cython available
                    img_array = mandelbrot_set_numba(
                        xmin, xmax, ymin, ymax, 256, 256, max_iter,
                        coloring_fn, simple_index, palette_fn
                    )
                    compute_time = time.perf_counter() - compute_start
                    print(f"NUMBA (fallback) tile z={z}, iter={max_iter}: {compute_time:.3f}s")
        else:
            # Generate Mandelbrot data with all required parameters
            img_array = mandelbrot_set_numba(
                xmin, xmax, ymin, ymax, 256, 256, max_iter,
                coloring_fn, simple_index, palette_fn
            )
            compute_time = time.perf_counter() - compute_start
            print(f"NUMBA tile z={z}, iter={max_iter}: {compute_time:.3f}s")
        
        # img_array is already RGB uint8 from mandelbrot_set_numba
        
        # Convert to PNG
        img = Image.fromarray(img_array)
        buf = BytesIO()
        img.save(buf, format='PNG', optimize=True)
        buf.seek(0)
        
        # Cache the result
        TILE_CACHE[cache_key] = buf.getvalue()
        
        return send_file(BytesIO(TILE_CACHE[cache_key]), mimetype='image/png')
    
    except Exception as e:
        print(f"Error generating tile {z}/{x}/{y}: {e}")
        import traceback
        traceback.print_exc()
        # Return a blank tile on error
        blank = Image.new('RGB', (256, 256), color='gray')
        buf = BytesIO()
        blank.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')


# Register the route (called from app.py after app creation)
_route_registered = False

def register_tile_route(server):
    """Register the tile serving route with the Flask server."""
    global _route_registered
    if _route_registered:
        print("Tile route already registered, skipping")
        return  # Already registered, skip
    
    server.add_url_rule(
        '/api/fractal-tiles/<int:z>/<int:x>/<int:y>',
        'serve_fractal_tile',
        serve_tile
    )
    _route_registered = True
    print("Tile route registered successfully at /api/fractal-tiles/<z>/<x>/<y>")
    _route_registered = True
