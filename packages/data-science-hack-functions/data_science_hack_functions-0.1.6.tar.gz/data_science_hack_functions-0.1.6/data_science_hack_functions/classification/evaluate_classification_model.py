import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
accuracy_score, precision_score, recall_score, f1_score, 
roc_auc_score, classification_report, confusion_matrix,
precision_recall_curve, roc_curve
)
from sklearn.model_selection import learning_curve, validation_curve
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import calibration_curve
from sklearn.metrics import DetCurveDisplay
from rich.console import Console
from rich.table import Table
import inspect
from tabulate import tabulate

console = Console()

def evaluate_classification_model(
    model = None,
    X_train =None, y_train = None,
    X_test = None, y_test = None,
    cv=5,
    cost_fn=None,
    cost_fp=None,
    validation_params=None,
    scoring_curve="accuracy",
    verbose=True,
    return_dict=False,
    extra_plots=None  # List of strings like ['threshold', 'calibration', 'ks']
):
    """
    Evaluates a binary classification model with rich diagnostics.

    Parameters:
    - model: Classifier (sklearn-style)
    - X_train, y_train: Training data
    - X_test, y_test: Test data
    - cv: Number of folds for learning/validation curves
    - cost_fn, cost_fp: Optional misclassification costs
    - validation_params: dict of {param_name: param_range} for validation curves
    - scoring_curve: Metric for learning/validation curves
    - verbose: Print/log information
    - return_dict: Return all metrics in a dictionary
    - extra_plots: List of extras like ['threshold', 'calibration', 'ks']
    """

    if not all([model is not None, X_train is not None, y_train is not None, X_test is not None, y_test is not None]):
        console.print("[bold red]\nERROR:[/bold red] Missing required inputs.")
        signature = inspect.signature(evaluate_classification_model)
        for param in signature.parameters.values():
            default = f"(default={param.default})" if param.default is not param.empty else "[required]"
            console.print(f"  • [bold yellow]{param.name}[/bold yellow]: {default}")

        console.print("""
[bold green]\\nFunction: evaluate_classification_model()[/bold green]

[bold cyan]Purpose:[/bold cyan]
Evaluates [bold]binary classification models[/bold] using test data and produces detailed performance reports.
Supports misclassification cost evaluation, learning and validation curves, and insightful probability-based diagnostics.

[bold green]Required Parameters:[/bold green]
• [bold yellow]model[/bold yellow]: A sklearn-compatible classifier (must implement .fit and .predict).
• [bold yellow]X_train[/bold yellow], [bold yellow]y_train[/bold yellow]: Training features and target labels.
• [bold yellow]X_test[/bold yellow], [bold yellow]y_test[/bold yellow]: Test features and target labels.

[bold green]Optional Parameters:[/bold green]
• [bold yellow]cv[/bold yellow] (int): Number of folds for learning/validation curves. Default: 5.
• [bold yellow]cost_fn[/bold yellow], [bold yellow]cost_fp[/bold yellow]: Cost of false negatives and false positives for custom cost evaluation.
• [bold yellow]validation_params[/bold yellow] (dict): Hyperparameter tuning config — {param_name: param_range}.
• [bold yellow]scoring_curve[/bold yellow] (str): Metric used for learning/validation curves. E.g., 'accuracy', 'f1', 'roc_auc'. Default: 'accuracy'.
• [bold yellow]verbose[/bold yellow] (bool): Whether to print metrics and show plots. Default: True.
• [bold yellow]return_dict[/bold yellow] (bool): If True, returns a dictionary of all key evaluation outputs.
• [bold yellow]extra_plots[/bold yellow] (list): Add any of the following optional plots:
    → 'threshold', 'calibration', 'ks', 'det', 'lift'
• [bold yellow]print_style[/bold yellow] (str): Style of terminal output. Options: 'tabulate' (ASCII) or 'rich' (colorful).

[bold green]Computed Metrics:[/bold green]
• [bold cyan]Accuracy[/bold cyan]   → Overall percentage of correct predictions  
• [bold cyan]Precision[/bold cyan] → Proportion of predicted positives that are correct  
• [bold cyan]Recall[/bold cyan]    → Proportion of actual positives that are correctly predicted  
• [bold cyan]F1 Score[/bold cyan]  → Harmonic mean of precision and recall  
• [bold cyan]ROC AUC[/bold cyan]   → Area under ROC curve (if probabilities available)  
• [bold cyan]Avg Cost[/bold cyan]  → Weighted cost of misclassifications (FN & FP)

[bold green]Optional Diagnostic Plots (extra_plots):[/bold green]
• [bold cyan]'threshold'[/bold cyan] → Shows precision, recall, and F1 across thresholds to fine-tune decision boundary  
• [bold cyan]'calibration'[/bold cyan] → Evaluates how well predicted probabilities reflect actual class likelihoods  
• [bold cyan]'ks'[/bold cyan] → KS statistic plot (separation between positive and negative probability distributions)  
• [bold cyan]'lift'[/bold cyan] → Lift curve shows model effectiveness in ranking positive samples  
• [bold cyan]'det'[/bold cyan] → DET curve shows trade-off between false negative and false positive rates (requires scikit-learn ≥ 1.1)

[bold green]Features:[/bold green]
✓ Auto-detects available probability method (predict_proba or decision_function)  
✓ Confusion matrix with auto-labeled classes  
✓ Cost-sensitive analysis for real-world risk modeling  
✓ Learning and validation curves with metric-based scoring  
✓ Easy integration into model evaluation pipelines  
✓ Optional return of all results in structured format  

[bold green]Example Usage:[/bold green]
>>> evaluate_model(
        model=clf,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        cost_fn=10,
        cost_fp=1,
        validation_params={'C': [0.1, 1, 10]},
        scoring_curve='f1',
        extra_plots=['threshold', 'calibration', 'ks', 'lift'],
        print_style='rich',
        return_dict=True
    )

[bold magenta]Tip:[/bold magenta] To tune hyperparameters using validation curves, make sure to wrap your model in a pipeline and prefix parameters using 'clf__'.
""")

        return


    extra_plots = extra_plots or []
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Probabilities if available
    if hasattr(model, "predict_proba"):
        y_pred_proba = model.predict_proba(X_test)[:, 1]
    elif hasattr(model, "decision_function"):
        y_pred_proba = model.decision_function(X_test)
    else:
        y_pred_proba = None

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None

    if verbose:
        print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))
        print("\nTest Set Evaluation:")
        print(f"Accuracy : {accuracy:.2f}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall   : {recall:.2f}")
        print(f"F1 Score : {f1:.2f}")
        print(f"ROC AUC  : {roc_auc:.2f}" if roc_auc is not None else "ROC AUC  : N/A")

    cm = confusion_matrix(y_test, y_pred)
    avg_cost = None
    if cost_fn is not None and cost_fp is not None:
        fn = cm[1, 0]
        fp = cm[0, 1]
        avg_cost = (cost_fn * fn + cost_fp * fp) / len(y_test)
        if verbose:
            print(f"Avg Misclassification Cost (FN={cost_fn}, FP={cost_fp}): {avg_cost:.4f}")

    if verbose:
        class_labels = list(np.unique(y_test))
        plt.figure(figsize=(10, 6))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=class_labels, yticklabels=class_labels)
        plt.xlabel("Predicted Label")
        plt.ylabel("True Label")
        plt.title("Confusion Matrix")
        plt.tight_layout()
        plt.show()

    # Threshold Tuning Plot
    if "threshold" in extra_plots and y_pred_proba is not None:
        thresholds = np.linspace(0.01, 0.99, 50)
        precisions = []
        recalls = []
        f1s = []
        for t in thresholds:
            preds = (y_pred_proba >= t).astype(int)
            precisions.append(precision_score(y_test, preds, zero_division=0))
            recalls.append(recall_score(y_test, preds, zero_division=0))
            f1s.append(f1_score(y_test, preds, zero_division=0))
        plt.figure(figsize=(10, 6))
        plt.plot(thresholds, precisions, label="Precision")
        plt.plot(thresholds, recalls, label="Recall")
        plt.plot(thresholds, f1s, label="F1 Score")
        plt.xlabel("Threshold")
        plt.ylabel("Score")
        plt.title("Threshold Tuning Curve")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    # Calibration Curve
    if "calibration" in extra_plots and y_pred_proba is not None:
        prob_true, prob_pred = calibration_curve(y_test, y_pred_proba, n_bins=10)
        plt.figure(figsize=(10, 6))
        plt.plot(prob_pred, prob_true, marker='o', label='Calibration')
        plt.plot([0, 1], [0, 1], linestyle='--', color='gray')
        plt.xlabel("Mean Predicted Probability")
        plt.ylabel("Fraction of Positives")
        plt.title("Calibration Curve")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    # KS Statistic Curve
    if "ks" in extra_plots and y_pred_proba is not None:
        from scipy.stats import ks_2samp
        positives = y_pred_proba[y_test == 1]
        negatives = y_pred_proba[y_test == 0]
        ks_stat, _ = ks_2samp(positives, negatives)
        plt.figure(figsize=(10, 6))
        sns.ecdfplot(positives, label="Positive", linestyle="-", color="blue")
        sns.ecdfplot(negatives, label="Negative", linestyle="--", color="red")
        plt.title(f"KS Curve (Statistic = {ks_stat:.2f})")
        plt.xlabel("Predicted Probability")
        plt.ylabel("ECDF")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    # Learning curve
    if cv > 1 and verbose:
        train_sizes, train_scores, test_scores = learning_curve(
            model, X_train, y_train, train_sizes=np.linspace(0.1, 1.0, 10),
            cv=cv, scoring=scoring_curve
        )
        plt.figure(figsize=(10, 6))
        plt.plot(train_sizes, np.mean(train_scores, axis=1), label="Train", marker='o')
        plt.plot(train_sizes, np.mean(test_scores, axis=1), label="Validation", marker='s', linestyle='--')
        plt.xlabel("Training Size")
        plt.ylabel(scoring_curve.capitalize())
        plt.title(f"Learning Curve: {model.__class__.__name__}")
        plt.legend()
        plt.grid()
        plt.tight_layout()
        plt.show()

    # Validation curves
    if validation_params and verbose:
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
            plt.figure(figsize=(10, 6))
            plt.plot(param_range, np.mean(train_scores, axis=1), label="Train", marker='o')
            plt.plot(param_range, np.mean(val_scores, axis=1), label="Validation", marker='s', linestyle='--')
            plt.xlabel(param_name)
            plt.ylabel(scoring_curve.capitalize())
            plt.title(f"Validation Curve: {param_name} ({model.__class__.__name__})")
            plt.legend()
            plt.grid()
            plt.tight_layout()
            plt.show()

    if return_dict:
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm,
            'avg_cost': avg_cost
        }