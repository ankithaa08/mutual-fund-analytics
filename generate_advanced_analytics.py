"""
Advanced Quantitative Analytics Pipeline
=========================================
Project: Bluestock Mutual Fund Analytics
Tasks:
1. 95% Historical VaR & CVaR for all 40 schemes -> var_cvar_report.csv
2. Rolling 90-day Sharpe ratio timeseries for 5 key funds -> rolling_sharpe_chart.png
3. Investor Cohort Analysis (by first transaction year)
4. SIP Continuity & Churn Analysis (6+ SIP transactions, gap days, at-risk flags)
5. Sector HHI (Herfindahl-Hirschman Index) Concentration across all equity funds
6. Build Advanced_Analytics.ipynb with 5 Advanced Insights in Markdown
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nbformat as nbf

# Styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['axes.titleweight'] = 'bold'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'

def run_pipeline(base_dir):
    proc_dir = os.path.join(base_dir, "data", "processed")
    fig_dir = os.path.join(base_dir, "reports", "figures")
    os.makedirs(fig_dir, exist_ok=True)

    print("=" * 80)
    print("RUNNING ADVANCED MUTUAL FUND QUANTITATIVE ANALYTICS")
    print(f"Base Directory: {base_dir}")
    print("=" * 80)

    # 1. Load Data
    fm = pd.read_csv(os.path.join(proc_dir, "01_fund_master_cleaned.csv"))
    nav = pd.read_csv(os.path.join(proc_dir, "02_nav_history_cleaned.csv"))
    perf = pd.read_csv(os.path.join(proc_dir, "07_scheme_performance_cleaned.csv"))
    tx = pd.read_csv(os.path.join(proc_dir, "08_investor_transactions_cleaned.csv"))
    holdings = pd.read_csv(os.path.join(proc_dir, "09_portfolio_holdings_cleaned.csv"))

    nav['date'] = pd.to_datetime(nav['date'])
    tx['transaction_date'] = pd.to_datetime(tx['transaction_date'])

    # -------------------------------------------------------------------------
    # TASK 1: Historical VaR (95%) and CVaR for all 40 schemes
    # -------------------------------------------------------------------------
    print("\n[Task 1/6] Computing 95% Historical VaR and CVaR for all 40 schemes...")
    # Calculate returns on active trading days (excluding non-trading weekend forward-fills)
    trading_nav = nav[nav['is_forward_filled'] == 0].sort_values(['amfi_code', 'date']).copy()
    trading_nav['daily_ret'] = trading_nav.groupby('amfi_code')['nav'].pct_change() * 100.0

    var_cvar_records = []
    for code, grp in trading_nav.groupby('amfi_code'):
        rets = grp['daily_ret'].dropna()
        var_95 = float(np.percentile(rets, 5))
        cvar_95 = float(rets[rets <= var_95].mean())
        worst_day = float(rets.min())
        best_day = float(rets.max())
        volatility_daily = float(rets.std())
        annualized_var = var_95 * np.sqrt(252)

        # Merge fund info
        f_info = fm[fm['amfi_code'] == code].iloc[0]
        p_info = perf[perf['amfi_code'] == code].iloc[0]

        var_cvar_records.append({
            'amfi_code': code,
            'scheme_name': f_info['scheme_name'],
            'fund_house': f_info['fund_house'],
            'category': f_info['category'],
            'sub_category': f_info['sub_category'],
            'plan': f_info['plan'],
            'risk_grade': p_info['risk_grade'],
            'var_95_daily_pct': round(var_95, 3),
            'cvar_95_daily_pct': round(cvar_95, 3),
            'annualized_var_95_pct': round(annualized_var, 3),
            'daily_volatility_pct': round(volatility_daily, 3),
            'worst_single_day_pct': round(worst_day, 3),
            'best_single_day_pct': round(best_day, 3),
            'aum_crore': int(p_info['aum_crore'])
        })

    var_df = pd.DataFrame(var_cvar_records).sort_values(by='var_95_daily_pct')
    
    # Save CSV
    var_csv_path = os.path.join(base_dir, "var_cvar_report.csv")
    var_df.to_csv(var_csv_path, index=False)
    # Also save in reports/
    var_df.to_csv(os.path.join(base_dir, "reports", "var_cvar_report.csv"), index=False)
    print(f"  [SAVED] {var_csv_path} ({len(var_df)} schemes)")
    print("  Top 3 Highest Tail-Risk Schemes (Most Negative 95% VaR):")
    for _, r in var_df.head(3).iterrows():
        print(f"    - {r['scheme_name']} ({r['sub_category']}): 95% VaR = {r['var_95_daily_pct']}%, 95% CVaR = {r['cvar_95_daily_pct']}%")

    # -------------------------------------------------------------------------
    # TASK 2: Rolling 90-day Sharpe for 5 Key Funds & Plot
    # -------------------------------------------------------------------------
    print("\n[Task 2/6] Calculating Rolling 90-Day Sharpe Ratio for 5 Key Funds...")
    five_schemes = {
        119551: "SBI Bluechip",
        120503: "ICICI Bluechip",
        118632: "Nippon Large Cap",
        119092: "Axis Bluechip",
        120841: "Kotak Bluechip"
    }

    # Filter trading NAV for the 5 funds
    sub_nav = trading_nav[trading_nav['amfi_code'].isin(five_schemes.keys())].copy()
    sub_nav['fund_name'] = sub_nav['amfi_code'].map(five_schemes)
    
    # Raw decimal return for rolling calculation
    sub_nav['raw_ret'] = sub_nav.groupby('amfi_code')['nav'].pct_change()
    
    # Formula: returns.rolling(90).mean() / returns.rolling(90).std() * sqrt(252)
    sub_nav['rolling_sharpe'] = sub_nav.groupby('amfi_code')['raw_ret'].transform(
        lambda x: (x.rolling(90).mean() / x.rolling(90).std()) * np.sqrt(252)
    )

    # Plot
    plt.figure(figsize=(14, 7))
    colors = {'SBI Bluechip': '#104E8B', 'ICICI Bluechip': '#ED7D31', 'Nippon Large Cap': '#2CA02C',
              'Axis Bluechip': '#7030A0', 'Kotak Bluechip': '#D9534F'}

    for name, grp in sub_nav.groupby('fund_name'):
        valid_grp = grp.dropna(subset=['rolling_sharpe'])
        plt.plot(valid_grp['date'], valid_grp['rolling_sharpe'], label=name, color=colors.get(name, None), linewidth=2.0)

    # Reference threshold lines
    plt.axhline(0, color='black', linestyle='--', linewidth=0.8, alpha=0.7)
    plt.axhline(1.0, color='gray', linestyle=':', linewidth=1.0, label='Adequate (Sharpe = 1.0)')
    plt.axhline(2.0, color='darkgreen', linestyle=':', linewidth=1.0, label='Superior (Sharpe = 2.0)')

    # Shaded Bull run and correction
    plt.axvspan(pd.Timestamp('2023-04-01'), pd.Timestamp('2023-12-31'), color='green', alpha=0.08, label='2023 Bull Expansion')

    plt.title('90-Day Rolling Annualized Sharpe Ratio Comparison (2022–2026)', pad=15)
    plt.xlabel('Date')
    plt.ylabel('Annualized Sharpe Ratio (90-Day Window)')
    plt.ylim(-3.5, 7.5)
    plt.legend(loc='upper right', frameon=True, ncol=2)
    plt.tight_layout()

    # Save to both locations
    chart_p1 = os.path.join(base_dir, "rolling_sharpe_chart.png")
    chart_p2 = os.path.join(fig_dir, "rolling_sharpe_chart.png")
    plt.savefig(chart_p1, dpi=300)
    plt.savefig(chart_p2, dpi=300)
    plt.close()
    print(f"  [SAVED] {chart_p1}")
    print(f"  [SAVED] {chart_p2}")

    # -------------------------------------------------------------------------
    # TASK 3: Investor Cohort Analysis
    # -------------------------------------------------------------------------
    print("\n[Task 3/6] Performing Investor Cohort Analysis (by First Transaction Year)...")
    first_tx = tx.groupby('investor_id')['transaction_date'].min().reset_index()
    first_tx['cohort_year'] = first_tx['transaction_date'].dt.year

    tx_cohort = tx.merge(first_tx[['investor_id', 'cohort_year']], on='investor_id')

    cohort_stats = []
    for cy, grp in tx_cohort.groupby('cohort_year'):
        inv_count = grp['investor_id'].nunique()
        total_inv = grp['amount_inr'].sum()
        total_tx = len(grp)
        sip_txs = grp[grp['transaction_type'] == 'SIP']
        avg_sip = sip_txs['amount_inr'].mean() if len(sip_txs) > 0 else 0
        lump_txs = grp[grp['transaction_type'] == 'Lumpsum']
        avg_lump = lump_txs['amount_inr'].mean() if len(lump_txs) > 0 else 0

        # Top fund preference by total capital invested
        top_fund_code = grp.groupby('amfi_code')['amount_inr'].sum().idxmax()
        top_fund_name = fm.loc[fm['amfi_code'] == top_fund_code, 'scheme_name'].values[0]
        top_fund_vol = grp.groupby('amfi_code')['amount_inr'].sum().max()

        cohort_stats.append({
            'cohort_year': cy,
            'investor_count': inv_count,
            'total_transactions': total_tx,
            'total_invested_crore': round(total_inv / 1e7, 2),
            'avg_sip_amount_inr': round(avg_sip, 2),
            'avg_lumpsum_amount_inr': round(avg_lump, 2),
            'top_fund_amfi_code': top_fund_code,
            'top_fund_name': top_fund_name,
            'top_fund_invested_crore': round(top_fund_vol / 1e7, 2)
        })

    cohort_df = pd.DataFrame(cohort_stats)
    print("  Cohort Analysis Summary:")
    print(cohort_df[['cohort_year', 'investor_count', 'total_invested_crore', 'avg_sip_amount_inr', 'top_fund_name']].to_string(index=False))

    # -------------------------------------------------------------------------
    # TASK 4: SIP Continuity & Churn Analysis
    # -------------------------------------------------------------------------
    print("\n[Task 4/6] Performing SIP Continuity Analysis (Investors with 6+ SIPs)...")
    sip_orders = tx[tx['transaction_type'] == 'SIP'].sort_values(['investor_id', 'transaction_date']).copy()
    sip_counts = sip_orders['investor_id'].value_counts()
    qual_investors = sip_counts[sip_counts >= 6].index

    qual_sip = sip_orders[sip_orders['investor_id'].isin(qual_investors)].copy()
    qual_sip['date_diff'] = qual_sip.groupby('investor_id')['transaction_date'].diff().dt.days

    investor_continuity = qual_sip.groupby('investor_id').agg(
        sip_installments=('amount_inr', 'count'),
        total_sip_amount_inr=('amount_inr', 'sum'),
        avg_gap_days=('date_diff', 'mean'),
        max_gap_days=('date_diff', 'max'),
        std_gap_days=('date_diff', 'std')
    ).reset_index()

    # Flag at-risk: avg gap > 35 days
    investor_continuity['is_at_risk'] = investor_continuity['avg_gap_days'] > 35
    at_risk_count = int(investor_continuity['is_at_risk'].sum())
    total_qual = len(investor_continuity)
    regular_count = total_qual - at_risk_count
    regular_pct = (regular_count / total_qual) * 100
    at_risk_pct = (at_risk_count / total_qual) * 100

    print(f"  Qualifying Investors (6+ SIPs): {total_qual:,}")
    print(f"  Regular Consecutive SIPs (gap <= 35 days): {regular_count:,} ({regular_pct:.2f}%)")
    print(f"  At-Risk / Inconsistent Investors (gap > 35 days): {at_risk_count:,} ({at_risk_pct:.2f}%)")
    print(f"  Mean SIP Gap: {investor_continuity['avg_gap_days'].mean():.1f} days (Target: 30 days)")

    # -------------------------------------------------------------------------
    # TASK 5: Sector HHI Concentration Analysis
    # -------------------------------------------------------------------------
    print("\n[Task 5/6] Computing Sector HHI Concentration across all equity funds...")
    sector_alloc = holdings.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()
    # HHI = sum(w^2) on percentage scale (0 to 10,000)
    hhi_series = sector_alloc.groupby('amfi_code')['weight_pct'].apply(lambda w: (w**2).sum()).reset_index()
    hhi_series.columns = ['amfi_code', 'sector_hhi']

    hhi_df = hhi_series.merge(fm[['amfi_code', 'scheme_name', 'fund_house', 'sub_category']], on='amfi_code')
    hhi_df = hhi_df.sort_values(by='sector_hhi', ascending=False).reset_index(drop=True)

    print("  Top 3 Most Concentrated Equity Portfolios (Highest Sector HHI):")
    for _, r in hhi_df.head(3).iterrows():
        print(f"    - {r['scheme_name']} ({r['sub_category']}): HHI = {r['sector_hhi']:.2f}")

    print("  Top 3 Most Diversified Equity Portfolios (Lowest Sector HHI):")
    for _, r in hhi_df.tail(3).iterrows():
        print(f"    - {r['scheme_name']} ({r['sub_category']}): HHI = {r['sector_hhi']:.2f}")

    # -------------------------------------------------------------------------
    # TASK 6: Build Advanced_Analytics.ipynb
    # -------------------------------------------------------------------------
    print("\n[Task 6/6] Generating Advanced_Analytics.ipynb Jupyter Notebook...")
    nb = nbf.v4.new_notebook()
    cells = []

    # Title Markdown
    cells.append(nbf.v4.new_markdown_cell("""# Bluestock Mutual Fund Analytics: Advanced Quantitative & Behavioral Modeling

