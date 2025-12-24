"""Dynamic Fractal Explorer using Leaflet for smooth pan/zoom interaction."""

import sys
from pathlib import Path

# Add parent directory to path to allow imports from components
sys.path.insert(0, str(Path(__file__).parent.parent))

import dash
from dash import html, Input, Output, callback
import dash_leaflet as dl
import dash_mantine_components as dmc
from flask import send_file
from io import BytesIO
import numpy as np
from PIL import Image

from fraktal.engines.mandelbrot import mandelbrot_set_numba
from fraktal.engines.palette import hot_palette, cool_palette, simple_palette

dash.register_page(__name__, name="Explorer", path="/explorer")

# In-memory tile cache (in production, consider Redis)
TILE_CACHE = {}

# Current parameters (will be improved with proper state management)
CURRENT_PARAMS = {
    'max_iter': 256,
    'palette': 'hot',
    'use_cython': False
}

PALETTE_FUNCTIONS = {
    'hot': hot_palette,
    'cool': cool_palette,
    'simple': simple_palette
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
    
    # Full Mandelbrot view at z=0
    real_min, real_max = -2.5, 1.5  # Wider view to show full set
    imag_min, imag_max = -2.0, 2.0  # Square aspect ratio
    
    real_range = real_max - real_min
    imag_range = imag_max - imag_min
    
    # Calculate bounds for this tile
    xmin = real_min + (x / n) * real_range
    xmax = real_min + ((x + 1) / n) * real_range
    ymax = imag_max - (y / n) * imag_range  # Y is inverted in tile coords
    ymin = imag_max - ((y + 1) / n) * imag_range
    
    return xmin, xmax, ymin, ymax


# Page layout
layout = dmc.Container([
    dmc.Title("Fractal Explorer", order=1, mt="md", mb="lg"),
    
    dmc.Text(
        "Pan and zoom to explore the Mandelbrot set. Use mouse wheel to zoom, drag to pan.",
        c="dimmed",
        mb="md"
    ),
    
    dmc.Grid([
        # Left sidebar: Controls
        dmc.GridCol([
            dmc.Stack([
                dmc.Card([
                    dmc.CardSection([
                        dmc.Text("Parameters", weight=500, mb="sm"),
                    ]),
                    dmc.Stack([
                        dmc.Slider(
                            id='explorer-max-iter',
                            min=50,
                            max=1000,
                            step=50,
                            value=256,
                            label="Max Iterations",
                            marks=[
                                {"value": 50, "label": "50"},
                                {"value": 250, "label": "250"},
                                {"value": 500, "label": "500"},
                                {"value": 1000, "label": "1000"}
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
                        
                        dmc.Switch(
                            id='explorer-use-cython',
                            label="Use Cython (faster)",
                            checked=False
                        ),
                    ], gap="md")
                ], withBorder=True, p="md"),
                
                dmc.Card([
                    dmc.CardSection([
                        dmc.Text("View Info", weight=500, mb="sm"),
                    ]),
                    dmc.Stack([
                        dmc.Text(id='explorer-coords', size='sm', c="dimmed"),
                        dmc.Text(id='explorer-zoom-level', size='sm', c="dimmed"),
                        dmc.Badge(id='explorer-cache-size', color="gray", variant="light"),
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
                    children=[
                        dl.TileLayer(
                            id='fractal-tiles',
                            url='/api/fractal-tiles/{z}/{x}/{y}',
                            minZoom=0,
                            maxZoom=12,
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


# Callback to update info display
@callback(
    Output('explorer-coords', 'children'),
    Output('explorer-zoom-level', 'children'),
    Output('explorer-cache-size', 'children'),
    Input('explorer-map', 'viewport')
)
def update_info(viewport):
    """Update coordinate display and zoom level."""
    if not viewport:
        return "Loading...", "Zoom: -", "Cache: 0 tiles"
    
    center = viewport.get('center', [0, 0])
    zoom = viewport.get('zoom', 0)
    
    # Approximate conversion to complex coordinates
    # (This is simplified - exact conversion would require tile math)
    lat, lng = center
    
    cache_size = len(TILE_CACHE)
    
    return (
        f"Center: ~{lng:.4f} + {lat:.4f}i",
        f"Zoom Level: {zoom}",
        f"Cache: {cache_size} tiles"
    )


# Callback to update parameters and clear cache
@callback(
    Output('explorer-map', 'children', allow_duplicate=True),
    Input('explorer-max-iter', 'value'),
    Input('explorer-palette', 'value'),
    Input('explorer-use-cython', 'checked'),
    prevent_initial_call=True
)
def update_params(max_iter, palette, use_cython):
    """Update parameters and clear tile cache."""
    global CURRENT_PARAMS, TILE_CACHE
    
    CURRENT_PARAMS['max_iter'] = max_iter
    CURRENT_PARAMS['palette'] = palette
    CURRENT_PARAMS['use_cython'] = use_cython
    
    # Clear cache when parameters change
    TILE_CACHE.clear()
    
    # Force tile reload by returning new TileLayer with updated URL timestamp
    import time
    timestamp = int(time.time())
    
    return [
        dl.TileLayer(
            id='fractal-tiles',
            url=f'/api/fractal-tiles/{{z}}/{{x}}/{{y}}?t={timestamp}',
            minZoom=0,
            maxZoom=12,
            tileSize=256,
        )
    ]


# Register Flask route for tile serving
@dash.get_app().server.route('/api/fractal-tiles/<int:z>/<int:x>/<int:y>')
def serve_tile(z, x, y):
    """Serve a 256x256 fractal tile as PNG."""
    
    # Get current parameters
    max_iter = CURRENT_PARAMS['max_iter']
    palette = CURRENT_PARAMS['palette']
    use_cython = CURRENT_PARAMS['use_cython']
    
    # Create cache key
    cache_key = f"{z}:{x}:{y}:{max_iter}:{palette}:{use_cython}"
    
    # Return cached tile if available
    if cache_key in TILE_CACHE:
        return send_file(BytesIO(TILE_CACHE[cache_key]), mimetype='image/png')
    
    # Generate tile bounds
    xmin, xmax, ymin, ymax = tile_to_bounds(x, y, z)
    
    # Choose implementation
    if use_cython:
        try:
            from fraktal.engines.mandelbrot_cy import mandelbrot_set_cython
            mandelbrot_fn = mandelbrot_set_cython
        except ImportError:
            # Fallback to Numba if Cython not available
            mandelbrot_fn = mandelbrot_set_numba
    else:
        mandelbrot_fn = mandelbrot_set_numba
    
    # Generate Mandelbrot data
    data = mandelbrot_fn(xmin, xmax, ymin, ymax, 256, 256, max_iter)
    
    # Convert to RGB using selected palette
    palette_fn = PALETTE_FUNCTIONS[palette]
    img_array = np.zeros((256, 256, 3), dtype=np.uint8)
    norm = data.astype(float) / max_iter
    
    for i in range(256):
        for j in range(256):
            r, g, b = palette_fn(norm[i, j])
            img_array[i, j] = [r, g, b]
    
    # Convert to PNG
    img = Image.fromarray(img_array)
    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    
    # Cache the result
    TILE_CACHE[cache_key] = buf.getvalue()
    
    return send_file(BytesIO(TILE_CACHE[cache_key]), mimetype='image/png')
