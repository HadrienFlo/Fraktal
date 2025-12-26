# Cython Integration: Build Instructions

## Prerequisites

### Windows Users: Install Microsoft C++ Build Tools

**Required for compiling Cython extensions on Windows**

1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run the installer
3. Select "Desktop development with C++"
4. Install (requires ~6GB disk space)

**Alternative:** If you have Visual Studio installed, ensure "C++ build tools" is included.

## Quick Start

To build the Cython extension for seed.py, run:

```powershell
# 1. Install Cython (if not already installed)
pip install Cython>=0.29.0

# 2. Build the extension
python setup.py build_ext --inplace

# 3. Verify installation
python -c "from fraktal.engines.seed_cy import f_cython; print('Cython import successful!')"
```

## Using Cython vs Numba

By default, the library uses **Numba**. To switch to **Cython**:

```powershell
# Set environment variable
$env:FRAKTAL_USE_CYTHON="true"

# Run your application
python dash_app/app.py
```

To switch back to Numba:
```powershell
$env:FRAKTAL_USE_CYTHON="false"
# or simply remove the variable
Remove-Item Env:FRAKTAL_USE_CYTHON
```

## Verifying Which Implementation is Active

```python
import os
os.environ['FRAKTAL_USE_CYTHON'] = 'true'  # or 'false'

from fraktal.engines import seed
print(f"Using: {seed.f.__name__}")  # Will show 'f_cython' or 'f_numba'
```

## Development Workflow

After modifying `.pyx` files:
```powershell
python setup.py build_ext --inplace
```

After modifying `.py` files with Numba:
- No rebuild needed - changes take effect immediately

## Troubleshooting

### "Microsoft Visual C++ 14.0 or greater is required"
Install Microsoft C++ Build Tools from:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Import error for seed_cy
Make sure you've run the build command:
```powershell
python setup.py build_ext --inplace
```

### Cython not being used despite setting environment variable
Check that:
1. The build was successful
2. The `.pyd` file exists in `fraktal/engines/`
3. The environment variable is set in the same session
