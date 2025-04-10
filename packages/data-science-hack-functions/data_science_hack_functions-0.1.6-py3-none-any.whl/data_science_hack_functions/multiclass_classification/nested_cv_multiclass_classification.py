import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator
from sklearn.utils.multiclass import type_of_target
from typing import Dict, List, Union, Callable, Optional, Any
from tabulate import tabulate
from rich.console import Console
from rich.table import Table
import inspect

console = Console()

def run_nested_cv_multiclass_classification(
    X: Optional[Union[pd.DataFrame, np.ndarray]] = None,
    y: Optional[Union[pd.Series, np.ndarray]] = None,
    model_dict: Optional[Dict[str, BaseEstimator]] = None,
    param_grids: Optional[Dict[str, Dict[str, List[Any]]]] = None,
    scoring_list: List[Union[str, Callable]] = ['accuracy'],
    outer_splits: int = 3,
    inner_splits: int = 3,
    random_state: int = 42,
    use_scaling: Optional[Callable[[str], bool]] = lambda name: name not in ['random_forest', 'gboost'],
    verbose: bool = True,
    return_results: bool = False,
    print_style: str = 'tabulate',  # or 'rich'
    show_plots: bool = True
) -> Optional[Dict[str, Any]]:
    """
    Performs nested cross-validation for multiclass classification models with multiple scoring metrics.

    Parameters:
    - X: Feature matrix.
    - y: Multiclass target vector.
    - model_dict: Dictionary of models to evaluate.
    - param_grids: Dictionary of hyperparameter grids for each model.
    - scoring_list: List of scoring metrics (e.g., ['accuracy', 'f1_macro', 'roc_auc_ovr']).
    - outer_splits / inner_splits: Number of CV folds.
    - use_scaling: Function to determine if StandardScaler is needed.
    - verbose: Whether to print intermediate info.
    - return_results: If True, returns a result dictionary.
    - print_style: 'tabulate' or 'rich' for styled terminal output.
    - show_plots: If True, display performance comparison plots.

    Returns:
    Optional dict with summary, results, best_params, and figures.
    """

    if X is None or y is None or model_dict is None or param_grids is None:
        console.print("[bold red]\nERROR:[/bold red] Missing required parameters: 'X', 'y', 'model_dict', and 'param_grids'.\n")
        console.print("[bold cyan]run_nested_cv_multiclass[/bold cyan] expects the following inputs:")
        signature = inspect.signature(run_nested_cv_multiclass_classification)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")

        console.print("""
[bold green]\\nFunction: run_nested_cv_multiclass()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Performs nested cross-validation for [bold]multiclass classification[/bold] problems.
It automatically tunes hyperparameters using GridSearchCV inside the inner folds, evaluates model performance on outer folds,
and presents results in visually pleasing tables and optional performance plots.

[bold green]Required Parameters:[/bold green]
• [bold yellow]X[/bold yellow] (DataFrame or ndarray): Feature matrix of shape (n_samples, n_features).
• [bold yellow]y[/bold yellow] (Series or ndarray): Target labels (with 3 or more classes).
• [bold yellow]model_dict[/bold yellow] (dict): A dictionary mapping model names to sklearn-compatible classifiers.
• [bold yellow]param_grids[/bold yellow] (dict): A dictionary mapping model names to parameter grids.
  Use `'clf__param_name'` syntax to refer to parameters inside pipelines.

[bold green]Optional Parameters:[/bold green]
• [bold yellow]scoring_list[/bold yellow] (list): List of scoring metrics (e.g., ['accuracy', 'f1_macro', 'roc_auc_ovr']).
• [bold yellow]outer_splits[/bold yellow] (int): Number of outer CV folds (default: 3).
• [bold yellow]inner_splits[/bold yellow] (int): Number of inner CV folds (default: 3).
• [bold yellow]random_state[/bold yellow] (int): Random seed for reproducibility (default: 42).
• [bold yellow]use_scaling[/bold yellow] (function): Function that takes model name and returns True/False if scaling is needed.
  By default, StandardScaler is applied to all models except tree-based ones.
• [bold yellow]verbose[/bold yellow] (bool): Whether to print detailed progress (default: True).
• [bold yellow]return_results[/bold yellow] (bool): If True, returns a structured dictionary with scores, best params, and figures (default: False).
• [bold yellow]print_style[/bold yellow] (str): Table style. Use 'tabulate' (clean ASCII) or 'rich' (colored CLI tables).
• [bold yellow]show_plots[/bold yellow] (bool): If True, displays score comparison plots after execution (default: True).

[bold green]Scoring Metrics Supported:[/bold green]
• 'accuracy'
• 'f1_macro', 'f1_weighted'
• 'precision_macro', 'recall_macro'
• 'roc_auc_ovr' (One-vs-Rest AUC for multiclass)
• You can also pass any [italic]custom scoring function[/italic] using `make_scorer()`.

[bold green]Features:[/bold green]
✓ Nested cross-validation (outer loop for evaluation, inner loop for tuning)  
✓ Multiple models evaluated simultaneously  
✓ Hyperparameter tuning via GridSearchCV  
✓ Visual performance comparison (bar/line plots)  
✓ Choice of output format: clean (tabulate) or colorful (rich)  
✓ Returns all results as a dictionary if needed  
✓ Automatic scaling logic (customizable)

[bold green]Example Usage:[/bold green]
>>> run_nested_cv_multiclass(
        X, y,
        model_dict=models,
        param_grids=grids,
        scoring_list=['accuracy', 'f1_macro', 'roc_auc_ovr'],
        print_style='rich',
        return_results=True,
        show_plots=True
    )

[bold magenta]Tip:[/bold magenta] Always use 'clf__' prefix in param_grids to reference model parameters inside a pipeline.
""")

        return

    if type_of_target(y) != 'multiclass':
        raise ValueError("This function only supports multiclass classification targets.")

    y = pd.Series(y).astype(str)

    outer_cv = StratifiedKFold(n_splits=outer_splits, shuffle=True, random_state=random_state)
    inner_cv = StratifiedKFold(n_splits=inner_splits, shuffle=True, random_state=random_state)

    results, summary_rows = {}, []

    for model_name, model in model_dict.items():
        pretty_model_name = model_name.replace("_", " ").upper()
        print(f"\n{'='*60}\n Running Nested CV for: {pretty_model_name}\n{'='*60}")

        steps = [('scaler', StandardScaler())] if use_scaling(model_name) else []
        steps.append(('clf', model))
        pipe = Pipeline(steps)

        param_grid = {f'clf__{k}': v for k, v in param_grids[model_name].items()}
        results[model_name] = {}

        for scoring in scoring_list:
            scoring_label = scoring.upper() if isinstance(scoring, str) else 'CUSTOM SCORER'
            print(f"\n→ Scoring Metric: {scoring_label}")

            grid = GridSearchCV(pipe, param_grid, cv=inner_cv, scoring=scoring, n_jobs=-1)
            nested_scores = cross_val_score(grid, X, y, cv=outer_cv, scoring=scoring, n_jobs=-1)

            grid.fit(X, y)
            best_params = dict(sorted(grid.best_params_.items()))
            mean_score = nested_scores.mean()
            std_score = nested_scores.std()

            if print_style == 'rich':
                score_table = Table(show_header=True, header_style="bold magenta")
                score_table.add_column("Mean Score")
                score_table.add_column("Std Dev")
                score_table.add_row(f"{mean_score:.4f}", f"{std_score:.4f}")
                console.print(score_table)

                console.print("[bold green]Best Hyperparameters:[/bold green]")
                for k in sorted(best_params):
                    console.print(f"   [cyan]- {k}: {best_params[k]}")
            else:
                print(tabulate([[f"{mean_score:.4f}", f"{std_score:.4f}"]], headers=["Mean Score", "Std Dev"], tablefmt="pretty"))
                print("Best Hyperparameters:")
                for k in sorted(best_params):
                    print(f"   - {k}: {best_params[k]}")

            results[model_name][scoring] = {
                'score_mean': mean_score,
                'score_std': std_score,
                'best_params': best_params
            }

            summary_rows.append({
                'Model': model_name,
                'Metric': scoring,
                'Mean Score': mean_score,
                'Std Dev': std_score
            })

    summary_df = pd.DataFrame(summary_rows)

    print(f"\n{'='*60}\n Final Model Performance Summary\n{'='*60}")
    if print_style == 'rich':
        table = Table(title="Final Model Performance Summary", header_style="bold magenta")
        table.add_column("Model")
        table.add_column("Metric")
        table.add_column("Mean Score", justify="right")
        table.add_column("Std Dev", justify="right")
        for _, row in summary_df.iterrows():
            table.add_row(
                row['Model'],
                row['Metric'],
                f"{row['Mean Score']:.4f}",
                f"{row['Std Dev']:.4f}"
            )
        console.print(table)
    else:
        print(tabulate(summary_df, headers='keys', tablefmt='fancy_grid', showindex=False))

    print("\n Generating Model Comparison Visuals...")
    plot_df = summary_df.pivot(index='Model', columns='Metric', values='Mean Score')
    bounded_metrics = {'accuracy', 'f1_macro', 'f1_weighted', 'precision_macro', 'recall_macro'}
    all_metrics = set(plot_df.columns)
    bounded = sorted(list(all_metrics.intersection(bounded_metrics)))
    unbounded = sorted(list(all_metrics.difference(bounded_metrics)))

    sns.set(style="whitegrid")
    palette = sns.color_palette("Set2", n_colors=len(plot_df))
    fig_bounded, fig_unbounded = None, None

    if show_plots and bounded:
        print(" Plotting bounded [0–1] metrics...")
        fig_bounded, ax = plt.subplots(figsize=(10, 6))
        plot_df[bounded].plot(kind='bar', ax=ax, color=palette, rot=0)
        ax.set_title("Model Comparison (Bounded Metrics 0–1)")
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1)
        ax.set_xlabel("Model")
        ax.grid(axis='y')
        ax.legend(title="Metric", bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()

    if show_plots and unbounded:
        print(" Plotting unbounded/other-range metrics...")
        fig_unbounded, axes = plt.subplots(1, len(unbounded), figsize=(6 * len(unbounded), 6), sharey=True)
        if len(unbounded) == 1:
            axes = [axes]
        for ax, metric in zip(axes, unbounded):
            metric_data = plot_df[metric].sort_values()
            metric_data.plot(kind='barh', ax=ax, color=palette)
            ax.set_title(f"Model Comparison ({metric})")
            ax.set_xlabel("Mean Score")
            ax.set_ylabel("Model")
            ax.grid(axis='x')
        plt.tight_layout()
        plt.show()

    if return_results:
        return {
            'summary': summary_df,
            'results': results,
            'best_params': {
                model: {metric: results[model][metric]['best_params'] for metric in results[model]}
                for model in results
            },
            'figures': {
                'bounded': fig_bounded,
                'unbounded': fig_unbounded
            }
        }