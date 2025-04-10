
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import kurtosis, skew, entropy
from tabulate import tabulate
from IPython.display import display, HTML

def summary_dataframe(df: pd.DataFrame, verbose: bool = True, return_dataframes: bool = False,
                      detailing: bool = False, correlation_matrix: bool = False):
    """
    Generate a summary for a DataFrame with optional deep statistics.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    verbose (bool): If True, displays the output.
    return_dataframes (bool): If True, returns the DataFrames.
    detailing (bool): If True, runs detailed computations (slow for large data).
    correlation_matrix (bool): If True, computes the correlation matrix.

    Returns (optional):
    - summary (pd.DataFrame)
    - desc_numeric (pd.DataFrame)
    - desc_categorical (pd.DataFrame)
    - correlation_matrix (pd.DataFrame or None)
    """
    if df.empty:
        raise ValueError("The provided DataFrame is empty. Provide a valid dataset.")

    total_rows = df.shape[0]
    numeric_df = df.select_dtypes(include=["number"])
    categorical_df = df.select_dtypes(include=["object", "category"])

    summary = pd.DataFrame({
        "Column Name": df.columns,
        "Data Type": df.dtypes.values,
        "Total Values": df.count().values,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (df.isnull().sum().values / total_rows * 100).round(2),
        "Unique Values": df.nunique().values,
        "Unique %": (df.nunique().values / total_rows * 100).round(2)
    })

    summary["Constant Column"] = summary["Unique Values"] == 1
    summary["Cardinality Category"] = summary["Unique Values"].apply(
        lambda x: "Low" if x <= 10 else "Medium" if x <= 100 else "High"
    )

    if detailing:
        duplicate_rows = df.duplicated().sum()
        try:
            duplicate_columns = df.T.duplicated().sum()
        except Exception:
            duplicate_columns = "Too large to compute"

        if not numeric_df.empty:
            desc_numeric = numeric_df.describe().transpose()
            desc_numeric["Skewness"] = numeric_df.apply(lambda x: skew(x.dropna()), axis=0)
            desc_numeric["Kurtosis"] = numeric_df.apply(lambda x: kurtosis(x.dropna()), axis=0)
            desc_numeric["Z-score Outliers"] = numeric_df.apply(
                lambda x: (np.abs((x - x.mean()) / x.std()) > 3).sum(), axis=0
            )
        else:
            desc_numeric = None

        if not categorical_df.empty:
            desc_categorical = categorical_df.describe().transpose()
            desc_categorical["Entropy"] = categorical_df.apply(
                lambda x: entropy(x.value_counts(normalize=True), base=2) if x.nunique() > 1 else 0
            )
        else:
            desc_categorical = None
    else:
        duplicate_rows = None
        duplicate_columns = None
        desc_numeric = numeric_df.describe().transpose() if not numeric_df.empty else None
        desc_categorical = categorical_df.describe().transpose() if not categorical_df.empty else None

    corr_matrix = numeric_df.corr() if (not numeric_df.empty and correlation_matrix) else None

    if verbose:
        def show_df(df_, title):
            if df_ is not None:
                html = df_.to_html(classes='scroll-table', escape=False)
                display(HTML(f"<h3>{title}</h3>" + html))

        display(HTML("""
        <style>
        .scroll-table {
            display: block;
            max-height: 400px;
            overflow-y: auto;
            overflow-x: auto;
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 14px;
        }
        </style>
        """))

        show_df(summary, "Summary Statistics")
        show_df(desc_numeric, "Descriptive Statistics (Numerical)")
        show_df(desc_categorical, "Descriptive Statistics (Categorical)")
        show_df(corr_matrix, "Correlation Matrix")

        if detailing:
            print(f"\nTotal Duplicate Rows: {duplicate_rows}")
            print(f"Total Duplicate Columns: {duplicate_columns}")

    if return_dataframes:
        return summary, desc_numeric, desc_categorical, corr_matrix



