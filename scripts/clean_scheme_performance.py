from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DATA_DIR / "07_scheme_performance.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "07_scheme_performance_clean.csv"


# --------------------------------------------------
# 2. Load raw data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("SCHEME PERFORMANCE CLEANING")
print("=" * 70)

print("\nOriginal shape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nExpense ratio statistics:")
print(df["expense_ratio_pct"].describe())

print("\nReturn columns:")
return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
]

for column in return_columns:
    print(f"\n{column}:")
    print(df[column].describe())


# --------------------------------------------------
# 3. Convert performance columns to numeric
# --------------------------------------------------

performance_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
    "beta",
    "sharpe_ratio",
    "sortino_ratio",
    "std_dev_ann_pct",
    "max_drawdown_pct",
    "aum_crore",
    "expense_ratio_pct",
]

for column in performance_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("\nMissing values after numeric conversion:")
print(df[performance_columns].isna().sum().sum())


# --------------------------------------------------
# 4. Validate expense ratio
# --------------------------------------------------

invalid_expense = (
    (df["expense_ratio_pct"] < 0.1) |
    (df["expense_ratio_pct"] > 2.5)
).sum()

print("\nExpense ratios outside 0.1% - 2.5%:")
print(invalid_expense)


# --------------------------------------------------
# 5. Check performance anomalies
# --------------------------------------------------

anomaly_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct",
    "alpha",
]

print("\nPerformance anomaly check:")

for column in anomaly_columns:
    print(
        f"{column}: "
        f"min={df[column].min()}, "
        f"max={df[column].max()}"
    )

# --------------------------------------------------
# 6. Save cleaned data
# --------------------------------------------------

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned scheme performance saved to:")
print(OUTPUT_FILE)

print("\nFinal shape:")
print(df.shape)