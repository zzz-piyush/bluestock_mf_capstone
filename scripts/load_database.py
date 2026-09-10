from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# 1. Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
DB_DIR = PROJECT_ROOT / "db"
SCHEMA_FILE = PROJECT_ROOT / "sql" / "schema.sql"

DB_DIR.mkdir(parents=True, exist_ok=True)

DB_FILE = DB_DIR / "bluestock_mf.db"

engine = create_engine(
    f"sqlite:///{DB_FILE}"
)


# ============================================================
# 2. Load datasets
# ============================================================

fund_df = pd.read_csv(
    PROCESSED_DATA_DIR / "01_fund_master.csv"
)

nav_df = pd.read_csv(
    PROCESSED_DATA_DIR / "02_nav_history_clean.csv"
)

transaction_df = pd.read_csv(
    PROCESSED_DATA_DIR / "08_investor_transactions_clean.csv"
)

performance_df = pd.read_csv(
    PROCESSED_DATA_DIR / "07_scheme_performance_clean.csv"
)

aum_df = pd.read_csv(
    RAW_DATA_DIR / "03_aum_by_fund_house.csv"
)


# ============================================================
# 3. Prepare dates
# ============================================================

fund_df["launch_date"] = pd.to_datetime(
    fund_df["launch_date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

nav_df["date"] = pd.to_datetime(
    nav_df["date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

transaction_df["transaction_date"] = pd.to_datetime(
    transaction_df["transaction_date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")

aum_df["date"] = pd.to_datetime(
    aum_df["date"],
    errors="coerce"
).dt.strftime("%Y-%m-%d")


# ============================================================
# 4. Create Date Dimension
# ============================================================

all_dates = pd.concat([
    nav_df["date"],
    transaction_df["transaction_date"],
    aum_df["date"]
]).dropna().unique()

date_df = pd.DataFrame({
    "date": sorted(all_dates)
})

date_df["date"] = pd.to_datetime(date_df["date"])

date_df["year"] = date_df["date"].dt.year
date_df["month"] = date_df["date"].dt.month
date_df["month_name"] = date_df["date"].dt.month_name()
date_df["quarter"] = date_df["date"].dt.quarter

date_df["date"] = date_df["date"].dt.strftime("%Y-%m-%d")


# ============================================================
# 5. Recreate database using schema.sql
# ============================================================

schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")

with engine.begin() as connection:

    # Enable foreign key enforcement in SQLite
    connection.execute(text("PRAGMA foreign_keys = ON"))

    # Drop existing tables
    connection.execute(text("DROP TABLE IF EXISTS fact_nav"))
    connection.execute(text("DROP TABLE IF EXISTS fact_transactions"))
    connection.execute(text("DROP TABLE IF EXISTS fact_performance"))
    connection.execute(text("DROP TABLE IF EXISTS fact_aum"))
    connection.execute(text("DROP TABLE IF EXISTS dim_fund"))
    connection.execute(text("DROP TABLE IF EXISTS dim_date"))

    # Execute each CREATE TABLE statement
    for statement in schema_sql.split(";"):
        statement = statement.strip()

        if statement:
            connection.execute(text(statement))


# ============================================================
# 6. Load data into existing tables
# ============================================================

fund_df.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False
)

date_df.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

nav_df.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False
)

transaction_df.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False
)

performance_df.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False
)

aum_df.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False
)


# ============================================================
# 7. Verify row counts
# ============================================================

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

print("=" * 70)
print("DATABASE LOAD COMPLETE")
print("=" * 70)

with engine.connect() as connection:

    for table in tables:

        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )

        count = result.scalar()

        print(f"{table:25} {count:,} rows")


print("\nDatabase:")
print(DB_FILE)