@echo off
setlocal
echo ========================================================
echo   Setting up Python Challenge Environment
echo ========================================================

where poetry >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Found Poetry. Installing dependencies...
    poetry install
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ========================================================
        echo   Setup completed successfully with Poetry!
        echo   - Run app:   poetry run app
        echo   - Run tests: poetry run test
        echo ========================================================
        exit /b 0
    ) else (
        echo [WARNING] poetry install encountered an issue. Falling back to pip...
    )
) else (
    echo [INFO] Poetry not found in PATH. Checking python and pip...
)

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found in PATH. Please install Python 3.10+.
    exit /b 1
)

echo Installing dependencies via pip...
python -m pip install --upgrade pip
python -m pip install "rich>=13.7.0"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo   Setup completed successfully with pip!
    echo   - Run app:   python app.py
    echo   - Run tests: python app.py --test
    echo ========================================================
    exit /b 0
) else (
    echo [ERROR] Dependency installation failed.
    exit /b 1
)
