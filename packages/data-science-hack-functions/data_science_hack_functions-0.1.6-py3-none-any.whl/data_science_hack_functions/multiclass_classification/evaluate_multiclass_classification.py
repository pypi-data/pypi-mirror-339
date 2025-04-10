import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    precision_recall_curve, roc_curve
)
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import calibration_curve
from sklearn.metrics import DetCurveDisplay
from scipy.stats import ks_2samp
from rich.console import Console
import inspect
from tabulate import tabulate

console = Console()

def evaluate_multiclass_classification_model(
    model=None,
    X_train=None, y_train=None,
    X_test=None, y_test=None,
    cv=5,
    average='macro',
    validation_params=None,
    scoring_curve="accuracy",
    verbose=True,
    return_dict=False,
    extra_plots=None
):
    """
    Evaluates a multiclass classification model with diagnostics.

    Parameters:
    - model: Classifier
    - X_train, y_train: Training data
    - X_test, y_test: Test data
    - cv: CV folds for learning/validation curves
    - average: Averaging method ('macro', 'weighted')
    - validation_params: Hyperparam ranges {param_name: list}
    - scoring_curve: Metric for learning/validation curves
    - verbose: Whether to print and plot
    - return_dict: Return dictionary of results
    - extra_plots: List like ['learning', 'validation', 'lift', 'calibration', 'ks']
    """

    if not all([model is not None, X_train is not None, y_train is not None, X_test is not None, y_test is not None]):
        console.print("[bold red]\nERROR:[/bold red] Missing required inputs.")
        signature = inspect.signature(evaluate_multiclass_classification_model)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")

        console.print("""
[bold green]\\nFunction: evaluate_multiclass_classification_model()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Evaluates multiclass classification models using test data and presents detailed performance metrics.
It supports confusion matrix visualization, learning/validation curves, and optional advanced diagnostic plots.
Returns a summary dictionary if needed.

[bold green]Required Parameters:[/bold green]
• [bold yellow]model[/bold yellow]: Any sklearn-compatible classifier (must support .fit and .predict).
• [bold yellow]X_train[/bold yellow], [bold yellow]y_train[/bold yellow]: Training data (features & labels).
• [bold yellow]X_test[/bold yellow], [bold yellow]y_test[/bold yellow]: Test data (features & labels).

[bold green]Optional Parameters:[/bold green]
• [bold yellow]cv[/bold yellow] (int): Number of cross-validation folds used in learning/validation curves. Default: 5.
• [bold yellow]average[/bold yellow] (str): Averaging method for metrics like F1/precision/recall. Options:
    - 'macro'   → treats all classes equally  
    - 'weighted' → accounts for class imbalance  
  Default: 'macro'.
• [bold yellow]validation_params[/bold yellow] (dict): Hyperparameter search space: {param_name: param_range}.
• [bold yellow]scoring_curve[/bold yellow] (str): Metric used during learning/validation curve scoring. Default: 'accuracy'.
• [bold yellow]verbose[/bold yellow] (bool): Whether to print outputs and show plots. Default: True.
• [bold yellow]return_dict[/bold yellow] (bool): If True, returns metrics and confusion matrix in a dictionary.
• [bold yellow]extra_plots[/bold yellow] (list): Additional plot names to include. Choose any:
    → 'learning', 'validation', 'lift', 'calibration', 'ks'

[bold green]Computed Metrics:[/bold green]
• [bold cyan]Accuracy[/bold cyan]: Overall percentage of correct predictions  
• [bold cyan]Precision[/bold cyan]: True Positives / (True Positives + False Positives), per class  
• [bold cyan]Recall[/bold cyan]: True Positives / (True Positives + False Negatives), per class  
• [bold cyan]F1 Score[/bold cyan]: Harmonic mean of precision and recall  
(All metrics respect the selected [italic]average[/italic] method: macro or weighted)

[bold green]Diagnostic Plots (extra_plots):[/bold green]
• [bold cyan]'learning'[/bold cyan] → Shows how model performance evolves with more training data  
• [bold cyan]'validation'[/bold cyan] → Visualizes model performance across hyperparameter values  
• [bold cyan]'lift'[/bold cyan] → Measures effectiveness of probability ranking across all classes  
• [bold cyan]'calibration'[/bold cyan] → Checks how well predicted probabilities match observed outcomes  
• [bold cyan]'ks'[/bold cyan] → Uses ECDF to measure separation between predicted classes

[bold green]Features:[/bold green]
✓ Automatically detects number of classes  
✓ Works with any estimator supporting `fit()` and `predict()`  
✓ Flexible metric averaging (macro/weighted)  
✓ Built-in learning and validation curves  
✓ Optional deep diagnostics: lift, calibration, KS curve  
✓ Returns structured dictionary (optional)  

[bold green]Example Usage:[/bold green]
>>> evaluate_multiclass_model(
        model=clf,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        average='weighted',
        validation_params={'max_depth': [3, 5, 7]},
        scoring_curve='f1_weighted',
        extra_plots=['learning', 'validation', 'lift', 'ks'],
        return_dict=True
    )

[bold magenta]Tip:[/bold magenta] For pipeline models, use `'clf__param_name'` in validation_params for hyperparameter tuning!
""")

        return

    extra_plots = extra_plots or []
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average=average, zero_division=0)
    rec = recall_score(y_test, y_pred, average=average, zero_division=0)
    f1 = f1_score(y_test, y_pred, average=average, zero_division=0)

    if verbose:
        print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))
        print("\nTest Set Metrics:")
        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1 Score : {f1:.4f}")
    
    if "confusion_matrix" in extra_plots and verbose:
       cm = confusion_matrix(y_test, y_pred)
       labels = np.unique(y_test)
       plt.figure(figsize=(8, 6))
       sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=labels, yticklabels=labels)
       plt.title("Confusion Matrix")
       plt.xlabel("Predicted")
       plt.ylabel("Actual")
       plt.tight_layout()
       plt.show()

    if "learning" in extra_plots and verbose:
        train_sizes, train_scores, test_scores = learning_curve(
            model, X_train, y_train, train_sizes=np.linspace(0.1, 1.0, 5),
            cv=cv, scoring=scoring_curve
        )
        plt.figure(figsize=(8, 6))
        plt.plot(train_sizes, np.mean(train_scores, axis=1), label="Train", marker='o')
        plt.plot(train_sizes, np.mean(test_scores, axis=1), label="Validation", marker='s', linestyle='--')
        plt.xlabel("Training Size")
        plt.ylabel(scoring_curve.capitalize())
        plt.title("Learning Curve")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    if validation_params and "validation" in extra_plots and verbose:
        for param_name, param_range in validation_params.items():
            print(f"\nValidation Curve for: {param_name}")
            pipe = Pipeline([('scaler', StandardScaler()), ('clf', model)])
            train_scores, val_scores = validation_curve(
                pipe, X_train, y_train,
                param_name=f'clf__{param_name}',
                param_range=param_range,
                scoring=scoring_curve,
                cv=cv,
                n_jobs=-1
            )
            plt.figure(figsize=(8, 6))
            plt.plot(param_range, np.mean(train_scores, axis=1), label="Train", marker='o')
            plt.plot(param_range, np.mean(val_scores, axis=1), label="Validation", marker='s', linestyle='--')
            plt.xlabel(param_name)
            plt.ylabel(scoring_curve.capitalize())
            plt.title(f"Validation Curve: {param_name}")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

    if "lift" in extra_plots and hasattr(model, "predict_proba"):
        probas = model.predict_proba(X_test)
        for i in range(probas.shape[1]):
            y_true = (y_test == i).astype(int)
            y_scores = probas[:, i]
            precision_vals, recall_vals, _ = precision_recall_curve(y_true, y_scores)
            lift = precision_vals / (np.sum(y_true) / len(y_true))
            plt.figure(figsize=(8, 6))
            plt.plot(recall_vals, lift, label=f"Class {i}")
            plt.xlabel("Recall")
            plt.ylabel("Lift")
            plt.title("Lift Curve")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

    if "calibration" in extra_plots and hasattr(model, "predict_proba"):
        probas = model.predict_proba(X_test)
        for i in range(probas.shape[1]):
            prob_true, prob_pred = calibration_curve((y_test == i).astype(int), probas[:, i], n_bins=10)
            plt.figure(figsize=(8, 6))
            plt.plot(prob_pred, prob_true, marker='o', label=f"Class {i}")
            plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
            plt.xlabel("Mean Predicted Probability")
            plt.ylabel("Fraction of Positives")
            plt.title("Calibration Curve")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

    if "ks" in extra_plots and hasattr(model, "predict_proba"):
        probas = model.predict_proba(X_test)
        for i in range(probas.shape[1]):
            pos = probas[y_test == i, i]
            neg = probas[y_test != i, i]
            ks_stat, _ = ks_2samp(pos, neg)
            plt.figure(figsize=(8, 6))
            sns.ecdfplot(pos, label=f"Positive (Class {i})", linestyle="-")
            sns.ecdfplot(neg, label=f"Negative (Others)", linestyle="--")
            plt.title(f"KS Curve - Class {i} (Statistic = {ks_stat:.2f})")
            plt.xlabel("Predicted Probability")
            plt.ylabel("ECDF")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

    if return_dict:
        return {
            'accuracy': acc,
            'precision': prec,
            'recall': rec,
            'f1': f1,
            'confusion_matrix': cm
        }