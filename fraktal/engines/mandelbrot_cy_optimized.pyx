# cython: language_level=3, boundscheck=False, wraparound=False, cdivision=True
# cython: initializedcheck=False, nonecheck=False
"""
Optimized Cython implementation of Mandelbrot set generation.
All functions are inlined in C with nogil for maximum performance.
"""
cimport numpy as cnp
import numpy as np
from libc.math cimport log, sqrt
cimport cython
from cython.parallel cimport prange

ctypedef unsigned char uint8

# Inline palette functions (pure C, no Python)
cdef inline void simple_palette_cy(double color_index, uint8 *r, uint8 *g, uint8 *b) nogil:
    """Simple grayscale palette"""
    cdef uint8 intensity = <uint8>(color_index * 255.0)
    if intensity > 255:
        intensity = 255
    r[0] = intensity
    g[0] = intensity
    b[0] = intensity

cdef inline void hot_palette_cy(double color_index, uint8 *r, uint8 *g, uint8 *b) nogil:
    """Hot color palette (red -> yellow -> white)"""
    cdef double intensity = color_index * 2.5
    if intensity < 0.0:
        intensity = 0.0
    elif intensity > 1.0:
        intensity = 1.0
    
    cdef uint8 ri, gi, bi
    if intensity < 1.0/3.0:
        ri = <uint8>(intensity * 3.0 * 255.0)
        gi = 0
        bi = 0
    elif intensity < 2.0/3.0:
        ri = 255
        gi = <uint8>((intensity - 1.0/3.0) * 3.0 * 255.0)
        bi = 0
    else:
        ri = 255
        gi = 255
        bi = <uint8>((intensity - 2.0/3.0) * 3.0 * 255.0)
    
    r[0] = ri
    g[0] = gi
    b[0] = bi

cdef inline void cool_palette_cy(double color_index, uint8 *r, uint8 *g, uint8 *b) nogil:
    """Cool color palette (cyan -> blue -> green -> cyan)"""
    cdef double intensity = color_index * 2.5
    if intensity < 0.0:
        intensity = 0.0
    elif intensity > 1.0:
        intensity = 1.0
    
    cdef uint8 ri, gi, bi
    if intensity < 1.0/3.0:
        ri = 0
        gi = <uint8>(intensity * 3.0 * 255.0)
        bi = 255
    elif intensity < 2.0/3.0:
        ri = 0
        gi = 255
        bi = <uint8>((1.0 - (intensity - 1.0/3.0) * 3.0) * 255.0)
    else:
        ri = <uint8>((intensity - 2.0/3.0) * 3.0 * 255.0)
        gi = 255
        bi = 0
    
    r[0] = ri
    g[0] = gi
    b[0] = bi

cdef inline double simple_index_cy(double u, double m) nogil:
    """Simple color index function"""
    return u / m

cdef inline double smooth_iteration_count_cy(
    double complex z,
    int escape_time,
    int max_iter,
    double bailout,
    int p
) nogil:
    """Smooth iteration count for continuous coloring"""
    if escape_time >= max_iter:
        return <double>max_iter
    
    cdef double abs_z = sqrt(z.real * z.real + z.imag * z.imag)
    if abs_z <= 0.0:
        return <double>escape_time
    
    cdef double log_zn = log(abs_z)
    cdef double nu = log(log_zn / log(bailout)) / log(<double>p)
    
    return <double>escape_time + 1.0 - nu

cdef inline void compute_pixel(
    double c_real,
    double c_imag,
    int max_iter,
    double bailout,
    int p,
    int palette_choice,
    uint8 *r,
    uint8 *g,
    uint8 *b
) nogil:
    """Compute single pixel color with full Mandelbrot iteration inline"""
    # Declare all variables at the top (Cython requirement)
    cdef double zr = 0.0
    cdef double zi = 0.0
    cdef double zr2 = 0.0
    cdef double zi2 = 0.0
    cdef double zr_tmp
    cdef int i
    cdef int escape_time = max_iter
    cdef double bailout2 = bailout * bailout
    cdef double u
    cdef double abs_z
    cdef double log_zn
    cdef double nu
    cdef double I
    
    # Mandelbrot iteration (optimized)
    for i in range(max_iter):
        zr2 = zr * zr
        zi2 = zi * zi
        if zr2 + zi2 > bailout2:
            escape_time = i
            break
        zr_tmp = zr2 - zi2 + c_real
        zi = 2.0 * zr * zi + c_imag
        zr = zr_tmp
    
    # Smooth coloring
    if escape_time < max_iter:
        abs_z = sqrt(zr * zr + zi * zi)
        if abs_z > 0.0:
            log_zn = log(abs_z)
            nu = log(log_zn / log(bailout)) / log(<double>p)
            u = <double>escape_time + 1.0 - nu
        else:
            u = <double>escape_time
    else:
        u = <double>max_iter
    
    # Color index
    I = simple_index_cy(u, <double>max_iter)
    
    # Apply palette
    if palette_choice == 0:  # simple
        simple_palette_cy(I, r, g, b)
    elif palette_choice == 1:  # hot
        hot_palette_cy(I, r, g, b)
    elif palette_choice == 2:  # cool
        cool_palette_cy(I, r, g, b)
    else:
        simple_palette_cy(I, r, g, b)

@cython.boundscheck(False)
@cython.wraparound(False)
def mandelbrot_set_cython_optimized(
    double xmin,
    double xmax,
    double ymin,
    double ymax,
    int width,
    int height,
    int max_iter,
    int palette_choice=0,
    double bailout=2.0,
    int p=2
):
    """
    Optimized Cython Mandelbrot set generator with no Python callbacks.
    
    Args:
        xmin, xmax: Real axis range
        ymin, ymax: Imaginary axis range
        width, height: Output image dimensions
        max_iter: Maximum iteration count
        palette_choice: 0=simple, 1=hot, 2=cool
        bailout: Escape threshold (default: 2.0)
        p: Power parameter (default: 2)
    
    Returns:
        NumPy array of shape (height, width, 3) with RGB values
    """
    # Create array (requires GIL)
    cdef cnp.ndarray[uint8, ndim=3] result = np.empty((height, width, 3), dtype=np.uint8)
    
    # Get typed memoryview for fast access
    cdef uint8[:, :, :] result_view = result
    cdef int i, j
    cdef double c_real, c_imag
    cdef double dx = (xmax - xmin) / <double>(width - 1)
    cdef double dy = (ymax - ymin) / <double>(height - 1)
    
    # Simple loop without prange first (to test base performance)
    # OpenMP overhead can be significant for small arrays
    with nogil:
        for i in range(height):
            for j in range(width):
                c_real = xmin + j * dx
                c_imag = ymin + i * dy
                
                compute_pixel(c_real, c_imag, max_iter, bailout, p, palette_choice, 
                            &result_view[i, j, 0], &result_view[i, j, 1], &result_view[i, j, 2])
    
    return result
