# Fraktal

Small Python library + Dash app scaffold for Fraktal project.

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

- `fraktal/` : library package with `config` loader and `decorators`.
  - Dual Numba/Cython implementation for performance-critical functions
  - Toggle between JIT (Numba) and AOT (Cython) compilation
- `dash_app/` : Dash app skeleton using `dash-mantine-components`.
  - Interactive Mandelbrot fractal generator with real-time rendering
  - **Cython/Numba toggle switch** to compare performance
- `config/default.yaml` : default YAML configuration loaded by `fraktal`.
- `tests/` : pytest tests for the basic components.
- `requirements.txt`, `pyproject.toml`, `.gitignore`, `README.md`.
- `setup.py` : Cython extension build configuration.

## Performance: Numba vs Cython

The Dash app includes a toggle switch to compare Numba (JIT compilation) vs Cython (ahead-of-time compilation) performance:

- **Numba (default)**: Just-In-Time compilation, no build step required
- **Cython**: Ahead-of-time compilation, requires building extensions (see step 3)

Toggle the "Use Cython" switch in the Mandelbrot form to switch implementations and compare rendering times.

**📖 For detailed usage instructions, see [docs/dash-app-user-guide.md](docs/dash-app-user-guide.md)**

## Documentation

- **[Dash App User Guide](docs/dash-app-user-guide.md)** - Complete guide to using the fractal generator
- **[Cython Integration Guide](docs/cython-integration-guide.md)** - Technical details on Numba/Cython implementation
- **[Cython Build Instructions](docs/cython-build-instructions.md)** - Platform-specific build setup

## Next steps (suggested)

- Benchmark and compare Numba vs Cython performance for different image sizes
- Implement additional fractal types (Julia sets, Burning Ship, etc.)
- Improve logging configuration (structured logs, file handlers).
- Add GitHub Actions workflow for CI (run tests and linting).
