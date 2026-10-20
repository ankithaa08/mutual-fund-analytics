# Bluestock Mutual Fund Analytics Engineering Platform

A production-ready data engineering and analytics repository for Indian Mutual Funds, incorporating raw ingestion, automated data cleaning, forward-filling algorithms, star schema dimensional modeling, SQLite database integration, and analytical SQL querying.

---

## 📁 Project Folder Structure

```text
mutual_fund_analysis/
│
├── bluestock_mf.db                # SQLite Database (Star Schema loaded with SQLAlchemy)
├── schema.sql                     # Star Schema DDL with PKs, FKs, and Indexes
├── queries.sql                    # 10 Analytical SQL Queries (AUM, NAV trends, YoY growth, Demographics)
├── data_dictionary.md             # Comprehensive Data Dictionary & Column Business Definitions
├── clean_and_load_db.py           # Day 2 Automated Cleaning, Star Schema Creation & SQLite ETL
│
├── data/
│   ├── raw/                       # Raw input CSV datasets & API dumps
│   │   ├── 01_fund_master.csv
│   │   ├── 02_nav_history.csv
│   │   ├── 03_aum_by_fund_house.csv
│   │   ├── 04_monthly_sip_inflows.csv
│   │   ├── 05_category_inflows.csv
│   │   ├── 06_industry_folio_count.csv
│   │   ├── 07_scheme_performance.csv
│   │   ├── 08_investor_transactions.csv
│   │   ├── 09_portfolio_holdings.csv
│   │   ├── 10_benchmark_indices.csv
│   │   └── live_nav_*.csv
│   └── processed/                 # 10 Cleaned, validated, and normalized CSV datasets
│       ├── 01_fund_master_cleaned.csv
│       ├── 02_nav_history_cleaned.csv          # Forward-filled weekends & holidays (64,320 rows)
│       ├── 03_aum_by_fund_house_cleaned.csv
│       ├── 04_monthly_sip_inflows_cleaned.csv
│       ├── 05_category_inflows_cleaned.csv
│       ├── 06_industry_folio_count_cleaned.csv
│       ├── 07_scheme_performance_cleaned.csv   # Verified numeric returns & SEBI TER bounds
│       ├── 08_investor_transactions_cleaned.csv# Standardized types (SIP/Lumpsum/Redemption)
│       ├── 09_portfolio_holdings_cleaned.csv
│       ├── 10_benchmark_indices_cleaned.csv
│       └── dim_date.csv                        # Generated 5-year calendar dimension
│
├── sql/                           # DDL schemas and analytical SQL queries
│   ├── schema.sql
│   └── queries.sql
│
├── notebooks/                     # Exploratory Data Analysis & prototyping
│   └── 01_data_ingestion_and_eda.ipynb
│
├── dashboard/                     # Interactive Streamlit & Plotly BI application
│   └── app.py
│
├── reports/                       # Data quality audits, data dictionaries, and summaries
│   ├── data_quality_summary.txt
│   └── data_dictionary.md
│
├── data_ingestion.py              # Day 1: Data loading, profiling, & validation pipeline
├── live_nav_fetch.py              # Day 1: Real-time NAV fetcher via mfapi.in REST API
├── requirements.txt               # Project Python package dependencies
└── .gitignore                     # Git ignore rules for data science
```

---

## 🌟 Day 2 Milestone: Cleaned Data & SQLite Star Schema

### 1. Data Cleaning Highlights
- **`nav_history`**:
  - Reindexed each fund against complete calendar dates (2022 to 2026).
  - Forward-filled (`.ffill()`) NAV values for Saturdays, Sundays, and public holidays (added 18,320 non-trading records, bringing the total to **64,320 rows**).
  - Calculated daily percentage returns (`daily_return_pct`).
  - Validated zero negative or zero NAV entries (`NAV > 0`).
