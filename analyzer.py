"""
analyzer.py
-----------
Core analysis module for the CSV Data Analyzer project.
Handles all data loading, inspection, and statistical computations
using pandas. This module is intentionally separated from the CLI
so it can also be imported as a library in other projects.
"""

import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────
# 1. LOADING
# ─────────────────────────────────────────────

def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded data.

    Raises
    ------
    FileNotFoundError
        If the given path does not exist.
    ValueError
        If the file cannot be parsed as CSV.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    if path.suffix.lower() != ".csv":
        raise ValueError(f"Expected a .csv file, got: {path.suffix}")

    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        raise ValueError(f"Could not parse CSV: {e}")

    return df


# ─────────────────────────────────────────────
# 2. OVERVIEW
# ─────────────────────────────────────────────

def get_shape(df: pd.DataFrame) -> dict:
    """
    Return the number of rows and columns in the DataFrame.

    Returns
    -------
    dict
        {"rows": int, "columns": int}
    """
    rows, cols = df.shape
    return {"rows": rows, "columns": cols}


def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary table of column names, data types, and
    the count of missing (null) values per column.

    Returns
    -------
    pd.DataFrame
        Columns: ["Column", "Data Type", "Missing Values", "Missing %"]
    """
    info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.values,
        "Missing Values": df.isnull().sum().values,
        "Missing %": (df.isnull().mean().values * 100).round(2),
    })
    return info.reset_index(drop=True)


# ─────────────────────────────────────────────
# 3. NUMERIC STATISTICS
# ─────────────────────────────────────────────

def get_numeric_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute descriptive statistics for every numeric column.

    Statistics calculated:
      - count  : number of non-null values
      - mean   : arithmetic average
      - median : middle value (50th percentile)
      - std    : standard deviation
      - min    : minimum value
      - max    : maximum value
      - range  : max - min

    Returns
    -------
    pd.DataFrame
        One row per numeric column. Returns an empty DataFrame
        if no numeric columns are found.
    """
    # Select only numeric columns
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.empty:
        return pd.DataFrame()

    stats = pd.DataFrame({
        "Column": numeric_df.columns,
        "Count":  numeric_df.count().values,
        "Mean":   numeric_df.mean().round(4).values,
        "Median": numeric_df.median().round(4).values,
        "Std Dev": numeric_df.std().round(4).values,
        "Min":    numeric_df.min().values,
        "Max":    numeric_df.max().values,
        "Range":  (numeric_df.max() - numeric_df.min()).values,
    })
    return stats.reset_index(drop=True)


# ─────────────────────────────────────────────
# 4. CATEGORICAL STATISTICS
# ─────────────────────────────────────────────

def get_categorical_stats(df: pd.DataFrame, top_n: int = 5) -> dict:
    """
    Analyse categorical (object / boolean) columns.

    For each categorical column this function returns:
      - unique_count : total number of distinct values
      - top_values   : the `top_n` most frequent values with their counts

    Parameters
    ----------
    df    : pd.DataFrame
    top_n : int
        How many top values to display per column (default 5).

    Returns
    -------
    dict
        {column_name: {"unique_count": int, "top_values": pd.Series}}
        Returns an empty dict if no categorical columns are found.
    """
    # Include object and boolean columns
    cat_df = df.select_dtypes(include=["object", "bool", "category"])

    if cat_df.empty:
        return {}

    result = {}
    for col in cat_df.columns:
        value_counts = cat_df[col].value_counts()
        result[col] = {
            "unique_count": cat_df[col].nunique(),
            "top_values": value_counts.head(top_n),
        }
    return result


# ─────────────────────────────────────────────
# 5. DUPLICATE DETECTION
# ─────────────────────────────────────────────

def get_duplicate_info(df: pd.DataFrame) -> dict:
    """
    Detect fully duplicate rows in the DataFrame.

    Returns
    -------
    dict
        {"duplicate_rows": int, "duplicate_percentage": float}
    """
    dup_count = int(df.duplicated().sum())
    dup_pct = round((dup_count / len(df)) * 100, 2) if len(df) > 0 else 0.0
    return {
        "duplicate_rows": dup_count,
        "duplicate_percentage": dup_pct,
    }
