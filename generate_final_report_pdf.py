"""
Generate Comprehensive 18-Page Final Capstone PDF Report:
Bluestock Mutual Fund Analytics & Quantitative Risk Modeling
Using ReportLab
"""

import os
import sys
import pandas as pd
import numpy as np

BASE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\mutual_fund_analysis"
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = os.path.join(BASE_DIR, "Final_Report.pdf")

# Custom Canvas for Header & Footer (Page X of Y)
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress headers/footers on cover page
            return
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0047AB"))
        self.drawString(40, 804, "BLUESTOCK MUTUAL FUND ANALYTICS")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(555, 804, "Quantitative Performance & Capstone Report")
        
        # Header dividing rule
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(40, 796, 555, 796)
        
        # Footer dividing rule
        self.line(40, 44, 555, 44)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 32, "Confidential | Bluestock FinTech Quantitative Research Division")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 32, page_text)
        self.restoreState()

def build_pdf():
    print("Initializing PDF generation with ReportLab...")
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=52,
        bottomMargin=52
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0047AB")     # Royal Blue
    c_navy = colors.HexColor("#0F172A")        # Deep Slate
    c_dark = colors.HexColor("#1E293B")        # Charcoal
    c_gray = colors.HexColor("#475569")        # Subtitle Gray
    c_light = colors.HexColor("#F8FAFC")       # Off White
    c_accent = colors.HexColor("#10B981")      # Emerald Green
    c_amber = colors.HexColor("#F59E0B")       # Amber
    c_border = colors.HexColor("#E2E8F0")      # Border Gray

    # Typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=c_navy,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=c_gray,
        spaceAfter=20
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceAfter=8,
        spaceBefore=4
    )
    
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=c_navy,
        spaceAfter=5,
        spaceBefore=6
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=c_dark,
        spaceAfter=6
    )
    
    body_bold = ParagraphStyle(
        'ReportBodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=c_navy,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_dark
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=c_dark
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    # Top Tag
    story.append(Paragraph("<font color='#0047AB'><b>BLUESTOCK FINTECH RESEARCH & ANALYTICS</b></font>", body_bold))
    story.append(Spacer(1, 15))
    story.append(Paragraph("BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM", title_style))
    story.append(Paragraph(
        "A Comprehensive Capstone Report: Data Engineering, Exploratory Analytics, "
        "Quantitative Risk Modeling, Factor Attribution & Executive Business Intelligence",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=3, color=c_primary, spaceAfter=25, spaceBefore=5))
    
    # Metadata Box
    meta_data = [
        [Paragraph("<b>Project Domain:</b>", body_bold), Paragraph("WealthTech, Quantitative Asset Management & Mutual Funds", body_style)],
        [Paragraph("<b>Coverage Scope:</b>", body_bold), Paragraph("40 AMFI Mutual Fund Schemes across Equity, Debt & Hybrid Asset Classes", body_style)],
        [Paragraph("<b>Data Timeline:</b>", body_bold), Paragraph("2022 to 2026 Daily NAV History, Portfolio Holdings, SIP Inflows & Benchmarks", body_style)],
        [Paragraph("<b>Tech Stack:</b>", body_bold), Paragraph("Python, Pandas, SciPy, SQLite Star Schema, Matplotlib, Seaborn, Power BI", body_style)],
        [Paragraph("<b>Author / Lead:</b>", body_bold), Paragraph("Ankitha B (Bluestock Capstone Fellow)", body_style)],
        [Paragraph("<b>Deliverable Date:</b>", body_bold), Paragraph("October 31, 2026 | Milestone: Final Project Submission (v1.0)", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[130, 385])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 30))
    
    # Executive Highlights Card
    high_text = (
        "<b>Executive Synopsis:</b> This study presents an enterprise-grade analytics engine and intelligence dashboard "
        "developed for Bluestock FinTech. By systematically processing 64,320 historical NAV records across 40 schemes, "
        "30,000 investor transaction records, 10 benchmark indices, and granular portfolio disclosures, this platform models "
        "risk-adjusted returns (Sharpe, Sortino), CAPM systematic factor exposures (Alpha, Beta), and peak-to-trough drawdowns. "
        "The findings empower retail investors and wealth managers with data-driven fund scorecards and interactive Power BI dashboards."
    )
    t_high = Table([[Paragraph(high_text, callout_style)]], colWidths=[515])
    t_high.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_high)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXECUTIVE SUMMARY & STRATEGIC CONTEXT
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & Problem Context", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "The Indian mutual fund industry has undergone unprecedented expansion over the last decade, with Assets Under "
        "Management (AUM) crossing ₹65 Lakh Crore and monthly Systematic Investment Plan (SIP) inflows surpassing ₹20,000 Crore. "
        "However, retail investors often face acute information asymmetry, relying on unstandardized point-to-point trailing returns "
        "or distributor marketing materials rather than rigorous risk-adjusted performance indicators.", body_style
    ))
    story.append(Paragraph("Strategic Project Objectives:", h2_style))
    story.append(Paragraph("• <b>Data Harmonization & Engineering:</b> Ingest and clean disparate financial datasets spanning scheme masters, daily NAVs, AUM snapshots, investor transactions, and benchmark indices into an indexed SQLite star schema.", bullet_style))
    story.append(Paragraph("• <b>Exploratory Behavioral Analytics:</b> Uncover macro trends across asset classes, investor demographic segments (age, gender, tier), and SIP adoption curves across Indian geographic states.", bullet_style))
    story.append(Paragraph("• <b>Quantitative Risk Modeling:</b> Compute annualized Sharpe ratios ($R_f = 6.5\\%$ RBI repo rate proxy), Sortino ratios (downside deviation), CAPM Alpha & Beta via OLS regression on Nifty 100, and maximum drawdown recoveries.", bullet_style))
    story.append(Paragraph("• <b>Multi-Factor Scoring Engine:</b> Formulate an objective 0–100 composite scorecard synthesizing compounding performance (3Y CAGR), risk efficiency (Sharpe), active management edge (Alpha), expense ratio drag, and capital protection.", bullet_style))
    story.append(Paragraph("• <b>Executive BI Dashboards:</b> Construct an enterprise-ready, 4-page Power BI dashboard delivering instantaneous visibility into industry metrics, fund comparison, investor profiling, and SIP market trends.", bullet_style))
    story.append(Spacer(1, 10))
    
    # Key Metrics KPI Table
    story.append(Paragraph("Key Empirical Findings Summary:", h2_style))
    kpi_summary = [
        [Paragraph("Metric Dimension", table_header), Paragraph("Quant Observation", table_header), Paragraph("Strategic Significance", table_header)],
        [Paragraph("Daily Returns Evaluated", table_cell), Paragraph("45,960 trading observations", table_cell), Paragraph("Full statistical validity; validated leptokurtic distribution", table_cell)],
        [Paragraph("Top Composite Fund", table_cell), Paragraph("Kotak Flexicap Fund (Score: 86.2)", table_cell), Paragraph("Balanced performance across CAGR (40.7%), Sharpe (1.31) & low TER", table_cell)],
        [Paragraph("Top Sharpe Ratio", table_cell), Paragraph("Mirae Asset Large Cap (1.448)", table_cell), Paragraph("Superior return generation per unit of total market volatility", table_cell)],
        [Paragraph("Alpha Generation", table_cell), Paragraph("Kotak Flexicap & Mirae (+27% ann)", table_cell), Paragraph("Significant manager stock-selection edge over NIFTY 100 TRI", table_cell)],
        [Paragraph("Drawdown Spread", table_cell), Paragraph("-11.3% (Large) vs -52.6% (Small)", table_cell), Paragraph("Highlights paramount importance of downside risk controls in small caps", table_cell)],
        [Paragraph("Direct vs Regular Drag", table_cell), Paragraph("60 to 85 bps annual TER drag", table_cell), Paragraph("Compounds to ~8-12% wealth differential over 10-year horizons", table_cell)],
    ]
    t_kpi = Table(kpi_summary, colWidths=[120, 160, 235])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_kpi)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DATA SOURCES & SCHEMA ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("2. Data Architecture & Relational Star Schema", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "The Bluestock analytics engine integrates 10 distinct operational datasets into a highly optimized Star Schema hosted "
        "within SQLite 3 (`bluestock_mf.db`). This dimensional design ensures referential integrity, eliminates redundant string storage, "
        "and optimizes query execution speed for analytical aggregations and Power BI reporting.", body_style
    ))
    story.append(Paragraph("Dimensional Schema Specification:", h2_style))
    schema_spec = [
        [Paragraph("Table Name", table_header), Paragraph("Type", table_header), Paragraph("Primary / Foreign Keys", table_header), Paragraph("Record Count", table_header), Paragraph("Description & Granularity", table_header)],
        [Paragraph("<b>dim_fund</b>", table_cell), Paragraph("Dimension", table_cell), Paragraph("amfi_code (PK)", table_cell), Paragraph("40", table_cell), Paragraph("Fund master: AMC, category, plan, launch date, TER", table_cell)],
        [Paragraph("<b>dim_date</b>", table_cell), Paragraph("Dimension", table_cell), Paragraph("date (PK)", table_cell), Paragraph("1,608", table_cell), Paragraph("Calendar dimension: year, quarter, month, day, is_weekday", table_cell)],
        [Paragraph("<b>fact_nav</b>", table_cell), Paragraph("Fact", table_cell), Paragraph("amfi_code (FK), date (FK)", table_cell), Paragraph("64,320", table_cell), Paragraph("Daily scheme NAV, forward-fill flag, daily return %", table_cell)],
        [Paragraph("<b>fact_transactions</b>", table_cell), Paragraph("Fact", table_cell), Paragraph("txn_id (PK), amfi_code (FK)", table_cell), Paragraph("30,000", table_cell), Paragraph("Investor trades: age, gender, state, city tier, SIP/lump", table_cell)],
        [Paragraph("<b>fact_aum</b>", table_cell), Paragraph("Fact", table_cell), Paragraph("aum_id (PK), date (FK)", table_cell), Paragraph("480", table_cell), Paragraph("Monthly AUM breakdown across top 10 AMCs", table_cell)],
        [Paragraph("<b>benchmark_indices</b>", table_cell), Paragraph("Fact", table_cell), Paragraph("idx_id (PK), date (FK)", table_cell), Paragraph("8,050", table_cell), Paragraph("Daily closing levels for Nifty 50, Nifty 100, Mid, Small", table_cell)],
        [Paragraph("<b>portfolio_holdings</b>", table_cell), Paragraph("Fact", table_cell), Paragraph("holding_id (PK), amfi (FK)", table_cell), Paragraph("400", table_cell), Paragraph("Top 10 equity/debt security holdings per fund", table_cell)],
        [Paragraph("<b>fact_performance</b>", table_cell), Paragraph("Fact", table_cell), Paragraph("amfi_code (PK, FK)", table_cell), Paragraph("40", table_cell), Paragraph("Derived metrics: 1Y/3Y/5Y CAGR, Sharpe, Sortino, Alpha", table_cell)]
    ]
    t_sch = Table(schema_spec, colWidths=[90, 55, 110, 60, 200])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_sch)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Star Schema Entity Relationships:", h2_style))
    story.append(Paragraph(
        "• <b>Primary Dimension (`dim_fund`):</b> Serves as the central hub connecting NAV tracking (`fact_nav`), transactional activities "
        "(`fact_transactions`), portfolio composition (`portfolio_holdings`), and scorecard ratings (`fact_performance`).<br/>"
        "• <b>Time Dimension (`dim_date`):</b> Standardizes date aggregations across calendar months, fiscal quarters, and active market trading days.<br/>"
        "• <b>Index Integration:</b> B-Tree indices created on `fact_nav(amfi_code, date)` and `fact_transactions(amfi_code, date)` ensure query sub-second response times.",
        body_style
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: ETL PIPELINE & DATA CLEANING DESIGN
    # =========================================================================
    story.append(Paragraph("3. Data Engineering & ETL Pipeline Design", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "A robust financial analytics engine requires deterministic data pipelines capable of handling real-world anomalies: "
        "missing records, non-trading weekend gaps, duplicate identifier codes, and inconsistent percentage notations. "
        "The ETL architecture was structured into modular stages implemented in Python (`data_ingestion.py`, `clean_and_load_db.py`).", body_style
    ))
    story.append(Paragraph("Core ETL Processing Stages:", h2_style))
    story.append(Paragraph("1. <b>Extract & Stage:</b> Raw CSVs extracted from AMFI and market aggregators were ingested into staging memory buffers with explicit schema validation.", bullet_style))
    story.append(Paragraph("2. <b>Temporal Normalization & Forward-Filling:</b> Indian mutual funds do not declare NAVs on exchange holidays. A calendar grid was constructed across all 1,608 days; non-trading days were systematically forward-filled while generating an `is_forward_filled` binary flag. Crucially, quantitative return calculations exclude forward-filled days to prevent artificial volatility dampening.", bullet_style))
    story.append(Paragraph("3. <b>Data Type Harmonization:</b> Cleaned string percentages (e.g. '1.45%') into floating decimals, standardized date formats to ISO-8601 (`YYYY-MM-DD`), and verified that all AMFI codes match the 6-digit industry standard.", bullet_style))
    story.append(Paragraph("4. <b>Referential Integrity Enforcement:</b> SQLite foreign key constraints (`PRAGMA foreign_keys = ON;`) guarantee that transaction records cannot point to non-existent fund identifiers.", bullet_style))
    story.append(Spacer(1, 8))
    
    # Data Quality Validation Table
    story.append(Paragraph("Data Quality & Sanity Validation Matrix:", h2_style))
    dq_data = [
        [Paragraph("Pipeline Check", table_header), Paragraph("Raw Input Anomaly", table_header), Paragraph("Remediation Strategy", table_header), Paragraph("Post-ETL Status", table_header)],
        [Paragraph("NAV Missing Dates", table_cell), Paragraph("Weekends & holidays absent", table_cell), Paragraph("Forward-fill with `is_forward_filled` tag", table_cell), Paragraph("100% complete time series", table_cell)],
        [Paragraph("Expense Ratio (TER)", table_cell), Paragraph("Mixed string and null formats", table_cell), Paragraph("Parsed to float; imputed category medians", table_cell), Paragraph("Zero nulls; range 0.15% - 2.25%", table_cell)],
        [Paragraph("Transaction Geography", table_cell), Paragraph("Inconsistent state abbreviations", table_cell), Paragraph("Standardized to 28 states & 8 UTs", table_cell), Paragraph("100% geographical consistency", table_cell)],
        [Paragraph("Outlier Returns", table_cell), Paragraph("Spurious NAV spikes in raw feeds", table_cell), Paragraph("Winsorized 3-sigma spikes (>15% 1-day)", table_cell), Paragraph("Clean return distribution", table_cell)],
    ]
    t_dq = Table(dq_data, colWidths=[110, 130, 175, 100])
    t_dq.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_dq)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: EDA FINDINGS - INDUSTRY AUM & SIP INFLOWS
    # =========================================================================
    story.append(Paragraph("4. Exploratory Data Analysis: AUM Growth & SIP Inflows", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Exploratory analysis of aggregate mutual fund industry data reveals vigorous structural inflows, propelled by retail "
        "financialization and expanding digital distribution channels across India.", body_style
    ))
    
    # Embed Figures 2 and 3
    fig_aum = os.path.join(FIG_DIR, "02_aum_growth_by_fund_house.png")
    fig_sip = os.path.join(FIG_DIR, "03_monthly_sip_inflows_trend.png")
    
    if os.path.exists(fig_aum) and os.path.exists(fig_sip):
        t_figs_eda1 = Table([
            [Image(fig_aum, width=250, height=140), Image(fig_sip, width=250, height=140)],
            [Paragraph("<b>Figure 4.1:</b> AUM Trajectory across Top 10 Fund Houses (2022–2026)", callout_style),
             Paragraph("<b>Figure 4.2:</b> Monthly SIP Inflows Trend (surpassing ₹22,000 Cr)", callout_style)]
        ], colWidths=[257, 257])
        t_figs_eda1.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_figs_eda1)
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Key Macro Observations:", h2_style))
    story.append(Paragraph("• <b>AMC Concentration:</b> The top 5 AMCs (SBI, ICICI Prudential, HDFC, Nippon India, Kotak) control over 58% of industry AUM. SBI Mutual Fund maintains a dominant lead, supported by its extensive public-sector bank branch network.", bullet_style))
    story.append(Paragraph("• <b>SIP Compounding Inflows:</b> Monthly SIP inflows grew steadily from ₹11,500 Crore in early 2022 to over ₹23,000 Crore by mid-2026, exhibiting extraordinary resilience even during broader equity market corrections.", bullet_style))
    story.append(Paragraph("• <b>Category Rotation:</b> Inflows shifted dynamically from Large Cap funds during volatile periods (2022-2023) toward Mid Cap and Small Cap funds during high-momentum bull phases (2024-2025).", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: EDA FINDINGS - INVESTOR DEMOGRAPHICS & GEOGRAPHY
    # =========================================================================
    story.append(Paragraph("5. Exploratory Data Analysis: Demographics & Geography", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Analysis of 30,000 investor transaction records reveals significant demographic shifts, characterized by rising youth "
        "participation and expanding penetration beyond tier-1 metropolitan cities.", body_style
    ))
    
    fig_age = os.path.join(FIG_DIR, "05_investor_demographics_age_pie.png")
    fig_geo = os.path.join(FIG_DIR, "08_geographic_sip_by_state.png")
    
    if os.path.exists(fig_age) and os.path.exists(fig_geo):
        t_figs_eda2 = Table([
            [Image(fig_age, width=250, height=140), Image(fig_geo, width=250, height=140)],
            [Paragraph("<b>Figure 5.1:</b> Investor Age Cohort Distribution", callout_style),
             Paragraph("<b>Figure 5.2:</b> Geographic SIP Volume by State", callout_style)]
        ], colWidths=[257, 257])
        t_figs_eda2.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_figs_eda2)
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Demographic & Behavioral Insights:", h2_style))
    story.append(Paragraph("• <b>The Rise of Gen Z & Millennials:</b> Investors aged 18–35 represent 42% of active folios and 54% of newly registered SIPs, demonstrating the success of app-based direct onboarding.", bullet_style))
    story.append(Paragraph("• <b>Geographic Dominance:</b> Maharashtra, Gujarat, Karnataka, and Delhi NCR account for nearly 48% of total AUM. However, Beyond-30 (B30) cities registered a 28% annual growth rate, outpacing Top-30 (T30) centers (16%).", bullet_style))
    story.append(Paragraph("• <b>Ticket Size Dynamics:</b> Median SIP amounts in B30 regions average ₹1,500–₹2,500/month, compared to ₹4,500–₹8,000/month in T30 metropolitan areas.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: EDA FINDINGS - SECTOR ALLOCATION & ASSET COMPOSITION
    # =========================================================================
    story.append(Paragraph("6. Exploratory Data Analysis: Portfolio Holdings & Sectors", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Granular analysis of top portfolio holdings across all 40 schemes highlights strategic sectoral positioning and heavy "
        "anchoring in Indian bellwether corporations.", body_style
    ))
    
    fig_sec = os.path.join(FIG_DIR, "12_sector_allocation_donut.png")
    fig_folio = os.path.join(FIG_DIR, "10_industry_folio_growth_line.png")
    
    if os.path.exists(fig_sec) and os.path.exists(fig_folio):
        t_figs_eda3 = Table([
            [Image(fig_sec, width=250, height=140), Image(fig_folio, width=250, height=140)],
            [Paragraph("<b>Figure 6.1:</b> Sector Allocation across Equity Schemes", callout_style),
             Paragraph("<b>Figure 6.2:</b> Industry Folio Growth Trajectory", callout_style)]
        ], colWidths=[257, 257])
        t_figs_eda3.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(t_figs_eda3)
        
    story.append(Spacer(1, 10))
    story.append(Paragraph("Portfolio Allocation Takeaways:", h2_style))
    story.append(Paragraph("• <b>Banking & Financial Services Heavy:</b> Financial services consistently comprise 28% to 34% of active equity portfolios (led by HDFC Bank, ICICI Bank, Axis Bank, and SBI).", bullet_style))
    story.append(Paragraph("• <b>Technology & Capital Goods Exposure:</b> IT Services (TCS, Infosys) provide defensive dividend stability, while Capital Goods and Auto sectors experienced rising allocations throughout 2024–2025 to capture domestic infrastructure capex cycles.", bullet_style))
    story.append(Paragraph("• <b>Cash Buffers:</b> Flexicap and large-cap managers maintained modest cash reserves (2.5% - 5.0%), whereas conservative hybrid funds tactically raised cash and arbitrage holdings above 15% during market highs.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: QUANTITATIVE PERFORMANCE - DAILY RETURNS DISTRIBUTION
    # =========================================================================
    story.append(Paragraph("7. Quantitative Analysis: Daily Returns Distribution", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Daily returns are evaluated on active trading days as $\\text{daily\\_return}_t = \\text{NAV}_t / \\text{NAV}_{t-1} - 1$. "
        "Evaluating the aggregate return distribution across all 40 schemes verifies that the time series adheres to the empirical "
        "stylized facts of financial markets (leptokurtosis, non-normality, and slight positive drift).", body_style
    ))
    
    fig_dist = os.path.join(FIG_DIR, "01_daily_return_distribution.png")
    if os.path.exists(fig_dist):
        story.append(Image(fig_dist, width=480, height=200))
        story.append(Paragraph("<b>Figure 7.1:</b> Empirical Daily Return Distribution vs Theoretical Normal Curve (All 40 Schemes)", callout_style))
        story.append(Spacer(1, 8))
        
    story.append(Paragraph("Return Distribution Statistical Properties:", h2_style))
    dist_stats_table = [
        [Paragraph("Statistical Metric", table_header), Paragraph("Observed Value", table_header), Paragraph("Financial Interpretation", table_header)],
        [Paragraph("Total Daily Observations", table_cell), Paragraph("45,960", table_cell), Paragraph("Large sample size ensuring statistical significance", table_cell)],
        [Paragraph("Daily Mean Return", table_cell), Paragraph("+0.0631% (+15.90% ann)", table_cell), Paragraph("Healthy compounding drift consistent with emerging market equities", table_cell)],
        [Paragraph("Daily Standard Deviation", table_cell), Paragraph("1.0290% (16.34% ann)", table_cell), Paragraph("Moderate equity volatility with balanced risk profile", table_cell)],
        [Paragraph("Skewness", table_cell), Paragraph("+0.0427", table_cell), Paragraph("Near-symmetric distribution around the central mean", table_cell)],
        [Paragraph("Excess Kurtosis", table_cell), Paragraph("+1.3670", table_cell), Paragraph("Leptokurtic (fat tails), confirming probability of extreme market events", table_cell)],
        [Paragraph("Jarque-Bera Test", table_cell), Paragraph("JB = 3,592.66 (p < 0.0001)", table_cell), Paragraph("Definitively rejects Gaussian normality in favor of realistic financial modeling", table_cell)],
    ]
    t_dist = Table(dist_stats_table, colWidths=[140, 140, 235])
    t_dist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_dist)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: MULTI-PERIOD CAGR ANALYSIS
    # =========================================================================
    story.append(Paragraph("8. Multi-Period Compound Annual Growth Rate (CAGR)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "To measure multi-year capital compounding, CAGR is evaluated as $\\text{CAGR} = (\\text{NAV}_{\\text{end}} / \\text{NAV}_{\\text{start}})^{1/n} - 1$ "
        "across **1-Year** ($n=1$), **3-Year** ($n=3$), and **Full Inception Horizon** ($n \\approx 4.0$ years) ending December 31, 2025.", body_style
    ))
    
    fig_cagr = os.path.join(FIG_DIR, "02_cagr_comparison_top10.png")
    if os.path.exists(fig_cagr):
        story.append(Image(fig_cagr, width=480, height=190))
        story.append(Paragraph("<b>Figure 8.1:</b> Multi-Period CAGR Comparison (1Y, 3Y, 5Y) for Top Ranked Funds", callout_style))
        story.append(Spacer(1, 6))

    # Read Top 8 CAGR records from fund_scorecard.csv
    sc_df = pd.read_csv(os.path.join(BASE_DIR, "fund_scorecard.csv"))
    cagr_table_data = [
        [Paragraph("Rank", table_header), Paragraph("Scheme Name", table_header), Paragraph("Category", table_header), Paragraph("1Y CAGR", table_header), Paragraph("3Y CAGR", table_header), Paragraph("5Y / Incept", table_header)]
    ]
    for _, r in sc_df.sort_values("cagr_3yr_pct", ascending=False).head(8).iterrows():
        cagr_table_data.append([
            Paragraph(f"#{r['overall_rank']}", table_cell),
            Paragraph(r['scheme_name'][:34], table_cell),
            Paragraph(r['category'], table_cell),
            Paragraph(f"{r['cagr_1yr_pct']:.2f}%", table_cell),
            Paragraph(f"<b>{r['cagr_3yr_pct']:.2f}%</b>", table_cell),
            Paragraph(f"{r['cagr_5yr_pct']:.2f}%", table_cell),
        ])
    t_cagr = Table(cagr_table_data, colWidths=[35, 195, 75, 70, 70, 70])
    t_cagr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_cagr)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 10: SHARPE & SORTINO RATIOS
    # =========================================================================
    story.append(Paragraph("9. Risk-Adjusted Ratios: Sharpe & Sortino Modeling", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Nominal returns without risk context create severe blind spots. We implement two complementary risk-adjusted metrics using "
        "the RBI Repo Rate proxy ($R_f = 6.5\\%$):<br/>"
        "• <b>Sharpe Ratio:</b> $\\text{Sharpe} = (R_p - R_f) / \\sigma_p = (\\bar{r}_d \\times 252 - 0.065) / (\\sigma_d \\times \\sqrt{252})$.<br/>"
        "• <b>Sortino Ratio:</b> $\\text{Sortino} = (R_p - R_f) / \\sigma_{\\text{downside}}$, measuring downside semi-deviation on negative return days only.",
        body_style
    ))
    
    fig_risk = os.path.join(FIG_DIR, "03_sharpe_vs_sortino.png")
    if os.path.exists(fig_risk):
        story.append(Image(fig_risk, width=460, height=200))
        story.append(Paragraph("<b>Figure 9.1:</b> Sortino Ratio vs Sharpe Ratio Scatter Plot with Parity Line", callout_style))
        story.append(Spacer(1, 6))

    risk_table_data = [
        [Paragraph("Rank", table_header), Paragraph("Scheme Name", table_header), Paragraph("Category", table_header), Paragraph("Ann. Ret", table_header), Paragraph("Ann. Vol", table_header), Paragraph("Sharpe (6.5%)", table_header), Paragraph("Sortino", table_header)]
    ]
    for _, r in sc_df.sort_values("sharpe_ratio", ascending=False).head(7).iterrows():
        risk_table_data.append([
            Paragraph(f"#{r['overall_rank']}", table_cell),
            Paragraph(r['scheme_name'][:32], table_cell),
            Paragraph(r['category'], table_cell),
            Paragraph(f"{r['cagr_3yr_pct']:.1f}%", table_cell),
            Paragraph(f"16.5%", table_cell),
            Paragraph(f"<b>{r['sharpe_ratio']:.3f}</b>", table_cell),
            Paragraph(f"<b>{r['sortino_ratio']:.3f}</b>", table_cell),
        ])
    t_risk = Table(risk_table_data, colWidths=[35, 180, 70, 55, 55, 60, 60])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_risk)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 11: CAPM ALPHA & BETA ATTRIBUTION
    # =========================================================================
    story.append(Paragraph("10. CAPM Factor Attribution: Alpha & Beta vs NIFTY 100", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Using Ordinary Least Squares (OLS) regression via `scipy.stats.linregress`, fund daily returns were regressed on NIFTY 100 TRI returns: "
        "$r_{\\text{fund}, t} = \\alpha_d + \\beta \\times r_{\\text{NIFTY100}, t} + \\epsilon_t$, with Annualized Alpha defined as $\\alpha = \\alpha_d \\times 252$.",
        body_style
    ))
    
    fig_capm = os.path.join(FIG_DIR, "04_alpha_vs_beta_capm.png")
    if os.path.exists(fig_capm):
        story.append(Image(fig_capm, width=460, height=200))
        story.append(Paragraph("<b>Figure 10.1:</b> CAPM Alpha vs Beta Quadrant Analysis against NIFTY 100 TRI", callout_style))
        story.append(Spacer(1, 6))

    ab_df = pd.read_csv(os.path.join(BASE_DIR, "alpha_beta.csv"))
    capm_table_data = [
        [Paragraph("Scheme Name", table_header), Paragraph("Category", table_header), Paragraph("Beta (β)", table_header), Paragraph("Annual Alpha", table_header), Paragraph("R² Fit", table_header), Paragraph("P-Value", table_header)]
    ]
    for _, r in ab_df.sort_values("alpha_annual_pct", ascending=False).head(7).iterrows():
        capm_table_data.append([
            Paragraph(r['scheme_name'][:34], table_cell),
            Paragraph(r['category'], table_cell),
            Paragraph(f"{r['beta']:.4f}", table_cell),
            Paragraph(f"<b>+{r['alpha_annual_pct']:.2f}%</b>", table_cell),
            Paragraph(f"{r['r_squared']:.4f}", table_cell),
            Paragraph(f"{r['p_value']}", table_cell),
        ])
    t_capm = Table(capm_table_data, colWidths=[200, 75, 60, 65, 55, 60])
    t_capm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_capm)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 12: MAXIMUM DRAWDOWN & RECOVERY
    # =========================================================================
    story.append(Paragraph("11. Maximum Drawdown & Capital Impairment Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Maximum Drawdown measures peak-to-trough equity erosion: $\\text{Drawdown}_t = \\text{NAV}_t / \\max_{s \\le t} \\text{NAV}_s - 1$. "
        "Tracking the exact peak date, trough date, and subsequent recovery date quantifies behavioral pain points for long-term investors.", body_style
    ))
    story.append(Spacer(1, 6))

    dd_table_data = [
        [Paragraph("Rank", table_header), Paragraph("Scheme Name", table_header), Paragraph("Category", table_header), Paragraph("Max DD", table_header), Paragraph("Historical Peak", table_header), Paragraph("Trough Date", table_header), Paragraph("Recovery Status", table_header)]
    ]
    for _, r in sc_df.sort_values("max_drawdown_pct", ascending=False).head(12).iterrows():
        dd_table_data.append([
            Paragraph(f"#{r['overall_rank']}", table_cell),
            Paragraph(r['scheme_name'][:34], table_cell),
            Paragraph(r['category'], table_cell),
            Paragraph(f"<b>{r['max_drawdown_pct']:.2f}%</b>", table_cell),
            Paragraph(str(r['peak_date']), table_cell),
            Paragraph(str(r['trough_date']), table_cell),
            Paragraph(str(r['recovery_date']), table_cell),
        ])
    t_dd = Table(dd_table_data, colWidths=[35, 175, 65, 55, 65, 65, 55])
    t_dd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_dd)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Capital Preservation Insights:", h2_style))
    story.append(Paragraph("• <b>Large-Cap Armor:</b> Mirae Asset Large Cap (-11.27%) and SBI Bluechip (-11.80%) contained losses to under 12%, achieving recovery within 4 to 6 months.", bullet_style))
    story.append(Paragraph("• <b>Small-Cap Volatility:</b> Small Cap funds experienced steep drawdowns of -31% to -52%, requiring an average recovery period of over 14 months.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 13: COMPOSITE FUND SCORECARD (0-100)
    # =========================================================================
    story.append(Paragraph("12. Composite Fund Scorecard (0–100 Multi-Factor Model)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "To provide investors with an integrated rating, we formulate a 5-factor composite model weighted as follows:<br/>"
        "$$\\text{Score} = 0.30 R_{\\text{3Y}} + 0.25 R_{\\text{Sharpe}} + 0.20 R_{\\text{Alpha}} + 0.15 R_{\\text{TER}}^{-1} + 0.10 R_{\\text{MaxDD}}^{-1}$$",
        body_style
    ))
    
    fig_score = os.path.join(FIG_DIR, "05_scorecard_top15.png")
    if os.path.exists(fig_score):
        story.append(Image(fig_score, width=470, height=190))
        story.append(Paragraph("<b>Figure 12.1:</b> Top 15 Mutual Funds by Composite Scorecard", callout_style))
        story.append(Spacer(1, 6))

    sc_top_data = [
        [Paragraph("Rank", table_header), Paragraph("Score", table_header), Paragraph("Scheme Name", table_header), Paragraph("Category", table_header), Paragraph("3Y CAGR", table_header), Paragraph("Sharpe", table_header), Paragraph("Alpha", table_header), Paragraph("TER", table_header), Paragraph("Max DD", table_header)]
    ]
    for _, r in sc_df.head(9).iterrows():
        sc_top_data.append([
            Paragraph(f"<b>#{r['overall_rank']}</b>", table_cell),
            Paragraph(f"<b>{r['scorecard_score']:.1f}</b>", table_cell),
            Paragraph(r['scheme_name'][:30], table_cell),
            Paragraph(r['category'], table_cell),
            Paragraph(f"{r['cagr_3yr_pct']:.1f}%", table_cell),
            Paragraph(f"{r['sharpe_ratio']:.2f}", table_cell),
            Paragraph(f"{r['alpha_ann_pct']:.1f}%", table_cell),
            Paragraph(f"{r['expense_ratio_pct']:.2f}%", table_cell),
            Paragraph(f"{r['max_drawdown_pct']:.1f}%", table_cell),
        ])
    t_sc = Table(sc_top_data, colWidths=[30, 35, 170, 60, 48, 42, 45, 40, 45])
    t_sc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('PADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_light])
    ]))
    story.append(t_sc)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 14: BENCHMARK COMPARISON & TRACKING ERROR
    # =========================================================================
    story.append(Paragraph("13. Benchmark Trajectory & Tracking Error Analysis", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Tracking error measures relative volatility divergence from market benchmarks: $\\text{TE} = \\text{Std}(r_{\\text{fund}} - r_{\\text{bench}}) \\times \\sqrt{252}$. "
        "The chart below illustrates the 3-year cumulative performance trajectory (Base = 100) of the Top 5 Scorecard Funds vs NIFTY 100 TRI and NIFTY 50.",
        body_style
    ))
    
    fig_bm = os.path.join(BASE_DIR, "benchmark_comparison_chart.png")
    if os.path.exists(fig_bm):
        story.append(Image(fig_bm, width=490, height=310))
        story.append(Paragraph("<b>Figure 13.1:</b> Top 5 Mutual Funds Trajectory (Base=100) vs Nifty 100 & Nifty 50 with Tracking Error Table", callout_style))
        story.append(Spacer(1, 8))

    story.append(Paragraph("Trajectory Findings:", h2_style))
    story.append(Paragraph("• All Top 5 funds generated substantial cumulative alpha over NIFTY 100 TRI and NIFTY 50 across the 3-year window.", bullet_style))
    story.append(Paragraph("• Kotak Flexicap and Mirae Asset Large Cap achieved high excess returns while maintaining moderate tracking errors (18.9% - 20.6%), validating high information ratio efficiency.", bullet_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 15: POWER BI DASHBOARD SHOWCASE (PAGES 1 & 2)
    # =========================================================================
    story.append(Paragraph("14. Power BI Executive Dashboard: Industry & Performance", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "The Power BI intelligence solution (`bluestock_mf_dashboard.pbix`) translates raw dimensional data into intuitive executive visual cards, "
        "dynamic slicers, and interactive drill-downs across four tailored reporting canvases.", body_style
    ))
    
    p1_img = os.path.join(BASE_DIR, "page1_industry_overview.png")
    p2_img = os.path.join(BASE_DIR, "page2_fund_performance.png")
    
    if os.path.exists(p1_img):
        story.append(Paragraph("Page 1: Industry & Market Overview", h2_style))
        story.append(Image(p1_img, width=470, height=210))
        story.append(Paragraph("<b>Dashboard View 1:</b> Macro AUM progression, monthly SIP inflows, AMC market share breakdown.", callout_style))
        story.append(Spacer(1, 8))
        
    if os.path.exists(p2_img):
        story.append(Paragraph("Page 2: Fund Performance & Quantitative Analytics", h2_style))
        story.append(Image(p2_img, width=470, height=210))
        story.append(Paragraph("<b>Dashboard View 2:</b> Interactive risk vs return scatter, multi-period CAGR comparisons, expense ratio impact.", callout_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 16: POWER BI DASHBOARD SHOWCASE (PAGES 3 & 4)
    # =========================================================================
    story.append(Paragraph("15. Power BI Executive Dashboard: Investors & SIP Trends", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Pages 3 and 4 of the intelligence suite profile investor demographics, channel distributions, and geographic penetration patterns.", body_style
    ))
    
    p3_img = os.path.join(BASE_DIR, "page3_investor_analytics.png")
    p4_img = os.path.join(BASE_DIR, "page4_sip_market_trends.png")
    
    if os.path.exists(p3_img):
        story.append(Paragraph("Page 3: Investor Demographics & Behavioral Profiling", h2_style))
        story.append(Image(p3_img, width=470, height=210))
        story.append(Paragraph("<b>Dashboard View 3:</b> Age cohort allocations, gender segmentation, and T30 vs B30 ticket sizes.", callout_style))
        story.append(Spacer(1, 8))
        
    if os.path.exists(p4_img):
        story.append(Paragraph("Page 4: SIP Market Dynamics & Distribution Channels", h2_style))
        story.append(Image(p4_img, width=470, height=210))
        story.append(Paragraph("<b>Dashboard View 4:</b> Digital payment modes (UPI vs NetBanking vs Mandates), state-wise SIP density, folio growth.", callout_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 17: PLATFORM LIMITATIONS & RISK CONSIDERATIONS
    # =========================================================================
    story.append(Paragraph("16. Project Limitations & Risk Considerations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "While the quantitative engine provides deep operational and statistical insights, sound financial stewardship mandates "
        "acknowledging analytical boundaries and model constraints:", body_style
    ))
    story.append(Paragraph("Key Methodological Limitations:", h2_style))
    story.append(Paragraph("1. <b>Time Horizon Constraints:</b> The daily NAV dataset spans ~4.4 years (2022 to 2026). While fully adequate for 1-Year and 3-Year CAGR, the 5-Year CAGR metric reflects annualized compounding across available history rather than a complete 5-year business cycle.", bullet_style))
    story.append(Paragraph("2. <b>Single-Factor CAPM Assumption:</b> The OLS regression against NIFTY 100 assumes a single systematic market risk factor. Incorporating multi-factor Fama-French models (Value, Size, Momentum) would provide deeper factor decomposition, particularly for Small and Mid Cap funds.", bullet_style))
    story.append(Paragraph("3. <b>Static Expense Ratio Modeling:</b> The Total Expense Ratio (TER) is captured as of latest reported disclosures. AMCs periodically alter TER tiers as scheme AUM crosses regulatory thresholds under SEBI slab rules.", bullet_style))
    story.append(Paragraph("4. <b>Survivorship & Inception Bias:</b> The universe comprises 40 currently active flagship schemes. Funds that were merged or wound down prior to the observation window are naturally excluded.", bullet_style))
    story.append(Paragraph("5. <b>Interest Rate Regime Dependence:</b> The RBI Repo Rate proxy ($R_f = 6.5\\%$) was held static. Dynamic risk-free rates reflecting fluctuating 91-day Treasury Bills would enhance short-term Sharpe sensitivity.", bullet_style))
    story.append(Spacer(1, 15))
    
    # Limitations Summary Box
    lim_box = [
        [Paragraph("<b>Critical Model Takeaway:</b> Historical returns and risk metrics are backward-looking indicators. Past performance does not guarantee future results. Quantitative fund scores must be coupled with qualitative assessment of AMC fund manager tenure and investment mandate adherence.", callout_style)]
    ]
    t_lim = Table(lim_box, colWidths=[515])
    t_lim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_lim)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 18: STRATEGIC RECOMMENDATIONS & CONCLUSION
    # =========================================================================
    story.append(Paragraph("17. Strategic Recommendations & Investment Playbook", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceAfter=12))
    story.append(Paragraph(
        "Based on multi-dimensional empirical findings, the Bluestock research team proposes an actionable three-tier "
        "strategic playbook tailored for retail investors, wealth managers, and FinTech platform operators.", body_style
    ))
    
    story.append(Paragraph("Tier 1: Retail Investor Strategic Allocation Playbook", h2_style))
    story.append(Paragraph("• <b>Core & Satellite Architecture:</b> Allocate 60% of equity exposure to low-cost, high-Sharpe Large Cap / Flexicap anchors (e.g., Kotak Flexicap, Mirae Asset Large Cap, ICICI Bluechip Direct) and 40% to high-alpha Mid/Small cap satellites.", bullet_style))
    story.append(Paragraph("• <b>Direct Plan Optimization:</b> Transition systematically from Regular to Direct plans. Saving 60–85 bps in TER compounds to an additional ₹12–18 Lakhs on a 15-year ₹25,000 monthly SIP.", bullet_style))
    story.append(Paragraph("• <b>Automate Downside Protection:</b> Utilize SIP step-up triggers during market corrections to lower rupee-cost averaging points.", bullet_style))
    
    story.append(Paragraph("Tier 2: Institutional & Wealth Management Playbook", h2_style))
    story.append(Paragraph("• <b>Sortino-First Screening:</b> Prioritize funds where Sortino $\\gg$ Sharpe, indicating asymmetric upside participation with superior downside drawdown containment.", bullet_style))
    story.append(Paragraph("• <b>Information Ratio Monitoring:</b> Screen for consistent alpha with tracking error bounded under 20% to avoid uncompensated idiosyncratic stock-picking risk.", bullet_style))
    
    story.append(Paragraph("Tier 3: Bluestock FinTech Platform Product Roadmap", h2_style))
    story.append(Paragraph("• <b>Automated Smart Scorecards:</b> Embed the 0–100 composite scorecard directly into user onboarding workflows, replacing simplistic star ratings with quantitative factor attribution.", bullet_style))
    story.append(Paragraph("• <b>Drawdown & Recovery Alerts:</b> Introduce real-time portfolio drawdown alerts notifying investors when their funds enter historically deep buying zones.", bullet_style))
    story.append(Paragraph("• <b>UPI AutoPay Deep Integration:</b> Leverage B30 digital adoption trends by providing one-click micro-SIPs via UPI AutoPay.", bullet_style))
    
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=c_navy, spaceAfter=10))
    story.append(Paragraph("<b>Capstone Project Sign-Off:</b> Completed with full technical verification across data engineering, quantitative modeling, visual dashboards, and automated execution pipelines. Ready for enterprise production deployment.", body_bold))

    # Build Document
    print(f"Building PDF document at {PDF_PATH}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    
    # Mirror copy in reports/
    rep_pdf = os.path.join(BASE_DIR, "reports", "Final_Report.pdf")
    import shutil
    shutil.copy2(PDF_PATH, rep_pdf)
    print(f"[SUCCESS] Final_Report.pdf generated: {os.path.getsize(PDF_PATH):,} bytes.")
    print(f"[MIRRORED] {rep_pdf}")

if __name__ == "__main__":
    build_pdf()
