# fraktal/mapping.py
"""Mapping of coloring, color index, and palette functions for fractal rendering.
This module provides a centralized dictionary to access various models used in fractal computations.
"""
from fraktal.models.iteration_count import (
    iteration_count,
    continuous_iteration_count,
    smooth_iteration_count,
)
from fraktal.engines.color_index import simple_index
from fraktal.engines.palette import simple_palette, hot_palette, cool_palette

FRAKTAL_MODELS = {
    "coloring": {
        "iteration-count": {
            "function": iteration_count,
            "name": "Iteration Count",
        },
        "continuous-iteration-count": {
            "function": continuous_iteration_count,
            "name": "Continuous Iteration Count",
        },
        "smooth-iteration-count": {
            "function": smooth_iteration_count,
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