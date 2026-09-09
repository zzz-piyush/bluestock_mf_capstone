from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

fund_master = pd.read_csv(RAW_DATA_DIR / "01_fund_master.csv")
nav_history = pd.read_csv(RAW_DATA_DIR / "02_nav_history.csv")

fund_codes = set(fund_master["amfi_code"])
nav_codes = set(nav_history["amfi_code"])

missing_codes = fund_codes - nav_codes

print("\n" + "=" * 70)
print("AMFI CODE VALIDATION")
print("=" * 70)

print(f"\nFund master AMFI codes: {len(fund_codes)}")
print(f"NAV history AMFI codes: {len(nav_codes)}")
print(f"Missing AMFI codes: {len(missing_codes)}")

if missing_codes:
    print("\nMissing AMFI codes:")
    print(sorted(missing_codes))
else:
    print("\nSUCCESS: All fund master AMFI codes exist in NAV history.")