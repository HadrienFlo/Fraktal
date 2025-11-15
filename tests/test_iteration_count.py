"""Tests for the models/iteration_count.py module."""

import pytest
import numpy as np
from fraktal.models.iteration_count import truncated_orbit_length


class TestTruncatedOrbitLength:
    """Tests for the truncated_orbit_length function."""

    def test_truncated_orbit_length_basic(self):
        """Test basic truncated orbit length calculation."""
        orbit = np.array([0.0+0.0j, 0.5+0.5j, 1.0+1.0j], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert isinstance(result, (int, float, np.number))
        assert result == pytest.approx(3.0 / 20)
        assert result == pytest.approx(0.15)

    def test_truncated_orbit_length_single_element(self):
        """Test with single element orbit."""
        orbit = np.array([0.0+0.0j], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(1.0 / 20)
        assert result == pytest.approx(0.05)

    def test_truncated_orbit_length_empty_array(self):
        """Test with empty array."""
        orbit = np.array([], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(0.0)

    def test_truncated_orbit_length_large_orbit(self):
        """Test with large orbit."""
        orbit = np.arange(100, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(100.0 / 20)
        assert result == pytest.approx(5.0)

    def test_truncated_orbit_length_exact_division(self):
        """Test with orbit length that divides evenly by 20."""
        orbit = np.zeros(20, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(1.0)

    def test_truncated_orbit_length_multiple_of_twenty(self):
        """Test with various multiples of 20."""
        for size in [20, 40, 60, 100]:
            orbit = np.zeros(size, dtype=np.complex128)
            result = truncated_orbit_length(orbit)
            assert result == pytest.approx(size / 20.0)

    def test_truncated_orbit_length_non_multiple(self):
        """Test with orbit length that doesn't divide evenly by 20."""
        orbit = np.zeros(25, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(25.0 / 20)
        assert result == pytest.approx(1.25)

    def test_truncated_orbit_length_with_complex_values(self):
        """Test with actual complex orbit values."""
        orbit = np.array([
            0.0+0.0j,
            0.5+0.5j,
            1.0+0.0j,
            0.5-0.5j,
            -0.5-0.5j,
            -1.0+0.0j
        ], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(6.0 / 20)
        assert result == pytest.approx(0.3)

    def test_truncated_orbit_length_dtype_complex64(self):
        """Test with complex64 dtype."""
        orbit = np.array([0.0+0.0j, 1.0+1.0j, 2.0+2.0j], dtype=np.complex64)
        result = truncated_orbit_length(orbit)
        # Should still work with complex64
        assert result == pytest.approx(3.0 / 20)

    def test_truncated_orbit_length_very_small_orbit(self):
        """Test with very small orbit (2 elements)."""
        orbit = np.array([0.0+0.0j, 1.0+1.0j], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(2.0 / 20)
        assert result == pytest.approx(0.1)

    def test_truncated_orbit_length_very_large_orbit(self):
        """Test with very large orbit."""
        orbit = np.zeros(2000, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(2000.0 / 20)
        assert result == pytest.approx(100.0)

    def test_truncated_orbit_length_consistency(self):
        """Test that function returns consistent results for same input."""
        orbit = np.array([1.0+2.0j, 3.0+4.0j, 5.0+6.0j], dtype=np.complex128)
        result1 = truncated_orbit_length(orbit)
        result2 = truncated_orbit_length(orbit)
        assert result1 == result2

    def test_truncated_orbit_length_linspace_orbit(self):
        """Test with linearly spaced orbit."""
        orbit = np.linspace(0, 1, 50, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(50.0 / 20)
        assert result == pytest.approx(2.5)

    def test_truncated_orbit_length_mandelbrot_like_orbit(self):
        """Test with realistic Mandelbrot-like orbit."""
        c = -0.7+0.27015j  # A point in the Mandelbrot set
        orbit_list = [0+0j]
        z = 0+0j
        for _ in range(19):
            z = z**2 + c
            orbit_list.append(z)
        orbit = np.array(orbit_list, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(20.0 / 20)
        assert result == pytest.approx(1.0)

    def test_truncated_orbit_length_return_type(self):
        """Test that return type is numeric."""
        orbit = np.array([0.0+0.0j, 1.0+1.0j], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        # Result should be numeric (int or float)
        assert isinstance(result, (int, float, np.integer, np.floating))

    def test_truncated_orbit_length_fractional_result(self):
        """Test that fractional results are calculated correctly."""
        orbit = np.zeros(33, dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(33.0 / 20)
        assert result == pytest.approx(1.65)

    def test_truncated_orbit_length_with_large_complex_values(self):
        """Test with large magnitude complex values."""
        orbit = np.array([
            0.0+0.0j,
            100.0+200.0j,
            -150.0+250.0j,
            500.0-300.0j
        ], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(4.0 / 20)
        assert result == pytest.approx(0.2)

    def test_truncated_orbit_length_with_small_complex_values(self):
        """Test with very small magnitude complex values."""
        orbit = np.array([
            0.0+0.0j,
            0.001+0.001j,
            0.0001+0.0001j
        ], dtype=np.complex128)
        result = truncated_orbit_length(orbit)
        assert result == pytest.approx(3.0 / 20)
        assert result == pytest.approx(0.15)
