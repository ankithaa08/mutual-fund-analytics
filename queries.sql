-- =============================================================================
-- Bluestock Mutual Fund Analytics Platform - 10 Analytical SQL Queries
-- File: queries.sql
-- Database: bluestock_mf.db (SQLite Star Schema)
-- =============================================================================

-- =============================================================================
-- QUERY 1: Top 5 Funds by Assets Under Management (AUM)
-- Business Objective: Identify the largest flagship funds in the portfolio,
-- their fund house, category, and 3-year performance.
-- =============================================================================
SELECT 
    f.amfi_code,
    f.scheme_name,
    f.fund_house,
    f.category,
    f.sub_category,
    p.aum_crore,
    ROUND(p.aum_crore / 1000.0, 2) AS aum_thousand_crore,
    p.return_3yr_pct,
    p.morningstar_rating
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 5;


-- =============================================================================
-- QUERY 2: Average NAV per Month Across Time (Overall Market & Specific Fund)
-- Business Objective: Track historical NAV trajectory on a monthly basis,
-- observing market expansion and monthly volatility.
-- =============================================================================
SELECT 
    strftime('%Y-%m', n.date) AS year_month,
    COUNT(DISTINCT n.amfi_code) AS active_schemes,
    ROUND(AVG(n.nav), 4) AS market_avg_nav,
    ROUND(MIN(n.nav), 4) AS market_min_nav,
    ROUND(MAX(n.nav), 4) AS market_max_nav,
    ROUND(AVG(CASE WHEN n.amfi_code = 125497 THEN n.nav END), 4) AS hdfc_top100_avg_nav
FROM fact_nav n
GROUP BY strftime('%Y-%m', n.date)
ORDER BY year_month DESC
LIMIT 12;


-- =============================================================================
-- QUERY 3: Monthly SIP Inflow & Year-over-Year (YoY) Growth Analysis
-- Business Objective: Evaluate retail investor momentum through monthly SIP book
-- size, compare against previous year inflows using LAG() window function.
-- =============================================================================
SELECT 
    month,
    sip_inflow_crore,
    active_sip_accounts_crore,
    sip_aum_lakh_crore,
    LAG(sip_inflow_crore, 12) OVER (ORDER BY month) AS prev_year_sip_inflow_crore,
    yoy_growth_pct AS recorded_yoy_growth_pct,
    ROUND(
        ((sip_inflow_crore - LAG(sip_inflow_crore, 12) OVER (ORDER BY month)) * 100.0 / 
         NULLIF(LAG(sip_inflow_crore, 12) OVER (ORDER BY month), 0)), 
        2
    ) AS calculated_yoy_growth_pct
FROM monthly_sip_inflows
ORDER BY month DESC
LIMIT 12;


-- =============================================================================
-- QUERY 4: Investor Transaction Distribution & Capital Flow by State
-- Business Objective: Determine geographic capital concentration, ticket size,
-- and KYC compliance health across Indian states.
-- =============================================================================
SELECT 
    state,
    COUNT(transaction_id) AS total_transactions,
    ROUND(SUM(amount_inr) / 10000000.0, 2) AS total_volume_crore,
    ROUND(AVG(amount_inr), 2) AS avg_ticket_size_inr,
    ROUND(COUNT(CASE WHEN transaction_type = 'SIP' THEN 1 END) * 100.0 / COUNT(*), 2) AS sip_tx_share_pct,
    ROUND(COUNT(CASE WHEN kyc_status = 'Verified' THEN 1 END) * 100.0 / COUNT(*), 2) AS kyc_verified_pct
FROM fact_transactions
GROUP BY state
ORDER BY total_volume_crore DESC;


-- =============================================================================
-- QUERY 5: Cost-Efficient Funds (Expense Ratio < 1.0%)
-- Business Objective: Screen ultra-low-cost schemes (primarily Direct plans),
-- reviewing their return generation and Morningstar ratings.
-- =============================================================================
SELECT 
    f.amfi_code,
    f.scheme_name,
    f.fund_house,
    f.category,
    f.plan,
    f.expense_ratio_pct,
    p.return_1yr_pct,
    p.return_3yr_pct,
    p.return_5yr_pct,
    p.morningstar_rating,
    p.risk_grade
FROM dim_fund f
JOIN fact_performance p ON f.amfi_code = p.amfi_code
WHERE f.expense_ratio_pct < 1.0
ORDER BY f.expense_ratio_pct ASC, p.return_3yr_pct DESC;


