#!/usr/bin/env python3
"""
Launcher script for Concrete Predictor GUI
"""

import sys
import os

def check_requirements():
    """Check if required packages are installed"""
    required_packages = {
        'numpy': 'numpy',
        'pandas': 'pandas',
        'sklearn': 'scikit-learn',
        'joblib': 'joblib',
        'tkinter': 'tkinter (built-in with Python)'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("ERROR: Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\nPlease install missing packages using:")
        print("  pip install -r requirements.txt")
        return False
    
    return True

def check_models():
    """Check if trained models exist"""
    if not os.path.exists('trained_models'):
        print("\nWARNING: 'trained_models' folder not found!")
        print("\nPlease follow these steps:")
        print("1. Open concrete_ml_analysis.ipynb in Google Colab or Jupyter")
        print("2. Upload REVISED_DATASET.xlsx to the Files panel")
        print("3. Run all cells to train the models")
        print("4. Download the 'trained_models' folder")
        print("5. Place it in the same directory as this script")
        return False
    
    if not os.path.exists('trained_models/model_registry.pkl'):
        print("\nERROR: Model registry file not found!")
        print("Please ensure you have completed the training process.")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("="*60)
    print("Concrete Mixture Prediction System".center(60))
    print("="*60)
    print()
    
    # Check requirements
    print("Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    print("✓ All required packages installed")
    
    # Check models
    print("\nChecking trained models...")
    if not check_models():
        sys.exit(1)
    print("✓ Trained models found")
    
    print("\nLaunching GUI...")
    print("-"*60)
    
    # Import and run GUI
    try:
        from concrete_predictor_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"\nERROR: Failed to launch GUI")
        print(f"Error message: {str(e)}")
        print("\nPlease check:")
        print("1. All files are in the correct location")
        print("2. Requirements are properly installed")
        print("3. Trained models exist in 'trained_models' folder")
        sys.exit(1)

if __name__ == "__main__":
    main()
