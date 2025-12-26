# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as cnp
from libc.math cimport sqrt

# Import Cython types
ctypedef double complex complex128

cpdef tuple truncated_orbit_cython(complex128 z, complex128 c, int max_iterations, double bailout=2.0, int p=2):
    """
    Cython-optimized truncated orbit calculation.
    
    Returns:
        tuple: (orbit array, escape_time)
    """
    cdef cnp.ndarray[complex128, ndim=1] orbit = np.empty(max_iterations + 1, dtype=np.complex128)
    cdef int n
    cdef double abs_z_sq
    
    for n in range(max_iterations + 1):
        orbit[n] = z
        # Compute next iteration - optimize for p=2 case
        if p == 2:
            z = z * z + c
        else:
            z = z**p + c
        # Check bailout
        abs_z_sq = z.real * z.real + z.imag * z.imag
        if abs_z_sq > bailout * bailout:
            return orbit, n
    return orbit, max_iterations