-- =============================================================================
-- QUERY 6: Top 3 Risk-Adjusted Funds per Category (Window Function: DENSE_RANK)
-- Business Objective: Rank the top 3 schemes within Equity and Debt categories
-- based on Sharpe Ratio (excess return per unit of volatility).
-- =============================================================================
WITH category_rankings AS (
    SELECT 
        f.category,
        f.sub_category,
        f.scheme_name,
        f.fund_house,
        p.sharpe_ratio,
        p.sortino_ratio,
        p.alpha,
        p.return_3yr_pct,
        DENSE_RANK() OVER (
            PARTITION BY f.category 
            ORDER BY p.sharpe_ratio DESC
        ) AS category_rank
    FROM fact_performance p
    JOIN dim_fund f ON p.amfi_code = f.amfi_code
)
SELECT 
    category,
    category_rank,
    sub_category,
    scheme_name,
    fund_house,
    sharpe_ratio,
    sortino_ratio,
    alpha,
    return_3yr_pct
FROM category_rankings
WHERE category_rank <= 3
ORDER BY category, category_rank;


-- =============================================================================
-- QUERY 7: Category Net Inflow Aggregates & Market Share
-- Business Objective: Quantify investor fund allocation across scheme categories
-- to measure market sentiment between Growth (Equity) vs Liquidity (Debt).
-- =============================================================================
SELECT 
    category,
    COUNT(DISTINCT month) AS observed_months,
    ROUND(SUM(net_inflow_crore), 2) AS total_net_inflow_crore,
    ROUND(AVG(net_inflow_crore), 2) AS avg_monthly_inflow_crore,
    ROUND(
        SUM(net_inflow_crore) * 100.0 / (SELECT SUM(net_inflow_crore) FROM category_inflows), 
        2
    ) AS share_of_total_inflows_pct
FROM category_inflows
GROUP BY category
ORDER BY total_net_inflow_crore DESC;


-- =============================================================================
-- QUERY 8: Investor Demographics & Wealth Profiling (City Tier vs Age Group)
-- Business Objective: Profile investor behavior across Top 30 (T30) and
-- Beyond 30 (B30) cities, measuring adoption of systematic vs lumpsum investing.
-- =============================================================================
SELECT 
    city_tier,
    age_group,
    COUNT(DISTINCT investor_id) AS unique_investors,
    COUNT(transaction_id) AS total_orders,
    ROUND(SUM(amount_inr) / 10000000.0, 2) AS total_spend_crore,
    ROUND(AVG(amount_inr), 2) AS avg_ticket_size,
    ROUND(COUNT(CASE WHEN transaction_type = 'SIP' THEN 1 END) * 100.0 / COUNT(*), 2) AS sip_share_pct,
    ROUND(COUNT(CASE WHEN transaction_type = 'Lumpsum' THEN 1 END) * 100.0 / COUNT(*), 2) AS lumpsum_share_pct
FROM fact_transactions
GROUP BY city_tier, age_group
ORDER BY city_tier, total_spend_crore DESC;


-- =============================================================================
-- QUERY 9: Portfolio Stock Concentration & Institutional Conviction
-- Business Objective: Uncover which stocks have the highest institutional
-- conviction across mutual fund portfolios and their total invested value.
-- =============================================================================
SELECT 
    stock_symbol,
    stock_name,
    sector,
    COUNT(DISTINCT amfi_code) AS funds_holding_stock,
    ROUND(SUM(market_value_cr), 2) AS total_market_value_cr,
    ROUND(AVG(weight_pct), 2) AS avg_fund_weight_pct,
    ROUND(MAX(weight_pct), 2) AS max_single_fund_weight_pct
FROM portfolio_holdings
GROUP BY stock_symbol, stock_name, sector
ORDER BY total_market_value_cr DESC
LIMIT 10;


-- =============================================================================
-- QUERY 10: Alpha Generation & Benchmark Outperformance Audit
-- Business Objective: Compare each fund's 3-year CAGR against its designated
-- benchmark index, computing excess return (alpha) and outperformance status.
-- =============================================================================
SELECT 
    f.amfi_code,
    f.scheme_name,
    f.category,
    f.benchmark,
    p.return_3yr_pct AS scheme_3yr_cagr,
    p.benchmark_3yr_pct AS benchmark_3yr_cagr,
    ROUND(p.return_3yr_pct - p.benchmark_3yr_pct, 2) AS excess_alpha_cagr,
    p.alpha AS jensen_alpha,
    p.beta,
    CASE 
        WHEN p.return_3yr_pct > p.benchmark_3yr_pct THEN 'Outperforming'
        ELSE 'Underperforming'
    END AS performance_status
FROM fact_performance p
JOIN dim_fund f ON p.amfi_code = f.amfi_code
ORDER BY excess_alpha_cagr DESC;
