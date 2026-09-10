from pathlib import Path
from sqlalchemy import create_engine, text


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE = PROJECT_ROOT / "db" / "bluestock_mf.db"

engine = create_engine(
    f"sqlite:///{DB_FILE}"
)

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

print("=" * 70)
print("DATABASE SCHEMA VERIFICATION")
print("=" * 70)

with engine.connect() as connection:

    for table in tables:

        print(f"\nTABLE: {table}")
        print("-" * 50)

        result = connection.execute(
            text(f"PRAGMA table_info({table})")
        )

        for row in result:
            print(
                f"Column: {row[1]:25} "
                f"Type: {row[2]:10} "
                f"Primary Key: {row[5]}"
            )
            