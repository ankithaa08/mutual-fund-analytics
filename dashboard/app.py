"""
Mutual Fund Analytics Dashboard (Day 1 Starter)
Run with: streamlit run dashboard/app.py
"""

import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mutual Fund Analytics Hub", layout="wide")

st.title("📈 Mutual Fund Analytics Platform - Day 1 Ingestion Hub")
st.markdown("Explore Fund Master, NAV trends, and live data ingested from `mfapi.in`.")

DATA_RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

# Load Fund Master
fm_path = os.path.join(DATA_RAW_DIR, "01_fund_master.csv")
if os.path.exists(fm_path):
    fm_df = pd.read_csv(fm_path)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Schemes", len(fm_df))
    col2.metric("Fund Houses (AMCs)", fm_df["fund_house"].nunique())
    col3.metric("Broad Categories", fm_df["category"].nunique())
    col4.metric("Sub-Categories", fm_df["sub_category"].nunique())

    tab1, tab2, tab3 = st.tabs(["🏛️ Fund Master", "📊 Category Breakdown", "⚡ Live NAV Data"])

    with tab1:
        st.subheader("Fund Master Schemes")
        selected_amc = st.multiselect("Filter by Fund House:", fm_df["fund_house"].unique())
        filtered_df = fm_df if not selected_amc else fm_df[fm_df["fund_house"].isin(selected_amc)]
        st.dataframe(filtered_df, use_container_width=True)

    with tab2:
        st.subheader("Category & Risk Distribution")
        fig = px.sunburst(fm_df, path=["category", "sub_category", "risk_category"], title="Mutual Fund Taxonomy")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        live_path = os.path.join(DATA_RAW_DIR, "live_nav_5_key_schemes.csv")
        if os.path.exists(live_path):
            live_df = pd.read_csv(live_path)
            st.subheader("Live Ingested NAV Data from mfapi.in")
            st.dataframe(live_df.head(100), use_container_width=True)
        else:
            st.info("Run `python live_nav_fetch.py` to populate live NAV data.")
else:
    st.error("Fund master file not found. Please verify data ingestion.")
