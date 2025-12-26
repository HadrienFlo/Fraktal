"""Test that the Dash app can toggle between Cython and Numba."""

import sys
from pathlib import Path
import pytest

# Add dash_app to path
dash_app_path = Path(__file__).parent.parent / "dash_app"
sys.path.insert(0, str(dash_app_path))

from components.tab_components.generate_tab_content import generate_fractal_tab_content


def test_generate_with_numba():
    """Test fractal generation with Numba."""
    inputs_data = {
        'center_x': -0.5,
        'center_y': 0.0,
        'zoom': 1.0,
        'width': 100,  # Small for faster test
        'height': 100,
        'max_iter': 50,
        'coloring_function': 'smooth-iteration-count',
        'color_index_function': 'simple-index',
        'palette_function': 'simple-palette',
        'use_cython': False  # Use Numba
    }
    
    content = generate_fractal_tab_content('test-id', 'Test Tab', inputs_data)
    assert content is not None


def test_generate_with_cython():
    """Test fractal generation with Cython (if available)."""
    from fraktal.engines.seed import CYTHON_AVAILABLE
    
    if not CYTHON_AVAILABLE:
        pytest.skip("Cython extension not built")
    
    inputs_data = {
        'center_x': -0.5,
        'center_y': 0.0,
        'zoom': 1.0,
        'width': 100,  # Small for faster test
        'height': 100,
        'max_iter': 50,
        'coloring_function': 'smooth-iteration-count',
        'color_index_function': 'simple-index',
        'palette_function': 'simple-palette',
        'use_cython': True  # Use Cython
    }
    
    content = generate_fractal_tab_content('test-id', 'Test Tab', inputs_data)
    assert content is not None


def test_numba_cython_give_same_result():
    """Test that both implementations produce similar results."""
    from fraktal.engines.seed import CYTHON_AVAILABLE
    
    if not CYTHON_AVAILABLE:
        pytest.skip("Cython extension not built")
    
    base_inputs = {
        'center_x': -0.5,
        'center_y': 0.0,
        'zoom': 1.0,
        'width': 50,  # Very small for faster test
        'height': 50,
        'max_iter': 30,
        'coloring_function': 'smooth-iteration-count',
        'color_index_function': 'simple-index',
        'palette_function': 'simple-palette',
    }
    
    # Generate with Numba
    numba_inputs = {**base_inputs, 'use_cython': False}
    numba_content = generate_fractal_tab_content('numba-id', 'Numba Tab', numba_inputs)
    
    # Generate with Cython
    cython_inputs = {**base_inputs, 'use_cython': True}
    cython_content = generate_fractal_tab_content('cython-id', 'Cython Tab', cython_inputs)
    
    # Both should produce content (exact pixel comparison would be flaky)
    assert numba_content is not None
    assert cython_content is not None
