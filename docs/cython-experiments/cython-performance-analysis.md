# Cython Performance Analysis

## Performance Test Results

**Numba is ~10x faster than Cython:**

```
Cython z=8 (815 iter):  ~0.20s average
Numba  z=9 (1060 iter): ~0.02s average  ← 10x faster with 30% MORE iterations
Numba  z=12 (2329 iter): ~0.33s average ← Still competitive at 3x iterations
```

## Root Cause Analysis

### 1. Compilation Flags ❌

**Current:** Only `/O2` (basic optimization)

```c
"extra_compile_args": [
    "/O2"
]
```

**Missing optimizations:**
- No `/fp:fast` (fast floating-point math)
- No `/arch:AVX2` or `/arch:AVX` (SIMD vectorization)
- No `/GL` (whole program optimization)
- No `/Ot` (favor speed over size)

**Recommendation:**
```python
extra_compile_args=[
    "/O2",           # Optimize for speed
    "/fp:fast",      # Fast floating-point
    "/arch:AVX2",    # Use AVX2 instructions
    "/GL",           # Whole program optimization  
    "/Ot",           # Favor speed
]
```

### 2. Python Callback Overhead ❌ **MAJOR BOTTLENECK**

The Cython code calls Python functions **3 times per pixel** (65,536 calls per tile):

```python
# Inside nested loop (height × width iterations):
u = coloring_function(orbit, escape_time, bailout=bailout, p=p)      # Python call #1
I = color_index_function(u, max_iter)                                 # Python call #2
rgb = palette_function(I)                                             # Python call #3
```

Each Python call involves:
- GIL acquisition
- Reference counting
- Type checking
- Python object creation/destruction
- Vectorcall overhead

**Numba advantage:** JIT-compiles these functions inline as native code with **zero** Python overhead.

**Evidence from generated C:**
```c
// Each call goes through PyObject_FastCall with full Python overhead:
__pyx_t_1 = __Pyx_PyObject_FastCall((PyObject*)__pyx_t_6, __pyx_callargs+__pyx_t_7, ...)
```

### 3. No GIL Release ❌

The main loop **holds the GIL** throughout execution:

```c
__Pyx_RefNannySetupContext("mandelbrot_set_cython", 0);  // Acquires GIL
// ... nested loops with Python calls ...
__Pyx_RefNannyFinishContext();  // Releases GIL
```

**Impact:**
- Cannot use multi-threading
- Cannot parallelize computation
- GIL contention on every Python callback

**Numba advantage:** Automatically releases GIL when possible, uses `prange` for parallel execution.

### 4. Missing Source File ⚠️

The `.pyx` source was deleted after compilation - only `.c` and `.pyd` remain.

**Impact:**
- Cannot modify Cython implementation
- Cannot add `nogil` declarations
- Cannot cythonize the callback functions
- Cannot rebuild with better flags

## Optimization Recommendations

### Option A: Cythonize Callback Functions (Best Performance)

Create Cython versions of palette, color_index, and coloring functions:

**File: `fraktal/engines/palette_cy.pyx`**
```cython
# cython: language_level=3, boundscheck=False, wraparound=False

cdef inline (unsigned char, unsigned char, unsigned char) simple_palette_cy(double color_index) nogil:
    cdef unsigned char intensity = <unsigned char>(color_index * 255.0)
    return (intensity, intensity, intensity)

cdef inline (unsigned char, unsigned char, unsigned char) hot_palette_cy(double color_index) nogil:
    cdef double intensity = max(0.0, min(1.0, color_index))
    cdef unsigned char r, g, b
    
    if intensity < 1.0/3.0:
        r = <unsigned char>(intensity * 3.0 * 255.0)
        g = 0
        b = 0
    elif intensity < 2.0/3.0:
        r = 255
        g = <unsigned char>((intensity - 1.0/3.0) * 3.0 * 255.0)
        b = 0
    else:
        r = 255
        g = 255
        b = <unsigned char>((intensity - 2.0/3.0) * 3.0 * 255.0)
    
    return (r, g, b)
```

**File: `fraktal/engines/color_index_cy.pyx`**
```cython
# cython: language_level=3, boundscheck=False, wraparound=False

cdef inline double simple_index_cy(double u, double m) nogil:
    return u / m
```

