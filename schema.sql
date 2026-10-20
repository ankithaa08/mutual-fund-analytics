-- =============================================================================
-- Bluestock Mutual Fund Analytics Platform - SQLite Star Schema DDL
-- File: schema.sql
-- =============================================================================
-- Architecture: Star Schema with Fact and Dimension Tables
-- Dimensions: dim_fund, dim_date
-- Facts:      fact_nav, fact_transactions, fact_performance, fact_aum
-- Supporting: monthly_sip_inflows, category_inflows, industry_folio_count,
--             portfolio_holdings, benchmark_indices
-- =============================================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------------------------------
-- 1. DIMENSION TABLE: dim_fund (Fund Master)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS portfolio_holdings;
DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    fund_house TEXT NOT NULL,
    scheme_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    plan TEXT NOT NULL CHECK (plan IN ('Regular', 'Direct')),
    launch_date TEXT NOT NULL,
    benchmark TEXT NOT NULL,
    expense_ratio_pct REAL NOT NULL CHECK (expense_ratio_pct BETWEEN 0.1 AND 2.5),
    exit_load_pct REAL NOT NULL DEFAULT 0.0,
    min_sip_amount REAL NOT NULL DEFAULT 500.0,
    min_lumpsum_amount REAL NOT NULL DEFAULT 1000.0,
    fund_manager TEXT NOT NULL,
    risk_category TEXT NOT NULL,
    sebi_category_code TEXT NOT NULL
);

-- -----------------------------------------------------------------------------
-- 2. DIMENSION TABLE: dim_date (Calendar Dimension)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS benchmark_indices;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date TEXT PRIMARY KEY,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    month_name TEXT NOT NULL,
    day INTEGER NOT NULL CHECK (day BETWEEN 1 AND 31),
    day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
    day_name TEXT NOT NULL,
    is_weekend INTEGER NOT NULL CHECK (is_weekend IN (0, 1)),
    fiscal_year TEXT NOT NULL,
    fiscal_quarter TEXT NOT NULL
);

-- -----------------------------------------------------------------------------
-- 3. FACT TABLE: fact_nav (Daily Historical Net Asset Value)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_nav (
    date TEXT NOT NULL,
    amfi_code INTEGER NOT NULL,
    nav REAL NOT NULL CHECK (nav > 0),
    is_forward_filled INTEGER NOT NULL DEFAULT 0 CHECK (is_forward_filled IN (0, 1)),
    daily_return_pct REAL NOT NULL DEFAULT 0.0,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE,
    FOREIGN KEY (date) REFERENCES dim_date(date) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_nav_date ON fact_nav(date);
CREATE INDEX IF NOT EXISTS idx_nav_code ON fact_nav(amfi_code);

-- -----------------------------------------------------------------------------
-- 4. FACT TABLE: fact_transactions (Investor Order Book)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    amfi_code INTEGER NOT NULL,
    transaction_type TEXT NOT NULL CHECK (transaction_type IN ('SIP', 'Lumpsum', 'Redemption')),
    amount_inr REAL NOT NULL CHECK (amount_inr > 0),
    state TEXT NOT NULL,
    city TEXT NOT NULL,
    city_tier TEXT NOT NULL CHECK (city_tier IN ('T30', 'B30')),
    age_group TEXT NOT NULL,
    gender TEXT NOT NULL CHECK (gender IN ('Male', 'Female')),
    annual_income_lakh REAL NOT NULL,
    payment_mode TEXT NOT NULL,
    kyc_status TEXT NOT NULL CHECK (kyc_status IN ('Verified', 'Pending', 'Rejected')),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE,
    FOREIGN KEY (transaction_date) REFERENCES dim_date(date) ON DELETE CASCADE
);

-- Indexes for analytical slicing
CREATE INDEX IF NOT EXISTS idx_tx_date ON fact_transactions(transaction_date);
CREATE INDEX IF NOT EXISTS idx_tx_code ON fact_transactions(amfi_code);
CREATE INDEX IF NOT EXISTS idx_tx_state ON fact_transactions(state);
CREATE INDEX IF NOT EXISTS idx_tx_tier ON fact_transactions(city_tier);

