import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator
from sklearn.metrics import make_scorer, mean_squared_error, mean_absolute_error, r2_score, explained_variance_score, mean_squared_log_error
from typing import Dict, List, Union, Callable, Optional, Any
from tabulate import tabulate
from rich.console import Console
from rich.table import Table
import inspect

console = Console()

def run_nested_cv_regression(
    X: Optional[Union[pd.DataFrame, np.ndarray]] = None,
    y: Optional[Union[pd.Series, np.ndarray]] = None,
    model_dict: Optional[Dict[str, BaseEstimator]] = None,
    param_grids: Optional[Dict[str, Dict[str, List[Any]]]] = None,
    scoring_list: List[Union[str, Callable]] = ['r2'],
    outer_splits: int = 3,
    inner_splits: int = 3,
    random_state: int = 42,
    use_scaling: Optional[Callable[[str], bool]] = lambda name: name not in ['random_forest', 'gboost'],
    verbose: bool = True,
    return_results: bool = False,
    print_style: str = 'tabulate',  # or 'rich'
    show_plots: bool = True,
    normalize: bool = False  # normalize for relative comparison plot
) -> Optional[Dict[str, Any]]:
    """
    Performs nested cross-validation for regression models with support for multiple metrics and visual output.
    """

    if X is None or y is None or model_dict is None or param_grids is None:
        console.print("[bold red]\nERROR:[/bold red] Missing required parameters: 'X', 'y', 'model_dict', and 'param_grids'.\n")
        console.print("[bold cyan]run_nested_cv_regression[/bold cyan] expects the following inputs:")
        signature = inspect.signature(run_nested_cv_regression)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")
        
        console.print("""
[bold green]\nFunction: run_nested_cv()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Performs nested cross-validation for binary classification tasks, with automatic hyperparameter tuning,
scoring, scaling, tabular output, and visualization.

[bold green]Required Parameters:[/bold green]
• [bold yellow]X[/bold yellow] (DataFrame or ndarray): Feature matrix (independent variables).
• [bold yellow]y[/bold yellow] (Series or ndarray): Target vector (binary classification labels).
• [bold yellow]model_dict[/bold yellow] (dict): Dictionary of models to evaluate. Keys = model names, values = sklearn estimators.
• [bold yellow]param_grids[/bold yellow] (dict): Dictionary of hyperparameter grids for each model using sklearn's param format (e.g., 'clf__C').

[bold green]Optional Parameters:[/bold green]
• [bold yellow]scoring_list[/bold yellow] (list): List of scoring metrics (e.g., ['accuracy', 'roc_auc']). Default = ['accuracy'].
• [bold yellow]outer_splits[/bold yellow] (int): Number of folds in the outer CV loop. Default = 3.
• [bold yellow]inner_splits[/bold yellow] (int): Number of folds in the inner CV loop. Default = 3.
• [bold yellow]random_state[/bold yellow] (int): Random seed for reproducibility. Default = 42.
• [bold yellow]use_scaling[/bold yellow] (function): Function to determine whether to scale a model. By default, skips tree-based models.
• [bold yellow]verbose[/bold yellow] (bool): Whether to print detailed progress. Default = True.
• [bold yellow]return_results[/bold yellow] (bool): If True, returns all results, figures, and summaries. Default = False.
• [bold yellow]print_style[/bold yellow] (str): Style of printed tables. 'tabulate' (default) or 'rich'.
• [bold yellow]normalize[/bold yellow] (bool): To display relative model comparision graphs. Default = False.

[bold green]Features:[/bold green]
• Runs nested cross-validation with inner tuning and outer evaluation.
• Handles multiple models and metrics simultaneously.
• Automatically applies scaling where needed.
• Displays results in beautiful tables (choose between tabulate or rich).
• Plots bounded and unbounded metric comparisons.
• Works with both string and custom callable scorers.
• Returns a structured output (if return_results=True) for further analysis or saving.

[bold green]Example Usage:[/bold green]
>>> run_nested_cv(X, y, model_dict=models, param_grids=grids, scoring_list=['accuracy', 'roc_auc'])
>>> run_nested_cv(X, y, models, grids, print_style='rich', return_results=True)

[bold magenta]Tip:[/bold magenta] You can use 'clf__' prefix in param_grids to target parameters inside the pipeline.
        """)

        return

    y = np.ravel(y)
    outer_cv = KFold(n_splits=outer_splits, shuffle=True, random_state=random_state)
    inner_cv = KFold(n_splits=inner_splits, shuffle=True, random_state=random_state)

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
            if isinstance(scoring, str):
                scoring_label = scoring
                postprocess = None

                if scoring == 'rmse':
                    scorer = 'neg_mean_squared_error'
                    postprocess = lambda s: np.sqrt(-s)
                elif scoring == 'rmsle':
                    scorer = 'neg_mean_squared_log_error'
                    postprocess = lambda s: np.sqrt(-s)
                elif scoring == 'mae':
                    scorer = 'neg_mean_absolute_error'
                    postprocess = lambda s: -s
                elif scoring == 'mape':
                    scorer = make_scorer(lambda yt, yp: np.mean(np.abs((yt - yp) / np.clip(np.abs(yt), 1e-8, None))) * 100, greater_is_better=False)
                    postprocess = lambda s: -s
                elif scoring == 'adjusted_r2':
                    scorer = make_scorer(lambda yt, yp: 1 - ((1 - r2_score(yt, yp)) * (len(yt) - 1) / (len(yt) - X.shape[1] - 1)))
                else:
                    scorer = scoring
            else:
                scoring_label = scoring.__name__
                scorer = scoring
                postprocess = None

            print(f"\n→ Scoring Metric: {scoring_label.upper()}")

            grid = GridSearchCV(pipe, param_grid, cv=inner_cv, scoring=scorer, n_jobs=-1)
            raw_scores = cross_val_score(grid, X, y, cv=outer_cv, scoring=scorer, n_jobs=-1)
            scores = postprocess(raw_scores) if postprocess else raw_scores

            grid.fit(X, y)
            best_params = dict(sorted(grid.best_params_.items()))
            mean_score = scores.mean()
            std_score = scores.std()

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

            results[model_name][scoring_label] = {
                'score_mean': mean_score,
                'score_std': std_score,
                'best_params': best_params
            }

            summary_rows.append({
                'Model': model_name,
                'Metric': scoring_label,
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

    if show_plots:
        print("\n Generating Model Comparison Visuals...")
        plot_df = summary_df.pivot(index='Model', columns='Metric', values='Mean Score')

        if normalize:
            plot_df_norm = plot_df.copy()
            for metric in plot_df_norm.columns:
                col = plot_df_norm[metric]
                if metric in {'rmse', 'mae', 'mape', 'rmsle'}:
                    col = -col  # invert error (lower is better)
                min_, max_ = col.min(), col.max()
                plot_df_norm[metric] = (col - min_) / (max_ - min_ + 1e-8)

            fig_norm, ax = plt.subplots(figsize=(10, 6))
            plot_df_norm.plot(kind='bar', ax=ax, rot=0)
            ax.set_title("Normalized Model Comparison (All Metrics)")
            ax.set_ylabel("Normalized Score")
            ax.set_xlabel("Model")
            ax.grid(axis='y')
            ax.legend(title="Metric", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()
        else:
            error_metrics = {'mae', 'rmse', 'rmsle', 'mape'}
            score_metrics = set(plot_df.columns) - error_metrics

            sns.set(style="whitegrid")
            palette = sns.color_palette("Set2", n_colors=len(plot_df))

            if score_metrics:
                fig_score, ax = plt.subplots(figsize=(10, 6))
                plot_df[sorted(score_metrics)].plot(kind='bar', ax=ax, color=palette, rot=0)
                ax.set_title("Model Comparison (Score Metrics)")
                ax.set_ylabel("Score")
                ax.set_xlabel("Model")
                ax.grid(axis='y')
                ax.legend(title="Metric", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                plt.show()

            if error_metrics & set(plot_df.columns):
                fig_error, ax = plt.subplots(figsize=(10, 6))
                plot_df[sorted(error_metrics & set(plot_df.columns))].plot(kind='bar', ax=ax, color=palette, rot=0)
                ax.set_title("Model Comparison (Error Metrics)")
                ax.set_ylabel("Error")
                ax.set_xlabel("Model")
                ax.grid(axis='y')
                ax.legend(title="Metric", bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.tight_layout()
                plt.show()

    if return_results:
        return {
            'summary': summary_df,
            'results': results,
            'best_params': {
                model: {metric: results[model][metric]['best_params'] for metric in results[model]}
                for model in results
            }
        }