**Then recreate `mandelbrot_cy.pyx` with:**
```cython
# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
cimport numpy as cnp
import numpy as np
from fraktal.engines.orbit_cy import truncated_orbit_cython
from fraktal.engines.palette_cy cimport simple_palette_cy, hot_palette_cy
from fraktal.engines.color_index_cy cimport simple_index_cy

ctypedef unsigned char uint8

cdef inline (uint8, uint8, uint8) compute_pixel(
    double c_real, 
    double c_imag,
    int max_iter,
    double bailout,
    int p,
    int palette_choice
) nogil:
    cdef double complex z0 = 0.0 + 0.0j
    cdef double complex c = c_real + c_imag*1j
    
    # Inline orbit computation (no Python calls)
    cdef int escape_time = max_iter
    cdef double complex z = z0
    cdef int i
    for i in range(max_iter):
        if z.real*z.real + z.imag*z.imag > bailout*bailout:
            escape_time = i
            break
        z = z*z + c
    
    # Smooth coloring (inline)
    cdef double u
    if escape_time < max_iter:
        u = <double>escape_time + 1.0 - log(log(abs(z))) / log(<double>p)
    else:
        u = <double>max_iter
    
    # Color index (inline)
    cdef double I = simple_index_cy(u, <double>max_iter)
    
    # Palette (inline, no Python)
    if palette_choice == 0:  # simple
        return simple_palette_cy(I)
    elif palette_choice == 1:  # hot
        return hot_palette_cy(I)
    else:
        return simple_palette_cy(I)

cpdef cnp.ndarray[uint8, ndim=3] mandelbrot_set_cython_optimized(
    double xmin, double xmax, double ymin, double ymax,
    int width, int height, int max_iter,
    int palette_choice = 0,
    double bailout = 2.0,
    int p = 2
) nogil:
    cdef cnp.ndarray[uint8, ndim=3] result = np.empty((height, width, 3), dtype=np.uint8)
    cdef int i, j
    cdef double c_real, c_imag
    cdef uint8 r, g, b
    
    with nogil:
        for i in prange(height, schedule='static'):
            for j in range(width):
                c_real = xmin + j * (xmax - xmin) / (width - 1)
                c_imag = ymin + i * (ymax - ymin) / (height - 1)
                
                r, g, b = compute_pixel(c_real, c_imag, max_iter, bailout, p, palette_choice)
                
                result[i, j, 0] = r
                result[i, j, 1] = g
                result[i, j, 2] = b
    
    return result
```

**Build script:**
```python
# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "fraktal.engines.mandelbrot_cy_optimized",
        ["fraktal/engines/mandelbrot_cy_optimized.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=[
            "/O2",           # Optimize for speed
            "/fp:fast",      # Fast floating-point
            "/arch:AVX2",    # Use AVX2 instructions (if supported)
            "/GL",           # Whole program optimization
            "/Ot",           # Favor speed over size
            "/openmp",       # Enable OpenMP for prange
        ],
        extra_link_args=["/LTCG"],  # Link-time code generation
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    ),
]

setup(
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': '3',
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'initializedcheck': False,
        },
        annotate=True,  # Generates HTML report showing Python interaction
    )
)
```

**Expected improvement:** 20-50x faster than current Cython, potentially faster than Numba

### Option B: Improve Existing Build (Quick Fix)

If the `.pyx` source can be recovered:

1. Add compilation flags (see above)
2. Add `nogil` to declaration:
   ```cython
   cpdef cnp.ndarray[uint8, ndim=3] mandelbrot_set_cython(...) with gil:
   ```
3. Rebuild:
   ```bash
   python setup.py build_ext --inplace
   ```

**Expected improvement:** 2-3x faster (still slower than Numba due to Python callbacks)

### Option C: Use Numba Exclusively (Simplest)

Given Numba's superior performance:

1. Remove Cython toggle from UI
2. Always use `mandelbrot_set_numba`
3. Delete Cython build artifacts
4. Focus optimization efforts on Numba (which is already excellent)

**Pros:**
- Zero Python callback overhead
- Automatic GIL release
- Automatic parallelization with `prange`
- No compilation step
- Easier to maintain

**Cons:**
- One less option for users
- Loses educational comparison

## Technical Deep Dive

### Why Numba is Faster

1. **JIT compilation**: Compiles entire function graph to native code at runtime
2. **Inlining**: Automatically inlines all Numba-decorated functions (palette, color_index, coloring)
3. **LLVM optimization**: Uses LLVM backend with aggressive optimizations
4. **Type specialization**: Generates specialized code for each argument type combination
5. **GIL management**: Automatically releases GIL for pure NumPy/numeric code
6. **SIMD**: Automatically vectorizes loops when possible

### Current Cython Bottleneck

```c
// EVERY pixel iteration (256×256 = 65,536 times per tile):
PyObject *coloring_result = __Pyx_PyObject_FastCall(coloring_function, ...);  // 1. GIL, refcount, boxing
PyObject *index_result = __Pyx_PyObject_FastCall(color_index_function, ...);  // 2. GIL, refcount, boxing
PyObject *palette_result = __Pyx_PyObject_FastCall(palette_function, ...);    // 3. GIL, refcount, boxing
PyObject *r = __Pyx_GetItemInt(palette_result, 0, ...);                       // 4. Tuple unpacking
result[i,j,0] = __Pyx_PyLong_As_unsigned_char(r);                             // 5. Python→C conversion
```

At z=8 (815 iterations), this is:
- **65,536 pixels**
- **196,608 Python function calls** (3 per pixel)
- **~1,000,000 reference count operations**
- **~500,000 GIL acquisitions/releases**

This explains the ~100-200ms overhead vs Numba's ~8-20ms.

## Recommendations Summary

**Immediate action:**
1. ✅ Use Numba exclusively - remove Cython toggle (simplest, already optimal)
2. 🔧 OR recover `.pyx` source and implement Option A (best Cython performance)

**Long-term:**
1. Keep Numba as default
2. Add Cython-optimized version for educational comparison
3. Benchmark both implementations thoroughly
4. Document findings for fractal generation best practices

## References

- Cython compilation: https://cython.readthedocs.io/en/latest/src/userguide/source_files_and_compilation.html
- MSVC compiler flags: https://learn.microsoft.com/en-us/cpp/build/reference/compiler-options
- Numba performance tips: https://numba.pydata.org/numba-doc/latest/user/performance-tips.html
- GIL and Cython: https://cython.readthedocs.io/en/latest/src/userguide/parallelism.html
