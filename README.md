# Bluestock Mutual Fund Analytics Platform

## End-to-End Data Engineering, ETL Pipeline & Interactive Dashboard

A complete mutual fund analytics platform developed as part of the **Bluestock Fintech Data Analytics Internship Capstone**.

The project combines Python-based ETL, data cleaning, SQL/SQLite database design, exploratory data analysis, performance and risk analytics, advanced analytics, and an interactive Power BI dashboard.

## Project Overview

The objective is to build an end-to-end analytics platform for analyzing Indian mutual fund data.

The platform processes datasets covering:

- Mutual fund schemes
- Historical NAV
- Fund-house AUM
- SIP inflows
- Category-level inflows
- Industry folios
- Scheme performance
- Investor transactions
- Portfolio holdings
- Benchmark indices

## Objectives

1. Build an automated Python ETL pipeline.
2. Clean and validate mutual fund datasets.
3. Design a normalized relational/star-schema database.
4. Perform exploratory data analysis.
5. Calculate fund performance and risk metrics.
6. Build an interactive Power BI dashboard.
7. Perform advanced investor, risk and diversification analytics.
8. Create a complete technical report and presentation.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | ETL, cleaning and analytics |
| Pandas | Data manipulation |
| NumPy | Numerical calculations |
| Matplotlib | Data visualization |
| SQLite | Relational database |
| SQL | Analytical queries |
| Jupyter Notebook | EDA and analytics |
| Power BI | Interactive dashboard |
| Git/GitHub | Version control |

## Data Sources

The project combines publicly available mutual fund information with project-generated analytical datasets.

### Public / Market Data

- AMFI India
- mfapi.in
- Public benchmark/index data
- Public mutual fund scheme information

### Project-Generated / Constructed Data

Some datasets were generated or constructed for demonstrating investor and portfolio analytics, including investor transactions and certain category/sector analytical data. These should not be interpreted as official AMFI statistics.

## Dataset Inventory

| Dataset | Records |
|---|---:|
| Fund Master | 40 |
| NAV History | 46,000 |
| Scheme Performance | 40 |
| Investor Transactions | 32,778 |
| AUM by Fund House | 90 |
| Monthly SIP Inflows | 48 |
| Category Inflows | 144 |
| Industry Folio Count | 21 |
| Portfolio Holdings | 322 |
| Benchmark Indices | 8,050 |

The project covers **40 mutual fund schemes across 10 fund houses**.

## ETL Pipeline

```text
Raw Data
   ↓
Data Ingestion
   ↓
Validation
   ↓
Data Cleaning
   ↓
Processed CSV Files
   ↓
SQLite Database
   ↓
SQL Analytics
   ↓
Python EDA & Performance Analysis
   ↓
Advanced Analytics
   ↓
Power BI Dashboard
```

### Validation

- Fund master AMFI codes: 40
- NAV history AMFI codes: 40
- Missing AMFI codes: 0
- Duplicate fund-date NAV records: 0
- Non-positive NAV values: 0

## Database Design

### Dimension Tables

- `dim_fund`
- `dim_date`

### Fact Tables

- `fact_nav`
- `fact_transactions`
- `fact_performance`
- `fact_aum`

| Table | Rows |
|---|---:|
| dim_fund | 40 |
| dim_date | 1,297 |
| fact_nav | 46,000 |
| fact_transactions | 32,778 |
| fact_performance | 40 |
| fact_aum | 90 |

The AMFI code is used as the primary fund identifier across the model.

## Exploratory Data Analysis

### Industry AUM

| Year | AUM |
|---|---:|
| 2022 | ₹30.90 Lakh Cr |
| 2023 | ₹37.42 Lakh Cr |
| 2024 | ₹52.68 Lakh Cr |
| 2025 | ₹62.74 Lakh Cr |

### SIP Inflows

December 2025 SIP inflow: **₹31,002 Cr**

### Folio Growth

Industry folios increased from **13.26 Cr to 26.12 Cr**, representing approximately **96.98% growth**.

### Investor Age Distribution

| Age Group | Share |
|---|---:|
| 26–35 | 41.07% |
| 36–45 | 24.85% |
| 18–25 | 15.00% |
| 46–55 | 11.53% |
| 56+ | 7.55% |

## Performance & Risk Analysis

The project calculates:

- CAGR till date
- Sharpe Ratio
- Sortino Ratio
- Alpha
- Beta
- Maximum Drawdown

The available NAV history covers approximately **January 2022 to May 2026**, so a genuine five-year CAGR was not calculated. CAGR is calculated over the available period.

Sharpe and Sortino calculations use an assumed annual risk-free rate of **6%**.

### Alpha/Beta Analysis

- Funds with benchmark data: 37
- Funds without benchmark data: 3
- Mean alpha: 10.94%
- Positive alpha: 31 of 37 funds

### Maximum Drawdown

- Mean maximum drawdown: -17.87%
- Median maximum drawdown: -16.31%

## Fund Performance Scorecard

The project-specific scorecard uses:

| Metric | Weight |
|---|---:|
| CAGR 1Y | 20% |
| CAGR 3Y | 20% |
| Sharpe Ratio | 20% |
| Sortino Ratio | 15% |
| Alpha | 15% |
| Maximum Drawdown | 10% |

