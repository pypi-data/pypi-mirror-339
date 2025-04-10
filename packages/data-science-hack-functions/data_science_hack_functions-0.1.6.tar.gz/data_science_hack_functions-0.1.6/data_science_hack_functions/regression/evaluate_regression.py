import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score, mean_absolute_percentage_error
)
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from scipy import stats
from rich.console import Console
import inspect

console = Console()

def evaluate_regression_model(
    model=None,
    X_train=None, y_train=None,
    X_test=None, y_test=None,
    cv=5,
    validation_params=None,
    scoring_curve='r2',
    verbose=True,
    return_dict=False,
    extra_plots=None,
    custom_metrics=None,
    log_transform=False
):
    """
    Evaluates a regression model with core metrics, residual diagnostics, validation, and learning curves.

    Parameters:
    - model: Regressor model (must implement .fit/.predict)
    - X_train, y_train: Training data
    - X_test, y_test: Test data
    - cv: Number of folds for learning/validation curves
    - validation_params: Dict of hyperparameter ranges for validation curves
    - scoring_curve: Metric used in learning/validation curves
    - verbose: Whether to print/log output
    - return_dict: If True, returns metrics in a dictionary
    - extra_plots: List of extra plots — ['residuals', 'error_dist', 'qq', 'pred_vs_actual', 'feature_importance']
    - custom_metrics: Dict of custom metric functions: {name: func(y_true, y_pred)}
    - log_transform: Evaluate metrics on log1p scale (optional)
    """

    if not all([model is not None, X_train is not None, y_train is not None, X_test is not None, y_test is not None]):
        console.print("[bold red]\nERROR:[/bold red] Missing required inputs.")
        signature = inspect.signature(evaluate_regression_model)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")

        console.print("""
[bold green]\\nFunction: evaluate_regression_model()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Evaluates regression models on test data and visualizes performance through metrics, learning/validation curves,
residual analysis, and diagnostic plots. Supports both built-in and custom metrics for flexible analysis.

[bold green]Required Parameters:[/bold green]
• [bold yellow]model[/bold yellow]: Any sklearn-compatible regressor (must support .fit and .predict).
• [bold yellow]X_train[/bold yellow], [bold yellow]y_train[/bold yellow]: Training data.
• [bold yellow]X_test[/bold yellow], [bold yellow]y_test[/bold yellow]: Test data.

[bold green]Optional Parameters:[/bold green]
• [bold yellow]cv[/bold yellow] (int): Cross-validation folds for learning/validation curves. Default: 5.
• [bold yellow]validation_params[/bold yellow] (dict): Dictionary of hyperparameter ranges for tuning curves.
• [bold yellow]scoring_curve[/bold yellow] (str): Scoring metric for learning/validation curves. Default: 'r2'.
• [bold yellow]log_transform[/bold yellow] (bool): If True, log1p transform is applied to y before metric evaluation.
• [bold yellow]extra_plots[/bold yellow] (list): List of diagnostic plots to display (see below).
• [bold yellow]custom_metrics[/bold yellow] (dict): Dictionary of {metric_name: function(y_true, y_pred)}.
• [bold yellow]verbose[/bold yellow] (bool): Whether to display metrics/plots. Default: True.
• [bold yellow]return_dict[/bold yellow] (bool): Return results in dictionary format for further use.

[bold green]Built-in Metrics Computed:[/bold green]
• R² (Coefficient of determination)
• Adjusted R²
• RMSE (Root Mean Squared Error)
• MAE (Mean Absolute Error)
• MAPE (Mean Absolute Percentage Error)
• RMSLE (Root Mean Squared Log Error) [skipped if y < 0]

[bold green]Supported Diagnostic Plots (via extra_plots):[/bold green]
• [bold cyan]'pred_vs_actual'[/bold cyan] — Scatterplot of predicted vs actual values  
• [bold cyan]'residuals'[/bold cyan] — Residual vs prediction plot  
• [bold cyan]'error_dist'[/bold cyan] — Histogram of prediction errors  
• [bold cyan]'qq'[/bold cyan] — Q-Q plot to check normality of residuals  
• [bold cyan]'feature_importance'[/bold cyan] — Bar chart of model feature importances  
• [bold cyan]'learning'[/bold cyan] — Learning curve showing training vs validation scores  
• [bold cyan]'validation'[/bold cyan] — Hyperparameter validation curve (requires validation_params)

[bold green]Example Usage:[/bold green]
>>> evaluate_regression_model(
        model=my_model,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        validation_params={'alpha': [0.01, 0.1, 1]},
        extra_plots=['residuals', 'qq', 'learning', 'validation'],
        scoring_curve='neg_root_mean_squared_error',
        return_dict=True
    )

[bold magenta]Tip:[/bold magenta] Pass `log_transform=True` if your target variable is skewed or exponential in nature.
""")

        return

    start_time = time.time()
    extra_plots = extra_plots or []
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    if log_transform:
        y_test = np.log1p(y_test)
        y_pred = np.log1p(y_pred)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    try:
        if (y_test < 0).any() or (y_pred < 0).any():
            rmsle = np.nan
            if verbose:
                print("Warning: Negative values detected. Skipping RMSLE computation.")
        else:
            rmsle = np.sqrt(mean_squared_error(np.log1p(y_test), np.log1p(y_pred)))
    except Exception as e:
        rmsle = np.nan
        if verbose:
            print(f"RMSLE computation failed: {e}")

    n, p = X_test.shape
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

    if verbose:
        print("\nTest Set Regression Metrics:")
        print(f"R²           : {r2:.4f}")
        print(f"Adjusted R²  : {adj_r2:.4f}")
        print(f"RMSE         : {rmse:.4f}")
        print(f"MAE          : {mae:.4f}")
        print(f"MAPE         : {mape:.4f}")
        print(f"RMSLE        : {rmsle:.4f}")

    if custom_metrics:
        for name, func in custom_metrics.items():
            val = func(y_test, y_pred)
            if verbose:
                print(f"{name:<12}: {val:.4f}")

    # --- Diagnostic Plots ---
    if 'pred_vs_actual' in extra_plots:
        plt.figure(figsize=(6, 6))
        sns.scatterplot(x=y_test, y=y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.title("Predicted vs Actual")
        plt.tight_layout()
        plt.show()

    if 'residuals' in extra_plots:
        residuals = y_test - y_pred
        plt.figure(figsize=(8, 5))
        sns.scatterplot(x=y_pred, y=residuals)
        plt.axhline(0, color='red', linestyle='--')
        plt.xlabel("Predicted")
        plt.ylabel("Residual")
        plt.title("Residual Plot")
        plt.tight_layout()
        plt.show()

    if 'error_dist' in extra_plots:
        errors = y_test - y_pred
        plt.figure(figsize=(8, 5))
        sns.histplot(errors, kde=True)
        plt.title("Error Distribution")
        plt.xlabel("Prediction Error")
        plt.tight_layout()
        plt.show()

    if 'qq' in extra_plots:
        residuals = y_test - y_pred
        stats.probplot(residuals, dist="norm", plot=plt)
        plt.title("Q-Q Plot of Residuals")
        plt.tight_layout()
        plt.show()

    if hasattr(model, 'feature_importances_') and 'feature_importance' in extra_plots:
        plt.figure(figsize=(8, 5))
        feat_imp = pd.Series(model.feature_importances_, index=X_train.columns)
        feat_imp.sort_values().plot(kind='barh')
        plt.title("Feature Importance")
        plt.tight_layout()
        plt.show()

    if 'learning' in extra_plots:
        train_sizes, train_scores, test_scores = learning_curve(
            model, X_train, y_train,
            train_sizes=np.linspace(0.1, 1.0, 10),
            cv=cv, scoring=scoring_curve
        )
        plt.figure(figsize=(8, 5))
        plt.plot(train_sizes, np.mean(train_scores, axis=1), label="Train", marker='o')
        plt.plot(train_sizes, np.mean(test_scores, axis=1), label="Validation", marker='s')
        plt.xlabel("Training Size")
        plt.ylabel(scoring_curve)
        plt.title("Learning Curve")
        plt.legend()
        plt.tight_layout()
        plt.show()

    if validation_params and 'validation' in extra_plots:
        for param_name, param_range in validation_params.items():
            print(f"\nValidation Curve for: {param_name}")
            pipe = Pipeline([('scaler', StandardScaler()), ('clf', model)])
            train_scores, val_scores = validation_curve(
                pipe, X_train, y_train,
                param_name=f'clf__{param_name}',
                param_range=param_range,
                scoring=scoring_curve,
                cv=cv, n_jobs=-1
            )
            plt.figure(figsize=(8, 5))
            plt.plot(param_range, np.mean(train_scores, axis=1), label="Train", marker='o')
            plt.plot(param_range, np.mean(val_scores, axis=1), label="Validation", marker='s')
            plt.xlabel(param_name)
            plt.ylabel(scoring_curve)
            plt.title(f"Validation Curve: {param_name}")
            plt.legend()
            plt.tight_layout()
            plt.show()

    if return_dict:
        return {
            'r2': r2,
            'adj_r2': adj_r2,
            'rmse': rmse,
            'mae': mae,
            'mape': mape,
            'rmsle': rmsle,
            'custom_metrics': {
                name: func(y_test, y_pred) for name, func in (custom_metrics or {}).items()
            },
            'runtime_secs': time.time() - start_time
        }