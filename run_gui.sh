#!/bin/bash

# Concrete Predictor GUI Launcher for Linux/macOS

echo "============================================================"
echo "          Concrete Mixture Prediction System"
echo "============================================================"
echo ""

echo "Launching GUI application..."
echo ""

python3 run_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "============================================================"
    echo "ERROR: Failed to launch the application"
    echo "============================================================"
    echo ""
    echo "Please ensure:"
    echo "  1. Python 3.8 or higher is installed"
    echo "  2. Requirements are installed: pip3 install -r requirements.txt"
    echo "  3. Trained models exist in 'trained_models' folder"
    echo ""
    echo "For tkinter issues on Linux:"
    echo "  Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "  Fedora: sudo dnf install python3-tkinter"
    echo ""
    read -p "Press Enter to exit..."
fi
