# Concrete Mixture Prediction System

## Overview
This project provides a comprehensive machine learning solution for predicting concrete mixture properties when replacing cement with 7 different ash types:
- POFA (Palm Oil Fuel Ash)
- RHA (Rice Husk Ash)
- SCBA (Sugarcane Bagasse Ash)
- GSA (Glass Powder Ash)
- WSA (Wheat Straw Ash)
- BLA (Bamboo Leaf Ash)
- CCA (Corn Cob Ash)

## Predicted Variables
The system predicts four key concrete properties:
1. **Cost** (USD per m³)
2. **Slump** (mm)
3. **Compressive Strength** (MPa)
4. **CO₂ Emissions** (kgCO₂e/kg)


## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Extract the project folder**

2. **Install dependencies**
   ```cmd
   py -m pip install -r requirements.txt
   ```

## Usage

### Part 1: Training Models (Google Colab or Jupyter)

1. **Upload to Google Colab:**
   - Open Google Colab (https://colab.research.google.com)
   - Upload `concrete_ml_analysis.ipynb`
   - Upload `REVISED_DATASET.xlsx` to the Files panel (left sidebar)

2. **Run the notebook:**
   - Click Runtime → Run all
   - The notebook will:
     - Clean and prepare data
     - Perform exploratory data analysis (EDA)
     - Train 10 machine learning models per target variable
     - Generate visualizations
     - Save best models to `trained_models/` folder

3. **Download trained models:**
   - After execution, download the `trained_models` folder
   - Place it in the same directory as `concrete_predictor_gui.py`

### Part 2: Using the GUI

1. **Launch the application:**
   ```cmd
   python concrete_predictor_gui.py
   ```

2. **Make predictions:**
   - Select an ash type by clicking the corresponding button
   - Choose pozzolan type from the dropdown
   - Enter mixture parameters (hover over ℹ for descriptions)
   - Click "Predict" to get results
   - Use "Load Example" for sample values
   - Use "Clear" to reset all fields

## Notebook Sections

The `concrete_ml_analysis.ipynb` notebook includes:

1. **Setup and Imports** - Install and import required libraries
2. **Data Loading** - Load the 7 ash type datasets
3. **Data Exploration** - Initial data inspection before cleaning
4. **Data Cleaning** - Handle missing values, outliers, duplicates
5. **EDA** - Comprehensive exploratory data analysis:
   - Outlier visualizations for each variable by ash type
   - Pearson correlation matrices
   - Frequency distributions
6. **Model Training** - Train 10 models with hyperparameter tuning:
   - Linear Regression
   - Ridge Regression
   - Lasso Regression
   - ElasticNet
   - Decision Tree
   - Random Forest
   - Gradient Boosting
   - XGBoost
   - LightGBM
   - CatBoost
7. **Model Evaluation** - Compare performance metrics (R², RMSE, MAE)
8. **Feature Importance** - Visualize feature weights for best models
9. **Model Export** - Save best models for GUI application

## Input Variables

The system requires the following mixture parameters:

| Parameter | Description | Units |
|-----------|-------------|-------|
| Replacement % | Percentage of cement replaced with ash | % |
| Cement | Cement content | kg/m³ |
| Ash | Ash content | kg/m³ |
| Fine Aggregate | Fine aggregate content | kg/m³ |
| Coarse Aggregate | Coarse aggregate content | kg/m³ |
| Pozzolan Added | Additional pozzolanic material | kg/m³ |
| Superplasticizer | Superplasticizer content | kg/m³ |
| Water | Water content | kg/m³ |
| Curing Days | Number of days for curing | days |

## Data Split

- **Training**: 75%
- **Testing**: 15%
- **Validation**: 10%

## Model Selection

For each ash type and target variable, the system:
1. Trains 10 different ML models
2. Performs hyperparameter tuning using GridSearchCV
3. Evaluates on validation set
4. Selects the best performing model based on R² score
5. Saves the best model for deployment

## Features

## Troubleshooting

### Common Issues

1. **"Failed to load models" error:**
   - Ensure `trained_models/` folder is in the same directory as the GUI script
   - Verify that you've run the notebook and downloaded the models

2. **Import errors:**
   - Run `py -m pip install -r requirements.txt` again
   - Check Python version (3.8+ required)

3. **Notebook cells fail:**
   - Ensure `REVISED_DATASET.xlsx` is uploaded to Colab Files panel
   - Run cells sequentially from top to bottom
   - Check for sufficient Colab runtime resources

4. **GUI doesn't start:**
   - Check if tkinter is installed: `python -m tkinter`
   - On Linux: `sudo apt-get install python3-tk`
   - On Mac: tkinter comes with Python installation

## Output Files

After running the notebook, you'll get:

1. **trained_models/** folder containing:
   - Best model files (.pkl) for each ash type and target variable
   - `model_registry.pkl` - Complete model registry
   - `best_models_summary.csv` - Summary table of all best models

2. **Visualizations** (displayed in notebook):
   - Data entry histograms (before/after cleaning)
   - Outlier box plots and distributions
   - Correlation heatmaps
   - Frequency distributions
   - Model performance comparisons
   - Feature importance plots

## Performance Metrics

The system evaluates models using:
- **R² Score**: Coefficient of determination (closer to 1 is better)
- **RMSE**: Root Mean Squared Error (lower is better)
- **MAE**: Mean Absolute Error (lower is better)

All metrics are calculated for training, testing, and validation sets.

## Technical Details

### Machine Learning Pipeline
1. Data preprocessing with StandardScaler
2. Train-test-validation split (75-15-10)
3. Hyperparameter tuning with cross-validation
4. Model evaluation on unseen data
5. Best model selection based on validation performance

### Models Trained
The system trains the following 10 models for each target variable:
- **Linear Models**: Linear Regression, Ridge, Lasso, ElasticNet
- **Tree-based**: Decision Tree, Random Forest, Gradient Boosting
- **Advanced**: XGBoost, LightGBM, CatBoost

### Feature Engineering
- Standardization of numerical features
- Handling of different pozzolan types
- Separate models for each ash type (no cross-ash prediction)


## Credits

This system was developed for concrete mixture analysis using machine learning.

Dataset contains data for 7 different ash types with measurements for:
- Mixture composition
- Physical properties (slump)
- Mechanical properties (compressive strength)
- Economic metrics (cost)
- Environmental impact (CO₂ emissions)


## Future Enhancements

Potential improvements:
- Cross-ash type predictions
- Additional material properties
- More visualization options in GUI
- Export predictions to CSV/Excel
- Batch prediction mode
- Model retraining interface
- Web-based deployment

---

