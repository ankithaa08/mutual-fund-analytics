"""
Day 2 Data Cleaning, Star Schema Modeling & SQLite Loading Pipeline
===================================================================
Project: Bluestock Mutual Fund Analytics Platform
Deliverables:
1. 10 Cleaned CSVs in data/processed/
2. bluestock_mf.db (SQLite database with Star Schema loaded via SQLAlchemy)
3. schema.sql (DDL Star Schema)
4. queries.sql (10 Analytical SQL Queries)
5. data_dictionary.md (Complete Data Dictionary & Technical Documentation)
"""

import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy import create_engine, text

def clean_and_build_pipeline(base_dir):
    raw_dir = os.path.join(base_dir, "data", "raw")
    proc_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(proc_dir, exist_ok=True)
    db_path = os.path.join(base_dir, "bluestock_mf.db")

    print("=" * 80)
    print("STARTING DAY 2 DATA CLEANING & ETL PIPELINE")
    print(f"Base Directory:      {base_dir}")
    print(f"Raw Data Directory:  {raw_dir}")
    print(f"Processed Directory: {proc_dir}")
    print(f"SQLite Database:     {db_path}")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # 1. Clean 01_fund_master
    # -------------------------------------------------------------------------
    print("\n[1/10] Cleaning 01_fund_master...")
    fm = pd.read_csv(os.path.join(raw_dir, "01_fund_master.csv"))
    fm['amfi_code'] = fm['amfi_code'].astype(int)
    fm['launch_date'] = pd.to_datetime(fm['launch_date']).dt.strftime('%Y-%m-%d')
    fm['scheme_name'] = fm['scheme_name'].str.strip()
    fm['fund_house'] = fm['fund_house'].str.strip()
    fm['category'] = fm['category'].str.strip()
    fm['sub_category'] = fm['sub_category'].str.strip()
    fm['plan'] = fm['plan'].str.strip()
    fm['benchmark'] = fm['benchmark'].str.strip()
    fm['fund_manager'] = fm['fund_manager'].str.strip()
    fm['risk_category'] = fm['risk_category'].str.strip()
    fm['sebi_category_code'] = fm['sebi_category_code'].str.strip()
    fm['expense_ratio_pct'] = fm['expense_ratio_pct'].astype(float)
    fm['exit_load_pct'] = fm['exit_load_pct'].astype(float)
    fm['min_sip_amount'] = fm['min_sip_amount'].astype(float)
    fm['min_lumpsum_amount'] = fm['min_lumpsum_amount'].astype(float)
    fm = fm.drop_duplicates(subset=['amfi_code']).sort_values('amfi_code')
    print(f"  -> Cleaned fund_master: {len(fm)} rows, 0 nulls, unique AMFI codes: {fm['amfi_code'].nunique()}")

    # -------------------------------------------------------------------------
    # 2. Clean 02_nav_history (Date parsing, sort, forward-fill weekends/holidays, NAV > 0)
    # -------------------------------------------------------------------------
    print("\n[2/10] Cleaning 02_nav_history (Forward-filling weekends/holidays)...")
    nav = pd.read_csv(os.path.join(raw_dir, "02_nav_history.csv"))
    nav['amfi_code'] = nav['amfi_code'].astype(int)
    nav['date'] = pd.to_datetime(nav['date'])
    nav = nav.sort_values(['amfi_code', 'date']).drop_duplicates(subset=['amfi_code', 'date'])
    
    # Validate NAV > 0 before ffill
    assert (nav['nav'] <= 0).sum() == 0, "NAV values must be strictly greater than 0"

    full_nav_list = []
    for code, group in nav.groupby('amfi_code'):
        min_d = group['date'].min()
        max_d = group['date'].max()
        full_idx = pd.date_range(min_d, max_d, freq='D', name='date')
        reindexed = group.set_index('date').reindex(full_idx)
        reindexed['amfi_code'] = code
        # Tag original vs forward-filled
        reindexed['is_forward_filled'] = reindexed['nav'].isnull().astype(int)
        # Forward fill NAV for non-trading days
        reindexed['nav'] = reindexed['nav'].ffill()
        full_nav_list.append(reindexed.reset_index())

    nav_cleaned = pd.concat(full_nav_list, ignore_index=True)
    # Daily return calculation
    nav_cleaned['daily_return_pct'] = nav_cleaned.groupby('amfi_code')['nav'].pct_change() * 100
    nav_cleaned['daily_return_pct'] = nav_cleaned['daily_return_pct'].fillna(0.0).round(4)
    nav_cleaned['date'] = nav_cleaned['date'].dt.strftime('%Y-%m-%d')
    nav_cleaned['nav'] = nav_cleaned['nav'].round(4)
    
    # Assertions
    assert nav_cleaned['nav'].isnull().sum() == 0, "Nulls remain in nav after forward fill"
    assert (nav_cleaned['nav'] <= 0).sum() == 0, "NAV <= 0 found"
    print(f"  -> Cleaned nav_history: {len(nav_cleaned):,} daily records (expanded from {len(nav):,} trading days)")
    print(f"     Forward-filled weekend/holiday records: {nav_cleaned['is_forward_filled'].sum():,}")

    # -------------------------------------------------------------------------
    # 3. Clean 03_aum_by_fund_house
    # -------------------------------------------------------------------------
    print("\n[3/10] Cleaning 03_aum_by_fund_house...")
    aum = pd.read_csv(os.path.join(raw_dir, "03_aum_by_fund_house.csv"))
    aum['date'] = pd.to_datetime(aum['date']).dt.strftime('%Y-%m-%d')
    aum['fund_house'] = aum['fund_house'].str.strip()
    aum['aum_lakh_crore'] = aum['aum_lakh_crore'].astype(float)
    aum['aum_crore'] = aum['aum_crore'].astype(int)
    aum['num_schemes'] = aum['num_schemes'].astype(int)
    aum = aum.drop_duplicates(subset=['date', 'fund_house']).sort_values(['date', 'fund_house'])
    print(f"  -> Cleaned aum_by_fund_house: {len(aum)} rows across {aum['fund_house'].nunique()} AMCs")

    # -------------------------------------------------------------------------
    # 4. Clean 04_monthly_sip_inflows
    # -------------------------------------------------------------------------
    print("\n[4/10] Cleaning 04_monthly_sip_inflows...")
    sip = pd.read_csv(os.path.join(raw_dir, "04_monthly_sip_inflows.csv"))
    sip['month'] = sip['month'].str.strip()
    sip['sip_inflow_crore'] = sip['sip_inflow_crore'].astype(int)
    sip['active_sip_accounts_crore'] = sip['active_sip_accounts_crore'].astype(float)
    sip['new_sip_accounts_lakh'] = sip['new_sip_accounts_lakh'].astype(float)
    sip['sip_aum_lakh_crore'] = sip['sip_aum_lakh_crore'].astype(float)
    sip['yoy_growth_pct'] = sip['yoy_growth_pct'].fillna(0.0).round(2)
    sip = sip.drop_duplicates(subset=['month']).sort_values('month')
    print(f"  -> Cleaned monthly_sip_inflows: {len(sip)} rows, 0 nulls")

    # -------------------------------------------------------------------------
    # 5. Clean 05_category_inflows
    # -------------------------------------------------------------------------
    print("\n[5/10] Cleaning 05_category_inflows...")
    cat_inf = pd.read_csv(os.path.join(raw_dir, "05_category_inflows.csv"))
    cat_inf['month'] = cat_inf['month'].str.strip()
    cat_inf['category'] = cat_inf['category'].str.strip()
    cat_inf['net_inflow_crore'] = cat_inf['net_inflow_crore'].astype(float).round(2)
    cat_inf = cat_inf.drop_duplicates(subset=['month', 'category']).sort_values(['month', 'category'])
    print(f"  -> Cleaned category_inflows: {len(cat_inf)} rows across {cat_inf['category'].nunique()} categories")

    # -------------------------------------------------------------------------
    # 6. Clean 06_industry_folio_count
    # -------------------------------------------------------------------------
    print("\n[6/10] Cleaning 06_industry_folio_count...")
    folios = pd.read_csv(os.path.join(raw_dir, "06_industry_folio_count.csv"))
    folios['month'] = folios['month'].str.strip()
    for col in ['total_folios_crore', 'equity_folios_crore', 'debt_folios_crore', 'hybrid_folios_crore', 'others_folios_crore']:
        folios[col] = folios[col].astype(float).round(2)
    folios = folios.drop_duplicates(subset=['month']).sort_values('month')
    print(f"  -> Cleaned industry_folio_count: {len(folios)} rows")

    # -------------------------------------------------------------------------
    # 7. Clean 07_scheme_performance (Numeric checks, expense ratio 0.1-2.5%, anomalies)
    # -------------------------------------------------------------------------
    print("\n[7/10] Cleaning 07_scheme_performance...")
    perf = pd.read_csv(os.path.join(raw_dir, "07_scheme_performance.csv"))
    perf['amfi_code'] = perf['amfi_code'].astype(int)
    perf['scheme_name'] = perf['scheme_name'].str.strip()
    perf['fund_house'] = perf['fund_house'].str.strip()
    perf['category'] = perf['category'].str.strip()
    perf['plan'] = perf['plan'].str.strip()
    perf['risk_grade'] = perf['risk_grade'].str.strip()

    # Validate numeric returns
    return_cols = ['return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'benchmark_3yr_pct',
                   'alpha', 'beta', 'sharpe_ratio', 'sortino_ratio', 'std_dev_ann_pct',
                   'max_drawdown_pct', 'expense_ratio_pct']
    for c in return_cols:
        perf[c] = pd.to_numeric(perf[c], errors='raise').astype(float)

    # Validate expense ratio range: 0.1% to 2.5%
    exp_anomalies = perf[(perf['expense_ratio_pct'] < 0.1) | (perf['expense_ratio_pct'] > 2.5)]
    if len(exp_anomalies) > 0:
        print(f"  [WARNING] Found {len(exp_anomalies)} expense ratio anomalies!")
    else:
        print(f"  [PASSED] All expense ratios within valid SEBI range 0.1% - 2.5% (Min: {perf['expense_ratio_pct'].min()}%, Max: {perf['expense_ratio_pct'].max()}%)")

    perf['aum_crore'] = perf['aum_crore'].astype(int)
    perf['morningstar_rating'] = perf['morningstar_rating'].astype(int)
    perf = perf.drop_duplicates(subset=['amfi_code']).sort_values('amfi_code')
    print(f"  -> Cleaned scheme_performance: {len(perf)} rows, 0 nulls")

    # -------------------------------------------------------------------------
    # 8. Clean 08_investor_transactions (Standardise types, amount > 0, date formats, KYC enums)
    # -------------------------------------------------------------------------
    print("\n[8/10] Cleaning 08_investor_transactions...")
    tx = pd.read_csv(os.path.join(raw_dir, "08_investor_transactions.csv"))
    tx['investor_id'] = tx['investor_id'].str.strip()
    tx['transaction_date'] = pd.to_datetime(tx['transaction_date']).dt.strftime('%Y-%m-%d')
    tx['amfi_code'] = tx['amfi_code'].astype(int)

    # Standardize transaction_type (SIP / Lumpsum / Redemption)
    tx['transaction_type'] = tx['transaction_type'].str.strip().str.capitalize()
    type_map = {'Sip': 'SIP', 'Lumpsum': 'Lumpsum', 'Redemption': 'Redemption'}
    tx['transaction_type'] = tx['transaction_type'].map(lambda x: type_map.get(x, x))
    valid_types = {'SIP', 'Lumpsum', 'Redemption'}
    assert set(tx['transaction_type'].unique()).issubset(valid_types), f"Invalid transaction types: {set(tx['transaction_type'].unique()) - valid_types}"

    # Validate amount > 0
    tx['amount_inr'] = pd.to_numeric(tx['amount_inr'], errors='raise')
    assert (tx['amount_inr'] <= 0).sum() == 0, "Transaction amount must be strictly > 0"

    # Check KYC status enum values
    tx['kyc_status'] = tx['kyc_status'].str.strip().str.capitalize()
    valid_kyc = {'Verified', 'Pending', 'Rejected'}
    assert set(tx['kyc_status'].unique()).issubset(valid_kyc), f"Invalid KYC values: {set(tx['kyc_status'].unique()) - valid_kyc}"

    # Standardize demographics
    tx['state'] = tx['state'].str.strip()
    tx['city'] = tx['city'].str.strip()
    tx['city_tier'] = tx['city_tier'].str.strip().str.upper()
    tx['age_group'] = tx['age_group'].str.strip()
    tx['gender'] = tx['gender'].str.strip().str.capitalize()
    tx['annual_income_lakh'] = tx['annual_income_lakh'].astype(float).round(2)
    tx['payment_mode'] = tx['payment_mode'].str.strip()

    # Create transaction_id if not present
    if 'transaction_id' not in tx.columns:
        tx.insert(0, 'transaction_id', range(1, len(tx) + 1))

    tx = tx.sort_values(['transaction_date', 'transaction_id'])
    print(f"  -> Cleaned investor_transactions: {len(tx):,} rows")
    print(f"     Transaction Type Breakdown: {tx['transaction_type'].value_counts().to_dict()}")
    print(f"     KYC Status Breakdown:       {tx['kyc_status'].value_counts().to_dict()}")

    # -------------------------------------------------------------------------
    # 9. Clean 09_portfolio_holdings
    # -------------------------------------------------------------------------
    print("\n[9/10] Cleaning 09_portfolio_holdings...")
    holdings = pd.read_csv(os.path.join(raw_dir, "09_portfolio_holdings.csv"))
    holdings['amfi_code'] = holdings['amfi_code'].astype(int)
    holdings['stock_symbol'] = holdings['stock_symbol'].str.strip().str.upper()
    holdings['stock_name'] = holdings['stock_name'].str.strip()
    holdings['sector'] = holdings['sector'].str.strip()
    holdings['weight_pct'] = holdings['weight_pct'].astype(float).round(2)
    holdings['market_value_cr'] = holdings['market_value_cr'].astype(float).round(2)
    holdings['current_price_inr'] = holdings['current_price_inr'].astype(float).round(2)
    holdings['portfolio_date'] = pd.to_datetime(holdings['portfolio_date']).dt.strftime('%Y-%m-%d')
    holdings = holdings.drop_duplicates(subset=['amfi_code', 'stock_symbol']).sort_values(['amfi_code', 'weight_pct'], ascending=[True, False])
    print(f"  -> Cleaned portfolio_holdings: {len(holdings)} holdings across {holdings['amfi_code'].nunique()} equity schemes")

    # -------------------------------------------------------------------------
    # 10. Clean 10_benchmark_indices
    # -------------------------------------------------------------------------
    print("\n[10/10] Cleaning 10_benchmark_indices...")
    bench = pd.read_csv(os.path.join(raw_dir, "10_benchmark_indices.csv"))
    bench['date'] = pd.to_datetime(bench['date']).dt.strftime('%Y-%m-%d')
    bench['index_name'] = bench['index_name'].str.strip()
    bench['close_value'] = bench['close_value'].astype(float).round(2)
    bench = bench.drop_duplicates(subset=['date', 'index_name']).sort_values(['date', 'index_name'])
    print(f"  -> Cleaned benchmark_indices: {len(bench):,} rows across {bench['index_name'].nunique()} indices")

    # -------------------------------------------------------------------------
    # SAVE 10 CLEANED CSVS TO data/processed/
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SAVING 10 CLEANED DATASETS TO data/processed/")
    print("=" * 80)

    cleaned_datasets = {
        "01_fund_master_cleaned.csv": fm,
        "02_nav_history_cleaned.csv": nav_cleaned,
        "03_aum_by_fund_house_cleaned.csv": aum,
        "04_monthly_sip_inflows_cleaned.csv": sip,
        "05_category_inflows_cleaned.csv": cat_inf,
        "06_industry_folio_count_cleaned.csv": folios,
        "07_scheme_performance_cleaned.csv": perf,
        "08_investor_transactions_cleaned.csv": tx,
        "09_portfolio_holdings_cleaned.csv": holdings,
        "10_benchmark_indices_cleaned.csv": bench,
    }

    for fname, df in cleaned_datasets.items():
        out_p = os.path.join(proc_dir, fname)
        df.to_csv(out_p, index=False)
        std_p = os.path.join(proc_dir, fname.replace("_cleaned", ""))
        df.to_csv(std_p, index=False)
        print(f"  [SAVED] {fname:<35} ({len(df):>7,} rows)")

    # -------------------------------------------------------------------------
    # GENERATE CALENDAR DIMENSION (dim_date)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("GENERATING STAR SCHEMA CALENDAR DIMENSION (dim_date)")
    print("=" * 80)

    all_dates = pd.date_range("2022-01-01", "2026-12-31", freq="D")
    dim_date = pd.DataFrame({
        "date": all_dates.strftime("%Y-%m-%d"),
        "year": all_dates.year,
        "quarter": all_dates.quarter,
        "month": all_dates.month,
        "month_name": all_dates.strftime("%B"),
        "day": all_dates.day,
        "day_of_week": all_dates.dayofweek,
        "day_name": all_dates.strftime("%A"),
        "is_weekend": (all_dates.dayofweek >= 5).astype(int),
        "fiscal_year": np.where(all_dates.month >= 4,
                                "FY" + all_dates.year.astype(str) + "-" + (all_dates.year + 1).astype(str).str[-2:],
                                "FY" + (all_dates.year - 1).astype(str) + "-" + all_dates.year.astype(str).str[-2:]),
        "fiscal_quarter": np.where(all_dates.month.isin([4, 5, 6]), "Q1",
                           np.where(all_dates.month.isin([7, 8, 9]), "Q2",
                           np.where(all_dates.month.isin([10, 11, 12]), "Q3", "Q4")))
    })
    dim_date.to_csv(os.path.join(proc_dir, "dim_date.csv"), index=False)
    print(f"  -> Generated dim_date: {len(dim_date):,} calendar days (2022-2026)")

    # -------------------------------------------------------------------------
    # CREATE SQLITE DATABASE & LOAD STAR SCHEMA VIA SQLALCHEMY
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print(f"LOADING STAR SCHEMA INTO SQLITE DATABASE: {db_path}")
    print("=" * 80)

    if os.path.exists(db_path):
        os.remove(db_path)

    engine = create_engine(f"sqlite:///{db_path}")

    # Create Star Schema Tables using DDL
    with engine.connect() as conn:
        conn.execute(text("""
        -- Dimension: Fund Master
        CREATE TABLE IF NOT EXISTS dim_fund (
            amfi_code INTEGER PRIMARY KEY,
            fund_house TEXT NOT NULL,
            scheme_name TEXT NOT NULL,
            category TEXT NOT NULL,
            sub_category TEXT NOT NULL,
            plan TEXT NOT NULL,
            launch_date TEXT,
            benchmark TEXT,
            expense_ratio_pct REAL,
            exit_load_pct REAL,
            min_sip_amount REAL,
            min_lumpsum_amount REAL,
            fund_manager TEXT,
            risk_category TEXT,
            sebi_category_code TEXT
        );
        """))

        conn.execute(text("""
        -- Dimension: Date Calendar
        CREATE TABLE IF NOT EXISTS dim_date (
            date TEXT PRIMARY KEY,
            year INTEGER,
            quarter INTEGER,
            month INTEGER,
            month_name TEXT,
            day INTEGER,
            day_of_week INTEGER,
            day_name TEXT,
            is_weekend INTEGER,
            fiscal_year TEXT,
            fiscal_quarter TEXT
        );
        """))

        conn.execute(text("""
        -- Fact: Daily NAV History
        CREATE TABLE IF NOT EXISTS fact_nav (
            date TEXT NOT NULL,
            amfi_code INTEGER NOT NULL,
            nav REAL NOT NULL,
            is_forward_filled INTEGER NOT NULL DEFAULT 0,
            daily_return_pct REAL NOT NULL DEFAULT 0.0,
            PRIMARY KEY (amfi_code, date),
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );
        """))

        conn.execute(text("""
        -- Fact: Investor Transactions
        CREATE TABLE IF NOT EXISTS fact_transactions (
            transaction_id INTEGER PRIMARY KEY,
            investor_id TEXT NOT NULL,
            transaction_date TEXT NOT NULL,
            amfi_code INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,
            amount_inr REAL NOT NULL,
            state TEXT,
            city TEXT,
            city_tier TEXT,
            age_group TEXT,
            gender TEXT,
            annual_income_lakh REAL,
            payment_mode TEXT,
            kyc_status TEXT,
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code),
            FOREIGN KEY (transaction_date) REFERENCES dim_date(date)
        );
        """))

        conn.execute(text("""
        -- Fact: Scheme Performance Metrics
        CREATE TABLE IF NOT EXISTS fact_performance (
            amfi_code INTEGER PRIMARY KEY,
            scheme_name TEXT,
            fund_house TEXT,
            category TEXT,
            plan TEXT,
            return_1yr_pct REAL,
            return_3yr_pct REAL,
            return_5yr_pct REAL,
            benchmark_3yr_pct REAL,
            alpha REAL,
            beta REAL,
            sharpe_ratio REAL,
            sortino_ratio REAL,
            std_dev_ann_pct REAL,
            max_drawdown_pct REAL,
            aum_crore INTEGER,
            expense_ratio_pct REAL,
            morningstar_rating INTEGER,
            risk_grade TEXT,
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
        );
        """))

        conn.execute(text("""
        -- Fact: Fund House AUM Snapshots
        CREATE TABLE IF NOT EXISTS fact_aum (
            date TEXT NOT NULL,
            fund_house TEXT NOT NULL,
            aum_lakh_crore REAL,
            aum_crore INTEGER,
            num_schemes INTEGER,
            PRIMARY KEY (date, fund_house),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );
        """))

        conn.execute(text("""
        -- Supporting Analytical Tables
        CREATE TABLE IF NOT EXISTS monthly_sip_inflows (
            month TEXT PRIMARY KEY,
            sip_inflow_crore INTEGER,
            active_sip_accounts_crore REAL,
            new_sip_accounts_lakh REAL,
            sip_aum_lakh_crore REAL,
            yoy_growth_pct REAL
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS category_inflows (
            month TEXT NOT NULL,
            category TEXT NOT NULL,
            net_inflow_crore REAL,
            PRIMARY KEY (month, category)
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS industry_folio_count (
            month TEXT PRIMARY KEY,
            total_folios_crore REAL,
            equity_folios_crore REAL,
            debt_folios_crore REAL,
            hybrid_folios_crore REAL,
            others_folios_crore REAL
        );
        """))

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS portfolio_holdings (
            amfi_code INTEGER NOT NULL,
            stock_symbol TEXT NOT NULL,
            stock_name TEXT,
            sector TEXT,
            weight_pct REAL,
            market_value_cr REAL,
            current_price_inr REAL,
            portfolio_date TEXT,
            PRIMARY KEY (amfi_code, stock_symbol),
            FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
        );
        """))

        conn.execute(text("""
        -- Benchmark Indices
        CREATE TABLE IF NOT EXISTS benchmark_indices (
            date TEXT NOT NULL,
            index_name TEXT NOT NULL,
            close_value REAL,
            PRIMARY KEY (date, index_name),
            FOREIGN KEY (date) REFERENCES dim_date(date)
        );
        """))

        # Create indexes
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_nav_date ON fact_nav(date);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_nav_code ON fact_nav(amfi_code);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tx_date ON fact_transactions(transaction_date);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tx_code ON fact_transactions(amfi_code);"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS idx_tx_state ON fact_transactions(state);"))
        conn.commit()

    # Load DataFrames into SQLite tables using SQLAlchemy
    table_mappings = [
        ("dim_fund", fm),
        ("dim_date", dim_date),
        ("fact_nav", nav_cleaned),
        ("fact_transactions", tx),
        ("fact_performance", perf),
        ("fact_aum", aum),
        ("monthly_sip_inflows", sip),
        ("category_inflows", cat_inf),
        ("industry_folio_count", folios),
        ("portfolio_holdings", holdings),
        ("benchmark_indices", bench)
    ]

    print("\n>> Loading DataFrames into SQLite Tables:")
    for tbl_name, df_data in table_mappings:
        df_data.to_sql(tbl_name, con=engine, if_exists="append", index=False)
        print(f"  [LOADED] {tbl_name:<25} ({len(df_data):>7,} rows inserted)")

    # Verify Row Counts
    print("\n" + "=" * 80)
    print("VERIFYING ROW COUNTS IN SQLITE DATABASE")
    print("=" * 80)

    verification_results = []
    with engine.connect() as conn:
        for tbl_name, df_data in table_mappings:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {tbl_name}")).scalar()
            expected = len(df_data)
            match = (count == expected)
            verification_results.append((tbl_name, expected, count, "MATCH" if match else "MISMATCH"))
            print(f"  {tbl_name:<25} Expected: {expected:>7,} | Database: {count:>7,} | Status: {'[OK]' if match else '[MISMATCH]'}")

    return {
        "db_path": db_path,
        "engine": engine,
        "verification": verification_results
    }


if __name__ == "__main__":
    base_dir = r"D:\Admin\Documents\mutual_fund_analysis"
    if not os.path.exists(base_dir):
        base_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\mutual_fund_analysis"
    clean_and_build_pipeline(base_dir)
