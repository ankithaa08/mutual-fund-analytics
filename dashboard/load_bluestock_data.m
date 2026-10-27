// ==============================================================================
// BLUESTOCK MUTUAL FUND ANALYTICS - AUTOMATED POWER QUERY M SCRIPT
// ==============================================================================
// Instructions:
// 1. Open Power BI Desktop
// 2. Click "Transform Data" -> In Power Query Editor, click "New Source" -> "Blank Query"
// 3. Click "Advanced Editor", replace everything with the code below, and click "Done"
// 4. Repeat or use the individual queries below to load all 11 tables instantly!
// ==============================================================================

// 1. dim_fund (40 Schemes)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/01_fund_master_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"amfi_code", Int64.Type}, {"expense_ratio_pct", type number}, {"exit_load_pct", type number}, {"min_sip_amount", Int64.Type}, {"min_lumpsum_amount", Int64.Type}})
in
    #"Changed Type"

// 2. dim_date (Calendar Dimension 2022-2026)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/dim_date.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date", type date}, {"year", Int64.Type}, {"quarter", Int64.Type}, {"month", Int64.Type}, {"day", Int64.Type}, {"is_weekend", Int64.Type}})
in
    #"Changed Type"

// 3. fact_nav (64,320 Cleaned Daily NAV Records)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/02_nav_history_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date", type date}, {"amfi_code", Int64.Type}, {"nav", type number}, {"daily_return_pct", type number}, {"is_forward_filled", Int64.Type}})
in
    #"Changed Type"

// 4. fact_transactions (32,778 Investor Transactions)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/08_investor_transactions_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"transaction_id", type text}, {"investor_id", type text}, {"transaction_date", type date}, {"amfi_code", Int64.Type}, {"amount_inr", type number}, {"annual_income_lakh", type number}})
in
    #"Changed Type"

// 5. fact_performance (Risk, Sharpe, Alpha, 3Y CAGR)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/07_scheme_performance_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"amfi_code", Int64.Type}, {"return_1yr_pct", type number}, {"return_3yr_pct", type number}, {"return_5yr_pct", type number}, {"sharpe_ratio", type number}, {"std_dev_ann_pct", type number}, {"aum_crore", type number}, {"expense_ratio_pct", type number}, {"morningstar_rating", Int64.Type}})
in
    #"Changed Type"

// 6. fact_aum (AUM Growth by Fund House)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/03_aum_by_fund_house_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"date", type date}, {"aum_lakh_crore", type number}, {"aum_crore", type number}, {"num_schemes", Int64.Type}})
in
    #"Changed Type"

// 7. monthly_sip_inflows (SIP Trend 2022-2025)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/04_monthly_sip_inflows_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"sip_inflow_crore", type number}, {"active_sip_accounts_crore", type number}, {"new_sip_accounts_lakh", type number}, {"sip_aum_lakh_crore", type number}, {"yoy_growth_pct", type number}})
in
    #"Changed Type"

// 8. category_inflows (Category Net Inflow Heatmap)
let
    Source = Csv.Document(File.Contents("D:/Admin/Documents/mutual_fund_analysis/data/processed/05_category_inflows_cleaned.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.None]),
    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"net_inflow_crore", type number}})
in
    #"Changed Type"