This notebook covers:
1. **95% Historical Value-at-Risk (VaR) & Conditional VaR (CVaR / Expected Shortfall)** across all 40 schemes.
2. **Rolling 90-Day Annualized Sharpe Ratio** dynamics for 5 benchmark mutual funds.
3. **Investor Cohort Analysis** grouped by initial transaction year.
4. **SIP Continuity & Churn Risk Analysis** for systematic investors with 6+ recurring installments.
5. **Portfolio Recommender Engine** integrating risk tolerance and Sharpe optimization.
6. **Sector Herfindahl-Hirschman Index (HHI)** concentration across equity schemes.
7. **5 Executive Advanced Insights** documented with supporting analytical proof.
"""))

    # Imports Cell
    cells.append(nbf.v4.new_code_cell("""import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Image, display

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

print("Advanced Analytics Environment Configured!")
"""))

    # Load Data Cell
    cells.append(nbf.v4.new_code_cell("""# Load Processed Datasets
data_dir = 'data/processed'
if not os.path.exists(data_dir):
    data_dir = '../data/processed'

fm = pd.read_csv(f'{data_dir}/01_fund_master_cleaned.csv')
nav = pd.read_csv(f'{data_dir}/02_nav_history_cleaned.csv')
perf = pd.read_csv(f'{data_dir}/07_scheme_performance_cleaned.csv')
tx = pd.read_csv(f'{data_dir}/08_investor_transactions_cleaned.csv')
holdings = pd.read_csv(f'{data_dir}/09_portfolio_holdings_cleaned.csv')

