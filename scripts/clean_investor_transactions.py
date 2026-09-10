from pathlib import Path
import pandas as pd


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

INPUT_FILE = RAW_DATA_DIR / "08_investor_transactions.csv"
OUTPUT_FILE = PROCESSED_DATA_DIR / "08_investor_transactions_clean.csv"


# --------------------------------------------------
# 2. Load raw data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("INVESTOR TRANSACTIONS CLEANING")
print("=" * 70)

print("\nOriginal shape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nTransaction types:")
print(df["transaction_type"].value_counts())

print("\nKYC statuses:")
print(df["kyc_status"].value_counts())

print("\nAmount statistics:")
print(df["amount_inr"].describe())


# --------------------------------------------------
# 3. Clean transaction date
# --------------------------------------------------

df["transaction_date"] = pd.to_datetime(
    df["transaction_date"],
    errors="coerce"
)

print("\nInvalid transaction dates:")
print(df["transaction_date"].isna().sum())


# --------------------------------------------------
# 4. Standardize transaction types
# --------------------------------------------------

df["transaction_type"] = (
    df["transaction_type"]
    .str.strip()
    .str.title()
)

valid_transaction_types = {
    "Sip": "SIP",
    "Lumpsum": "Lumpsum",
    "Redemption": "Redemption"
}

df["transaction_type"] = df["transaction_type"].replace(
    valid_transaction_types
)

print("\nTransaction types after standardization:")
print(df["transaction_type"].value_counts())


# --------------------------------------------------
# 5. Validate transaction types
# --------------------------------------------------

allowed_types = {"SIP", "Lumpsum", "Redemption"}

invalid_types = ~df["transaction_type"].isin(allowed_types)

print("\nInvalid transaction types:")
print(invalid_types.sum())

# --------------------------------------------------
# 6. Validate transaction amounts
# --------------------------------------------------

invalid_amounts = (df["amount_inr"] <= 0).sum()

print("\nTransactions with amount <= 0:")
print(invalid_amounts)


# --------------------------------------------------
# 7. Validate KYC status
# --------------------------------------------------

df["kyc_status"] = df["kyc_status"].str.strip().str.title()

allowed_kyc_status = {"Verified", "Pending"}

invalid_kyc = ~df["kyc_status"].isin(allowed_kyc_status)

print("\nKYC statuses after standardization:")
print(df["kyc_status"].value_counts())

print("\nInvalid KYC statuses:")
print(invalid_kyc.sum())

# --------------------------------------------------
# 8. Save cleaned data
# --------------------------------------------------

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\nCleaned investor transactions saved to:")
print(OUTPUT_FILE)

print("\nFinal shape:")
print(df.shape)