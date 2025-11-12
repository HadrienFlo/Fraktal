"""Paired with Coloring functions, defined in coloring.py, palette functions are defined here.
Given a coloring function u, a color index function I(u) maps the value u of the coloring function to a color index.
The color palette function P(I) is then used to map the color index I to an actual color in the RGB color space, where each color is represented as a triplet of integers (r, g, b) in [0, 1]^3.
More formally:
P: R -> [0, 1]^3 maps a color index I to the RGB color space. Its domain is [0, 1] and range [0, 1]^3. The domain can be extended to the real line by using the decimal part of the color index.
"""