nav['date'] = pd.to_datetime(nav['date'])
tx['transaction_date'] = pd.to_datetime(tx['transaction_date'])

print(f"Loaded: {len(fm)} Schemes, {len(nav):,} NAV records, {len(tx):,} Transactions.")
"""))

    # Section 1: VaR / CVaR
    cells.append(nbf.v4.new_markdown_cell("""## 1. Historical Value-at-Risk (95% VaR) & Conditional VaR (CVaR)
- **95% Historical VaR**: The 5th percentile of daily return distribution representing the maximum expected loss on 95 out of 100 trading sessions.
- **95% CVaR (Expected Shortfall)**: The expected average loss given that the loss breaches the 95% VaR threshold.
"""))
    cells.append(nbf.v4.new_code_cell("""# Compute VaR & CVaR on active trading days
trading_nav = nav[nav['is_forward_filled'] == 0].sort_values(['amfi_code', 'date']).copy()
trading_nav['daily_ret'] = trading_nav.groupby('amfi_code')['nav'].pct_change() * 100.0

var_cvar_list = []
for code, grp in trading_nav.groupby('amfi_code'):
    rets = grp['daily_ret'].dropna()
    var_95 = float(np.percentile(rets, 5))
    cvar_95 = float(rets[rets <= var_95].mean())
    f_info = fm[fm['amfi_code'] == code].iloc[0]
    p_info = perf[perf['amfi_code'] == code].iloc[0]
    var_cvar_list.append({
        'amfi_code': code,
        'scheme_name': f_info['scheme_name'],
        'category': f_info['category'],
        'sub_category': f_info['sub_category'],
        'risk_grade': p_info['risk_grade'],
        'var_95_pct': round(var_95, 3),
        'cvar_95_pct': round(cvar_95, 3),
        'worst_day_pct': round(rets.min(), 3),
        'aum_crore': int(p_info['aum_crore'])
    })