-- -----------------------------------------------------------------------------
-- 5. FACT TABLE: fact_performance (Trailing Returns & Risk Ratios)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_performance (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT NOT NULL,
    plan TEXT NOT NULL,
    return_1yr_pct REAL NOT NULL,
    return_3yr_pct REAL NOT NULL,
    return_5yr_pct REAL NOT NULL,
    benchmark_3yr_pct REAL NOT NULL,
    alpha REAL NOT NULL,
    beta REAL NOT NULL,
    sharpe_ratio REAL NOT NULL,
    sortino_ratio REAL NOT NULL,
    std_dev_ann_pct REAL NOT NULL,
    max_drawdown_pct REAL NOT NULL,
    aum_crore INTEGER NOT NULL CHECK (aum_crore >= 0),
    expense_ratio_pct REAL NOT NULL CHECK (expense_ratio_pct BETWEEN 0.1 AND 2.5),
    morningstar_rating INTEGER NOT NULL CHECK (morningstar_rating BETWEEN 1 AND 5),
    risk_grade TEXT NOT NULL,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE
);

-- -----------------------------------------------------------------------------
-- 6. FACT TABLE: fact_aum (Quarterly Fund House AUM)
-- -----------------------------------------------------------------------------
CREATE TABLE fact_aum (
    date TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    aum_lakh_crore REAL NOT NULL,
    aum_crore INTEGER NOT NULL,
    num_schemes INTEGER NOT NULL,
    PRIMARY KEY (date, fund_house),
    FOREIGN KEY (date) REFERENCES dim_date(date) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_aum_house ON fact_aum(fund_house);

-- -----------------------------------------------------------------------------
-- 7. SUPPORTING TABLES
-- -----------------------------------------------------------------------------

-- Monthly SIP Inflows
CREATE TABLE IF NOT EXISTS monthly_sip_inflows (
    month TEXT PRIMARY KEY,
    sip_inflow_crore INTEGER NOT NULL,
    active_sip_accounts_crore REAL NOT NULL,
    new_sip_accounts_lakh REAL NOT NULL,
    sip_aum_lakh_crore REAL NOT NULL,
    yoy_growth_pct REAL NOT NULL DEFAULT 0.0
);

-- Monthly Category Inflows
CREATE TABLE IF NOT EXISTS category_inflows (
    month TEXT NOT NULL,
    category TEXT NOT NULL,
    net_inflow_crore REAL NOT NULL,
    PRIMARY KEY (month, category)
);

-- Industry Folio Trajectory
CREATE TABLE IF NOT EXISTS industry_folio_count (
    month TEXT PRIMARY KEY,
    total_folios_crore REAL NOT NULL,
    equity_folios_crore REAL NOT NULL,
    debt_folios_crore REAL NOT NULL,
    hybrid_folios_crore REAL NOT NULL,
    others_folios_crore REAL NOT NULL
);

-- Portfolio Top 10 Holdings
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    amfi_code INTEGER NOT NULL,
    stock_symbol TEXT NOT NULL,
    stock_name TEXT NOT NULL,
    sector TEXT NOT NULL,
    weight_pct REAL NOT NULL,
    market_value_cr REAL NOT NULL,
    current_price_inr REAL NOT NULL,
    portfolio_date TEXT NOT NULL,
    PRIMARY KEY (amfi_code, stock_symbol),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code) ON DELETE CASCADE
);

-- Benchmark Market Indices
CREATE TABLE IF NOT EXISTS benchmark_indices (
    date TEXT NOT NULL,
    index_name TEXT NOT NULL,
    close_value REAL NOT NULL,
    PRIMARY KEY (date, index_name),
    FOREIGN KEY (date) REFERENCES dim_date(date) ON DELETE CASCADE
);
