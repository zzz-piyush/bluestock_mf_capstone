from pathlib import Path
import requests
import pandas as pd


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------
# Schemes to fetch
# --------------------------------------------------

schemes = {
    "HDFC_Top_100": "125497",
    "SBI_Bluechip": "119551",
    "ICICI_Bluechip": "120503",
    "Nippon_Large_Cap": "118632",
    "Axis_Bluechip": "119092",
    "Kotak_Bluechip": "120841",
}


# --------------------------------------------------
# Fetch NAV data
# --------------------------------------------------

for scheme_name, scheme_code in schemes.items():

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print("\n" + "=" * 70)
    print(f"Fetching: {scheme_name}")
    print(f"Scheme Code: {scheme_code}")
    print("=" * 70)

    success = False

    # Try the API up to 3 times
    for attempt in range(1, 4):

        try:
            print(f"Attempt {attempt}/3...")

            response = requests.get(
                url,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()
            nav_data = data.get("data", [])

            if not nav_data:
                print("No NAV data returned.")
                break

            df = pd.DataFrame(nav_data)

            print(f"Rows fetched: {len(df)}")
            print(f"Columns: {df.columns.tolist()}")

            output_file = RAW_DATA_DIR / f"live_nav_{scheme_code}.csv"

            df.to_csv(output_file, index=False)

            print(f"Saved to: {output_file}")

            success = True
            break

        except requests.exceptions.RequestException as e:

            print(f"Request failed: {e}")

            if attempt < 3:
                print("Retrying...\n")
            else:
                print(
                    f"Could not fetch {scheme_name} "
                    f"after 3 attempts."
                )

    if not success:
        print(f"SKIPPED: {scheme_name}")