# Cython Integration Guide for Fraktal

This document outlines how to integrate Cython as an alternative to Numba in the Fraktal library, using `fraktal/engines/seed.py` as an example.

## Table of Contents
- [Overview](#overview)
- [Example: Converting seed.py](#example-converting-seedpy)
- [Integration Steps](#integration-steps)
- [Build and Installation Process](#build-and-installation-process)
- [Impact Analysis](#impact-analysis)
- [Performance Comparison Strategy](#performance-comparison-strategy)

---

## Overview

**Current approach:** Using Numba's `@njit` decorator for JIT (Just-In-Time) compilation
- Pros: Easy to use, no build step, pure Python syntax
- Cons: First-call compilation overhead, limited static optimization

**Cython approach:** Pre-compiled extension modules
- Pros: Ahead-of-time compilation, C-level performance, static type declarations
- Cons: Requires build step, more complex setup, platform-specific binaries

---

## Example: Converting seed.py

### Current Numba Implementation

**File:** `fraktal/engines/seed.py`

```python
import numpy as np
from numba import njit

@njit
def f_numba(z, c, p=2):
    """Numba-compatible version of the seed function f(z) = z^p + c.
    Args:
        z: complex, current value
        c: complex, constant value
        p: int, power to raise z to (default is 2)
    Returns:
        return next iteration of f(z) = z**p + c
    """
    return z**p + c
```

### Proposed Cython Implementation

**File:** `fraktal/engines/seed_cy.pyx`

```cython
# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython
from libc.math cimport pow
import numpy as np
cimport numpy as cnp

# Define complex number type
ctypedef double complex complex128

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef complex128 f_cython(complex128 z, complex128 c, int p=2):
    """Cython-optimized version of the seed function f(z) = z^p + c.
    
    Args:
        z: complex, current value
        c: complex, constant value
        p: int, power to raise z to (default is 2)
    
    Returns:
        complex128: next iteration of f(z) = z**p + c
    """
    # For p=2 (most common case), use direct multiplication for better performance
    if p == 2:
        return z * z + c
    else:
        return z**p + c
```

**Key Cython features used:**
- `cimport cython`: Import Cython-specific decorators
- `ctypedef`: Define type aliases for complex numbers
- `cpdef`: Create both C and Python-callable functions
- `cimport numpy as cnp`: Import numpy C-API for fast array operations
- Compiler directives (`# cython:`) for optimization
- Static type declarations (`complex128`, `int`)

---

## Integration Steps

### 1. Project Structure Changes

```
fraktal/
├── __init__.py
├── config.py
├── decorators.py
├── mapping.py
├── engines/
│   ├── __init__.py
│   ├── seed.py              # Original Numba version
│   ├── seed_cy.pyx          # NEW: Cython source
│   ├── seed_cy.pyi          # NEW: Type stub for IDE support (optional)
│   ├── color_index.py
│   ├── color_index_cy.pyx   # NEW: Cython version
│   ├── ... (other modules)
│   └── ...
└── models/
    └── ...
```

### 2. Create setup.py for Compilation

**File:** `setup.py` (at project root)

```python
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Define Cython extensions
extensions = [
    Extension(
        "fraktal.engines.seed_cy",
        ["fraktal/engines/seed_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],  # Optimization level
    ),
    Extension(
        "fraktal.engines.color_index_cy",
        ["fraktal/engines/color_index_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "fraktal.engines.palette_cy",
        ["fraktal/engines/palette_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "fraktal.engines.orbit_cy",
        ["fraktal/engines/orbit_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "fraktal.engines.mandelbrot_cy",
        ["fraktal/engines/mandelbrot_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],
    ),
    Extension(
        "fraktal.models.iteration_count_cy",
        ["fraktal/models/iteration_count_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"],
    ),
]

setup(
    name="fraktal",
    version="0.0.1",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
        },
        annotate=True,  # Generate HTML files showing C interaction
    ),
    include_dirs=[np.get_include()],
)
```

### 3. Update pyproject.toml

**File:** `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=42", "wheel", "Cython>=0.29.0", "numpy>=1.22"]
build-backend = "setuptools.build_meta"

[project]
name = "fraktal"
version = "0.0.1"
description = "Fraktal library and Dash app"
authors = [ { name = "HFlo" } ]
license = "MIT"

[tool.setuptools]
[tool.setuptools.packages.find]
include = ["fraktal*"]

[tool.pytest]
minversion = "6.0"
```

### 4. Update requirements.txt

**File:** `requirements.txt`

```txt
dash>=2.0.0
dash-mantine-components>=1.0.0
pytest>=7.0
psutil>=5.0
PyYAML>=6.0
numpy>=1.22
numba>=0.56          # Keep for comparison
Cython>=0.29.0       # NEW: Add Cython
matplotlib>=3.5
dash-iconify>=0.1.2
```

### 5. Update mapping.py to Support Both Versions

**File:** `fraktal/mapping.py`

```python
"""Mapping of coloring, color index, and palette functions for fractal rendering.
This module provides a centralized dictionary to access various models used in fractal computations.
Supports both Numba and Cython implementations.
"""

# Try to import Cython versions, fallback to Numba if not available
try:
    from fraktal.models.iteration_count_cy import (
        iteration_count as iteration_count_cy,
        continuous_iteration_count as continuous_iteration_count_cy,
        smooth_iteration_count as smooth_iteration_count_cy,
    )
    CYTHON_AVAILABLE = True
except ImportError:
    CYTHON_AVAILABLE = False

# Always import Numba versions
from fraktal.models.iteration_count import (
    iteration_count,
    continuous_iteration_count,
    smooth_iteration_count,
)

from fraktal.engines.color_index import simple_index
from fraktal.engines.palette import simple_palette, hot_palette, cool_palette

# Use environment variable or config to choose implementation
import os
USE_CYTHON = os.getenv('FRAKTAL_USE_CYTHON', 'false').lower() == 'true' and CYTHON_AVAILABLE

if USE_CYTHON:
    # Use Cython implementations
    _iteration_count = iteration_count_cy
    _continuous_iteration_count = continuous_iteration_count_cy
    _smooth_iteration_count = smooth_iteration_count_cy
else:
    # Use Numba implementations (default)
    _iteration_count = iteration_count
    _continuous_iteration_count = continuous_iteration_count
    _smooth_iteration_count = smooth_iteration_count

FRAKTAL_MODELS = {
    "coloring": {
        "iteration-count": {
            "function": _iteration_count,
            "name": "Iteration Count",
        },
        "continuous-iteration-count": {
            "function": _continuous_iteration_count,
            "name": "Continuous Iteration Count",
        },
        "smooth-iteration-count": {
            "function": _smooth_iteration_count,
            "name": "Smooth Iteration Count",
        },
    },
    "color_index": {
        "simple-index": {
            "function": simple_index,
            "name": "Simple Index",
        },
    },
    "palette": {
        "simple-palette": {
            "function": simple_palette,
            "name": "Simple Palette (Grayscale)",
        },
        "hot-palette": {
            "function": hot_palette,
            "name": "Hot Palette (Red-Yellow-White)",
        },
        "cool-palette": {
            "function": cool_palette,
            "name": "Cool Palette (Cyan-Blue-Green)",
        },
    },
}

# Expose which implementation is being used
IMPLEMENTATION = "Cython" if USE_CYTHON else "Numba"
```

---

## Build and Installation Process

### Development Installation (Editable Mode)

#### Before Cython (Current - Numba only):
```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Install package in editable mode
pip install -e .

# 4. Run immediately - no build step needed
python dash_app/app.py
```

#### After Cython Integration:
```powershell
# 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies (now includes Cython)
pip install -r requirements.txt

# 3. Build Cython extensions (NEW STEP)
python setup.py build_ext --inplace

# 4. Install package in editable mode
pip install -e .

# 5. Run the app
python dash_app/app.py
```

### Production Installation:
```powershell
pip install .
```

This will automatically:
1. Compile Cython extensions
2. Install the package
3. Make both Numba and Cython versions available

### Rebuilding After Changes

**If you modify a `.pyx` file:**
```powershell
python setup.py build_ext --inplace
```

**If you modify a `.py` file with Numba:**
No rebuild needed - Numba recompiles automatically on first run

---

## Impact Analysis

### 1. Installation Process Impact

| Aspect | Numba (Current) | With Cython |
|--------|----------------|-------------|
| **Initial Setup Time** | ~1-2 minutes | ~3-5 minutes (includes compilation) |
| **Build Requirements** | None | C compiler (MSVC on Windows, GCC/Clang on Linux/Mac) |
| **Binary Artifacts** | None | `.pyd` files (Windows) or `.so` files (Linux/Mac) |
| **Package Size** | Small (~100KB) | Larger (~5-10MB with compiled extensions) |
| **Cross-platform** | Pure Python - works everywhere | Platform-specific binaries needed |

### 2. Development Workflow Impact

| Activity | Numba (Current) | With Cython |
|----------|----------------|-------------|
| **Code Changes** | Edit `.py` → Run immediately | Edit `.pyx` → Rebuild → Run |
| **Debugging** | Python debugger works | More difficult; may need C debugging tools |
| **Type Errors** | Runtime errors | Compile-time errors (better!) |
| **IDE Support** | Full Python support | Limited (need `.pyi` type stubs) |

### 3. Runtime Performance Impact

| Metric | Numba | Cython | Notes |
|--------|-------|--------|-------|
| **First Call** | Slow (JIT compilation) | Fast (pre-compiled) | Cython wins |
| **Subsequent Calls** | Fast (cached) | Fast | Similar performance |
| **Memory Usage** | Lower | Slightly higher | Minimal difference |
| **Startup Time** | Fast | Fast | Similar |

### 4. Dash App Impact

**No impact on running the Dash app!**
- The app code (`dash_app/app.py`) doesn't change
- Import statements remain the same
- The choice between Numba/Cython is transparent
- Set environment variable to switch: `$env:FRAKTAL_USE_CYTHON="true"`

```powershell
# Use Numba (default)
python dash_app/app.py

# Use Cython
$env:FRAKTAL_USE_CYTHON="true"
python dash_app/app.py
```

### 5. Testing Impact

Tests continue to work without changes:
```powershell
# Run with Numba
pytest

# Run with Cython
$env:FRAKTAL_USE_CYTHON="true"
pytest
```

You can even create comparison tests:
```python
# tests/test_numba_vs_cython.py
import os
import time
import pytest

def test_performance_comparison():
    # Test with Numba
    os.environ['FRAKTAL_USE_CYTHON'] = 'false'
    # ... reload modules ...
    start = time.perf_counter()
    # ... run computation ...
    numba_time = time.perf_counter() - start
    
    # Test with Cython
    os.environ['FRAKTAL_USE_CYTHON'] = 'true'
    # ... reload modules ...
    start = time.perf_counter()
    # ... run computation ...
    cython_time = time.perf_counter() - start
    
    print(f"Numba: {numba_time:.4f}s, Cython: {cython_time:.4f}s")
```

---

## Performance Comparison Strategy

### Benchmarking Approach

Create a dedicated benchmark script:

**File:** `benchmarks/compare_implementations.py`

```python
import time
import numpy as np
import os

def benchmark_mandelbrot(implementation='numba', size=1000, iterations=100):
    """Benchmark Mandelbrot generation."""
    os.environ['FRAKTAL_USE_CYTHON'] = 'true' if implementation == 'cython' else 'false'
    
    # Reload modules to pick up environment variable
    import importlib
    import fraktal.mapping
    importlib.reload(fraktal.mapping)
    
    from fraktal.engines.mandelbrot import mandelbrot_set_numba
    from fraktal.mapping import FRAKTAL_MODELS
    
    coloring_fn = FRAKTAL_MODELS['coloring']['smooth-iteration-count']['function']
    color_index_fn = FRAKTAL_MODELS['color_index']['simple-index']['function']
    palette_fn = FRAKTAL_MODELS['palette']['simple-palette']['function']
    
    # Warm-up run
    _ = mandelbrot_set_numba(-2, 1, -1.5, 1.5, 100, 100, 50, 
                             coloring_fn, color_index_fn, palette_fn)
    
    # Timed runs
    start = time.perf_counter()
    result = mandelbrot_set_numba(-2, 1, -1.5, 1.5, size, size, iterations,
                                  coloring_fn, color_index_fn, palette_fn)
    elapsed = time.perf_counter() - start
    
    return elapsed, result

if __name__ == "__main__":
    print("Benchmarking Numba vs Cython")
    print("-" * 50)
    
    for size in [500, 1000, 2000]:
        print(f"\nImage size: {size}x{size}, 256 iterations")
        
        numba_time, _ = benchmark_mandelbrot('numba', size, 256)
        print(f"  Numba:  {numba_time:.4f}s")
        
        cython_time, _ = benchmark_mandelbrot('cython', size, 256)
        print(f"  Cython: {cython_time:.4f}s")
        
        speedup = numba_time / cython_time
        print(f"  Speedup: {speedup:.2f}x {'(Cython faster)' if speedup > 1 else '(Numba faster)'}")
```

---

## Migration Checklist

- [ ] Install Cython: `pip install Cython>=0.29.0`
- [ ] Create `.pyx` file for `seed.py`
- [ ] Create `setup.py` for building extensions
- [ ] Update `pyproject.toml` build requirements
- [ ] Build extensions: `python setup.py build_ext --inplace`
- [ ] Test Cython version works: `$env:FRAKTAL_USE_CYTHON="true"; pytest`
- [ ] Create benchmarks comparing both implementations
- [ ] Document results and choose best approach
- [ ] Optionally: Convert remaining modules (orbit, palette, mandelbrot, etc.)

---

## Recommendations

1. **Start Small**: Convert one module at a time, starting with `seed.py`
2. **Keep Both**: Maintain both Numba and Cython implementations for comparison
3. **Benchmark Early**: Test performance before converting everything
4. **Document Differences**: Track which implementation is faster for which operations
5. **CI/CD Considerations**: If using GitHub Actions, ensure C compiler is available in build environment

---

## Dash App Integration: Runtime Toggle

The Fraktal Dash app includes a **toggle switch** that allows users to switch between Numba and Cython implementations at runtime.

### Implementation Overview

**UI Component** (`dash_app/components/tab_components/mandelbrot_form.py`):
```python
dmc.Switch(
    label="Use Cython (instead of Numba)",
    id="use-cython-switch",
    checked=mandelbrot_defaults.get('use_cython', False),
    description="Toggle between Cython and Numba implementations",
    my=10
),
```

**Backend Selection** (`dash_app/components/tab_components/generate_tab_content.py`):
```python
# Import both implementations
from fraktal.engines.mandelbrot import mandelbrot_set_numba
if CYTHON_AVAILABLE:
    from fraktal.engines.mandelbrot_cy import mandelbrot_set_cython

# Select based on user toggle
if use_cython and mandelbrot_set_cython is not None:
    mandelbrot_fn = mandelbrot_set_cython
else:
    mandelbrot_fn = mandelbrot_set_numba

# Generate fractal with selected implementation
img_array = mandelbrot_fn(xmin, xmax, ymin, ymax, width, height, max_iter,
                         coloring_fn, color_index_fn, palette_fn,
                         bailout=2.0, p=2)
```

### Cython Modules Created

1. **`fraktal/engines/seed_cy.pyx`**: Cython seed function `f_cython(z, c, p)`
2. **`fraktal/engines/orbit_cy.pyx`**: Cython orbit calculation `truncated_orbit_cython(...)`
3. **`fraktal/engines/mandelbrot_cy.pyx`**: Full Cython Mandelbrot generator `mandelbrot_set_cython(...)`

### Key Design Decisions

- **Separate Implementations**: Numba and Cython can't be mixed in the same JIT-compiled function, so we created parallel implementations
- **Graceful Fallback**: If Cython extensions aren't built, the app falls back to Numba automatically
- **Type Handling**: Cython version uses `object` types for `u` and `I` to handle infinity and large values without overflow
- **RGB Clamping**: Uses bitwise masking (`int(rgb[0]) & 0xFF`) to safely convert to uint8

### Testing

Run the toggle-specific tests:
```bash
pytest tests/test_dash_cython_toggle.py -v
```

This verifies:
- ✓ Numba implementation works
- ✓ Cython implementation works (if built)
- ✓ Both produce equivalent results

### Performance Comparison

Users can directly compare performance by:
1. Generating a fractal with Numba (toggle OFF)
2. Generating the same fractal with Cython (toggle ON)
3. Comparing render times in the UI

---

## Further Reading

- [Cython Documentation](https://cython.readthedocs.io/)
- [Cython for NumPy Users](https://cython.readthedocs.io/en/latest/src/userguide/numpy_tutorial.html)
- [Numba vs Cython Comparison](https://notes-on-cython.readthedocs.io/en/latest/std_dev.html)
- [Building Cython Extensions](https://cython.readthedocs.io/en/latest/src/quickstart/build.html)