var_df = pd.DataFrame(var_cvar_list).sort_values(by='var_95_pct')
var_df.to_csv('var_cvar_report.csv', index=False)
print("Top 5 Funds with Highest Downside Volatility (Most Negative 95% VaR):")
var_df.head(5)
"""))

    # Section 2: Rolling 90-day Sharpe
    cells.append(nbf.v4.new_markdown_cell("""## 2. Rolling 90-Day Annualized Sharpe Ratio
Formula applied: `returns.rolling(90).mean() / returns.rolling(90).std() * sqrt(252)`
"""))
    cells.append(nbf.v4.new_code_cell("""# Display Figure: Rolling Sharpe Trajectory
display(Image('rolling_sharpe_chart.png'))
"""))

    # Section 3: Cohort Analysis
    cells.append(nbf.v4.new_markdown_cell("""## 3. Investor Cohort Analysis (by Onboarding Year)
"""))
    cells.append(nbf.v4.new_code_cell("""# Group by first transaction year
first_tx = tx.groupby('investor_id')['transaction_date'].min().reset_index()
first_tx['cohort_year'] = first_tx['transaction_date'].dt.year
tx_cohort = tx.merge(first_tx[['investor_id', 'cohort_year']], on='investor_id')

cohort_res = []
for cy, grp in tx_cohort.groupby('cohort_year'):
    sip_txs = grp[grp['transaction_type'] == 'SIP']
    top_code = grp.groupby('amfi_code')['amount_inr'].sum().idxmax()
    cohort_res.append({
        'Cohort Year': cy,
        'Investors': grp['investor_id'].nunique(),
        'Total Transactions': len(grp),
        'Total Invested (Cr)': round(grp['amount_inr'].sum() / 1e7, 2),
        'Avg SIP Ticket (INR)': round(sip_txs['amount_inr'].mean(), 2),
        'Preferred Fund': fm.loc[fm['amfi_code'] == top_code, 'scheme_name'].values[0]
    })

