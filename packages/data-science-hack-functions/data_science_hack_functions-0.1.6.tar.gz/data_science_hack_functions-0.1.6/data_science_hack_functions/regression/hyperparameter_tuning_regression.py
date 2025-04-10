import numpy as np
import pandas as pd
import optuna
import time
from typing import Any, Callable, Dict, Union
from sklearn.model_selection import KFold
from sklearn.metrics import get_scorer
from tabulate import tabulate
from rich.console import Console
import inspect

console = Console()

def hyperparameter_tuning_regression(
    X: Union[pd.DataFrame, np.ndarray] = None,
    y: Union[pd.Series, np.ndarray] = None,
    model_class: Callable[..., Any] = None,
    param_grid: Dict[str, Callable[[optuna.Trial], Any]] = None,
    scoring: Union[str, Callable] = 'r2',
    n_trials: int = 50,
    cv_folds: int = 5,
    direction: str = 'maximize',
    verbose: bool = True,
    return_model: bool = True,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Optuna-based hyperparameter tuner for regression models.
    """

    if X is None or y is None or model_class is None or param_grid is None:
        console.print("[bold red]\nERROR:[/bold red] Missing required arguments: 'X', 'y', 'model_class', and 'param_grid'.")
        console.print("[bold cyan]Function Guide:[/bold cyan]")
        signature = inspect.signature(hyperparameter_tuning_regression)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")

        console.print("""
[bold green]\nFunction: tune_model_with_optuna_regression()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Tunes regression models using [bold]Optuna[/bold] for hyperparameter optimization.
Supports built-in and custom scoring metrics, k-fold cross-validation, and outputs optimal parameters and scores.

[bold green]Required Parameters:[/bold green]
• [bold yellow]X[/bold yellow]: Feature matrix (n_samples, n_features)
• [bold yellow]y[/bold yellow]: Target values (continuous)
• [bold yellow]model_class[/bold yellow]: sklearn-style regressor class (e.g., Ridge, RandomForestRegressor)
• [bold yellow]param_grid[/bold yellow]: Dictionary of optuna lambda search spaces for hyperparameters

[bold green]Optional Parameters:[/bold green]
• [bold yellow]scoring[/bold yellow]: Metric name (e.g. 'r2', 'neg_mean_squared_error', or callable). Default = 'r2'
• [bold yellow]n_trials[/bold yellow]: Number of optimization trials (default: 50)
• [bold yellow]cv_folds[/bold yellow]: Number of CV folds (default: 5)
• [bold yellow]direction[/bold yellow]: 'maximize' or 'minimize' (default: 'maximize')
• [bold yellow]verbose[/bold yellow]: Show logs (default: True)
• [bold yellow]return_model[/bold yellow]: Return best fitted model (default: True)
• [bold yellow]random_state[/bold yellow]: Seed for reproducibility (default: 42)

[bold green]Example:[/bold green]
>>> tune_model_with_optuna_regression(
        X, y,
        model_class=Ridge,
        param_grid={
            'alpha': lambda t: t.suggest_float('alpha', 0.01, 10.0, log=True)
        },
        scoring='neg_root_mean_squared_error',
        return_model=True
    )
        """)
        return

    if isinstance(scoring, str):
        scorer = get_scorer(scoring)
    elif callable(scoring):
        scorer = scoring
    else:
        raise ValueError("'scoring' must be a string or a callable.")

    if verbose:
        print("\n[Optuna Tuning Start]")
        print("=" * 50)
        print(f"Model       : {model_class.__name__}")
        print(f"Metric      : {scoring if isinstance(scoring, str) else 'custom function'}")
        print(f"Trials      : {n_trials}")
        print(f"CV Folds    : {cv_folds}")
        print(f"Direction   : {direction}")
        print("=" * 50)

    def objective(trial):
        params = {k: v(trial) for k, v in param_grid.items()}
        model = model_class(**params)
        cv = KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        scores = []
        for train_idx, test_idx in cv.split(X):
            X_train = X.iloc[train_idx] if hasattr(X, "iloc") else X[train_idx]
            y_train = y.iloc[train_idx] if hasattr(y, "iloc") else y[train_idx]
            X_test = X.iloc[test_idx] if hasattr(X, "iloc") else X[test_idx]
            y_test = y.iloc[test_idx] if hasattr(y, "iloc") else y[test_idx]
            model.fit(X_train, y_train)
            score = scorer(model, X_test, y_test)
            scores.append(score)
        return np.mean(scores)

    start_time = time.time()
    study = optuna.create_study(direction=direction)
    study.optimize(objective, n_trials=n_trials)
    elapsed = time.time() - start_time

    best_params = study.best_params
    best_score = study.best_value

    if verbose:
        print("\nBest Score:")
        print(f"  {best_score:.5f}")
        print("\nBest Hyperparameters:")
        print(tabulate(best_params.items(), headers=["Hyperparameter", "Value"], tablefmt="fancy_grid"))
        print(f"\nElapsed Time: {elapsed:.2f} seconds")

    output = {
        'best_score': best_score,
        'best_params': best_params,
        'study': study
    }

    if return_model:
        best_model = model_class(**best_params)
        best_model.fit(X, y)
        output['best_model'] = best_model

    return output