def summary_column(df: pd.DataFrame, column_name: str, top_n: int = 10,
                   verbose: bool = True, return_dataframes: bool = False,
                   detailing: bool = True, time_column: str = None,
                   plots: list = None):
    """
    Enhanced summary for a single column with optional deep stats and plotting.

    Parameters:
    - df: DataFrame
    - column_name: column to summarize
    - top_n: top N value counts to show
    - verbose: print stats
    - return_dataframes: return output tables
    - detailing: compute detailed stats + plots
    - time_column: datetime column to check missingness over time
    - plots: list of plots to show ['histogram', 'bar', 'missing_trend']
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in the DataFrame.")

    plots = plots or []

    column_data = df[column_name]
    data_type = column_data.dtype
    total_count = len(column_data)
    missing_values = column_data.isnull().sum()
    unique_values = column_data.nunique()
    non_missing_values = total_count - missing_values

    desc_stats = column_data.describe(include="all").to_frame()
    additional_stats = {}

    if np.issubdtype(data_type, np.number):
        additional_stats["Variance"] = column_data.var()
        additional_stats["IQR"] = column_data.quantile(0.75) - column_data.quantile(0.25)
        additional_stats["Mode"] = column_data.mode().values[0] if not column_data.mode().empty else np.nan
        additional_stats["Min"] = column_data.min()
        additional_stats["Max"] = column_data.max()

        if detailing:
            if non_missing_values > 1:
                additional_stats["Skewness"] = skew(column_data.dropna())
                additional_stats["Kurtosis"] = kurtosis(column_data.dropna())
            else:
                additional_stats["Skewness"] = np.nan
                additional_stats["Kurtosis"] = np.nan

            mean = column_data.mean()
            std = column_data.std()
            additional_stats["Z-score Outlier Count"] = ((np.abs((column_data - mean) / std) > 3).sum()) if std > 0 else 0

    elif data_type == "object" or data_type.name == "category":
        additional_stats["Mode"] = column_data.mode().values[0] if not column_data.mode().empty else "N/A"
        if detailing and unique_values < 10000:
            value_probs = column_data.value_counts(normalize=True)
            additional_stats["Entropy"] = entropy(value_probs, base=2) if unique_values > 1 else 0

    # ✅ Value Counts (Always computed)
    freq_dist = column_data.value_counts(dropna=False).reset_index().head(top_n)
    freq_dist.columns = ["Value", "Count"]
    freq_dist["Percentage"] = (freq_dist["Count"] / total_count * 100).round(2).astype(str) + " %"

    # Summary Table
    summary_table = pd.DataFrame([
        ["Data Type", data_type],
        ["Total Values", total_count],
        ["Non-Missing Values", non_missing_values],
        ["Missing Values", missing_values],
        ["Missing %", round((missing_values / total_count * 100), 2) if total_count > 0 else 0],
        ["Unique Values", unique_values],
    ] + list(additional_stats.items()), columns=["Metric", "Value"])

    if verbose:
        print("\n" + "=" * 100)
        print(f"Analysis for Column: {column_name}")
        print("=" * 100)

        print("\nSummary Statistics:")
        print(tabulate(summary_table, headers="keys", tablefmt="fancy_grid", showindex=False))

        print("\nDescriptive Statistics:")
        print(tabulate(desc_stats, headers="keys", tablefmt="fancy_grid"))

        if not freq_dist.empty:
            print(f"\nTop {top_n} Value Counts:")
            print(tabulate(freq_dist, headers="keys", tablefmt="fancy_grid"))

    # 🔍 Plots (only if detailing=True)
    if detailing:
        if np.issubdtype(data_type, np.number) and "histogram" in plots:
            plt.figure(figsize=(10, 4))
            column_data.hist(bins=30, edgecolor='black')
            plt.title(f"Histogram of {column_name}")
            plt.xlabel(column_name)
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        elif (data_type == "object" or data_type.name == "category") and "bar" in plots:
            if not freq_dist.empty:
                plt.figure(figsize=(10, 4))
                freq_dist.plot(kind="bar", x="Value", y="Count", legend=False)
                plt.title(f"Top {top_n} Categories in {column_name}")
                plt.xticks(rotation=45, ha='right')
                plt.ylabel("Count")
                plt.tight_layout()
                plt.show()

        if time_column and time_column in df.columns and "missing_trend" in plots:
            if pd.api.types.is_datetime64_any_dtype(df[time_column]):
                missing_series = df.set_index(time_column)[column_name].isnull().resample("W").mean()
                missing_series.plot(figsize=(10, 3), title=f"Missing Rate Over Time for {column_name}")
                plt.ylabel("Missing %")
                plt.grid(True)
                plt.tight_layout()
                plt.show()

    if return_dataframes:
        return summary_table, desc_stats, freq_dist
