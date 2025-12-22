# Build Cython Extensions with Visual Studio Build Tools

Write-Host "Searching for Visual Studio Build Tools..." -ForegroundColor Cyan

$vsWherePath = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

if (Test-Path $vsWherePath) {
    Write-Host "Found vswhere.exe, detecting Visual Studio installation..." -ForegroundColor Green
    
    $vsPath = & $vsWherePath -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
    
    if ($vsPath) {
        Write-Host "Visual Studio found at: $vsPath" -ForegroundColor Green
        
        $vcvarsall = Join-Path $vsPath "VC\Auxiliary\Build\vcvarsall.bat"
        
        if (Test-Path $vcvarsall) {
            Write-Host "Setting up Visual Studio environment..." -ForegroundColor Cyan
            
            $tempBat = [System.IO.Path]::GetTempFileName() + ".bat"
            $batchContent = "@echo off`r`ncall `"$vcvarsall`" x64`r`npython setup.py build_ext --inplace"
            $batchContent | Out-File -FilePath $tempBat -Encoding ASCII
            
            Write-Host "Building Cython extension..." -ForegroundColor Cyan
            cmd /c $tempBat
            
            Remove-Item $tempBat -ErrorAction SilentlyContinue
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "`nBuild successful!" -ForegroundColor Green
                Write-Host "`nTo use Cython, set the environment variable:" -ForegroundColor Yellow
                Write-Host '  $env:FRAKTAL_USE_CYTHON="true"' -ForegroundColor White
            } else {
                Write-Host "`nBuild failed. See errors above." -ForegroundColor Red
            }
        } else {
            Write-Host "Could not find vcvarsall.bat" -ForegroundColor Red
        }
    } else {
        Write-Host "Visual Studio Build Tools not found." -ForegroundColor Red
        Write-Host "Install from: https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor Yellow
    }
} else {
    Write-Host "vswhere.exe not found" -ForegroundColor Yellow
    Write-Host "`nPlease try one of the following:" -ForegroundColor Cyan
    Write-Host "1. Restart your computer for PATH changes to take effect" -ForegroundColor White
    Write-Host "2. Open Developer Command Prompt for VS and run:" -ForegroundColor White
    $scriptDir = Get-Location
    Write-Host "   cd $scriptDir" -ForegroundColor Gray
    Write-Host "   .venv\Scripts\Activate.ps1" -ForegroundColor Gray
    Write-Host "   python setup.py build_ext --inplace" -ForegroundColor Gray
}