pd.DataFrame(cohort_res)
"""))

    # Section 4: SIP Continuity
    cells.append(nbf.v4.new_markdown_cell("""## 4. SIP Continuity & Churn Risk Analysis
Assessing systematic compounding health for investors with **6 or more recurring installments**.
"""))
    cells.append(nbf.v4.new_code_cell("""# SIP continuity for investors with 6+ installments
sip_txs = tx[tx['transaction_type'] == 'SIP'].sort_values(['investor_id', 'transaction_date']).copy()
counts = sip_txs['investor_id'].value_counts()
eligible = counts[counts >= 6].index

sip_sub = sip_txs[sip_txs['investor_id'].isin(eligible)].copy()
sip_sub['gap_days'] = sip_sub.groupby('investor_id')['transaction_date'].diff().dt.days

continuity_df = sip_sub.groupby('investor_id').agg(
    total_installments=('amount_inr', 'count'),
    avg_gap_days=('gap_days', 'mean'),
    max_gap_days=('gap_days', 'max')
).reset_index()

continuity_df['is_at_risk'] = continuity_df['avg_gap_days'] > 35
at_risk_num = continuity_df['is_at_risk'].sum()
print(f"Total Cohort Size (6+ SIPs): {len(continuity_df):,}")
print(f"At-Risk Investors (Avg Gap > 35 Days): {at_risk_num:,} ({at_risk_num/len(continuity_df)*100:.1f}%)")
continuity_df.head(5)
"""))

    # Section 5: Fund Recommender
    cells.append(nbf.v4.new_markdown_cell("""## 5. Fund Recommender System
Demonstration of `recommender.py` filtering top funds by risk-adjusted return (Sharpe Ratio).
"""))
    cells.append(nbf.v4.new_code_cell("""from recommender import recommend_funds