- **`investor_transactions`**:
  - Standardized transaction types to exact title-case enums: `SIP`, `Lumpsum`, `Redemption`.
  - Enforced `amount_inr > 0` validation (range: ₹400 to ₹5,97,498).
  - Standardized KYC status to `Verified` and `Pending`.
  - Parsed all dates into ISO `YYYY-MM-DD` format.
- **`scheme_performance`**:
  - Validated that all trailing return metrics (1-yr, 3-yr, 5-yr, benchmark) and risk statistics (Sharpe, Sortino, Alpha, Beta) are numeric floats.
  - Verified that all Expense Ratios lie strictly within the SEBI regulatory range of **0.10% to 2.50%** (actual range: 0.55% to 1.64%).
- **Calendar Dimension (`dim_date`)**:
  - Generated a dedicated 1,826-day calendar dimension (2022 to 2026) supporting fiscal year, fiscal quarter, day-of-week, and weekend flags.

---

## 🏛️ Star Schema Architecture (`bluestock_mf.db`)

Loaded using **SQLAlchemy** `create_engine` and Pandas `to_sql()` with strict primary and foreign key constraints:

| Table Name | Role | Primary Key | Foreign Keys | Row Count |
| :--- | :--- | :--- | :--- | :---: |
| **`dim_fund`** | Dimension | `amfi_code` | — | **40** |
| **`dim_date`** | Dimension | `date` | — | **1,826** |
| **`fact_nav`** | Fact | (`amfi_code`, `date`) | `amfi_code` ➔ `dim_fund`, `date` ➔ `dim_date` | **64,320** |
| **`fact_transactions`** | Fact | `transaction_id` | `amfi_code` ➔ `dim_fund`, `transaction_date` ➔ `dim_date` | **32,778** |
| **`fact_performance`** | Fact | `amfi_code` | `amfi_code` ➔ `dim_fund` | **40** |
| **`fact_aum`** | Fact | (`date`, `fund_house`) | `date` ➔ `dim_date` | **90** |
| **`monthly_sip_inflows`** | Supporting Fact | `month` | — | **48** |
| **`category_inflows`** | Supporting Fact | (`month`, `category`) | — | **144** |
| **`industry_folio_count`**| Supporting Fact | `month` | — | **21** |
| **`portfolio_holdings`** | Supporting Fact | (`amfi_code`, `stock_symbol`)| `amfi_code` ➔ `dim_fund` | **322** |
| **`benchmark_indices`** | Supporting Fact | (`date`, `index_name`) | `date` ➔ `dim_date` | **8,050** |

---

## 🔍 Analytical SQL Queries Implemented (`queries.sql`)

1. **Top 5 Funds by AUM**: Flags highest capitalized schemes across Equity and Debt.
2. **Average NAV per Month**: Tracks monthly market averages and benchmark scheme NAV evolution.
3. **Monthly SIP Inflow & YoY Growth**: Computes rolling 12-month YoY growth using `LAG()`.
4. **Transactions by State**: Aggregates state-wise order volume, ticket size, and KYC compliance.
5. **Cost-Efficient Funds (< 1.0% TER)**: Screens low-cost Direct plans with high Morningstar ratings.
6. **Top 3 Risk-Adjusted Funds per Category**: Ranks funds by Sharpe Ratio using window function `DENSE_RANK()`.
7. **Category Net Inflows & Market Share**: Measures capital inflows across Liquid, Equity, and Thematic funds.
8. **Investor Demographics (T30 vs B30 & Age)**: Identifies ticket sizes and SIP adoption across cohorts.
9. **Portfolio Stock Concentration**: Uncovers top institutional equity holdings (e.g. Axis Bank, Reliance, Bharti Airtel).
10. **Alpha Generation Audit**: Evaluates scheme 3-year CAGR outperformance against benchmark indices.

---

## ⚡ Execution Instructions

### 1. Run Data Cleaning & Database Build
```bash
python clean_and_load_db.py
```

### 2. Execute SQL Queries via SQLite CLI / Python
```bash
sqlite3 bluestock_mf.db < queries.sql
```
*(Or query interactively via Python, DBeaver, or VS Code SQLite Viewer).*
