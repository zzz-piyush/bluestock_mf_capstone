from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# 1. PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

HOLDINGS_PATH = BASE_DIR / "data/raw/09_portfolio_holdings.csv"

OUTPUT_PATH = BASE_DIR / "data/processed/sector_hhi.csv"

CHART_PATH = BASE_DIR / "data/processed/sector_concentration_chart.png"


# ============================================================
# 2. LOAD DATA
# ============================================================

holdings = pd.read_csv(HOLDINGS_PATH)

print("Holdings shape:", holdings.shape)
print("\nColumns:")
print(holdings.columns.tolist())


# ============================================================
# 3. CLEAN DATA
# ============================================================

holdings["sector"] = holdings["sector"].astype(str).str.strip()

holdings["weight_pct"] = pd.to_numeric(
    holdings["weight_pct"],
    errors="coerce"
)

holdings = holdings.dropna(
    subset=["sector", "weight_pct"]
)


# ============================================================
# 4. AGGREGATE SECTOR WEIGHTS
# ============================================================

sector_weights = (
    holdings
    .groupby("sector", as_index=False)["weight_pct"]
    .sum()
    .sort_values("weight_pct", ascending=False)
    .reset_index(drop=True)
)


# ============================================================
# 5. CONVERT PERCENTAGE TO PROPORTION
# ============================================================

sector_weights["weight_proportion"] = (
    sector_weights["weight_pct"] / 100
)


# ============================================================
# 6. CALCULATE HHI CONTRIBUTION
# ============================================================

sector_weights["hhi_contribution"] = (
    sector_weights["weight_proportion"] ** 2
)


# HHI on 0-1 scale
hhi = sector_weights["hhi_contribution"].sum()

# HHI on 0-10,000 scale
hhi_10000 = hhi * 10000


# ============================================================
# 7. TOP 5 CONCENTRATION
# ============================================================

top5_concentration = (
    sector_weights
    .head(5)["weight_pct"]
    .sum()
)


# ============================================================
# 8. EFFECTIVE NUMBER OF SECTORS
# ============================================================

effective_number_sectors = (
    1 / hhi
    if hhi > 0
    else np.nan
)


# ============================================================
# 9. ADD SUMMARY COLUMNS
# ============================================================

sector_weights["overall_hhi"] = hhi
sector_weights["overall_hhi_10000"] = hhi_10000
sector_weights["top5_concentration_pct"] = top5_concentration
sector_weights["effective_number_of_sectors"] = (
    effective_number_sectors
)


# ============================================================
# 10. DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 70)
print("SECTOR CONCENTRATION ANALYSIS")
print("=" * 70)

print("\nSector Weights:")
print(
    sector_weights[
        [
            "sector",
            "weight_pct",
            "hhi_contribution"
        ]
    ].to_string(index=False)
)

print("\n" + "-" * 70)
print(f"HHI (0-1 scale): {hhi:.4f}")
print(f"HHI (0-10,000 scale): {hhi_10000:.2f}")
print(f"Top 5 sector concentration: {top5_concentration:.2f}%")
print(
    f"Effective number of sectors: "
    f"{effective_number_sectors:.2f}"
)


# ============================================================
# 11. SAVE REPORT
# ============================================================

sector_weights.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nSaved report to:")
print(OUTPUT_PATH)


# ============================================================
# 12. CREATE CHART
# ============================================================

plt.figure(figsize=(12, 6))

plt.bar(
    sector_weights["sector"],
    sector_weights["weight_pct"]
)

plt.title("Sector Concentration of Portfolio Holdings")
plt.xlabel("Sector")
plt.ylabel("Weight (%)")

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    CHART_PATH,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("\nSaved chart to:")
print(CHART_PATH)