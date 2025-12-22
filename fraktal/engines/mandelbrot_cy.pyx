# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as cnp
from fraktal.engines.orbit_cy import truncated_orbit_cython

ctypedef double complex complex128
ctypedef unsigned char uint8

cpdef cnp.ndarray[uint8, ndim=3] mandelbrot_set_cython(
    double xmin, double xmax, double ymin, double ymax,
    int width, int height, int max_iter,
    object coloring_function, object color_index_function, object palette_function,
    double bailout=2.0, int p=2
):
    """
    Cython-optimized Mandelbrot set generator.
    """
    cdef cnp.ndarray[uint8, ndim=3] result = np.full((height, width, 3), max_iter, dtype=np.uint8)
    cdef int i, j
    cdef double c_real, c_imag
    cdef complex128 c, z0
    cdef tuple orbit_result
    cdef cnp.ndarray orbit
    cdef int escape_time
    cdef object u  # Keep as Python object since it can be infinity
    cdef object I  # Keep as Python object to avoid overflow
    cdef object rgb  # Keep as Python tuple
    
    for i in range(height):
        for j in range(width):
            c_real = xmin + j * (xmax - xmin) / (width - 1)
            c_imag = ymin + i * (ymax - ymin) / (height - 1)
            c = complex(c_real, c_imag)
            z0 = complex(0.0, 0.0)
            
            orbit_result = truncated_orbit_cython(z0, c, max_iter, bailout=bailout, p=p)
            orbit = orbit_result[0]
            escape_time = orbit_result[1]
            
            u = coloring_function(orbit, escape_time, bailout=bailout, p=p)
            I = color_index_function(u, max_iter)
            rgb = palette_function(I)
            
            # Assign RGB values safely (keep as Python objects to avoid overflow)
            result[i, j, 0] = int(rgb[0]) & 0xFF  # Mask to 8 bits
            result[i, j, 1] = int(rgb[1]) & 0xFF
            result[i, j, 2] = int(rgb[2]) & 0xFF
    
    return result
