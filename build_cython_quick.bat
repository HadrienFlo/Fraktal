@echo off
REM Quick build script - checks prerequisites and builds

echo.
echo ========================================
echo Cython Optimized Build Script
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found in PATH
    echo Please install Python or activate your virtual environment
    pause
    exit /b 1
)

REM Check if Cython is installed
python -c "import Cython" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing Cython...
    pip install cython
)

REM Check if NumPy is installed
python -c "import numpy" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing NumPy...
    pip install numpy
)

REM Build the extension
echo.
echo Building optimized Cython extension...
echo.
python setup_cython.py build_ext --inplace

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo BUILD SUCCESS!
    echo ========================================
    echo.
    echo Next steps:
    echo   1. Restart the Dash app: python -m dash_app.app
    echo   2. Go to http://localhost:8050/explorer
    echo   3. Toggle "Use Cython (faster)" checkbox
    echo   4. Watch terminal for timing: CYTHON-OPT vs NUMBA
    echo.
    echo Expected performance:
    echo   - Old Cython: ~200ms per tile
    echo   - Optimized:  ~8-15ms per tile  (20-50x faster!)
    echo   - Numba:      ~10-20ms per tile
    echo.
    
    if exist "fraktal\engines\mandelbrot_cy_optimized.html" (
        echo Annotation file created: fraktal\engines\mandelbrot_cy_optimized.html
        echo   ^(Open in browser to see which code is pure C^)
        echo.
    )
) else (
    echo.
    echo ========================================
    echo BUILD FAILED
    echo ========================================
    echo.
    echo Common issues:
    echo   1. Missing Visual C++ Build Tools
    echo      Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo.
    echo   2. Wrong Python environment
    echo      Make sure you activated the correct venv
    echo.
    echo   3. Missing dependencies
    echo      Run: pip install cython numpy
    echo.
    echo See docs\building-cython.md for detailed instructions
    echo.
)

pause
