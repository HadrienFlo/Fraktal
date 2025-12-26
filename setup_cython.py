"""
Build script for optimized Cython extensions.

Usage:
    python setup_cython.py build_ext --inplace
"""
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import sys

# Compiler-specific flags
if sys.platform == 'win32':
    # MSVC flags for Windows
    extra_compile_args = [
        '/O2',           # Optimize for speed
        '/fp:fast',      # Fast floating-point model
        '/GL',           # Whole program optimization
        '/Ot',           # Favor speed over size
        # '/openmp',     # Disabled for testing - adds overhead for small arrays
        '/favor:AMD64',  # Optimize for x64
    ]
    extra_link_args = [
        '/LTCG',         # Link-time code generation
    ]
    
    # Try to enable AVX2 if supported
    try:
        extra_compile_args.append('/arch:AVX2')
    except:
        print("Warning: AVX2 not supported, using default architecture")
else:
    # GCC/Clang flags for Linux/Mac
    extra_compile_args = [
        '-O3',
        '-ffast-math',
        '-march=native',
        '-fopenmp',
    ]
    extra_link_args = ['-fopenmp']

extensions = [
    Extension(
        name="fraktal.engines.mandelbrot_cy_optimized",
        sources=["fraktal/engines/mandelbrot_cy_optimized.pyx"],
        include_dirs=[np.get_include()],
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        define_macros=[
            ("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION"),
        ],
    ),
]

setup(
    name="fraktal-cython-optimized",
    ext_modules=cythonize(
        extensions,
        compiler_directives={
            'language_level': '3',
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'initializedcheck': False,
            'nonecheck': False,
            'embedsignature': True,
        },
        annotate=True,  # Generates HTML report showing C interaction
    ),
)
