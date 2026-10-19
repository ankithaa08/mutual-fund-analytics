"""
Live NAV Ingestion Module (mfapi.in API)
========================================
Deliverable: Day 1 - Live Mutual Fund NAV Ingestion & API Integration

This script:
1. Connects to the public API `https://api.mfapi.in/mf/{scheme_code}`.
2. Fetches real-time / historical NAV for HDFC Top 100 Direct (AMFI: 125497).
3. Fetches live NAV for 5 key schemes:
   - SBI Bluechip (119551)
   - ICICI Bluechip (120503)
   - Nippon Large Cap (118632)
   - Axis Bluechip (119092)
   - Kotak Bluechip (120841)
4. Parses JSON responses into structured Pandas DataFrames with metadata.
5. Saves both individual CSVs and a consolidated raw CSV in `data/raw/`.
"""

import os
import sys
import time
import json
from datetime import datetime
import requests
import pandas as pd

BASE_API_URL = "https://api.mfapi.in/mf"

TARGET_SCHEMES = {
    125497: "HDFC Top 100 Direct",
    119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip",
}


def get_output_directory():
    """Returns path to data/raw directory."""
    out_dir = os.path.join(os.path.dirname(__file__), "data", "raw")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def fetch_scheme_nav(amfi_code, alias_name=""):
    """
    Fetches NAV data and scheme metadata from mfapi.in for a given AMFI code.
    
    Returns:
        tuple (meta_dict, nav_df)
    """
    url = f"{BASE_API_URL}/{amfi_code}"
    print(f"\n[API GET] Fetching NAV for AMFI {amfi_code} ({alias_name})...")
    print(f"Request URL: {url}")

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        payload = response.json()

        status = payload.get("status")
        if status == "FAIL":
            print(f" [ERROR] API returned FAIL for code {amfi_code}")
            return None, None

        meta = payload.get("meta", {})
        data_records = payload.get("data", [])

        if not data_records:
            print(f" [WARNING] No NAV data records found for AMFI code {amfi_code}")
            return meta, pd.DataFrame()

        # Parse data array
        df = pd.DataFrame(data_records)
        df["amfi_code"] = amfi_code
        df["alias_name"] = alias_name
        df["scheme_name"] = meta.get("scheme_name", alias_name)
        df["fund_house"] = meta.get("fund_house", "")
        df["scheme_category"] = meta.get("scheme_category", "")
        df["scheme_type"] = meta.get("scheme_type", "")
        df["isin_growth"] = meta.get("isin_growth", "")
        df["fetch_timestamp"] = datetime.now().isoformat()

        # Clean NAV numeric column
        df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

        # Reorder columns
        cols = [
            "amfi_code",
            "alias_name",
            "date",
            "nav",
            "scheme_name",
            "fund_house",
            "scheme_category",
            "scheme_type",
            "isin_growth",
            "fetch_timestamp",
        ]
        df = df[[c for c in cols if c in df.columns]]

        latest_nav = df.iloc[0]["nav"] if not df.empty else "N/A"
        latest_date = df.iloc[0]["date"] if not df.empty else "N/A"
        print(f" [SUCCESS] Fetched {len(df):,} NAV records.")
        print(f"           Scheme Name: {meta.get('scheme_name')}")
        print(f"           Latest NAV:  INR {latest_nav} (Date: {latest_date})")

        return meta, df

    except requests.exceptions.RequestException as e:
        print(f" [HTTP ERROR] Failed to fetch data for AMFI {amfi_code}: {e}")
        return None, None
    except Exception as e:
        print(f" [PARSE ERROR] Error parsing response for AMFI {amfi_code}: {e}")
        return None, None


def save_single_scheme_csv(df, amfi_code, alias_slug, output_dir):
    """Saves DataFrame of a single scheme to CSV."""
    filename = f"live_nav_{amfi_code}_{alias_slug}.csv"
    path = os.path.join(output_dir, filename)
    df.to_csv(path, index=False)
    print(f" [SAVED] {path} ({len(df):,} rows)")
    return path


def main():
    out_dir = get_output_directory()
    print("=" * 80)
    print("LIVE NAV FETCHER (mfapi.in)")
    print(f"Target Output Directory: {out_dir}")
    print("=" * 80)

    # 1. Fetch HDFC Top 100 Direct (125497)
    print("\n--- 1. FETCHING HDFC TOP 100 DIRECT (125497) ---")
    hdfc_meta, hdfc_df = fetch_scheme_nav(125497, "HDFC Top 100 Direct")
    if hdfc_df is not None and not hdfc_df.empty:
        save_single_scheme_csv(hdfc_df, 125497, "hdfc_top_100_direct", out_dir)
        # Also save generic raw name
        generic_path = os.path.join(out_dir, "live_nav_125497_raw.csv")
        hdfc_df.to_csv(generic_path, index=False)
        print(f" [SAVED] Raw CSV: {generic_path}")

    # 2. Fetch 5 Key Schemes
    print("\n--- 2. FETCHING 5 KEY SCHEMES ---")
    five_schemes = {
        119551: "sbi_bluechip",
        120503: "icici_bluechip",
        118632: "nippon_large_cap",
        119092: "axis_bluechip",
        120841: "kotak_bluechip",
    }

    all_dfs = []
    metadata_list = []

    for code, slug in five_schemes.items():
        alias_title = slug.replace("_", " ").title()
        meta, df = fetch_scheme_nav(code, alias_title)
        if df is not None and not df.empty:
            save_single_scheme_csv(df, code, slug, out_dir)
            all_dfs.append(df)
            if meta:
                metadata_list.append(meta)
        time.sleep(0.5)  # Friendly throttling for open API

    # 3. Save Consolidated CSV for all 5 schemes
    if all_dfs:
        consolidated_df = pd.concat(all_dfs, ignore_index=True)
        consolidated_path = os.path.join(out_dir, "live_nav_5_key_schemes.csv")
        consolidated_df.to_csv(consolidated_path, index=False)
        print("\n" + "=" * 80)
        print(f"[CONSOLIDATED FILE SAVED]: {consolidated_path}")
        print(f"Total Combined Records: {len(consolidated_df):,} rows")
        print(f"Schemes Included: {consolidated_df['alias_name'].unique().tolist()}")
        print("=" * 80)

        # Also save metadata json
        meta_path = os.path.join(out_dir, "live_schemes_metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata_list, f, indent=2)
        print(f"[METADATA SAVED]: {meta_path}")


if __name__ == "__main__":
    main()
