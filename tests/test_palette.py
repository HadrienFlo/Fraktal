"""Tests for the palette.py module."""

import pytest
import numpy as np
from fraktal.engines.palette import simple_palette


class TestSimplePalette:
    """Tests for the simple_palette function."""

    def test_simple_palette_basic(self):
        """Test basic palette function."""
        result = simple_palette(0.0, k=2.5, u0=0)
        assert isinstance(result, tuple)
        assert len(result) == 3
        assert all(isinstance(x, (int, float)) for x in result)

    def test_simple_palette_zero_index(self):
        """Test with zero color index."""
        result = simple_palette(0.0, k=2.5, u0=0)
        assert result == pytest.approx((0.0, 0.0, 0.0))
        # All channels should be equal (grayscale)
        assert result[0] == result[1] == result[2]

    def test_simple_palette_positive_index(self):
        """Test with positive color index."""
        result = simple_palette(1.0, k=2.5, u0=0)
        expected = 2.5 * 1.0
        expected = min(1.0, max(0.0, expected))
        assert result == pytest.approx((expected, expected, expected))

    def test_simple_palette_clamping_upper(self):
        """Test that values are clamped at 1.0."""
        result = simple_palette(1.0, k=2.5, u0=0)
        # 2.5 * 1.0 = 2.5, but should be clamped to 1.0
        assert result == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_clamping_lower(self):
        """Test that values are clamped at 0.0."""
        result = simple_palette(-1.0, k=2.5, u0=0)
        # 2.5 * -1.0 = -2.5, but should be clamped to 0.0
        assert result == pytest.approx((0.0, 0.0, 0.0))

    def test_simple_palette_with_offset(self):
        """Test palette with offset parameter."""
        result = simple_palette(2.0, k=2.5, u0=1.0)
        # intensity = 2.5 * (2.0 - 1.0) = 2.5, clamped to 1.0
        assert result == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_mid_range(self):
        """Test with mid-range color index."""
        result = simple_palette(0.2, k=2.5, u0=0)
        # intensity = 2.5 * 0.2 = 0.5, should be exactly 0.5
        assert result == pytest.approx((0.5, 0.5, 0.5))

    def test_simple_palette_grayscale(self):
        """Test that palette always returns grayscale (R=G=B)."""
        test_values = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, -0.1, -0.5, 1.0]
        for val in test_values:
            result = simple_palette(val, k=2.5, u0=0)
            # All channels should be equal
            assert result[0] == result[1] == result[2]

    def test_simple_palette_default_parameters(self):
        """Test that default parameters work correctly."""
        result = simple_palette(0.0)
        assert isinstance(result, tuple)
        assert len(result) == 3
        # Default u0=0, so 2.5 * (0.0 - 0) = 0
        assert result == pytest.approx((0.0, 0.0, 0.0))

    def test_simple_palette_range_validity(self):
        """Test that all RGB values are in [0, 1] range."""
        test_indices = [-2.0, -1.0, -0.5, 0.0, 0.1, 0.2, 0.4, 0.5, 2.0, 5.0]
        for idx in test_indices:
            result = simple_palette(idx, k=2.5, u0=0)
            for channel in result:
                assert 0.0 <= channel <= 1.0

    def test_simple_palette_small_k(self):
        """Test with small scaling factor."""
        result = simple_palette(1.0, k=0.2, u0=0)
        # intensity = 0.2 * 1.0 = 0.2
        assert result == pytest.approx((0.2, 0.2, 0.2))

    def test_simple_palette_large_k(self):
        """Test with large scaling factor."""
        result = simple_palette(0.1, k=10.0, u0=0)
        # intensity = 10.0 * 0.1 = 1.0 (not exceeded due to clamping)
        assert result == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_zero_k(self):
        """Test with zero scaling factor."""
        result = simple_palette(5.0, k=0.0, u0=0)
        # intensity = 0.0 * 5.0 = 0.0
        assert result == pytest.approx((0.0, 0.0, 0.0))

    def test_simple_palette_negative_k(self):
        """Test with negative scaling factor."""
        result = simple_palette(1.0, k=-2.5, u0=0)
        # intensity = -2.5 * 1.0 = -2.5, clamped to 0.0
        assert result == pytest.approx((0.0, 0.0, 0.0))

    def test_simple_palette_large_positive_index(self):
        """Test with very large positive color index."""
        result = simple_palette(100.0, k=2.5, u0=0)
        # intensity = 2.5 * 100.0 = 250.0, clamped to 1.0
        assert result == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_large_negative_index(self):
        """Test with very large negative color index."""
        result = simple_palette(-100.0, k=2.5, u0=0)
        # intensity = 2.5 * -100.0 = -250.0, clamped to 0.0
        assert result == pytest.approx((0.0, 0.0, 0.0))

    def test_simple_palette_boundary_below_zero(self):
        """Test boundary condition just below zero."""
        result = simple_palette(-0.0001, k=2.5, u0=0)
        # intensity = 2.5 * -0.0001 = -0.00025, clamped to 0.0
        assert result == pytest.approx((0.0, 0.0, 0.0))

    def test_simple_palette_boundary_at_half(self):
        """Test boundary condition at 0.5 intensity."""
        # To get exactly 0.5, we need k * (color_index - u0) = 0.5
        result = simple_palette(0.2, k=2.5, u0=0)
        # intensity = 2.5 * 0.2 = 0.5
        assert result == pytest.approx((0.5, 0.5, 0.5))

    def test_simple_palette_boundary_at_one(self):
        """Test boundary condition at 1.0 intensity."""
        result = simple_palette(0.4, k=2.5, u0=0)
        # intensity = 2.5 * 0.4 = 1.0
        assert result == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_offset_effect(self):
        """Test that offset shifts the color range."""
        # Without offset
        result1 = simple_palette(1.0, k=2.5, u0=0)
        # With offset u0=0.5
        result2 = simple_palette(1.0, k=2.5, u0=0.5)
        
        # result1: 2.5 * (1.0 - 0) = 2.5 → 1.0
        # result2: 2.5 * (1.0 - 0.5) = 1.25 → 1.0
        assert result1 == pytest.approx((1.0, 1.0, 1.0))
        assert result2 == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_fractional_index(self):
        """Test with fractional color index."""
        result = simple_palette(0.15, k=2.5, u0=0)
        # intensity = 2.5 * 0.15 = 0.375
        assert result == pytest.approx((0.375, 0.375, 0.375))

    def test_simple_palette_return_values_in_tuple(self):
        """Test that return values are properly in a tuple."""
        result = simple_palette(0.2, k=2.5, u0=0)
        r, g, b = result
        assert 0.0 <= r <= 1.0
        assert 0.0 <= g <= 1.0
        assert 0.0 <= b <= 1.0

    def test_simple_palette_monotonic_intensity(self):
        """Test that intensity increases monotonically with color index."""
        indices = [0.0, 0.1, 0.2, 0.3]
        results = [simple_palette(idx, k=2.5, u0=0) for idx in indices]
        intensities = [r[0] for r in results]  # All channels are equal
        
        # Intensities should be non-decreasing
        for i in range(len(intensities) - 1):
            assert intensities[i] <= intensities[i + 1]

    def test_simple_palette_negative_offset(self):
        """Test with negative offset."""
        result = simple_palette(1.0, k=2.5, u0=-1.0)
        # intensity = 2.5 * (1.0 - (-1.0)) = 2.5 * 2.0 = 5.0 → clamped to 1.0
        assert result == pytest.approx((1.0, 1.0, 1.0))

    def test_simple_palette_very_small_k_and_large_index(self):
        """Test with very small k and large index."""
        result = simple_palette(1000.0, k=0.0001, u0=0)
        # intensity = 0.0001 * 1000.0 = 0.1
        assert result == pytest.approx((0.1, 0.1, 0.1))

    def test_simple_palette_specific_gradient_points(self):
        """Test specific gradient points for a known palette."""
        # Test at 0%, 25%, 50%, 75%, 100%
        k = 4.0  # To easily reach 1.0 at 0.25
        
        result_0 = simple_palette(0.0, k=k, u0=0)
        result_25 = simple_palette(0.25, k=k, u0=0)
        result_50 = simple_palette(0.5, k=k, u0=0)
        
        assert result_0[0] == pytest.approx(0.0)
        assert result_25[0] == pytest.approx(1.0)
        assert result_50[0] == pytest.approx(1.0)  # Clamped

    def test_simple_palette_symmetry_around_offset(self):
        """Test palette values around offset."""
        u0 = 0.2
        k = 1.0
        
        # Points equidistant from offset
        result_below = simple_palette(u0 - 0.1, k=k, u0=u0)
        result_above = simple_palette(u0 + 0.1, k=k, u0=u0)
        
        # Below offset: 1.0 * (0.1 - 0.2) = -0.1 → 0.0
        # Above offset: 1.0 * (0.3 - 0.2) = 0.1
        assert result_below == pytest.approx((0.0, 0.0, 0.0))
        assert result_above == pytest.approx((0.1, 0.1, 0.1))
