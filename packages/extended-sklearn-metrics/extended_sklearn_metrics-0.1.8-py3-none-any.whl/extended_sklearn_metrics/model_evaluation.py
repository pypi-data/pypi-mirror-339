import numpy as np
import pandas as pd
from sklearn.model_selection import cross_validate
from typing import Union, Dict, Any

def evaluate_model_with_cross_validation(
    model: Any,
    X: Union[pd.DataFrame, np.ndarray],
    y: Union[pd.Series, np.ndarray],
    cv: int = 5,
    target_range: float = None
) -> pd.DataFrame:
    """
    Evaluates a regression model using cross-validation and generates a performance summary table.
    
    Parameters
    ----------
    model : estimator object
        The machine learning model to evaluate (must implement fit and predict).
    X : array-like of shape (n_samples, n_features)
        Training data.
    y : array-like of shape (n_samples,)
        Target values.
    cv : int, default=5
        Number of cross-validation folds.
    target_range : float, optional
        The range of the target variable (max(y) - min(y)). Required for RMSE and MAE percentage calculations.
        
    Returns
    -------
    pd.DataFrame
        A summary table containing performance metrics and their interpretations.
    """
    if target_range is None:
        target_range = np.max(y) - np.min(y)
        
    # Define scoring metrics
    scoring = {
        'neg_root_mean_squared_error': 'neg_root_mean_squared_error',
        'neg_mean_absolute_error': 'neg_mean_absolute_error',
        'r2': 'r2',
        'explained_variance': 'explained_variance'
    }
    
    # Perform cross-validation
    cv_results = cross_validate(
        model, X, y,
        cv=cv,
        scoring=scoring,
        return_train_score=False
    )
    
    # Calculate mean scores
    rmse = -np.mean(cv_results['test_neg_root_mean_squared_error'])
    mae = -np.mean(cv_results['test_neg_mean_absolute_error'])
    r2 = np.mean(cv_results['test_r2'])
    exp_var = np.mean(cv_results['test_explained_variance'])
    
    # Calculate error percentages
    rmse_percentage = (rmse / target_range) * 100
    mae_percentage = (mae / target_range) * 100
    
    # Define performance categories
    def get_error_performance(error_percentage: float) -> str:
        if error_percentage < 10:
            return "Excellent"
        elif error_percentage < 20:
            return "Good"
        elif error_percentage < 30:
            return "Moderate"
        else:
            return "Poor"
            
    def get_score_performance(score: float) -> str:
        if score > 0.7:
            return "Good"
        elif score > 0.5:
            return "Acceptable"
        else:
            return "Poor"
    
    # Create results DataFrame
    results = pd.DataFrame({
        'Metric': ['RMSE', 'MAE', 'R²', 'Explained Variance'],
        'Value': [rmse, mae, r2, exp_var],
        'Threshold': [
            '< 10%–20% of range',
            '< 10%–20% of range',
            '> 0.7 = Good, 0.5–0.7 = Acceptable, < 0.5 = Poor',
            '> 0.7 = Good, 0.5–0.7 = Acceptable, < 0.5 = Poor'
        ],
        'Calculation': [
            f'{rmse:.4f} / {target_range:.2f} * 100 ≈ {rmse_percentage:.2f}%',
            f'{mae:.4f} / {target_range:.2f} * 100 ≈ {mae_percentage:.2f}%',
            'N/A (unitless)',
            'N/A (unitless)'
        ],
        'Performance': [
            get_error_performance(rmse_percentage),
            get_error_performance(mae_percentage),
            get_score_performance(r2),
            get_score_performance(exp_var)
        ]
    })
    
    return results 