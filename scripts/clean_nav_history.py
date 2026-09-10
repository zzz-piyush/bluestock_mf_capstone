from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DATA_DIR / "02_nav_history.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "02_nav_history_clean.csv"


# --------------------------------------------------
# 2. Load raw data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("NAV HISTORY CLEANING")
print("=" * 70)

print("\nOriginal shape:")
print(df.shape)

print("\nOriginal data types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

# --------------------------------------------------
# 3. Convert date to datetime
# --------------------------------------------------

df["date"] = pd.to_datetime(df["date"], errors="coerce")

print("\nData types after date conversion:")
print(df.dtypes)

print("\nInvalid dates:")
print(df["date"].isna().sum())


# --------------------------------------------------
# 4. Sort data
# --------------------------------------------------

df = df.sort_values(
    by=["amfi_code", "date"]
).reset_index(drop=True)

print("\nData after sorting:")
print(df.head(10))

# --------------------------------------------------
# 5. Check and remove duplicates
# --------------------------------------------------

duplicates = df.duplicated(
    subset=["amfi_code", "date"]
).sum()

print("\nDuplicate fund-date records:")
print(duplicates)

if duplicates > 0:
    df = df.drop_duplicates(
        subset=["amfi_code", "date"],
        keep="last"
    ).reset_index(drop=True)

print("\nShape after duplicate removal:")
print(df.shape)


# --------------------------------------------------
# 6. Forward-fill missing NAV values
# --------------------------------------------------

missing_before = df["nav"].isna().sum()

df["nav"] = df.groupby("amfi_code")["nav"].ffill()

missing_after = df["nav"].isna().sum()

print("\nMissing NAV before forward-fill:")
print(missing_before)

print("\nMissing NAV after forward-fill:")
print(missing_after)


# --------------------------------------------------
# 7. Validate NAV values
# --------------------------------------------------

invalid_nav = (df["nav"] <= 0).sum()

print("\nNAV values <= 0:")
print(invalid_nav)

if invalid_nav > 0:
    print("\nWARNING: Invalid NAV values found.")
else:
    print("\nSUCCESS: All NAV values are greater than 0.")


# --------------------------------------------------
# 8. Save cleaned data
# --------------------------------------------------

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned NAV history saved to:")
print(OUTPUT_FILE)

print("\nFinal shape:")
print(df.shape)