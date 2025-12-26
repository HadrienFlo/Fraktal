# Building Optimized Cython Extensions

## Prerequisites

1. **Microsoft Visual C++ Build Tools** (Windows)
   - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++" workload
   - Or use Visual Studio 2019/2022 with C++ support

2. **Python packages:**
   ```powershell
   pip install cython numpy
   ```

## Build Instructions

### Option 1: Using the batch file (Windows)

```powershell
.\build_cython.bat
```

### Option 2: Manual build

```powershell
python setup_cython.py build_ext --inplace
```

## Verification

After building, you should see:

```
fraktal/engines/
├── mandelbrot_cy_optimized.pyx          # Source file
├── mandelbrot_cy_optimized.c            # Generated C code
├── mandelbrot_cy_optimized.cp310-win_amd64.pyd  # Compiled extension
└── mandelbrot_cy_optimized.html         # Annotation (yellow = Python, white = C)
```

## Testing Performance

1. Restart the Dash app:
   ```powershell
   python -m dash_app.app
   ```

2. Navigate to http://localhost:8050/explorer

3. Toggle "Use Cython (faster)" checkbox

4. Watch terminal output for timing comparisons:
   ```
   CYTHON-OPT tile z=9, iter=1060: 0.008s  ← New optimized version
   NUMBA tile z=9, iter=1060: 0.009s       ← Numba (for comparison)
   ```

## Expected Performance

| Implementation | z=8 (815 iter) | z=9 (1060 iter) | z=12 (2329 iter) | Notes |
|----------------|----------------|-----------------|------------------|-------|
| Cython (old)   | ~200ms         | ~250ms          | ~600ms           | Python callbacks, GIL |
| **Cython (optimized)** | **~8ms** | **~12ms** | **~180ms** | **No Python, nogil, parallel** |
| Numba          | ~10ms          | ~15ms           | ~300ms           | JIT compiled |

**Expected result:** Optimized Cython should be **20-50x faster** than old version, comparable to or slightly faster than Numba.

## Troubleshooting

### Build fails with "error: Microsoft Visual C++ 14.0 or greater is required"

**Solution:** Install Visual C++ Build Tools (see Prerequisites)

### Build fails with "cannot open file 'openmp.lib'"

**Solution:** Disable OpenMP by editing `setup_cython.py`:
```python
# Remove '/openmp' from extra_compile_args
extra_compile_args = [
    '/O2',
    '/fp:fast',
    '/GL',
    '/Ot',
    # '/openmp',  # <- Comment this out
    '/favor:AMD64',
]
```

Then rebuild. Performance will be slightly lower (no parallelization) but still much better than old Cython.

### Import error: "DLL load failed while importing mandelbrot_cy_optimized"

**Solution:** Make sure you're using the same Python environment that has NumPy installed:
```powershell
python --version
python -c "import numpy; print(numpy.__version__)"
```

### Performance not improved

1. Check which version is being used (look for `CYTHON-OPT` in terminal output)
2. View annotation file: `fraktal/engines/mandelbrot_cy_optimized.html`
   - Yellow lines = Python interaction (should be minimal)
   - White lines = Pure C code (should be most of the loop)

## Advanced: Viewing Generated C Code

The annotation HTML file shows exactly what was compiled:

1. Open `fraktal/engines/mandelbrot_cy_optimized.html` in a browser
2. Look for the `compute_pixel` function
3. **White background** = Compiled to pure C (fast)
4. **Yellow background** = Still using Python C-API (slow)

Ideally, the entire inner loop should be white.

## Compilation Flags Explained

| Flag | Purpose | Impact |
|------|---------|--------|
| `/O2` | Optimize for speed | +30% faster |
| `/fp:fast` | Fast floating-point math | +20% faster for fractals |
| `/GL` | Whole program optimization | +10% faster |
| `/Ot` | Favor speed over size | +5% faster |
| `/openmp` | Enable parallel loops | +2-3x faster (multi-core) |
| `/arch:AVX2` | Use AVX2 SIMD instructions | +10-20% faster |

**Combined effect:** ~20-50x faster than unoptimized Cython with Python callbacks.
