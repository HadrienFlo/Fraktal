from fraktal.mandelbrot import mandelbrot_set, mandelbrot_set_numba
import numpy as np
import time
# import matplotlib.pyplot as plt

def test_mandelbrot_basic():
    # Small grid, should run fast
    arr = mandelbrot_set(-2, 1, -1.5, 1.5, 10, 10, 20)
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (10, 10)
    # The center (0,0) should not diverge quickly
    center = arr[5, 3]
    assert center > 5
    # Points far right (real=1) should diverge quickly
    assert arr[5, -1] < 5

def test_mandelbrot_performance():
    # Larger grid to test performance
    arr = mandelbrot_set(-2, 1, -1.5, 1.5, 500, 500, 100)
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (500, 500)
    # Check some known points
    assert arr[250, 333] > 50  # Near center
    assert arr[250, 499] < 10   # Far right

def test_mandelbrot_numba_equivalence():
    arr_np = mandelbrot_set(-2, 1, -1.5, 1.5, 100, 100, 50)
    arr_nb = mandelbrot_set_numba(-2, 1, -1.5, 1.5, 100, 100, 50)
    assert np.allclose(arr_np, arr_nb)

def test_mandelbrot_numba_speed():
    t0 = time.time()
    mandelbrot_set(-2, 1, -1.5, 1.5, 300, 300, 100)
    t1 = time.time()
    mandelbrot_set_numba(-2, 1, -1.5, 1.5, 300, 300, 100)
    t2 = time.time()
    print(f"NumPy: {t1-t0:.6f}s, Numba: {t2-t1:.6f}s (first call includes JIT compile)")

# def test_mandelbrot_display():
#     arr = mandelbrot_set(-2, 1, -1.5, 1.5, 300, 200, 50)
#     plt.imshow(arr, cmap='hot', extent=[-2, 1, -1.5, 1.5])
#     plt.title('Mandelbrot Set')
#     plt.xlabel('Re')
#     plt.ylabel('Im')
#     plt.colorbar(label='Iterations to Divergence')
#     plt.show()

# def test_mandelbrot_numba_display():
#     arr = mandelbrot_set_numba(-2, 1, -1.5, 1.5, 300, 200, 50)
#     plt.imshow(arr, cmap='hot', extent=[-2, 1, -1.5, 1.5])
#     plt.title('Mandelbrot Set (Numba)')
#     plt.xlabel('Re')
#     plt.ylabel('Im')
#     plt.colorbar(label='Iterations to Divergence')
#     plt.show()
