"""Type stub for seed_cy module to provide IDE support."""

def f_cython(z: complex, c: complex, p: int = 2) -> complex:
    """Cython-optimized version of the seed function f(z) = z^p + c.
    
    Args:
        z: complex, current value
        c: complex, constant value
        p: int, power to raise z to (default is 2)
    
    Returns:
        complex: next iteration of f(z) = z**p + c
    """
    ...
