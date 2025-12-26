# Fraktal Dash App User Guide

## Overview

The Fraktal Dash app provides an interactive interface for generating and exploring Mandelbrot fractals with real-time parameter adjustment and performance comparison between Numba and Cython implementations.

## Features

### 1. Interactive Fractal Generation

Generate custom Mandelbrot fractals by adjusting:
- **Center X/Y**: Navigate around the complex plane
- **Zoom**: Zoom in/out to explore fractal details
- **Width/Height**: Set image resolution (in pixels)
- **Max Iterations**: Control fractal detail level (higher = more detail, slower render)

### 2. Visual Customization

Choose from different rendering algorithms:
- **Coloring Function**: How iteration counts are converted to colors
  - `iteration-count`: Simple iteration-based coloring
  - `continuous-iteration-count`: Smooth interpolation
  - `smooth-iteration-count`: Advanced smooth coloring (recommended)
  
- **Color Index Function**: How continuous values map to palette indices
  - `simple-index`: Direct mapping
  
- **Palette Function**: Color scheme
  - `simple-palette`: Rainbow gradient
  - `hot-palette`: Hot (red-yellow) gradient
  - `cool-palette`: Cool (blue-cyan) gradient

### 3. Performance Comparison: Numba vs Cython

**Toggle Switch**: "Use Cython (instead of Numba)"

This unique feature allows you to compare two high-performance computing approaches:

#### Numba (JIT Compilation) - Default
- ✓ No build step required
- ✓ Pure Python syntax
- ✓ Works immediately after `pip install`
- ⚠ First-call compilation overhead
- ⚠ Limited static optimization

#### Cython (AOT Compilation) - Optional
- ✓ Ahead-of-time compilation
- ✓ C-level performance
- ✓ Static type optimizations
- ⚠ Requires building extensions (`python setup.py build_ext --inplace`)
- ⚠ Platform-specific binaries
- ⚠ Requires C++ compiler on Windows

### How to Use the Toggle

1. **Without Cython** (default):
   - Just run `python -m dash_app.app`
   - Toggle will be OFF, using Numba
   
2. **With Cython** (for comparison):
   - Build extensions: `python setup.py build_ext --inplace`
   - Run app: `python -m dash_app.app`
   - Toggle ON to use Cython
   - Toggle OFF to use Numba
   - Compare render times!

### 4. Tab Management

- **Add Tab**: Create new fractals with different parameters
- **Multiple Tabs**: Keep multiple fractals open simultaneously
- **Close Tab**: Remove tabs you don't need
- **Persistent Storage**: Tab data saved to `dash_app/tabs/` folder

## Quick Start

### Basic Workflow

1. Start the app:
   ```powershell
   python -m dash_app.app
   ```

2. Adjust parameters in the left panel:
   - Set a custom tab name
   - Choose center coordinates and zoom
   - Select resolution (start with 400x300 for quick tests)
   - Pick max iterations (256 is good for testing)

3. Click "Add Tab" to generate the fractal

4. View the rendered image in the new tab

5. (Optional) Toggle "Use Cython" and regenerate to compare performance

### Example: Zooming into the Mandelbrot Set

**Famous Location 1 - Seahorse Valley**:
- Center X: `-0.75`
- Center Y: `0.1`
- Zoom: `50`
- Max Iter: `512`

**Famous Location 2 - Elephant Valley**:
- Center X: `0.3`
- Center Y: `0.0`
- Zoom: `20`
- Max Iter: `256`

**Famous Location 3 - Spiral**:
- Center X: `-0.7269`
- Center Y: `0.1889`
- Zoom: `1000`
- Max Iter: `1024`

## Performance Tips

### For Fast Iteration
- Use smaller resolutions (200x150 or 400x300)
- Lower max iterations (128 or 256)
- Use `iteration-count` coloring (faster than smooth)

### For High Quality
- Use larger resolutions (1920x1080 or higher)
- Higher max iterations (512, 1024, or more)
- Use `smooth-iteration-count` coloring
- Enable Cython for faster rendering

### Benchmarking Numba vs Cython

Create identical fractals with both implementations:

1. Set parameters (e.g., 800x600, max_iter=512)
2. Toggle OFF → Click "Add Tab" → Note render time
3. Toggle ON → Click "Add Tab" → Note render time
4. Compare!

**Expected Results** (will vary by hardware):
- Cython is typically faster for large images
- Numba may have first-call compilation overhead
- Both benefit from parallel processing

## Troubleshooting

### "Cython extension not built" or toggle doesn't work
- Make sure you've run `python setup.py build_ext --inplace`
- On Windows, ensure Visual C++ Build Tools are installed
- See [docs/cython-build-instructions.md](cython-build-instructions.md)

### Fractal renders slowly
- Reduce image size (width/height)
- Lower max iterations
- For very deep zooms (zoom > 1000), expect slower renders

### Colors look wrong
- Try different coloring functions
- Check that max_iter is high enough (low values = fewer colors)
- Experiment with different palette functions

## Technical Details

### Storage Location
Generated fractals are stored in: `dash_app/tabs/<tab-id>/`
- Each tab has a JSON file with parameters
- Tab folders are cleaned up when tabs are closed

### Default Configuration
See `config/default.yaml` for default values:
```yaml
mandelbrot:
  tab_name: "Untitled"
  center_x: -0.5
  center_y: 0.0
  zoom: 1.0
  width: 800
  height: 600
  max_iter: 256
  coloring_function: "smooth-iteration-count"
  color_index_function: "simple-index"
  palette_function: "simple-palette"
  use_cython: false
```

### Implementation Files
- Form UI: `dash_app/components/tab_components/mandelbrot_form.py`
- Fractal generation: `dash_app/components/tab_components/generate_tab_content.py`
- Tab management: `dash_app/components/tab_components/add_tab_to_store.py`

## References

- [Mandelbrot Set - Wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set)
- [Numba Documentation](https://numba.pydata.org/)
- [Cython Documentation](https://cython.readthedocs.io/)
- [Dash Documentation](https://dash.plotly.com/)
- [Dash Mantine Components](https://www.dash-mantine-components.com/)
