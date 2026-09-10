import sqlite3

DB_PATH = "db/bluestock_mf.db"

connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

queries = [
    (
        "QUERY 1: TOP 5 FUNDS BY AUM",
        """
        SELECT
            scheme_name,
            fund_house,
            ROUND(aum_crore, 2) AS aum_crore
        FROM fact_performance
        ORDER BY aum_crore DESC
        LIMIT 5;
        """
    ),

    (
        "QUERY 2: AVERAGE NAV BY MONTH",
        """
        SELECT
            strftime('%Y-%m', date) AS month,
            ROUND(AVG(nav), 2) AS average_nav
        FROM fact_nav
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month;
        """
    ),

    (
        "QUERY 3: SIP YEAR-OVER-YEAR GROWTH",
        """
        WITH yearly_sip AS (
            SELECT
                strftime('%Y', transaction_date) AS year,
                SUM(amount_inr) AS total_sip_amount
            FROM fact_transactions
            WHERE transaction_type = 'SIP'
            GROUP BY strftime('%Y', transaction_date)
        )

        SELECT
            year,
            ROUND(total_sip_amount, 2) AS total_sip_amount,
            ROUND(
                (
                    total_sip_amount
                    - LAG(total_sip_amount) OVER (ORDER BY year)
                ) * 100.0
                / NULLIF(
                    LAG(total_sip_amount) OVER (ORDER BY year),
                    0
                ),
                2
            ) AS yoy_growth_pct
        FROM yearly_sip
        ORDER BY year;
        """
    ),

    (
        "QUERY 4: TRANSACTIONS BY STATE",
        """
        SELECT
            state,
            COUNT(*) AS transaction_count,
            ROUND(SUM(amount_inr), 2) AS total_transaction_amount
        FROM fact_transactions
        GROUP BY state
        ORDER BY total_transaction_amount DESC;
        """
    ),

    (
        "QUERY 5: FUNDS WITH EXPENSE RATIO BELOW 1%",
        """
        SELECT
            scheme_name,
            fund_house,
            category,
            ROUND(expense_ratio_pct, 2) AS expense_ratio_pct
        FROM fact_performance
        WHERE expense_ratio_pct < 1.0
        ORDER BY expense_ratio_pct ASC;
        """
    ),

    (
        "QUERY 6: HIGHEST 3-YEAR RETURN BY CATEGORY",
        """
        SELECT
            category,
            scheme_name,
            ROUND(return_3yr_pct, 2) AS return_3yr_pct
        FROM fact_performance
        WHERE (category, return_3yr_pct) IN (
            SELECT
                category,
                MAX(return_3yr_pct)
            FROM fact_performance
            GROUP BY category
        )
        ORDER BY return_3yr_pct DESC;
        """
    ),

    (
        "QUERY 7: TOP FUNDS BY SHARPE RATIO",
        """
        SELECT
            scheme_name,
            fund_house,
            category,
            ROUND(sharpe_ratio, 2) AS sharpe_ratio,
            ROUND(return_3yr_pct, 2) AS return_3yr_pct,
            ROUND(std_dev_ann_pct, 2) AS volatility_pct
        FROM fact_performance
        ORDER BY sharpe_ratio DESC
        LIMIT 10;
        """
    ),

    (
        "QUERY 8: FUNDS WITH POSITIVE ALPHA",
        """
        SELECT
            scheme_name,
            fund_house,
            category,
            ROUND(return_3yr_pct, 2) AS return_3yr_pct,
            ROUND(benchmark_3yr_pct, 2) AS benchmark_3yr_pct,
            ROUND(alpha, 2) AS alpha
        FROM fact_performance
        WHERE alpha > 0
        ORDER BY alpha DESC;
        """
    ),

    (
        "QUERY 9: TRANSACTIONS BY CITY TIER",
        """
        SELECT
            city_tier,
            COUNT(*) AS transaction_count,
            ROUND(SUM(amount_inr), 2) AS total_transaction_amount,
            ROUND(AVG(amount_inr), 2) AS average_transaction_amount
        FROM fact_transactions
        GROUP BY city_tier
        ORDER BY total_transaction_amount DESC;
        """
    ),

    (
        "QUERY 10: TOTAL AUM BY FUND HOUSE",
        """
        SELECT
            fund_house,
            ROUND(SUM(aum_crore), 2) AS total_aum_crore,
            COUNT(*) AS number_of_schemes
        FROM fact_performance
        GROUP BY fund_house
        ORDER BY total_aum_crore DESC;
        """
    )
]


for title, query in queries:

    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    cursor.execute(query)
    results = cursor.fetchall()

    for row in results:
        print(row)


connection.close()

print("\n" + "=" * 80)
print("ALL 10 QUERIES EXECUTED SUCCESSFULLY")
print("=" * 80)