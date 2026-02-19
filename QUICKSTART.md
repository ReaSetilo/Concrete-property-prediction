# QUICK START GUIDE

## 🚀 Getting Started in 3 Steps

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the Models
1. Open `concrete_ml_analysis.ipynb` in Google Colab or Jupyter Notebook
2. Upload `REVISED_DATASET.xlsx` to the Files panel (in Colab's left sidebar)
3. Click `Runtime → Run all` (or `Cell → Run All` in Jupyter)
4. Wait for training to complete (~10-30 minutes depending on your system)
5. Download the `trained_models` folder that gets created
6. Place the `trained_models` folder in the same directory as the other project files

### Step 3: Run the GUI
**Windows:**
- Double-click `run_gui.bat`
OR
- Open Command Prompt and run: `python run_gui.py`

**Linux/macOS:**
- Open Terminal and run: `./run_gui.sh`
OR
- Run: `python3 run_gui.py`

---

## 📋 What Each File Does

| File | Purpose |
|------|---------|
| `concrete_ml_analysis.ipynb` | Main notebook for data analysis and model training |
| `REVISED_DATASET.xlsx` | Input dataset with 7 ash types |
| `concrete_predictor_gui.py` | GUI application code |
| `run_gui.py` | Launcher script with checks |
| `run_gui.bat` | Windows launcher |
| `run_gui.sh` | Linux/Mac launcher |
| `requirements.txt` | Python package dependencies |
| `README.md` | Comprehensive documentation |

---

## ⚠️ Troubleshooting

### "No module named 'xyz'" error
```bash
pip install -r requirements.txt
```

### "tkinter not found" error
**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install python3-tk
```

**Linux (Fedora):**
```bash
sudo dnf install python3-tkinter
```

**macOS/Windows:** tkinter comes pre-installed with Python

### "Failed to load models" error
- Make sure you've completed Step 2 (Train the Models)
- Verify `trained_models` folder exists in the same directory
- Check that `trained_models/model_registry.pkl` exists

### Notebook fails to run
- Ensure `REVISED_DATASET.xlsx` is uploaded in Colab
- Run cells from top to bottom sequentially
- Check you have enough RAM (4GB minimum)

---

## 💡 Tips

1. **First time?** Use "Load Example" button in the GUI to see sample values
2. **Hover over ℹ icons** in the GUI for parameter descriptions
3. **Check the notebook output** to see model performance metrics
4. **Each ash type** has separate optimized models
5. **Validation R² score** is used to select the best model

---

## 📊 What the System Does

1. **Loads** 7 different ash type datasets
2. **Cleans** data (removes outliers, handles missing values)
3. **Analyzes** with comprehensive EDA (visualizations, correlations)
4. **Trains** 10 ML models per target variable per ash type
5. **Selects** best model based on validation performance
6. **Predicts** Cost, Slump, Compressive Strength, and CO₂ Emissions

---

## ✅ System Requirements

- Python 3.8 or higher
- 4 GB RAM (8 GB recommended)
- 500 MB disk space
- Internet connection (for initial package installation)

---

## 🎯 Expected Results

After training, you'll have:
- ✓ Best models for each ash type and target variable
- ✓ Performance metrics (R², RMSE, MAE)
- ✓ Feature importance visualizations
- ✓ Working GUI for making predictions

---

## 📞 Need Help?

1. Check the main **README.md** for detailed documentation
2. Review the **Troubleshooting** section above
3. Verify all files are in the correct locations
4. Ensure Python version is 3.8 or higher: `python --version`

---

**Ready to start? Follow Step 1 above! 🚀**
