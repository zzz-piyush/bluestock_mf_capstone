from pathlib import Path
import pandas as pd


# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Raw data directory
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Load fund master
file_path = RAW_DATA_DIR / "01_fund_master.csv"

df = pd.read_csv(file_path)


print("\n" + "=" * 70)
print("FUND MASTER ANALYSIS")
print("=" * 70)


print("\nTotal schemes:")
print(len(df))


print("\nUnique fund houses:")
print(df["fund_house"].unique())


print("\nNumber of fund houses:")
print(df["fund_house"].nunique())


print("\nCategories:")
print(df["category"].unique())


print("\nSub-categories:")
print(df["sub_category"].unique())


print("\nRisk categories:")
print(df["risk_category"].unique())


print("\nSchemes per fund house:")
print(df["fund_house"].value_counts())


print("\nSchemes per category:")
print(df["category"].value_counts())


print("\nSchemes per risk category:")
print(df["risk_category"].value_counts())
