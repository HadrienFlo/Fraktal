"""Test Cython integration for seed module."""

import pytest
import os


def test_f_numba_basic():
    """Test basic Numba seed function."""
    os.environ['FRAKTAL_USE_CYTHON'] = 'false'
    
    # Need to reload to pick up environment variable
    import importlib
    import fraktal.engines.seed as seed_module
    importlib.reload(seed_module)
    
    from fraktal.engines.seed import f_numba
    
    z = complex(1.0, 1.0)
    c = complex(0.5, 0.5)
    
    result = f_numba(z, c, p=2)
    expected = z**2 + c
    
    assert abs(result - expected) < 1e-10
    assert isinstance(result, complex)


def test_f_cython_basic():
    """Test basic Cython seed function (if available)."""
    try:
        from fraktal.engines.seed_cy import f_cython
    except ImportError:
        pytest.skip("Cython extension not built")
    
    z = complex(1.0, 1.0)
    c = complex(0.5, 0.5)
    
    result = f_cython(z, c, p=2)
    expected = z**2 + c
    
    assert abs(result - expected) < 1e-10
    assert isinstance(result, complex)


def test_numba_cython_equivalence():
    """Test that Numba and Cython implementations give same results."""
    try:
        from fraktal.engines.seed_cy import f_cython
    except ImportError:
        pytest.skip("Cython extension not built")
    
    from fraktal.engines.seed import f_numba
    
    # Test multiple values
    test_cases = [
        (complex(0, 0), complex(0, 0), 2),
        (complex(1, 1), complex(0.5, 0.5), 2),
        (complex(-0.5, 0.3), complex(0.2, -0.1), 2),
        (complex(2, -1), complex(-0.8, 0.4), 3),
    ]
    
    for z, c, p in test_cases:
        numba_result = f_numba(z, c, p)
        cython_result = f_cython(z, c, p)
        
        assert abs(numba_result - cython_result) < 1e-10, \
            f"Results differ for z={z}, c={c}, p={p}"


def test_environment_variable_switching():
    """Test that environment variable switches implementation."""
    import importlib
    import fraktal.engines.seed as seed_module
    
    # Test with Numba
    os.environ['FRAKTAL_USE_CYTHON'] = 'false'
    importlib.reload(seed_module)
    
    from fraktal.engines.seed import f
    assert f.__name__ == 'f_numba'
    
    # Test with Cython (if available)
    try:
        from fraktal.engines.seed_cy import f_cython
        os.environ['FRAKTAL_USE_CYTHON'] = 'true'
        importlib.reload(seed_module)
        
        from fraktal.engines.seed import f
        assert f.__name__ == 'f_cython'
    except ImportError:
        pytest.skip("Cython extension not built")


def test_power_parameter():
    """Test that power parameter works correctly."""
    from fraktal.engines.seed import f_numba
    
    z = complex(2.0, 0.0)
    c = complex(1.0, 0.0)
    
    # Test p=2
    result_p2 = f_numba(z, c, p=2)
    assert abs(result_p2 - (4.0 + 1.0)) < 1e-10
    
    # Test p=3
    result_p3 = f_numba(z, c, p=3)
    assert abs(result_p3 - (8.0 + 1.0)) < 1e-10
    
    # Test Cython if available
    try:
        from fraktal.engines.seed_cy import f_cython
        
        result_cy_p2 = f_cython(z, c, p=2)
        assert abs(result_cy_p2 - (4.0 + 1.0)) < 1e-10
        
        result_cy_p3 = f_cython(z, c, p=3)
        assert abs(result_cy_p3 - (8.0 + 1.0)) < 1e-10
    except ImportError:
        pass
