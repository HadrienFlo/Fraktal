@echo off
REM Build optimized Cython extensions for Fraktal

echo Building optimized Cython extensions...
python setup_cython.py build_ext --inplace

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================
    echo Build completed successfully!
    echo ===================================
    echo.
    echo Optimized module: fraktal.engines.mandelbrot_cy_optimized
    echo HTML annotation: fraktal/engines/mandelbrot_cy_optimized.html
    echo.
    echo To test performance, restart the Dash app and toggle "Use Cython (faster)"
) else (
    echo.
    echo ===================================
    echo Build FAILED!
    echo ===================================
    echo.
    echo Make sure you have:
    echo   - Microsoft Visual C++ Build Tools installed
    echo   - Cython installed: pip install cython
    echo   - NumPy installed: pip install numpy
)

pause