This scorecard is an analytical comparison framework for the project and is not personalized investment advice.

## Advanced Analytics

The project includes:

- **VaR and CVaR:** downside risk analysis using daily returns.
- **Rolling Sharpe:** 90-day rolling risk-adjusted performance.
- **Investor Cohort Analysis:** grouping investors by first transaction year.
- **SIP Continuity:** transaction-gap analysis using a 35-day project threshold.
- **Sector Concentration:** HHI-based concentration analysis.
- **Rule-Based Fund Recommendation Prototype:** project-defined analytical scoring.

The top five constructed sector weights account for **61.89%** of the portfolio-sector distribution.

## Investor Analytics

The investor transaction dataset contains:

- 32,778 total transactions
- 19,716 SIP transactions
- 8,095 Lumpsum transactions
- 4,967 Redemption transactions

The project dataset contains approximately:

- T30: 66.72%
- B30: 33.28%

Investor transaction records are project-generated analytical data.

## Power BI Dashboard

The dashboard contains four main pages:

### 1. Industry Overview
- Industry AUM
- Latest SIP inflow
- Latest folios
- Number of schemes
- Fund-house AUM
- Industry trends

### 2. Fund Performance
- Average 1Y return
- Average 3Y return
- Average Sharpe ratio
- Average maximum drawdown
- Fund scorecard
- Risk vs return analysis
- Fund and fund-house filters

### 3. Investor Analytics
- Total investors
- Total investment
- Total redemptions
- Average transaction
- Age-group analysis
- City-tier analysis
- Transaction behavior

### 4. SIP & Market Trends
- Monthly SIP inflow
- Active SIP accounts
- New SIP accounts
- Category-wise inflows
- Folio growth
- Folio composition
- SIP YoY growth

Additional features include interactive slicers, drill-through fund details, page navigation and dynamic DAX measures.

## Project Structure

```text
bluestock_mf_capstone/
├── data/
│   ├── raw/
│   └── processed/
├── db/
│   └── bluestock_mf.db
├── dashboard/
│   └── Mutual_Fund_Analytics_Dashboard.pbix
├── notebooks/
│   ├── 03_eda_analysis.ipynb
│   ├── 04_performance.ipynb
│   └── 05_Advanced_Analytics.ipynb
├── reports/
│   ├── Final_Report.md
│   ├── Mutual_Fund_Analytics_Dashboard.pdf
│   ├── data_dictionary.md
│   ├── industry_overview.png
│   ├── fund_performance.png
│   ├── investor_analytics.png
│   └── sip_market_trends.png
├── scripts/
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── fund_master_analysis.py
│   ├── validate_amfi_codes.py
│   ├── clean_nav_history.py
│   ├── clean_investor_transactions.py
│   ├── clean_scheme_performance.py
│   ├── load_database.py
│   ├── verify_database.py
│   ├── run_all_queries.py
│   ├── recommender.py
│   └── sector_hhi.py
├── sql/
│   ├── schema.sql
│   └── queries.sql
├── requirements.txt
├── README.md
└── .gitignore
```

## How to Run

### Clone

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd bluestock_mf_capstone
```

### Create virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Run ingestion and validation

```powershell
python scripts/data_ingestion.py
python scripts/fund_master_analysis.py
python scripts/validate_amfi_codes.py
```

### Run cleaning

```powershell
python scripts/clean_nav_history.py
python scripts/clean_investor_transactions.py
python scripts/clean_scheme_performance.py
```

### Build and verify database

```powershell
python scripts/load_database.py
python scripts/verify_database.py
```

### Run SQL analytics

```powershell
python scripts/run_all_queries.py
```

### Run advanced analytics

```powershell
python scripts/recommender.py
python scripts/sector_hhi.py
```

EDA, performance analysis and advanced analytics can also be executed through the notebooks in `notebooks/`.

## Key Deliverables

- Python ETL pipeline
- Cleaned datasets
- SQLite database schema
- SQL analytical queries
- EDA notebook
- Performance analysis notebook
- Advanced analytics notebook
- Power BI dashboard
- Dashboard PDF
- Final project report
- Presentation
- Data dictionary
- Visualization outputs

## Limitations

1. The available NAV history does not provide a full genuine five-year period.
2. Sharpe and Sortino calculations use an assumed 6% annual risk-free rate.
3. Some funds do not have matching benchmark data.
4. Investor transaction data is project-generated.
5. Certain category and portfolio-sector analytical datasets are constructed for the capstone.
6. The rule-based recommendation module is a prototype and is not personalized financial advice.
7. Power BI uses cleaned CSV datasets for dashboard connectivity while SQLite remains the relational database deliverable.

## Future Enhancements

- Automated scheduled data ingestion
- Direct live AMFI/mfapi integration
- Real-time NAV updates
- More benchmark mappings
- Automated Power BI refresh
- Cloud database deployment
- Investor-level portfolio optimization
- Machine-learning-based fund ranking
- More sophisticated recommender models
- Real-time alerts for NAV and risk changes

## Project Status

**Version:** v1.0  
**Status:** Final Capstone Submission  
**Platform:** Bluestock Fintech Data Analytics Internship  
**Fund Schemes:** 40  
**Fund Houses:** 10  
**Primary Technologies:** Python | SQL | SQLite | Power BI
