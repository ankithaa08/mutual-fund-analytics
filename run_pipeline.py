"""
Bluestock Mutual Fund Analytics Platform - Master Pipeline Orchestrator
========================================================================

Author: Quantitative Analytics & Engineering Division (Bluestock FinTech)
Milestone: Capstone Final Automated Pipeline (v1.0)
Coverage: End-to-end Data Engineering, Quantitative Modeling, BI Reporting,
          and Professional Presentation & PDF Publication.

Execution Workflow:
-------------------
Stage 1: [Data Engineering] Star Schema ETL & Database Load (`clean_and_load_db.py`)
Stage 2: [Exploratory Data Analysis] Statistical Distributions & EDA Charts (`generate_eda_charts_and_notebook.py`)
Stage 3: [Advanced Quantitative Modeling] Rolling Sharpe, VaR/CVaR, Portfolio Optimization (`generate_advanced_analytics.py`)
Stage 4: [Performance & Scorecard] 0-100 Composite Scorecard & CAPM OLS Attribution (`build_full_analytics.py`)
Stage 5: [Executive PDF Publication] Enterprise 18-Page Capstone PDF (`generate_final_report_pdf.py`)
Stage 6: [Executive Presentation] 12-Slide Widescreen Presentation (`generate_presentation_pptx.py`)

Usage:
------
    python run_pipeline.py [optional_base_directory]
"""

import os
import sys
import time
import shutil
import subprocess

BASE_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
os.environ["MPLCONFIGDIR"] = os.path.join(BASE_DIR, ".mpl")
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

SCRIPTS = [
    ("Stage 1/6: Star Schema ETL & Database Ingestion", "clean_and_load_db.py"),
    ("Stage 2/6: Exploratory Data Analysis & Visualizations", "generate_eda_charts_and_notebook.py"),
    ("Stage 3/6: Advanced Risk Modeling (VaR, CVaR, Rolling Sharpe)", "generate_advanced_analytics.py"),
    ("Stage 4/6: Quantitative Performance Analytics & Scorecard", "build_full_analytics.py"),
    ("Stage 5/6: 18-Page Final Capstone PDF Report", "generate_final_report_pdf.py"),
    ("Stage 6/6: 12-Slide Executive Presentation", "generate_presentation_pptx.py"),
]

def log(msg, symbol="INFO"):
    """Format and print structured log message."""
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [{symbol}] {msg}")

def run_script(script_name, stage_desc):
    """
    Execute an individual pipeline script and verify exit code.
    
    Args:
        script_name (str): Script filename in base directory.
        stage_desc (str): Human-readable description of pipeline stage.
    
    Returns:
        bool: True if execution succeeded, False otherwise.
    """
    script_path = os.path.join(BASE_DIR, script_name)
    if not os.path.exists(script_path):
        log(f"Script file not found: {script_path}", symbol="ERROR")
        return False
    
    log(f"Starting {stage_desc}...", symbol="STAGE")
    t0 = time.time()
    
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    res = subprocess.run([sys.executable, script_path, BASE_DIR], env=env, capture_output=True, text=True, encoding="utf-8")
    elapsed = time.time() - t0
    
    if res.returncode != 0:
        log(f"Failed {stage_desc} (Code {res.returncode}) in {elapsed:.2f}s", symbol="FAIL")
        if res.stderr:
            print(res.stderr.strip()[:600])
        return False
    else:
        log(f"Completed {stage_desc} in {elapsed:.2f}s", symbol="SUCCESS")
        return True

def verify_deliverables():
    """Verify that all milestone deliverables exist and have non-zero size."""
    expected = [
        ("bluestock_mf.db", "SQLite 3 Star Schema Database", 1_000_000),
        ("fund_scorecard.csv", "Fund Scorecard (40 Schemes)", 5_000),
        ("alpha_beta.csv", "CAPM OLS Regression Parameters", 3_000),
        ("benchmark_comparison_chart.png", "Benchmark Comparison Visualization", 500_000),
        ("Performance_Analytics.ipynb", "Executed Performance Analytics Notebook", 10_000),
        ("Final_Report.pdf", "Comprehensive 18-Page PDF Report", 2_000_000),
        ("Bluestock_MF_Presentation.pptx", "12-Slide Executive Presentation", 1_000_000),
    ]
    
    log("Verifying output deliverable artifacts...", symbol="CHECK")
    all_ok = True
    for fname, desc, min_size in expected:
        fpath = os.path.join(BASE_DIR, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            if size >= min_size:
                log(f"  [OK] {fname:<32} ({desc}) - {size:,} bytes")
            else:
                log(f"  [WARN] {fname} exists but smaller than expected ({size:,} bytes)", symbol="WARN")
                all_ok = False
        else:
            log(f"  [MISSING] {fname} ({desc})", symbol="FAIL")
            all_ok = False
    return all_ok

def main():
    print("=" * 80)
    print("BLUESTOCK MUTUAL FUND CAPSTONE: MASTER PIPELINE ORCHESTRATOR")
    print(f"Working Directory: {BASE_DIR}")
    print("=" * 80)
    
    t_start = time.time()
    success_count = 0
    
    for stage_desc, script_name in SCRIPTS:
        if run_script(script_name, stage_desc):
            success_count += 1
        else:
            log("Pipeline halted due to error in stage.", symbol="ABORT")
            sys.exit(1)
            
    total_elapsed = time.time() - t_start
    print("\n" + "=" * 80)
    log(f"All {success_count}/{len(SCRIPTS)} pipeline stages completed in {total_elapsed:.2f}s!", symbol="COMPLETE")
    print("=" * 80)
    
    if verify_deliverables():
        log("All capstone deliverables successfully verified and publication-ready!", symbol="READY")
    else:
        log("Some deliverables did not meet verification criteria.", symbol="WARNING")

if __name__ == "__main__":
    main()
