from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

SCORECARD_PATH = BASE_DIR / "data/processed/fund_scorecard.csv"
PERFORMANCE_PATH = BASE_DIR / "data/processed/cagr_report.csv"
MASTER_PATH = BASE_DIR / "data/processed/01_fund_master.csv"

OUTPUT_PATH = BASE_DIR / "data/processed/fund_recommendations.csv"


# ============================================================
# 2. LOAD DATA
# ============================================================

scorecard = pd.read_csv(SCORECARD_PATH)
performance = pd.read_csv(PERFORMANCE_PATH)
fund_master = pd.read_csv(MASTER_PATH)

print("Scorecard shape:", scorecard.shape)
print("Performance shape:", performance.shape)
print("Fund master shape:", fund_master.shape)


# ============================================================
# 3. MERGE FUND INFORMATION
# ============================================================

funds = (
    fund_master[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "sub_category",
            "risk_category",
            "expense_ratio_pct",
            "min_sip_amount",
        ]
    ]
    .drop_duplicates("amfi_code")
)

recommendations = funds.merge(
    scorecard[
        [
            "amfi_code",
            "Overall_Score",
            "Overall_Rank",
        ]
    ],
    on="amfi_code",
    how="left"
)

recommendations = recommendations.merge(
    performance[
        [
            "amfi_code",
            "CAGR_Till_Date_pct",
        ]
    ],
    on="amfi_code",
    how="left"
)


# ============================================================
# 4. NORMALIZE PERFORMANCE VARIABLES
# ============================================================

def min_max_score(series):
    """
    Convert values into a 0-100 scale.
    Higher original value = higher score.
    """
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(50, index=series.index)

    return ((series - minimum) / (maximum - minimum)) * 100


recommendations["return_score"] = min_max_score(
    recommendations["CAGR_Till_Date_pct"]
)

recommendations["overall_score_norm"] = min_max_score(
    recommendations["Overall_Score"]
)


# ============================================================
# 5. RISK SCORE
# ============================================================

risk_score_map = {
    "Low": 100,
    "Moderate": 80,
    "Moderately High": 60,
    "High": 40,
    "Very High": 20,
}

recommendations["risk_score"] = (
    recommendations["risk_category"]
    .map(risk_score_map)
    .fillna(50)
)


# ============================================================
# 6. CATEGORY / HORIZON LOGIC
# ============================================================

def horizon_score(row, horizon):
    """
    Score fund suitability according to investment horizon.
    """

    category = str(row["category"]).lower()
    sub_category = str(row["sub_category"]).lower()

    # Short horizon: prefer lower-risk categories
    if horizon == "Short":

        if "liquid" in category or "liquid" in sub_category:
            return 100

        if "debt" in category or "gilt" in sub_category:
            return 85

        if "hybrid" in category:
            return 60

        return 30

    # Medium horizon
    elif horizon == "Medium":

        if "hybrid" in category:
            return 90

        if "debt" in category:
            return 80

        if "large" in category:
            return 75

        if "flexi" in category:
            return 75

        if "mid" in category:
            return 60

        if "small" in category:
            return 45

        return 60

    # Long horizon
    else:

        if "small" in category:
            return 95

        if "mid" in category:
            return 90

        if "flexi" in category:
            return 90

        if "large" in category:
            return 85

        if "equity" in category:
            return 85

        if "hybrid" in category:
            return 70

        return 50


# ============================================================
# 7. RECOMMENDATION FUNCTION
# ============================================================

def recommend_funds(
    investor_risk="Moderate",
    investment_horizon="Long",
    top_n=5
):

    df = recommendations.copy()

    # --------------------------------------------------------
    # Risk compatibility
    # --------------------------------------------------------

    risk_order = {
        "Low": 1,
        "Moderate": 2,
        "Moderately High": 3,
        "High": 4,
        "Very High": 5,
    }

    investor_risk_level = risk_order.get(
        investor_risk,
        2
    )

    df["risk_level"] = df["risk_category"].map(risk_order)

    # Penalize funds whose risk is far from investor preference
    df["risk_match_score"] = (
        100
        - abs(df["risk_level"] - investor_risk_level) * 25
    )

    df["risk_match_score"] = df["risk_match_score"].clip(
        lower=0,
        upper=100
    )

    # --------------------------------------------------------
    # Horizon suitability
    # --------------------------------------------------------

    df["horizon_score"] = df.apply(
        lambda row: horizon_score(
            row,
            investment_horizon
        ),
        axis=1
    )

    # --------------------------------------------------------
    # Final recommendation score
    #
    # 35% overall fund score
    # 25% risk match
    # 20% horizon suitability
    # 20% historical return
    # --------------------------------------------------------

    df["recommendation_score"] = (
        df["overall_score_norm"] * 0.35
        + df["risk_match_score"] * 0.25
        + df["horizon_score"] * 0.20
        + df["return_score"] * 0.20
    )

    # --------------------------------------------------------
    # Rank recommendations
    # --------------------------------------------------------

    df = df.sort_values(
        "recommendation_score",
        ascending=False
    ).reset_index(drop=True)

    df["recommendation_rank"] = (
        df.index + 1
    )

    # --------------------------------------------------------
    # Recommendation reason
    # --------------------------------------------------------

    def reason(row):

        return (
            f"{row['risk_category']} risk profile, "
            f"{investment_horizon.lower()}-term suitability, "
            f"historical return of "
            f"{row['CAGR_Till_Date_pct']:.2f}% "
            f"and overall fund score of "
            f"{row['Overall_Score']:.2f}"
        )

    df["recommendation_reason"] = df.apply(
        reason,
        axis=1
    )

    return df.head(top_n)


# ============================================================
# 8. EXAMPLE RECOMMENDATIONS
# ============================================================

print("\n" + "=" * 70)
print("MODERATE RISK + LONG HORIZON")
print("=" * 70)

moderate_long = recommend_funds(
    investor_risk="Moderate",
    investment_horizon="Long",
    top_n=5
)

print(
    moderate_long[
        [
            "recommendation_rank",
            "scheme_name",
            "category",
            "risk_category",
            "CAGR_Till_Date_pct",
            "recommendation_score",
        ]
    ].to_string(index=False)
)


# ============================================================
# 9. SAVE RESULTS
# ============================================================

moderate_long.to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nSaved to:")
print(OUTPUT_PATH)

print("\nRecommendation model completed successfully.")