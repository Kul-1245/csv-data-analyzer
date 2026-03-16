"""
main.py
-------
CLI entry-point for the CSV Data Analyzer.

Usage
-----
    python main.py                        # prompts for file path interactively
    python main.py --file data/sample.csv # pass the file directly as an argument
    python main.py --file data/sample.csv --top 10  # show top-10 categorical values
"""

import argparse
import sys

from analyzer import (
    load_csv,
    get_shape,
    get_column_info,
    get_numeric_stats,
    get_categorical_stats,
    get_duplicate_info,
)


# ─────────────────────────────────────────────
# DISPLAY HELPERS
# ─────────────────────────────────────────────

SEPARATOR = "=" * 60
THIN_SEP  = "-" * 60


def print_section(title: str) -> None:
    """Print a clearly visible section header."""
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


def print_overview(filepath: str, shape: dict) -> None:
    """Print file path and basic shape information."""
    print_section("FILE OVERVIEW")
    print(f"  File     : {filepath}")
    print(f"  Rows     : {shape['rows']:,}")
    print(f"  Columns  : {shape['columns']}")


def print_column_info(col_info) -> None:
    """Print the column summary table."""
    print_section("COLUMN INFORMATION")
    print(col_info.to_string(index=False))


def print_numeric_stats(stats) -> None:
    """Print numeric statistics table."""
    print_section("NUMERIC COLUMN STATISTICS")
    if stats.empty:
        print("  No numeric columns found.")
        return
    print(stats.to_string(index=False))


def print_categorical_stats(cat_stats: dict) -> None:
    """Print categorical column analysis."""
    print_section("CATEGORICAL COLUMN ANALYSIS")
    if not cat_stats:
        print("  No categorical columns found.")
        return

    for col, data in cat_stats.items():
        print(f"\n  Column   : {col}")
        print(f"  Unique   : {data['unique_count']}")
        print(f"  Top values:")
        for val, count in data["top_values"].items():
            # Truncate long values to keep output tidy
            display_val = str(val)[:40]
            print(f"    {display_val:<42}  {count:,}")
        print(THIN_SEP)


def print_duplicate_info(dup_info: dict) -> None:
    """Print duplicate row summary."""
    print_section("DUPLICATE ROW DETECTION")
    print(f"  Duplicate rows : {dup_info['duplicate_rows']:,}")
    print(f"  Percentage     : {dup_info['duplicate_percentage']}%")


# ─────────────────────────────────────────────
# ARGUMENT PARSING
# ─────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """
    Define and parse CLI arguments.

    --file : path to CSV file (optional; will prompt if omitted)
    --top  : number of top categorical values to show (default 5)
    """
    parser = argparse.ArgumentParser(
        prog="csv_analyzer",
        description="CSV Data Analyzer — Generate statistics and summaries from any CSV file.",
    )
    parser.add_argument(
        "--file", "-f",
        type=str,
        help="Path to the CSV file you want to analyze.",
    )
    parser.add_argument(
        "--top", "-t",
        type=int,
        default=5,
        help="Number of top values to display for categorical columns (default: 5).",
    )
    return parser.parse_args()


# ─────────────────────────────────────────────
# MAIN WORKFLOW
# ─────────────────────────────────────────────

def run(filepath: str, top_n: int) -> None:
    """
    Orchestrate the full analysis pipeline:
      1. Load the CSV
      2. Compute all statistics
      3. Print results to the terminal
    """
    # ── Step 1: Load ──────────────────────────
    print(f"\nLoading file: {filepath} ...")
    try:
        df = load_csv(filepath)
    except (FileNotFoundError, ValueError) as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

    print("File loaded successfully.\n")

    # ── Step 2: Compute ───────────────────────
    shape      = get_shape(df)
    col_info   = get_column_info(df)
    num_stats  = get_numeric_stats(df)
    cat_stats  = get_categorical_stats(df, top_n=top_n)
    dup_info   = get_duplicate_info(df)

    # ── Step 3: Display ───────────────────────
    print_overview(filepath, shape)
    print_column_info(col_info)
    print_numeric_stats(num_stats)
    print_categorical_stats(cat_stats)
    print_duplicate_info(dup_info)

    print(f"\n{SEPARATOR}")
    print("  Analysis complete.")
    print(f"{SEPARATOR}\n")


def main() -> None:
    """Parse arguments and kick off the analysis."""
    args = parse_args()

    # If --file was not provided, prompt the user interactively
    filepath = args.file
    if not filepath:
        filepath = input("Enter the path to your CSV file: ").strip()
        if not filepath:
            print("[ERROR] No file path provided. Exiting.")
            sys.exit(1)

    run(filepath=filepath, top_n=args.top)


if __name__ == "__main__":
    main()
