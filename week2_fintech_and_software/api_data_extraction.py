"""
REST API Ingestion & JSON Transformation Assignment
===================================================
Project: Week 2 FinTech & Software Ecosystem
Task: Call a public REST API, inspect the JSON response, parse nested structures,
      and export structured analytical datasets to CSV.

API Utilized:
1. Public Foreign Exchange Rates API (Frankfurter / European Central Bank)
   Endpoint: GET https://api.frankfurter.app/latest?from=USD
2. Indian FinTech Mutual Fund NAV API
   Endpoint: GET https://api.mfapi.in/mf/120503 (ICICI Prudential Bluechip)
"""

import os
import sys
import json
from datetime import datetime
import requests
import pandas as pd


def fetch_and_process_fx_api(output_dir):
    """
    Demonstrates HTTP GET request with query parameters,
    raw JSON inspection, parsing, and CSV transformation.
    """
    print("=" * 80)
    print("1. CALLING FOREIGN EXCHANGE RATES REST API")
    print("=" * 80)

    url = "https://api.frankfurter.app/latest"
    params = {"from": "USD"}
    headers = {"User-Agent": "Bluestock-FinTech-Data-Analyst/1.0"}

    print(f"Request Method: GET")
    print(f"Target URL:     {url}")
    print(f"Parameters:     {params}")

    response = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"HTTP Status:    {response.status_code} {response.reason}")
    response.raise_for_status()

    # Save raw JSON response
    json_data = response.json()
    raw_json_path = os.path.join(output_dir, "api_raw_fx_response.json")
    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    print(f"[SAVED] Raw JSON payload written to: {raw_json_path}")

    # Inspect JSON structure
    base_currency = json_data.get("base", "USD")
    rate_date = json_data.get("date", "")
    rates_dict = json_data.get("rates", {})

    print(f"Base Currency:  {base_currency}")
    print(f"Effective Date: {rate_date}")
    print(f"Total Currencies Tracked: {len(rates_dict)}")

    # Flatten nested JSON into tabular DataFrame
    records = []
    for currency, rate in rates_dict.items():
        records.append({
            "base_currency": base_currency,
            "target_currency": currency,
            "exchange_rate": float(rate),
            "inverse_rate_usd": round(1.0 / float(rate), 6) if float(rate) > 0 else 0.0,
            "effective_date": rate_date,
            "extracted_at_utc": datetime.utcnow().isoformat()
        })

    df_fx = pd.DataFrame(records)
    df_fx = df_fx.sort_values(by="exchange_rate", ascending=False)

    csv_path = os.path.join(output_dir, "api_extracted_fx_data.csv")
    df_fx.to_csv(csv_path, index=False)
    print(f"[SAVED] Transformed CSV written to:  {csv_path} ({len(df_fx)} rows)")
    print("\nSample Extracted Exchange Rates (Top 5):")
    print(df_fx.head(5).to_string(index=False))

    return df_fx


def fetch_and_process_mf_api(output_dir):
    """
    Demonstrates calling Indian Mutual Fund JSON API,
    extracting metadata, and unrolling historical timeseries into CSV.
    """
    print("\n" + "=" * 80)
    print("2. CALLING INDIAN FINTECH MUTUAL FUND REST API")
    print("=" * 80)

    scheme_code = 120503  # ICICI Pru Bluechip Direct
    url = f"https://api.mfapi.in/mf/{scheme_code}"

    print(f"Request Method: GET")
    print(f"Target URL:     {url}")

    response = requests.get(url, timeout=15)
    print(f"HTTP Status:    {response.status_code} {response.reason}")
    response.raise_for_status()

    payload = response.json()
    raw_mf_path = os.path.join(output_dir, "api_raw_mf_response.json")
    with open(raw_mf_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"[SAVED] Raw JSON payload written to: {raw_mf_path}")

    meta = payload.get("meta", {})
    data_points = payload.get("data", [])

    print(f"Scheme Name:    {meta.get('scheme_name')}")
    print(f"Fund House:     {meta.get('fund_house')}")
    print(f"Scheme Category:{meta.get('scheme_category')}")
    print(f"Historical Days:{len(data_points):,} trading points")

    df_mf = pd.DataFrame(data_points)
    df_mf["amfi_code"] = scheme_code
    df_mf["scheme_name"] = meta.get("scheme_name")
    df_mf["nav"] = pd.to_numeric(df_mf["nav"], errors="coerce")
    df_mf["date"] = pd.to_datetime(df_mf["date"], format="%d-%m-%Y").dt.strftime("%Y-%m-%d")
    df_mf = df_mf.sort_values(by="date", ascending=False)

    csv_mf_path = os.path.join(output_dir, "api_extracted_mf_data.csv")
    df_mf.to_csv(csv_mf_path, index=False)
    print(f"[SAVED] Transformed CSV written to:  {csv_mf_path} ({len(df_mf):,} rows)")
    print("\nSample Historical NAV Entries (Top 5):")
    print(df_mf.head(5).to_string(index=False))

    return df_mf


def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    fetch_and_process_fx_api(target_dir)
    fetch_and_process_mf_api(target_dir)
    print("\n" + "=" * 80)
    print("API DATA EXTRACTION ASSIGNMENT COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()
