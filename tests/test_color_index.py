"""Tests for the color_index.py module."""

import pytest
import numpy as np
from fraktal.engines.color_index import simple_coloring


class TestSimpleColoring:
    """Tests for the simple_coloring function."""

    def test_simple_coloring_basic(self):
        """Test basic color index calculation."""
        result = simple_coloring(1.0, k=2.5, u0=0.0)
        assert isinstance(result, float)
        assert result == pytest.approx(2.5)

    def test_simple_coloring_zero_input(self):
        """Test with zero input."""
        result = simple_coloring(0.0, k=2.5, u0=0.0)
        assert result == pytest.approx(0.0)

    def test_simple_coloring_negative_input(self):
        """Test with negative input."""
        result = simple_coloring(-1.0, k=2.5, u0=0.0)
        assert result == pytest.approx(-2.5)

    def test_simple_coloring_with_offset(self):
        """Test color index calculation with offset."""
        result = simple_coloring(3.0, k=2.5, u0=1.0)
        assert result == pytest.approx(2.5 * (3.0 - 1.0))
        assert result == pytest.approx(5.0)

    def test_simple_coloring_custom_k(self):
        """Test with custom scaling factor."""
        result = simple_coloring(2.0, k=1.0, u0=0.0)
        assert result == pytest.approx(2.0)
        
        result = simple_coloring(2.0, k=5.0, u0=0.0)
        assert result == pytest.approx(10.0)

    def test_simple_coloring_default_parameters(self):
        """Test that default parameters work correctly."""
        result = simple_coloring(1.0)
        assert result == pytest.approx(2.5)

    def test_simple_coloring_linear_scaling(self):
        """Test that the function is linear in u."""
        u1, u2 = 1.0, 2.0
        result1 = simple_coloring(u1, k=2.0, u0=0.0)
        result2 = simple_coloring(u2, k=2.0, u0=0.0)
        
        # Doubling u should double the result
        assert result2 == pytest.approx(2 * result1)

    def test_simple_coloring_offset_invariance(self):
        """Test that offset affects all values uniformly."""
        u = 5.0
        result1 = simple_coloring(u, k=2.0, u0=0.0)
        result2 = simple_coloring(u, k=2.0, u0=1.0)
        
        # Difference should be k * (1.0) = 2.0
        assert (result1 - result2) == pytest.approx(2.0)

    def test_simple_coloring_large_values(self):
        """Test with large input values."""
        result = simple_coloring(1000.0, k=2.5, u0=0.0)
        assert result == pytest.approx(2500.0)

    def test_simple_coloring_small_values(self):
        """Test with small input values."""
        result = simple_coloring(0.001, k=2.5, u0=0.0)
        assert result == pytest.approx(0.0025)

    def test_simple_coloring_zero_k(self):
        """Test with zero scaling factor."""
        result = simple_coloring(5.0, k=0.0, u0=0.0)
        assert result == pytest.approx(0.0)

    def test_simple_coloring_negative_k(self):
        """Test with negative scaling factor."""
        result = simple_coloring(2.0, k=-2.5, u0=0.0)
        assert result == pytest.approx(-5.0)

    def test_simple_coloring_complex_scenario(self):
        """Test complex scenario with various parameters."""
        u = 10.0
        k = 0.5
        u0 = 3.0
        result = simple_coloring(u, k=k, u0=u0)
        expected = k * (u - u0)
        assert result == pytest.approx(expected)
        assert result == pytest.approx(3.5)

    def test_simple_coloring_fractional_values(self):
        """Test with fractional input values."""
        result = simple_coloring(0.5, k=2.5, u0=0.0)
        assert result == pytest.approx(1.25)
        
        result = simple_coloring(0.1, k=0.5, u0=0.0)
        assert result == pytest.approx(0.05)

    def test_simple_coloring_symmetry(self):
        """Test symmetry around offset."""
        u0 = 5.0
        k = 2.0
        
        result_above = simple_coloring(u0 + 1.0, k=k, u0=u0)
        result_below = simple_coloring(u0 - 1.0, k=k, u0=u0)
        
        # Results should be symmetric around zero
        assert result_above == pytest.approx(-result_below)
        assert result_above == pytest.approx(2.0)
        assert result_below == pytest.approx(-2.0)

    def test_simple_coloring_very_large_k(self):
        """Test with very large scaling factor."""
        result = simple_coloring(1.0, k=1e6, u0=0.0)
        assert result == pytest.approx(1e6)

    def test_simple_coloring_very_small_k(self):
        """Test with very small scaling factor."""
        result = simple_coloring(1.0, k=1e-6, u0=0.0)
        assert result == pytest.approx(1e-6)
