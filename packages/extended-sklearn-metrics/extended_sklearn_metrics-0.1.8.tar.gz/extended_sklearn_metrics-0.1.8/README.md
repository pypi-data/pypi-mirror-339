# extended-sklearn-metrics

A Python library for evaluating scikit-learn regression models with comprehensive metrics and interpretable results.

## Features

- Cross-validation based model evaluation
- Automatic calculation of RMSE, MAE, R², and Explained Variance
- Error percentage calculations relative to target variable range
- Performance classification (Excellent, Good, Moderate, Poor)
- Easy-to-read summary tables

## Installation

### From PyPI

```bash
pip install extended-sklearn-metrics
```

### From Source

1. Clone this repository:
```bash
git clone https://github.com/SubaashNair/extended-sklearn-metrics.git
cd extended-sklearn-metrics
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Here's a simple example using the California Housing dataset:

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from extended_sklearn_metrics import evaluate_model_with_cross_validation

# Load and prepare data
housing = fetch_california_housing(as_frame=True)
X_train, X_test, y_train, y_test = train_test_split(
    housing.data, housing.target, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# Create and evaluate model
model = LinearRegression()
target_range = y_train.max() - y_train.min()

# Get performance metrics
performance_table = evaluate_model_with_cross_validation(
    model=model,
    X=X_train_scaled,
    y=y_train,
    cv=5,
    target_range=target_range
)

print(performance_table)
```

## Output Format

The library generates a DataFrame with the following columns:

| Column | Description |
|--------|-------------|
| Metric | Name of the metric (RMSE, MAE, R², etc.) |
| Value | Computed value of the metric |
| Threshold | Thresholds used for performance classification |
| Calculation | Formula/method used to compute the metric |
| Performance | Classification (Excellent, Good, Moderate, Poor) |

## Performance Thresholds

### RMSE and MAE
- < 10% of range: Excellent
- 10%–20% of range: Good
- 20%–30% of range: Moderate
- > 30% of range: Poor

### R² and Explained Variance
- > 0.7: Good
- 0.5–0.7: Acceptable
- < 0.5: Poor

## Requirements

- Python 3.9+
- pandas >= 2.0.0
- scikit-learn >= 1.0.0
- numpy >= 1.20.0

## License

This project is licensed under the MIT License - see the LICENSE file for details. 