"""Type stub for orbit_cy module to provide IDE support."""

import numpy as np

def truncated_orbit_cython(z: complex, c: complex, max_iterations: int, bailout: float = 2.0, p: int = 2) -> tuple[np.ndarray, int]:
    """Cython-optimized truncated orbit calculation.
    
    Args:
        z: complex, initial value
        c: complex, constant value
        max_iterations: int, maximum iterations
        bailout: float, escape threshold
        p: int, power parameter
    
    Returns:
        tuple: (orbit array, escape_time)
    """
    ...
