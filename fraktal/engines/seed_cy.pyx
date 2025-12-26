# cython: language_level=3
# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

cimport cython

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
