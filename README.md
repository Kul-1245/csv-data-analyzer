# CSV Data Analyzer

A lightweight command-line tool that analyzes any CSV file and generates
human-readable statistics and summaries — built with Python and pandas.

---

## Project Structure

```
csv_data_analyzer/
├── main.py            # CLI entry-point (argument parsing, display logic)
├── analyzer.py        # Core analysis module (pure functions, no I/O)
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── data/
    └── sample.csv     # Example CSV for quick testing
```

---

## Features

| Feature | Details |
|---|---|
| Row & column count | Instant shape overview |
| Column information | Name, data type, missing values & % |
| Numeric statistics | Count, mean, median, std dev, min, max, range |
| Categorical analysis | Unique count + top-N most frequent values |
| Duplicate detection | Number of duplicate rows and percentage |
| Flexible input | Pass file via `--file` flag or interactive prompt |

---

## Requirements

- Python 3.8+
- pandas 2.0+

---

## Installation

```bash
# 1. Clone or download the project
cd csv_data_analyzer

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

### Option A — Pass the file directly

```bash
python main.py --file data/sample.csv
```

### Option B — Interactive prompt

```bash
python main.py
# → Enter the path to your CSV file: data/sample.csv
```

### Option C — Show more top categorical values

```bash
python main.py --file data/sample.csv --top 10
```

### Help

```bash
python main.py --help
```

---

## Example Output

```
Loading file: data/sample.csv ...
File loaded successfully.

============================================================
  FILE OVERVIEW
============================================================
  File     : data/sample.csv
  Rows     : 30
  Columns  : 11

============================================================
  COLUMN INFORMATION
============================================================
         Column   Data Type  Missing Values  Missing %
    customer_id       int64               0       0.00
           name      object               0       0.00
            age       int64               0       0.00
           city      object               0       0.00
        country      object               0       0.00
         gender      object               0       0.00
  annual_income       int64               0       0.00
purchase_amount     float64               0       0.00
product_category      object               0       0.00
         rating     float64               0       0.00
      is_member        bool               0       0.00

============================================================
  NUMERIC COLUMN STATISTICS
============================================================
         Column  Count        Mean  Median  Std Dev    Min      Max    Range
    customer_id     30   1015.5000  1015.5   8.8034   1001     1030     29.0
            age     30     37.3000    36.5  10.5023     21       61     40.0
  annual_income     30  83566.6667   82500  28444.4  29000   145000  116000.0
purchase_amount     30   1406.2497   840.0  1531.7   35.0    5600.0   5565.0
         rating     30      4.1933     4.2    0.4007    3.5      4.9      1.4

============================================================
  CATEGORICAL COLUMN ANALYSIS
============================================================

  Column   : city
  Unique   : 6
  Top values:
    Mumbai                                      6
    Delhi                                       6
    Bangalore                                   6
    Chennai                                     6
    Hyderabad                                   6
------------------------------------------------------------
  Column   : product_category
  Unique   : 5
  Top values:
    Electronics                                13
    Clothing                                    7
    Books                                       6
    Home & Garden                               4
------------------------------------------------------------

============================================================
  DUPLICATE ROW DETECTION
============================================================
  Duplicate rows : 0
  Percentage     : 0.0%

============================================================
  Analysis complete.
============================================================
```

---

## Architecture

```
main.py  ──calls──▶  analyzer.py
   │                     │
   │  parse_args()        │  load_csv()
   │  run()               │  get_shape()
   │  print_*()           │  get_column_info()
   │                      │  get_numeric_stats()
   │                      │  get_categorical_stats()
   │                      │  get_duplicate_info()
```

`analyzer.py` contains **pure functions** with no print statements or CLI
dependencies, so it can be imported and reused in notebooks, APIs, or
other scripts without modification.

---

## Extending the Project

Some ideas for further development:

- **Export to HTML/PDF** — add a `--report` flag that saves an HTML summary
- **Correlation matrix** — detect relationships between numeric columns
- **Outlier detection** — flag values beyond 3 standard deviations
- **Chart generation** — integrate `matplotlib` for histograms and bar charts
- **Web UI** — wrap with Streamlit for a drag-and-drop browser interface

---

## License

MIT — free to use, modify, and distribute.
