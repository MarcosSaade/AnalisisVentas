# Sales Pattern Analysis

A comprehensive analysis of retail sales patterns to identify trends, seasonality, and demand forecasting opportunities. This project was developed as part of the **Multivariate Analysis for Data Science (MA2003B)** course.

## Project Overview

This project analyzes sales data from an Argentine retail business to:

- Detect trends and seasonality by region, category, and time period
- Segment products and zones using clustering techniques
- Build predictive models for weekly demand forecasting
- Provide actionable business insights for inventory and sales planning

## Dataset

The data used in this project comes from Kaggle:
[Datasets para Proyecto BI](https://www.kaggle.com/datasets/dataregina/datasets-para-proyecto-bi)

The dataset includes:
- `ventas.csv`: Individual sales transactions
- `productos.csv`: Product catalog with prices
- `categorias.csv`: Product categories
- `clientes.csv`: Customer information and regions
- `metodos_pago.csv`: Payment methods

## Repository Structure

```
AnalisisVentas/
|-- data_raw/              # Original datasets
|-- data_clean/            # Processed and cleaned data
|   |-- ventas_clean.csv
|   |-- data_fe.csv
|   |-- data_fe_clusters.csv
|   |-- data_modelado.csv
|   |-- data_con_predicciones.csv
|
|-- notebooks/             # Analysis notebooks
|   |-- EDA.ipynb                    # Exploratory Data Analysis
|   |-- clustering.ipynb             # K-Means clustering
|   |-- modelado-predictivo.ipynb    # Predictive modeling (LightGBM)
|   |-- best_lgbm_params.json        # Optimized hyperparameters
|
|-- src/                   # Source code
|   |-- feature_engineering.py       # Feature engineering pipeline
|
|-- reports/               # Documentation and reports
|   |-- reporte.tex                  # LaTeX technical report
|   |-- bitacora_desiciones.md       # Decision log
|   |-- images/                      # Generated figures
|
|-- README.md
```

## Methodology

### 1. Data Cleaning and Preparation
- Removed duplicates and outliers using IQR method
- Integrated auxiliary tables (products, categories, regions, payment methods)
- Standardized formats and handled missing values

### 2. Feature Engineering
- Created temporal features (week, month, day of week)
- Built lag variables and rolling statistics (mean, std) for multiple time windows
- Generated interaction features and ratio variables

### 3. Exploratory Data Analysis
- Analyzed sales distribution by category and region
- Identified temporal patterns and cyclicity using moving averages
- Examined payment method preferences across segments

### 4. Clustering
- Applied K-Means clustering to identify demand patterns
- Selected optimal number of clusters (k=6) using Elbow method and Silhouette Score
- Visualized clusters using PCA dimensionality reduction

### 5. Predictive Modeling
- **LightGBM**: For regions with sufficient data volume (Buenos Aires, Centro, Cuyo, Patagonia)
- **Moving Average**: For regions with lower data volume (NEA, NOA)
- Hyperparameter optimization using Optuna with TimeSeriesSplit cross-validation
- Evaluation metrics: RMSE, MAE

## Key Findings

- Sales exhibit cyclical patterns with peaks every 2-8 weeks
- Cuyo region has the highest average spend per customer, Patagonia the lowest (10% difference)
- Mercado Pago dominates as the preferred payment method across all regions
- Category "Carniceria" leads in revenue while "Frutas y Verduras" leads in volume

## Requirements

- Python 3.8+
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- lightgbm
- optuna

## Usage

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run notebooks in order:
   - `EDA.ipynb`
   - `clustering.ipynb`
   - `modelado-predictivo.ipynb`

## Reproducibility

- Random seeds are fixed (`seed=42`) across all components
- Optimized hyperparameters are saved in `best_lgbm_params.json`
- Feature engineering pipeline is modular and reusable

## Limitations

- Dataset covers only one year, limiting seasonal pattern validation
- Inventory and sales force optimization requires additional data (costs, volumes, lead times)
- Price elasticity analysis not possible due to fixed prices in the dataset
