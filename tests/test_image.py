"""Tests for the image.py module."""

import numpy as np
import pytest
from fraktal.engines.image import set_image_parameters, generate_fractal_image
from fraktal.engines.mandelbrot import mandelbrot_set, mandelbrot_set_numba


class TestSetImageParameters:
    """Tests for the set_image_parameters function."""

    def test_set_image_parameters_basic(self):
        """Test basic image parameter generation."""
        x, y = set_image_parameters(-2, 1, -1.5, 1.5, 10, 10)
        
        assert isinstance(x, np.ndarray)
        assert isinstance(y, np.ndarray)
        assert len(x) == 10
        assert len(y) == 10

    def test_set_image_parameters_real_axis(self):
        """Test that x values span the real axis correctly."""
        x, _ = set_image_parameters(-2, 1, -1.5, 1.5, 10, 10)
        
        assert x[0] == pytest.approx(-2.0)
        assert x[-1] == pytest.approx(1.0)
        assert np.all(x[:-1] < x[1:])  # Monotonically increasing

    def test_set_image_parameters_imag_axis(self):
        """Test that y values span the imaginary axis correctly."""
        _, y = set_image_parameters(-2, 1, -1.5, 1.5, 10, 10)
        
        assert y[0] == pytest.approx(-1.5)
        assert y[-1] == pytest.approx(1.5)
        assert np.all(y[:-1] < y[1:])  # Monotonically increasing

    def test_set_image_parameters_spacing(self):
        """Test that parameter values are evenly spaced."""
        x, y = set_image_parameters(-2, 1, -1.5, 1.5, 100, 100)
        
        # Check uniform spacing
        x_diff = np.diff(x)
        y_diff = np.diff(y)
        
        assert np.allclose(x_diff, x_diff[0])
        assert np.allclose(y_diff, y_diff[0])

    def test_set_image_parameters_different_dimensions(self):
        """Test with different image dimensions."""
        x1, y1 = set_image_parameters(-2, 1, -1.5, 1.5, 50, 100)
        x2, y2 = set_image_parameters(-2, 1, -1.5, 1.5, 100, 50)
        
        assert len(x1) == 50
        assert len(y1) == 100
        assert len(x2) == 100
        assert len(y2) == 50

    def test_set_image_parameters_single_pixel(self):
        """Test with single pixel (edge case)."""
        x, y = set_image_parameters(-2, 1, -1.5, 1.5, 1, 1)
        
        assert len(x) == 1
        assert len(y) == 1
        assert x[0] == pytest.approx(-2.0)
        assert y[0] == pytest.approx(-1.5)

    def test_set_image_parameters_high_resolution(self):
        """Test with high resolution."""
        x, y = set_image_parameters(-2, 1, -1.5, 1.5, 1000, 1000)
        
        assert len(x) == 1000
        assert len(y) == 1000
        assert x[0] == pytest.approx(-2.0)
        assert x[-1] == pytest.approx(1.0)


class TestGenerateFractalImage:
    """Tests for the generate_fractal_image function."""

    def test_generate_fractal_image_numpy(self):
        """Test fractal image generation with NumPy engine."""
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 30, mandelbrot_set
        )
        
        assert isinstance(result, np.ndarray)
        assert result.shape == (50, 50)
        assert result.dtype in (int, np.int32, np.int64)

    def test_generate_fractal_image_numba(self):
        """Test fractal image generation with Numba engine."""
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 30, mandelbrot_set_numba
        )
        
        assert isinstance(result, np.ndarray)
        assert result.shape == (50, 50)
        assert result.dtype in (int, np.int32, np.int64)

    def test_generate_fractal_image_values_in_range(self):
        """Test that generated values are within expected range."""
        max_iter = 50
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, max_iter, mandelbrot_set
        )
        
        assert np.all(result >= 0)
        assert np.all(result <= max_iter)

    def test_generate_fractal_image_numpy_numba_equivalence(self):
        """Test that NumPy and Numba engines produce equivalent results."""
        result_np = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 40, mandelbrot_set
        )
        result_nb = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 40, mandelbrot_set_numba
        )
        
        assert np.allclose(result_np, result_nb)

    def test_generate_fractal_image_symmetry(self):
        """Test that Mandelbrot set image has approximate vertical symmetry."""
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 100, 100, 50, mandelbrot_set
        )
        
        # Mandelbrot set should be roughly symmetric about the real axis
        # Check that top and bottom halves are similar
        top_half = result[:50, :]
        bottom_half = result[50:, :]
        
        # Should be approximately equal when flipped
        assert np.allclose(top_half, np.flip(bottom_half, axis=0), atol=2)

    def test_generate_fractal_image_center_convergence(self):
        """Test that the center region (0, 0) has higher iteration counts."""
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 100, 100, 100, mandelbrot_set
        )
        
        # The center region should have higher values (slower divergence)
        center = result[50, 50]
        edge = result[0, 0]
        
        assert center > edge

    def test_generate_fractal_image_small_region(self):
        """Test generation of a small fractal region."""
        result = generate_fractal_image(
            -0.75, -0.73, 0.1, 0.12, 50, 50, 100, mandelbrot_set
        )
        
        assert result.shape == (50, 50)
        assert np.all(result >= 0)
        assert np.all(result <= 100)

    def test_generate_fractal_image_with_kwargs(self):
        """Test that kwargs are properly passed to engine function."""
        # Test that we can pass the p parameter through kwargs
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 30, mandelbrot_set_numba, p=2
        )
        
        assert isinstance(result, np.ndarray)
        assert result.shape == (50, 50)

    def test_generate_fractal_image_different_resolutions(self):
        """Test with various resolutions."""
        for width, height in [(10, 10), (50, 30), (100, 100), (200, 150)]:
            result = generate_fractal_image(
                -2, 1, -1.5, 1.5, width, height, 30, mandelbrot_set
            )
            
            assert result.shape == (height, width)

    def test_generate_fractal_image_max_iteration_effect(self):
        """Test that higher max_iter values produce different results."""
        result_low = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 10, mandelbrot_set
        )
        result_high = generate_fractal_image(
            -2, 1, -1.5, 1.5, 50, 50, 100, mandelbrot_set
        )
        
        # With more iterations, we should have more pixels that don't diverge
        non_max_low = np.sum(result_low < 10)
        non_max_high = np.sum(result_high < 100)
        
        assert non_max_high >= non_max_low


class TestImageIntegration:
    """Integration tests for image generation."""

    def test_generate_full_mandelbrot_image(self):
        """Test generating a standard Mandelbrot set image."""
        result = generate_fractal_image(
            -2, 1, -1.5, 1.5, 300, 300, 100, mandelbrot_set_numba
        )
        
        assert result.shape == (300, 300)
        assert np.all(result >= 0)
        assert np.all(result <= 100)

    def test_zoomed_mandelbrot_region(self):
        """Test generating a zoomed-in region of the Mandelbrot set."""
        # Zoom into a known interesting region
        result = generate_fractal_image(
            -0.8, -0.4, -0.2, 0.2, 100, 100, 100, mandelbrot_set
        )
        
        assert result.shape == (100, 100)
        assert np.all(result >= 0)
        assert np.all(result <= 100)

    def test_extreme_zoom_region(self):
        """Test with very high zoom into a small region."""
        result = generate_fractal_image(
            -0.748, -0.746, 0.099, 0.101, 100, 100, 256, mandelbrot_set_numba
        )
        
        assert result.shape == (100, 100)
        assert np.all(result >= 0)
        assert np.all(result <= 256)
