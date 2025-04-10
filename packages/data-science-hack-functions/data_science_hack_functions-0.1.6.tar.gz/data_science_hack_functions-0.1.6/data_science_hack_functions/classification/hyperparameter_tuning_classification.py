import numpy as np
import pandas as pd
import optuna
import time
from typing import Any, Callable, Dict, Union
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import get_scorer
from tabulate import tabulate
from rich.console import Console
import inspect

console = Console()

def hyperparameter_tuning_classification(
    X: Union[pd.DataFrame, np.ndarray] = None,
    y: Union[pd.Series, np.ndarray] = None,
    model_class: Callable[..., Any] = None,
    param_grid: Dict[str, Callable[[optuna.Trial], Any]] = None,
    scoring: Union[str, Callable] = 'accuracy',
    n_trials: int = 50,
    cv_folds: int = 5,
    stratified: bool = True,
    direction: str = 'maximize',
    verbose: bool = True,
    return_model: bool = True,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Optuna-based hyperparameter tuner for binary classification models.
    """

    if X is None or y is None or model_class is None or param_grid is None:
        console.print("[bold red]\nERROR:[/bold red] Missing required arguments: 'X', 'y', 'model_class', and 'param_grid'.")
        console.print("[bold cyan]Function Guide:[/bold cyan]")
        signature = inspect.signature(hyperparameter_tuning_classication)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")

        console.print("""
[bold green]\nFunction: tune_model_with_optuna()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Tunes binary classification models using [bold]Optuna[/bold] for hyperparameter optimization.
Supports both built-in and custom metrics, cross-validation, and returns the best score, parameters, and optionally the final fitted model.

[bold green]Required Parameters:[/bold green]
• [bold yellow]X[/bold yellow] (DataFrame or ndarray): Feature matrix (n_samples, n_features).
• [bold yellow]y[/bold yellow] (Series or ndarray): Binary target variable (0/1).
• [bold yellow]model_class[/bold yellow] (sklearn class): The classifier class (e.g., LogisticRegression, RandomForestClassifier).
• [bold yellow]param_grid[/bold yellow] (dict): Dictionary mapping hyperparameter names to Optuna lambda suggestions.
  → Example: {"C": lambda t: t.suggest_loguniform("C", 0.01, 10)}

[bold green]Optional Parameters:[/bold green]
• [bold yellow]scoring[/bold yellow] (str or callable): Scoring function or string. Accepts any sklearn-compatible metric (default: 'accuracy').
• [bold yellow]n_trials[/bold yellow] (int): Number of Optuna trials to run (default: 50).
• [bold yellow]cv_folds[/bold yellow] (int): Number of cross-validation folds (default: 5).
• [bold yellow]stratified[/bold yellow] (bool): Whether to use StratifiedKFold (default: True).
• [bold yellow]direction[/bold yellow] (str): 'maximize' or 'minimize' based on metric (default: 'maximize').
• [bold yellow]verbose[/bold yellow] (bool): If True, prints progress and summary tables (default: True).
• [bold yellow]return_model[/bold yellow] (bool): If True, returns the best model fitted on full data (default: True).
• [bold yellow]random_state[/bold yellow] (int): Seed for reproducibility (default: 42).

[bold green]Supported Scoring Options:[/bold green]
You can use any of the following:
• [cyan]'accuracy'[/cyan] — Correct predictions
• [cyan]'f1'[/cyan], [cyan]'precision'[/cyan], [cyan]'recall'[/cyan] — Binary class metrics
• [cyan]'roc_auc'[/cyan] — Area under ROC curve
• [cyan]'log_loss'[/cyan] — Log loss (negated for maximization)

Or pass a [bold]custom metric[/bold] function:
→ Example:
>>> def cost_sensitive_score(y_true, y_pred):
>>>     return -(10 * FP + 1 * FN)

[italic]Note:[/italic] Your custom function must follow the signature:  
[dim]lambda est, X_val, y_val → float[/dim]

[bold green]Features:[/bold green]
✓ Flexible: works with any sklearn-style model  
✓ Compatible with both string and custom scorers  
✓ Cross-validation enabled (KFold or Stratified)  
✓ Hyperparameter space defined via Optuna lambdas  
✓ Clean tabulated results and timing  
✓ Returns full Optuna study object and best model

[bold green]Example Usage:[/bold green]
>>> tune_model_with_optuna(
        X=X, y=y,
        model_class=LogisticRegression,
        param_grid={
            "C": lambda t: t.suggest_float("C", 0.01, 10, log=True),
            "penalty": lambda t: t.suggest_categorical("penalty", ["l1", "l2"]),
            "solver": lambda t: t.suggest_categorical("solver", ["liblinear", "saga"])
        },
        scoring='f1',
        n_trials=30,
        return_model=True
    )

[bold magenta]Tip:[/bold magenta] Use [italic]'neg_log_loss'[/italic] or [italic]custom cost functions[/italic] when optimizing under business constraints!
        """)
        return

    if isinstance(scoring, str):
        scorer = get_scorer(scoring)
    elif callable(scoring):
        scorer = scoring  # Already a custom estimator-based scoring function
    else:
        raise ValueError("'scoring' must be a string or a callable taking (estimator, X, y).")

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
        cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=random_state) if stratified else KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)
        scores = []
        for train_idx, test_idx in cv.split(X, y):
            X_train = X.iloc[train_idx] if hasattr(X, "iloc") else X[train_idx]
            y_train = y.iloc[train_idx] if hasattr(y, "iloc") else y[train_idx]
            X_test  = X.iloc[test_idx]  if hasattr(X, "iloc") else X[test_idx]
            y_test  = y.iloc[test_idx]  if hasattr(y, "iloc") else y[test_idx]
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