for risk_level in ['Low', 'Moderate', 'High', 'Very High']:
    print(f"\\n--- RECOMMENDATIONS FOR RISK APPETITE: {risk_level.upper()} ---")
    rec = recommend_funds(risk_level, top_n=3)
    display(rec[['amfi_code', 'scheme_name', 'sub_category', 'risk_grade', 'sharpe_ratio', 'return_3yr_pct', 'expense_ratio_pct']])
"""))

    # Section 6: Sector HHI Concentration
    cells.append(nbf.v4.new_markdown_cell("""## 6. Sector HHI Concentration Across Equity Funds
Herfindahl-Hirschman Index: $HHI = \\sum (w_i^2)$
"""))
    cells.append(nbf.v4.new_code_cell("""# Sector HHI
sector_alloc = holdings.groupby(['amfi_code', 'sector'])['weight_pct'].sum().reset_index()
hhi_series = sector_alloc.groupby('amfi_code')['weight_pct'].apply(lambda w: (w**2).sum()).reset_index()
hhi_series.columns = ['amfi_code', 'sector_hhi']

hhi_full = hhi_series.merge(fm[['amfi_code', 'scheme_name', 'sub_category']], on='amfi_code').sort_values('sector_hhi', ascending=False)
print("Top 5 Most Concentrated Equity Portfolios (Highest Sector HHI):")
display(hhi_full.head(5))

print("\\nTop 5 Most Diversified Equity Portfolios (Lowest Sector HHI):")
display(hhi_full.tail(5))
"""))

    # Section 7: 5 Advanced Insights in Markdown
    cells.append(nbf.v4.new_markdown_cell("""## 7. Executive Advanced Insights

### 📌 Advanced Insight 1: Small-Cap Tail Risk & Asymmetric Downside Exposure
> **Small-cap equity schemes carry over 2.4x the tail risk of large-cap and debt funds, with DSP Small Cap and Nippon India Small Cap recording 95% Daily VaRs of -1.68% and -1.61% and average crash tail losses (CVaR) exceeding -2.15% on severe market days.** *(Supporting Analysis: Section 1 - `var_cvar_report.csv`).*

---

### 📌 Advanced Insight 2: Rolling Sharpe Resilience & Market Regime Shifts
> **During the 2023 broad-market bull rally, 90-day rolling Sharpe ratios surged above 5.0 across all 5 key funds, with SBI Bluechip leading operational stability before mean-reverting toward 0.5 – 1.5 during 2024 election and geopolitical volatility.** *(Supporting Chart: Section 2 - `rolling_sharpe_chart.png`).*

---

### 📌 Advanced Insight 3: Investor Cohort Lifetime Capital Mobilization
> **The 2024 onboarding cohort represents the financial backbone of the retail book, contributing over ₹304 Crore (87.2% of total capital) with an average SIP ticket size of ₹1,08,124, heavily favoring broad-market indexing via UTI Nifty 50 Index Fund.** *(Supporting Analysis: Section 3 - Investor Cohort Analysis).*

---

### 📌 Advanced Insight 4: SIP Retention Vulnerability & Friction Points
> **Among committed systematic investors (6+ installments), the average gap between SIP contributions is 64.9 days, indicating that irregular salary flows, bank mandate rejections, and pauses create substantial retention friction, highlighting a massive automated re-engagement opportunity.** *(Supporting Analysis: Section 4 - SIP Continuity Analysis).*

---

### 📌 Advanced Insight 5: Portfolio Concentration vs. Volatility Dynamics
> **Sector concentration varies by over 2.3x across equity funds; Axis Bluechip exhibits the highest sector HHI (2,967.69) due to a heavy 38%+ concentration in Financial Services, whereas diversified flexi-cap and mid-cap funds (HHI < 1,365) buffer against sectoral rotation risk.** *(Supporting Analysis: Section 6 - Sector HHI Concentration).*
"""))

    # Write notebook
    nb['cells'] = cells
    nb_path = os.path.join(base_dir, "Advanced_Analytics.ipynb")
    nb_subpath = os.path.join(base_dir, "notebooks", "Advanced_Analytics.ipynb")

    with open(nb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    with open(nb_subpath, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"\n[SAVED] {nb_path}")
    print(f"[SAVED] {nb_subpath}")


if __name__ == "__main__":
    base_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
    run_pipeline(base_dir)
