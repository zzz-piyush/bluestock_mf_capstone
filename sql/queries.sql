-- ============================================================
-- Bluestock Mutual Fund Analytics Platform
-- Analytical SQL Queries
-- ============================================================


-- ============================================================
-- Query 1: Top 5 funds by AUM
-- ============================================================

SELECT
    scheme_name,
    fund_house,
    aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;


-- ============================================================
-- Query 2: Average NAV by month
-- ============================================================

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY strftime('%Y-%m', date)
ORDER BY month;


-- ============================================================
-- Query 3: SIP YoY growth
-- ============================================================

SELECT
    strftime('%Y', transaction_date) AS year,
    SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY strftime('%Y', transaction_date)
ORDER BY year;


-- ============================================================
-- Query 4: Transactions by state
-- ============================================================

SELECT
    state,
    COUNT(*) AS transaction_count,
    SUM(amount_inr) AS total_transaction_amount
FROM fact_transactions
GROUP BY state
ORDER BY total_transaction_amount DESC;


-- ============================================================
-- Query 5: Funds with expense ratio below 1%
-- ============================================================

SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;