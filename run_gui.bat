@echo off
REM Concrete Predictor GUI Launcher for Windows

echo ============================================================
echo          Concrete Mixture Prediction System
echo ============================================================
echo.

echo Launching GUI application...
echo.

python run_gui.py

if errorlevel 1 (
    echo.
    echo ============================================================
    echo ERROR: Failed to launch the application
    echo ============================================================
    echo.
    echo Please ensure:
    echo   1. Python 3.8 or higher is installed
    echo   2. Requirements are installed: pip install -r requirements.txt
    echo   3. Trained models exist in 'trained_models' folder
    echo.
    pause
)
