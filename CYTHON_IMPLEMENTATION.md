# Cython Integration - Implementation Summary

## What Was Implemented

This branch (`feature/cython-integration`) adds Cython support to the Fraktal library as an alternative to Numba, starting with the `seed.py` module.

### Files Created

1. **`fraktal/engines/seed_cy.pyx`** - Cython implementation of the seed function
2. **`fraktal/engines/seed_cy.pyi`** - Type stub for IDE support
3. **`setup.py`** - Build configuration for Cython extensions
4. **`tests/test_cython_integration.py`** - Tests comparing Numba and Cython implementations
5. **`docs/cython-build-instructions.md`** - Build and usage instructions
6. **`docs/cython-integration-guide.md`** - Comprehensive integration guide

### Files Modified

1. **`fraktal/engines/seed.py`** - Now supports both Numba and Cython, switchable via environment variable
2. **`pyproject.toml`** - Added Cython to build requirements
3. **`requirements.txt`** - Added Cython dependency
4. **`.gitignore`** - Added Cython build artifacts (*.c, *.pyd, *.so, etc.)

## Current Status

✅ **Implemented:**
- Cython version of `f_numba()` as `f_cython()`
- Automatic selection based on `FRAKTAL_USE_CYTHON` environment variable
- Type-safe Cython implementation with optimizations
- Test suite for verifying equivalence
- Build configuration via setup.py

⚠️ **Pending:**
- **Windows:** Requires Microsoft C++ Build Tools installation
- **Building:** Run `python setup.py build_ext --inplace` to compile
- **Testing:** Run tests after successful build

## How It Works

### Dual Implementation Strategy

The `seed.py` module now exports a function `f` that automatically selects between:
- `f_numba` (default) - JIT-compiled with Numba
- `f_cython` - Pre-compiled with Cython (when available and enabled)

### Usage

```python
import os

# Use Numba (default)
from fraktal.engines.seed import f
result = f(z, c, p=2)  # Uses f_numba

# Switch to Cython
os.environ['FRAKTAL_USE_CYTHON'] = 'true'
# Reload module or restart application
from fraktal.engines.seed import f
result = f(z, c, p=2)  # Uses f_cython
```

### For Dash App

```powershell
# Run with Numba (default)
python dash_app/app.py

# Run with Cython
$env:FRAKTAL_USE_CYTHON="true"
python dash_app/app.py
```

## Next Steps

### 1. Install Build Tools (Windows)

Download and install Microsoft C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

Select "Desktop development with C++" during installation.

### 2. Build the Extension

```powershell
python setup.py build_ext --inplace
```

This will create `fraktal/engines/seed_cy.pyd` (Windows) or `seed_cy.so` (Linux/Mac).

### 3. Run Tests

```powershell
# Test with Numba
pytest tests/test_cython_integration.py

# Test with Cython
$env:FRAKTAL_USE_CYTHON="true"
pytest tests/test_cython_integration.py
```

### 4. Benchmark Performance

Create a benchmark script to compare:
```python
import time
import os
import importlib

def benchmark(implementation, iterations=100000):
    os.environ['FRAKTAL_USE_CYTHON'] = 'true' if implementation == 'cython' else 'false'
    
    import fraktal.engines.seed as seed_module
    importlib.reload(seed_module)
    from fraktal.engines.seed import f
    
    z = complex(0.5, 0.5)
    c = complex(-0.4, 0.6)
    
    start = time.perf_counter()
    for _ in range(iterations):
        result = f(z, c, p=2)
    elapsed = time.perf_counter() - start
    
    return elapsed

print(f"Numba:  {benchmark('numba'):.4f}s")
print(f"Cython: {benchmark('cython'):.4f}s")
```

### 5. Expand to Other Modules

Once `seed_cy` is working, convert other modules:
- `fraktal/engines/orbit.py` → `orbit_cy.pyx`
- `fraktal/engines/color_index.py` → `color_index_cy.pyx`
- `fraktal/engines/palette.py` → `palette_cy.pyx`
- `fraktal/models/iteration_count.py` → `iteration_count_cy.pyx`

## Technical Details

### Cython Optimizations Used

1. **Static typing**: `complex128`, `int` for better performance
2. **Compiler directives**:
   - `boundscheck=False` - Disable array bounds checking
   - `wraparound=False` - Disable negative indexing
   - `cdivision=True` - Use C division semantics
3. **Specialized p=2 case**: Direct multiplication instead of power operator

### Performance Expectations

- **First call**: Cython should be faster (no JIT overhead)
- **Subsequent calls**: Both should be similar (sub-microsecond per call)
- **Memory**: Minimal difference
- **Binary size**: Cython adds ~100KB per module

## Troubleshooting

### Build Error: "Microsoft Visual C++ 14.0 or greater is required"
Install the C++ Build Tools (see Prerequisites above)

### Import Error: "cannot import name 'f_cython'"
Run the build command: `python setup.py build_ext --inplace`

### Environment Variable Not Working
Make sure to:
1. Set it before importing the module
2. Reload the module if already imported
3. Or restart the Python process

### Tests Failing
Check that:
1. Build was successful (`.pyd` or `.so` file exists)
2. Virtual environment is activated
3. All dependencies are installed

## References

- Full integration guide: `docs/cython-integration-guide.md`
- Build instructions: `docs/cython-build-instructions.md`
- Tests: `tests/test_cython_integration.py`
- Example implementation: `fraktal/engines/seed_cy.pyx`
