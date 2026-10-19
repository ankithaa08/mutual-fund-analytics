# Mutual Fund Analytics Engineering Platform

## Day 1: Data Ingestion, Profiling & Live NAV Pipeline

A production-ready data ingestion and analytics repository for Indian Mutual Funds, incorporating historical NAV data, investor transactions, fund master schemas, industry-level inflows, and live API feeds from `mfapi.in`.

---

## 📁 Project Folder Structure

```text
mutual_fund_analysis/
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
│   │   ├── live_nav_125497_raw.csv
│   │   ├── live_nav_5_key_schemes.csv
│   │   └── live_schemes_metadata.json
│   └── processed/                 # Cleaned, transformed, and feature-engineered datasets
│
├── notebooks/                     # Exploratory Data Analysis & prototyping
│   └── 01_data_ingestion_and_eda.ipynb
│
├── sql/                           # DDL schemas and analytical SQL queries
│   └── schema.sql
│
├── dashboard/                     # Interactive Streamlit & Plotly BI application
│   └── app.py
│
├── reports/                       # Data quality audits and executive summaries
│   └── data_quality_summary.txt
│
├── data_ingestion.py              # Core data loading, profiling, & validation pipeline
├── live_nav_fetch.py              # Real-time NAV fetcher via mfapi.in REST API
├── requirements.txt               # Project Python package dependencies
├── .gitignore                     # Git ignore rules for data science
└── README.md                      # Project documentation and execution guide
```

---

## ⚡ Quickstart & Installation

### 1. Prerequisites
- Python 3.10+
- Git

### 2. Environment Setup & Dependency Installation
```bash
# Clone the repository
git clone <your-github-repo-url>
cd mutual_fund_analysis

# Install all required packages
pip install -r requirements.txt
```

### 3. Run Data Ingestion & Data Profiling
```bash
python data_ingestion.py
```
This loads all 10 datasets, displays shapes and dtypes, validates AMFI code integrity, flags anomalies, and writes an executive summary to `reports/data_quality_summary.txt`.

### 4. Run Live NAV API Fetcher
```bash
python live_nav_fetch.py
```
This fetches real-time NAV records from `https://api.mfapi.in/mf/{scheme_code}` for:
- **125497**: HDFC Top 100 Direct
- **119551**: SBI Bluechip
- **120503**: ICICI Bluechip
- **118632**: Nippon Large Cap
- **119092**: Axis Bluechip
- **120841**: Kotak Bluechip

Output files are stored directly in `data/raw/`.

### 5. Launch Interactive Dashboard (Optional)
```bash
streamlit run dashboard/app.py
```

---

## 🔍 Data Quality Summary & Dataset Profiles

| Dataset | Rows | Columns | Quality Status & Anomalies |
| :--- | :---: | :---: | :--- |
| `01_fund_master` | 40 | 15 | Clean. 40 schemes across 10 AMCs. Launch dates formatted as YYYY-MM-DD strings. |
| `02_nav_history` | 46,000 | 3 | Exactly 1,150 trading days per scheme (2022-01-03 to 2026-05-29). No missing values. |
| `03_aum_by_fund_house` | 90 | 5 | Quarterly AUM figures for top 10 AMCs. |
| `04_monthly_sip_inflows`| 48 | 6 | 12 null values in `yoy_growth_pct` (first 12 months in 2022 due to lack of 2021 prior baseline). |
| `05_category_inflows` | 144 | 3 | Monthly net inflows by scheme category (Equity, Debt, Hybrid, Liquid). |
| `06_industry_folio_count`| 21 | 6 | Bi-monthly / quarterly industry folio totals. |
| `07_scheme_performance`| 40 | 19 | 100% complete metrics: 1/3/5-year returns, Sharpe, Sortino, Alpha, Beta, Max Drawdown. |
| `08_investor_transactions`| 32,778| 13 | 5,000 unique investors across 40 schemes. Transactions span 2024-01-01 to 2025-05-30. |
| `09_portfolio_holdings` | 322 | 8 | Top 10 portfolio holdings for 34 equity schemes as of 2025-12-31. |
| `10_benchmark_indices` | 8,050 | 3 | Historical daily close for 7 major indices (NIFTY 50, NIFTY 100, NIFTY Midcap 150, etc.). |

### AMFI Referential Integrity Audit
- **Master Schemes**: 40
- **Schemes in NAV History**: 40
- **Unmatched AMFI Codes**: **0** (100% matched, zero orphan records).

---

## 🚀 Pushing to GitHub

To push this initialized repository to GitHub:

1. Create a new empty repository on [GitHub](https://github.com/new) named `mutual-fund-analytics` (do not initialize with README or license).
2. Run the following terminal commands:
```bash
git remote add origin https://github.com/<your-username>/mutual-fund-analytics.git
git branch -M main
git push -u origin main
```
