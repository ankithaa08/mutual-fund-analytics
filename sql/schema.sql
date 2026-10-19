-- =====================================================================
-- Mutual Fund Analytics Platform - SQL Database Schema (PostgreSQL/DuckDB)
-- =====================================================================

-- 1. Fund Master Table
CREATE TABLE IF NOT EXISTS fund_master (
    amfi_code INTEGER PRIMARY KEY,
    fund_house VARCHAR(100) NOT NULL,
    scheme_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    plan VARCHAR(20) NOT NULL,
    launch_date DATE,
    benchmark VARCHAR(100),
    expense_ratio_pct NUMERIC(5, 2),
    exit_load_pct NUMERIC(5, 2),
    min_sip_amount NUMERIC(12, 2),
    min_lumpsum_amount NUMERIC(12, 2),
    fund_manager VARCHAR(100),
    risk_category VARCHAR(50),
    sebi_category_code VARCHAR(20)
);

-- 2. NAV History Table
CREATE TABLE IF NOT EXISTS nav_history (
    amfi_code INTEGER NOT NULL REFERENCES fund_master(amfi_code),
    date DATE NOT NULL,
    nav NUMERIC(12, 4) NOT NULL,
    PRIMARY KEY (amfi_code, date)
);

-- 3. AUM by Fund House Table
CREATE TABLE IF NOT EXISTS aum_by_fund_house (
    date DATE NOT NULL,
    fund_house VARCHAR(100) NOT NULL,
    aum_lakh_crore NUMERIC(10, 2),
    aum_crore BIGINT,
    num_schemes INTEGER,
    PRIMARY KEY (date, fund_house)
);

-- 4. Monthly SIP Inflows Table
CREATE TABLE IF NOT EXISTS monthly_sip_inflows (
    month VARCHAR(7) PRIMARY KEY,
    sip_inflow_crore BIGINT,
    active_sip_accounts_crore NUMERIC(10, 2),
    new_sip_accounts_lakh NUMERIC(10, 2),
    sip_aum_lakh_crore NUMERIC(10, 2),
    yoy_growth_pct NUMERIC(6, 2)
);

-- 5. Category Inflows Table
CREATE TABLE IF NOT EXISTS category_inflows (
    month VARCHAR(7) NOT NULL,
    category VARCHAR(50) NOT NULL,
    net_inflow_crore NUMERIC(12, 2),
    PRIMARY KEY (month, category)
);

-- 6. Industry Folio Count Table
CREATE TABLE IF NOT EXISTS industry_folio_count (
    month VARCHAR(7) PRIMARY KEY,
    total_folios_crore NUMERIC(10, 2),
    equity_folios_crore NUMERIC(10, 2),
    debt_folios_crore NUMERIC(10, 2),
    hybrid_folios_crore NUMERIC(10, 2),
    others_folios_crore NUMERIC(10, 2)
);

-- 7. Scheme Performance Table
CREATE TABLE IF NOT EXISTS scheme_performance (
    amfi_code INTEGER PRIMARY KEY REFERENCES fund_master(amfi_code),
    scheme_name VARCHAR(255),
    fund_house VARCHAR(100),
    category VARCHAR(50),
    plan VARCHAR(20),
    return_1yr_pct NUMERIC(6, 2),
    return_3yr_pct NUMERIC(6, 2),
    return_5yr_pct NUMERIC(6, 2),
    benchmark_3yr_pct NUMERIC(6, 2),
    alpha NUMERIC(6, 2),
    beta NUMERIC(6, 2),
    sharpe_ratio NUMERIC(6, 2),
    sortino_ratio NUMERIC(6, 2),
    std_dev_ann_pct NUMERIC(6, 2),
    max_drawdown_pct NUMERIC(6, 2),
    aum_crore BIGINT,
    expense_ratio_pct NUMERIC(5, 2),
    morningstar_rating INTEGER,
    risk_grade VARCHAR(50)
);

-- 8. Investor Transactions Table
CREATE TABLE IF NOT EXISTS investor_transactions (
    transaction_id SERIAL PRIMARY KEY,
    investor_id VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    amfi_code INTEGER NOT NULL REFERENCES fund_master(amfi_code),
    transaction_type VARCHAR(20) NOT NULL,
    amount_inr NUMERIC(14, 2) NOT NULL,
    state VARCHAR(50),
    city VARCHAR(50),
    city_tier VARCHAR(10),
    age_group VARCHAR(20),
    gender VARCHAR(10),
    annual_income_lakh NUMERIC(8, 2),
    payment_mode VARCHAR(30),
    kyc_status VARCHAR(20)
);

-- 9. Portfolio Holdings Table
CREATE TABLE IF NOT EXISTS portfolio_holdings (
    id SERIAL PRIMARY KEY,
    amfi_code INTEGER NOT NULL REFERENCES fund_master(amfi_code),
    stock_symbol VARCHAR(30) NOT NULL,
    stock_name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    weight_pct NUMERIC(6, 2),
    market_value_cr NUMERIC(12, 2),
    current_price_inr NUMERIC(12, 2),
    portfolio_date DATE NOT NULL
);

-- 10. Benchmark Indices Table
CREATE TABLE IF NOT EXISTS benchmark_indices (
    date DATE NOT NULL,
    index_name VARCHAR(50) NOT NULL,
    close_value NUMERIC(12, 2) NOT NULL,
    PRIMARY KEY (date, index_name)
);
