"""
Mutual Fund Portfolio Recommender Module
========================================
Project: Bluestock Mutual Fund Analytics
Task: Simple fund recommender based on investor risk appetite and Sharpe ratio ranking.

Usage:
    python recommender.py --risk Moderate
    python recommender.py --risk High
    python recommender.py --risk Low
    python recommender.py  (Interactive mode)
"""

import os
import sys
import argparse
import pandas as pd


def load_performance_data():
    """Load cleaned fund master and performance datasets."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "data", "processed"),
        os.path.join(os.getcwd(), "data", "processed"),
        r"D:\Admin\Documents\mutual_fund_analysis\data\processed",
        r"C:\Users\Admin\.gemini\antigravity\scratch\mutual_fund_analysis\data\processed"
    ]
    for c in candidates:
        perf_p = os.path.join(c, "07_scheme_performance_cleaned.csv")
        fm_p = os.path.join(c, "01_fund_master_cleaned.csv")
        if os.path.exists(perf_p) and os.path.exists(fm_p):
            perf = pd.read_csv(perf_p)
            fm = pd.read_csv(fm_p)
            return fm.merge(perf[['amfi_code', 'sharpe_ratio', 'sortino_ratio', 'return_3yr_pct',
                                  'morningstar_rating', 'risk_grade']], on='amfi_code', suffixes=('', '_perf'))
    raise FileNotFoundError("Could not locate processed performance datasets.")


def recommend_funds(risk_appetite, top_n=3):
    """
    Recommends the top N funds by Sharpe ratio matching the user's risk appetite.
    
    Parameters:
        risk_appetite (str): 'Low', 'Moderate', 'Moderately High', 'High', 'Very High'
        top_n (int): Number of recommendations to return (default: 3)
    
    Returns:
        pd.DataFrame: Recommendation table
    """
    df = load_performance_data()

    # Normalize risk string
    risk_clean = risk_appetite.strip().lower()
    
    # Map common synonyms
    risk_mapping = {
        'low': ['Low'],
        'conservative': ['Low'],
        'moderate': ['Moderate'],
        'balanced': ['Moderate'],
        'moderately high': ['Moderately High'],
        'high': ['High', 'Very High'],
        'aggressive': ['High', 'Very High'],
        'very high': ['Very High']
    }

    target_grades = risk_mapping.get(risk_clean, [risk_appetite.title()])
    filtered_df = df[df['risk_grade'].isin(target_grades)].copy()

    if filtered_df.empty:
        # Fallback to case-insensitive partial match
        filtered_df = df[df['risk_grade'].str.lower().str.contains(risk_clean)].copy()

    if filtered_df.empty:
        valid_options = ", ".join(df['risk_grade'].unique())
        raise ValueError(f"No funds found for risk appetite '{risk_appetite}'. Valid options: {valid_options}")

    # Rank by Sharpe Ratio descending
    ranked_df = filtered_df.sort_values(by='sharpe_ratio', ascending=False).head(top_n)

    result_cols = [
        'amfi_code',
        'scheme_name',
        'fund_house',
        'category',
        'sub_category',
        'plan',
        'risk_grade',
        'sharpe_ratio',
        'return_3yr_pct',
        'expense_ratio_pct',
        'morningstar_rating'
    ]
    
    return ranked_df[[c for c in result_cols if c in ranked_df.columns]].reset_index(drop=True)


def print_recommendations(risk_appetite, rec_df):
    """Prints a clean, formatted ASCII recommendation table."""
    print("=" * 95)
    print(f"BLUESTOCK MUTUAL FUND RECOMMENDATION ENGINE")
    print(f"Target Risk Appetite: {risk_appetite.upper()} (Top {len(rec_df)} Funds by Sharpe Ratio)")
    print("=" * 95)
    
    for idx, row in rec_df.iterrows():
        stars = "*" * int(row['morningstar_rating'])
        print(f"\n[Rank #{idx + 1}] {row['scheme_name']}")
        print(f"  - AMFI Code:         {row['amfi_code']}")
        print(f"  - Fund House:        {row['fund_house']}")
        print(f"  - Category:          {row['category']} - {row['sub_category']} ({row['plan']})")
        print(f"  - Risk Grade:        {row['risk_grade']}")
        print(f"  - Sharpe Ratio:      {row['sharpe_ratio']:.2f} (Excess return per unit of total risk)")
        print(f"  - 3-Year CAGR:       {row['return_3yr_pct']:.2f}%")
        print(f"  - Expense Ratio:     {row['expense_ratio_pct']:.2f}% (TER)")
        print(f"  - Morningstar Rating:[{stars:<5}] ({row['morningstar_rating']}/5)")
    print("\n" + "=" * 95)


def main():
    parser = argparse.ArgumentParser(description="Bluestock Fund Recommender Engine")
    parser.add_argument("--risk", type=str, default=None,
                        help="Risk appetite: Low, Moderate, High, Very High, Conservative, Aggressive")
    parser.add_argument("--top", type=int, default=3, help="Number of funds to recommend")

    args = parser.parse_args()

    risk_input = args.risk
    if not risk_input:
        print("Available Risk Appetites:")
        print("  1. Low (Capital preservation, Debt / Liquid funds)")
        print("  2. Moderate (Balanced growth, Large Cap funds)")
        print("  3. High (High growth, Mid & Flexi Cap funds)")
        print("  4. Very High (Maximum capital appreciation, Small Cap funds)")
        user_choice = input("\nEnter your risk appetite (Low / Moderate / High / Very High) [Default: Moderate]: ").strip()
        risk_input = user_choice if user_choice else "Moderate"

    try:
        rec_df = recommend_funds(risk_input, top_n=args.top)
        print_recommendations(risk_input, rec_df)
    except Exception as e:
        print(f"Error generating recommendation: {e}")


if __name__ == "__main__":
    main()
