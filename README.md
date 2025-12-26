# Fraktal

High-performance Python library + Dash app for exploring and generating beautiful fractal images, with a focus on the Mandelbrot set. The home page is dedicated to give more explanations around the mathematical approach of fractal coloring techniques.

## Features

### 🗺️ **Interactive Explorer**
- **Leaflet-based tile system** for smooth pan and zoom navigation
- **Auto-adjusting iterations** - Automatically increases detail as you zoom in (100 × 1.3^zoom)
- **Real-time rendering** with intelligent tile caching
- **Multiple coloring methods**:
  - Smooth (recommended) - Eliminates banding artifacts using logarithmic smoothing
  - Continuous - Distance-based coloring for smooth gradients
  - Basic Iteration - Classic discrete coloring
- **Color palettes**: Hot, Cool, Simple
- **Performance metrics** - Live iteration count display and cache monitoring

### 🎨 **Image Generator**
- Generate high-resolution fractal images
- Customizable parameters (coordinates, zoom, iterations)
- Multiple coloring algorithms and palettes
- Export to PNG format

### 📊 **Analysis Tools**
- Orbit visualization - See the iteration path for any point
- Interactive parameter exploration
- Numba vs Cython performance comparison

## Setup (Windows / PowerShell)

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Build Cython extensions for better performance:

```powershell
python setup.py build_ext --inplace
```

**Note:** Requires Microsoft Visual C++ Build Tools 14.0 or greater. See [docs/cython-build-instructions.md](docs/cython-build-instructions.md) for details.

4. Run tests:

```powershell
pytest -q
```

4. Run the Dash app:

```powershell
python -m dash_app.app
```

Then open your browser to http://127.0.0.1:8050

### Using the Explorer

Navigate to the **Explorer** page (/explorer) for interactive fractal exploration:

- **Pan**: Click and drag the map
- **Zoom**: Use mouse wheel or zoom controls  
- **Auto-adjust iterations**: Toggle on for automatic detail optimization based on zoom level
- **Change coloring**: Try different methods (Smooth/Continuous/Basic) and palettes
- **Performance**: Monitor iteration count and tile cache in real-time

**Pro tip**: Zoom into the boundary of the Mandelbrot set to see incredible fractal detail!

## GitHub sync

Initialize git, create a repo on GitHub and push:

```powershell
git init
git add .
git commit -m "Initial scaffold"
# create a repo on GitHub and then:
git remote add origin https://github.com/<your-username>/fraktal.git
git push -u origin main
```

Alternatively, use GitHub Desktop to create and push the repository.

## What is included

- `fraktal/` : Core computation library with Numba-optimized rendering
  - `engines/` : High-performance fractal generators (Numba + optional Cython)
  - `models/` : Coloring algorithms (smooth, continuous, basic iteration count)
- `dash_app/` : Dash web application
  - `pages/explorer.py` : **Interactive Leaflet-based explorer with tile rendering**
  - `pages/mandelbrot.py` : Image generator
  - `pages/orbit.py` : Orbit visualization
  - `components/` : Reusable UI components
- `config/default.yaml` : Default YAML configuration
- `tests/` : pytest tests and Jupyter notebooks
- `docs/` : Comprehensive documentation
  - `features/` : Feature documentation
  - `maths/` : Mathematical explanations
  - `cython-experiments/` : Performance analysis (Numba vs Cython)
- `requirements.txt`, `pyproject.toml`, `.gitignore`, `README.md`
- `setup_cython.py` : Optional Cython build configuration

## Performance: Numba vs Cython

**Numba wins by 100-500x** for numerical Python code:

- **Numba**: ~0.01-0.02s per 256×256 tile (JIT compilation, LLVM optimization)
- **Cython** (experimental): ~1.4-6.0s per tile (AOT compilation, limited cross-module optimization)

**Why Numba wins:**
- JIT compilation sees the entire call graph for aggressive inlining
- LLVM backend provides superior numerical optimization  
- Runtime type specialization
- No build step required

The Dash app includes a "Use Cython" toggle to compare implementations. Numba is **strongly recommended** for this use case.

**📖 For detailed analysis, see [docs/cython-experiments/cython-vs-numba-conclusion.md](docs/cython-experiments/cython-vs-numba-conclusion.md)**

## Coloring Methods

### Smooth Iteration Count (Recommended)
Uses logarithmic smoothing to eliminate color banding:
```
μ = N + 1 - log(log(r_N) / log(bailout)) / log(p)
```
Perfect for high-quality renders with smooth gradients.

### Continuous Iteration Count
Distance-based coloring using the escaped orbit value:
```
μ = N + 1 - (|z_N|^p - bailout^p) / (|z_N|^p - bailout)
```
Good balance between smoothness and computational efficiency.

### Basic Iteration Count
Simple discrete iteration counting - classic fractal look with visible bands.

## Documentation

- **[Leaflet Explorer Features](docs/features/)** - Interactive tile-based explorer
- **[Dash App User Guide](docs/dash-app-user-guide.md)** - Complete guide to using the fractal generator
- **[Cython vs Numba Analysis](docs/cython-experiments/)** - Performance comparison and technical details
- **[Mathematics Documentation](docs/maths/)** - Fractal theory and algorithms
- **[Cython Build Instructions](docs/cython-build-instructions.md)** - Platform-specific build setup (optional)

## Next steps (suggested)

- Add more fractal types (Julia sets, Burning Ship, Newton fractals)
- Implement GPU acceleration with Numba CUDA
- Add animation/video export capabilities
- Bookmark favorite locations
- Share fractal coordinates via URL parameters
- Add GitHub Actions workflow for CI (run tests and linting)
