from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Define Cython extensions
extensions = [
    Extension(
        "fraktal.engines.seed_cy",
        ["fraktal/engines/seed_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"] if not __import__("sys").platform.startswith("win") else ["/O2"],
    ),
    Extension(
        "fraktal.engines.orbit_cy",
        ["fraktal/engines/orbit_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"] if not __import__("sys").platform.startswith("win") else ["/O2"],
    ),
    Extension(
        "fraktal.engines.mandelbrot_cy",
        ["fraktal/engines/mandelbrot_cy.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=["-O3"] if not __import__("sys").platform.startswith("win") else ["/O2"],
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
