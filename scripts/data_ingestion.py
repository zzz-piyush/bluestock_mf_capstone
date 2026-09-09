from pathlib import Path
import pandas as pd


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


# All datasets provided for the project
files = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv",
]


for file in files:

    file_path = RAW_DATA_DIR / file

    print("\n" + "=" * 70)
    print(f"FILE: {file}")
    print("=" * 70)

    df = pd.read_csv(file_path)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())