"""
Generate High-Quality 12-Slide Widescreen Presentation:
Bluestock Mutual Fund Analytics & Quantitative Risk Modeling
Using python-pptx
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"C:\Users\Admin\.gemini\antigravity\scratch\mutual_fund_analysis"
FIG_DIR = os.path.join(BASE_DIR, "reports", "figures")
PPTX_PATH = os.path.join(BASE_DIR, "Bluestock_MF_Presentation.pptx")

# Color Palette
C_NAVY = RGBColor(15, 23, 42)       # #0F172A
C_BLUE = RGBColor(0, 71, 171)      # #0047AB
C_LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
C_WHITE = RGBColor(255, 255, 255)
C_DARK = RGBColor(30, 41, 59)      # #1E293B
C_GRAY = RGBColor(100, 116, 139)   # #64748B
C_EMERALD = RGBColor(16, 185, 129) # #10B981
C_AMBER = RGBColor(245, 158, 11)   # #F59E0B
C_BORDER = RGBColor(226, 232, 240) # #E2E8F0
C_CARD_BG = RGBColor(255, 255, 255)

def create_presentation():
    print("Initializing PowerPoint creation...")
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="BLUESTOCK MUTUAL FUND CAPSTONE"):
        # Header background banner
        header_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
        header_box.fill.solid()
        header_box.fill.fore_color.rgb = C_NAVY
        header_box.line.color.rgb = C_NAVY
        
        # Category tag
        tx_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.7), Inches(0.3))
        tf_c = tx_cat.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(10)
        p_c.font.bold = True
        p_c.font.color.rgb = C_AMBER
        
        # Title text
        tx_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.7), Inches(0.6))
        tf_t = tx_title.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = C_WHITE

    def set_slide_background(slide, color=C_LIGHT_BG):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.color.rgb = color
        return bg

    def add_card(slide, left, top, width, height, title="", border_color=C_BORDER, fill_color=C_CARD_BG):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
        
        if title:
            tx = slide.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), width - Inches(0.3), Inches(0.45))
            tf = tx.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = C_BLUE
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (Dark Executive Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY)
    
    # Accent shape
    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.6))
    accent.fill.solid()
    accent.fill.fore_color.rgb = C_AMBER
    accent.line.color.rgb = C_AMBER

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.2), Inches(3.6))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "BLUESTOCK FINTECH RESEARCH"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = C_EMERALD
    p0.space_after = Pt(10)
    
    p1 = tf.add_paragraph()
    p1.text = "Mutual Fund Analytics & Quantitative Risk Modeling"
    p1.font.size = Pt(34)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(12)
    
    p2 = tf.add_paragraph()
    p2.text = "Enterprise Data Engineering, Factor Attribution, Composite Scorecard & Executive BI Solution"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_after = Pt(28)
    
    p3 = tf.add_paragraph()
    p3.text = "Author: Ankitha B | Bluestock Capstone Fellow  •  Timeline: 2022–2026 Data Universe  •  Version 1.0"
    p3.font.size = Pt(12)
    p3.font.color.rgb = C_AMBER

    # =========================================================================
    # SLIDE 2: PROBLEM & OBJECTIVE
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement & Strategic Objectives")
    
    # Card 1: Problem
    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), "The Market Dilemma")
    tx_p = s2.shapes.add_textbox(Inches(0.95), Inches(2.1), Inches(5.3), Inches(4.6))
    tf_p = tx_p.text_frame
    tf_p.word_wrap = True
    bullets_p = [
        ("Information Asymmetry:", " Retail investors rely heavily on 1-year trailing nominal returns, completely ignoring risk-adjusted factors and drawdown risks."),
        ("Direct vs Regular Inefficiencies:", " High distributor commissions (60-85 bps TER drag) compound silently into substantial wealth loss over 10+ year horizons."),
        ("Unstandardized Disclosures:", " AMFI data, daily NAVs, AUM snapshots, and benchmark indices are distributed in siloed formats lacking cohesive analytical tooling."),
        ("Absence of Downside Metrics:", " Standard metrics penalize positive upside volatility; investors lack access to semi-deviation (Sortino) and historical recovery timelines.")
    ]
    for b_title, b_desc in bullets_p:
        p = tf_p.add_paragraph()
        run1 = p.add_run()
        run1.text = b_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = C_DARK
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(12)

    # Card 2: Objectives
    add_card(s2, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), "Strategic Deliverables & Scope")
    tx_o = s2.shapes.add_textbox(Inches(6.95), Inches(2.1), Inches(5.4), Inches(4.6))
    tf_o = tx_o.text_frame
    tf_o.word_wrap = True
    bullets_o = [
        ("Automated ETL Pipeline:", " Build a deterministic SQLite star schema harmonizing 64,320 NAV records and 30,000 transactions across 40 schemes."),
        ("Quantitative Factor Engine:", " Implement multi-period CAGR, Sharpe ($R_f=6.5\\%$), Sortino, CAPM Alpha/Beta vs Nifty 100, and max drawdown analytics."),
        ("Composite Fund Scorecard (0–100):", " Design an objective 5-factor scoring model weighting return, efficiency, manager alpha, cost, and capital preservation."),
        ("Executive Power BI Suite:", " Deliver 4-page interactive dashboard covering industry growth, fund rankings, demographics, and SIP channel dynamics."),
        ("Actionable Playbook:", " Formulate tailored allocation strategies for retail investors, institutional desks, and FinTech platforms.")
    ]
    for b_title, b_desc in bullets_o:
        p = tf_o.add_paragraph()
        run1 = p.add_run()
        run1.text = b_title
        run1.font.bold = True
        run1.font.size = Pt(11)
        run1.font.color.rgb = C_BLUE
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(10.5)
        run2.font.color.rgb = C_GRAY
        p.space_after = Pt(10)

    # =========================================================================
    # SLIDE 3: DATA SOURCES & STAR SCHEMA
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Data Sources & Star Schema Dimensional Architecture")
    
    # 4 Data Stat Cards across top
    stats = [
        ("40 Schemes", "Across Equity, Debt & Hybrid", C_BLUE),
        ("64,320 Records", "Daily NAV History (2022-2026)", C_EMERALD),
        ("30,000 Rows", "Granular Investor Transactions", C_AMBER),
        ("10 Benchmarks", "NIFTY 50, 100, 500, CRISIL", C_NAVY)
    ]
    for i, (s_num, s_desc, s_col) in enumerate(stats):
        cx = Inches(0.8 + i * 2.95)
        card = add_card(s3, cx, Inches(1.4), Inches(2.8), Inches(1.1), border_color=s_col)
        tx = s3.shapes.add_textbox(cx + Inches(0.1), Inches(1.48), Inches(2.6), Inches(0.9))
        tf = tx.text_frame
        p1 = tf.paragraphs[0]
        p1.text = s_num
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = s_col
        p2 = tf.add_paragraph()
        p2.text = s_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = C_GRAY

    # Big Lower Card: Star Schema Architecture
    add_card(s3, Inches(0.8), Inches(2.7), Inches(11.7), Inches(4.3), "Star Schema Relational Architecture (SQLite 3)")
    tx_s = s3.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.3), Inches(3.6))
    tf_s = tx_s.text_frame
    tf_s.word_wrap = True
    
    tables_info = [
        ("dim_fund (Dimension):", " 40 AMC schemes, fund house, category, sub-category, plan (Direct/Regular), launch date, expense ratio (TER)"),
        ("dim_date (Dimension):", " 1,608 calendar dates (2022-01-03 to 2026-05-29), year, quarter, month, day, is_weekday flag"),
        ("fact_nav (Fact Table):", " 64,320 records tracking daily closing NAVs, is_forward_filled flag (0/1), calculated daily returns"),
        ("fact_transactions (Fact Table):", " 30,000 investor trades capturing age, gender, state, city tier (T30/B30), SIP vs lumpsum, payment mode"),
        ("fact_aum (Fact Table):", " 480 monthly AUM snapshots across top 10 AMCs detailing total managed assets and net inflows"),
        ("benchmark_indices (Fact):", " 8,050 index closing levels for Nifty 50, Nifty 100 TRI, Midcap 150, Smallcap 250, CRISIL Gilt"),
        ("portfolio_holdings (Fact):", " 400 top holding records detailing asset allocation, sector weights, and equity concentration"),
        ("fact_performance (Derived):", " Quant metrics: 1Y/3Y/5Y CAGR, Sharpe, Sortino, Alpha, Beta, Max Drawdown, and Composite Scorecard")
    ]
    for t_name, t_desc in tables_info:
        p = tf_s.add_paragraph()
        r1 = p.add_run()
        r1.text = t_name
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = t_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 4: ARCHITECTURE & DATA ENGINEERING PIPELINE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "End-to-End Data Engineering & ETL Pipeline")
    
    # 4 Pipeline Stage Cards
    stages = [
        ("Stage 1: Ingestion & Extract", "• Multi-source CSV ingestion\n• Schema contract verification\n• Staging buffer allocation\n• Raw AMFI format parsing", C_BLUE),
        ("Stage 2: Cleaning & Harmonize", "• Weekend calendar grid filling\n• `is_forward_filled` binary flag\n• TER percentage casting\n• Outlier 3-sigma winsorization", C_EMERALD),
        ("Stage 3: SQLite Storage", "• Star Schema relational load\n• Foreign key constraints\n• B-Tree index optimization\n• Automated VACUUM & ANALYZE", C_AMBER),
        ("Stage 4: BI & Analytics Layer", "• SciPy & Pandas quant engine\n• Scorecard rating synthesis\n• Power BI dataset sync\n• Automated report compilation", C_NAVY)
    ]
    for i, (st_title, st_body, st_col) in enumerate(stages):
        cx = Inches(0.8 + i * 2.95)
        add_card(s4, cx, Inches(1.5), Inches(2.8), Inches(4.3), border_color=st_col)
        tx = s4.shapes.add_textbox(cx + Inches(0.15), Inches(1.65), Inches(2.5), Inches(4.0))
        tf = tx.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = st_title
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = st_col
        p_t.space_after = Pt(12)
        
        for line in st_body.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_DARK
            p.space_after = Pt(6)

    # Bottom Callout Box
    add_card(s4, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.9), border_color=C_BLUE, fill_color=RGBColor(239, 246, 255))
    tx_bot = s4.shapes.add_textbox(Inches(0.95), Inches(6.08), Inches(11.4), Inches(0.75))
    tf_b = tx_bot.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "Data Integrity Guarantee: 100% complete time series across 1,608 days; non-trading days forward-filled with zero return distortion in downstream quant models."
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = C_BLUE

    # =========================================================================
    # SLIDE 5: EDA HIGHLIGHTS 1 (AUM & SIP Inflows)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Exploratory Data Analysis: AUM Growth & SIP Inflow Dynamics")
    
    # Left Chart Image: AUM
    img_aum = os.path.join(FIG_DIR, "02_aum_growth_by_fund_house.png")
    if os.path.exists(img_aum):
        s5.shapes.add_picture(img_aum, Inches(0.8), Inches(1.5), width=Inches(5.7), height=Inches(3.3))
    
    # Right Chart Image: SIP Inflows
    img_sip = os.path.join(FIG_DIR, "03_monthly_sip_inflows_trend.png")
    if os.path.exists(img_sip):
        s5.shapes.add_picture(img_sip, Inches(6.8), Inches(1.5), width=Inches(5.7), height=Inches(3.3))

    # Bottom Summary Card
    add_card(s5, Inches(0.8), Inches(5.0), Inches(11.7), Inches(2.0), "Key Macro Inflow Insights")
    tx_eda1 = s5.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.4))
    tf_e1 = tx_eda1.text_frame
    tf_e1.word_wrap = True
    eda1_points = [
        ("Exponential SIP Trajectory: ", "Monthly SIP inflows grew continuously from ₹11,500 Cr (Jan 2022) to >₹23,000 Cr (mid-2026), proving that retail systematic commitments act as a structural counterweight to foreign institutional selling."),
        ("Fund House Concentration: ", "Top 5 AMCs (SBI, ICICI Pru, HDFC, Nippon, Kotak) manage over 58% of industry AUM. SBI MF leads due to massive public-sector banking reach."),
        ("Category Inflow Rotation: ", "Inflows rotated cyclically from Large Cap (2022) into Mid and Small Caps (2024–2025) chasing high trailing returns, increasing downside exposure.")
    ]
    for b_title, b_desc in eda1_points:
        p = tf_e1.add_paragraph()
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 6: EDA HIGHLIGHTS 2 (Demographics & Geography)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Exploratory Data Analysis: Demographics & Geographic Expansion")
    
    # Left Chart Image: Age
    img_age = os.path.join(FIG_DIR, "05_investor_demographics_age_pie.png")
    if os.path.exists(img_age):
        s6.shapes.add_picture(img_age, Inches(0.8), Inches(1.5), width=Inches(5.7), height=Inches(3.3))
    
    # Right Chart Image: State SIP
    img_geo = os.path.join(FIG_DIR, "08_geographic_sip_by_state.png")
    if os.path.exists(img_geo):
        s6.shapes.add_picture(img_geo, Inches(6.8), Inches(1.5), width=Inches(5.7), height=Inches(3.3))

    # Bottom Summary Card
    add_card(s6, Inches(0.8), Inches(5.0), Inches(11.7), Inches(2.0), "Demographic & Geographic Takeaways")
    tx_eda2 = s6.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.4))
    tf_e2 = tx_eda2.text_frame
    tf_e2.word_wrap = True
    eda2_points = [
        ("Millennial & Gen Z Influx: ", "Investors aged 18–35 constitute 42% of active accounts and 54% of new SIP registrations, driven by frictionless digital KYC onboarding."),
        ("Geographic Breadth: ", "Maharashtra, Gujarat, Karnataka, and Delhi NCR represent 48% of AUM, while B30 locations expanded at 28% CAGR vs 16% for metropolitan T30."),
        ("Ticket Size Polarization: ", "Metropolitan T30 accounts average ₹4,500–₹8,000/month SIPs, whereas B30 centers average ₹1,500–₹2,500/month with high UPI AutoPay penetration.")
    ]
    for b_title, b_desc in eda2_points:
        p = tf_e2.add_paragraph()
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 7: PERFORMANCE METRICS 1 (Compounded Returns / CAGR)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Performance Analytics: Multi-Period Compounded Growth (CAGR)")
    
    # Left: CAGR Chart
    img_cagr = os.path.join(FIG_DIR, "02_cagr_comparison_top10.png")
    if os.path.exists(img_cagr):
        s7.shapes.add_picture(img_cagr, Inches(0.8), Inches(1.5), width=Inches(6.2), height=Inches(3.3))
        
    # Right: Daily Return Distribution
    img_ret = os.path.join(FIG_DIR, "01_daily_return_distribution.png")
    if os.path.exists(img_ret):
        s7.shapes.add_picture(img_ret, Inches(7.2), Inches(1.5), width=Inches(5.3), height=Inches(3.3))

    # Bottom Card: Table & Methodology
    add_card(s7, Inches(0.8), Inches(5.0), Inches(11.7), Inches(2.0), "CAGR Performance & Return Distribution Properties")
    tx_cagr = s7.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.4))
    tf_cg = tx_cagr.text_frame
    tf_cg.word_wrap = True
    cagr_points = [
        ("Geometric Formula: ", "CAGR = (NAV_end / NAV_start)^(1/n) - 1. Evaluated for 1Y (n=1), 3Y (n=3), and Full Horizon (n≈4.0 yrs) ending Dec 31, 2025."),
        ("Top Compounding Leaders: ", "Kotak Flexicap (3Y: 40.65%, 5Y: 34.42%), Mirae Asset Large Cap (3Y: 35.28%, 5Y: 35.60%), Axis Midcap (3Y: 36.66%)."),
        ("Empirical Distribution: ", "45,960 trading observations; Daily Mean: +0.0631% (15.9% ann); Skewness: +0.04; Excess Kurtosis: +1.37 (fat tails verified via Jarque-Bera).")
    ]
    for b_title, b_desc in cagr_points:
        p = tf_cg.add_paragraph()
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 8: PERFORMANCE METRICS 2 (Sharpe, Sortino, Alpha, Scorecard)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Performance Analytics: Risk-Adjusted Ratios & Composite Scorecard")
    
    # Left: Sharpe vs Sortino
    img_risk = os.path.join(FIG_DIR, "03_sharpe_vs_sortino.png")
    if os.path.exists(img_risk):
        s8.shapes.add_picture(img_risk, Inches(0.8), Inches(1.5), width=Inches(5.7), height=Inches(3.3))
        
    # Right: Scorecard Top 15
    img_sc = os.path.join(FIG_DIR, "05_scorecard_top15.png")
    if os.path.exists(img_sc):
        s8.shapes.add_picture(img_sc, Inches(6.8), Inches(1.5), width=Inches(5.7), height=Inches(3.3))

    # Bottom Summary Card
    add_card(s8, Inches(0.8), Inches(5.0), Inches(11.7), Inches(2.0), "Risk Efficiency & Multi-Factor Scorecard Weights")
    tx_sc = s8.shapes.add_textbox(Inches(1.0), Inches(5.45), Inches(11.3), Inches(1.4))
    tf_sc = tx_sc.text_frame
    tf_sc.word_wrap = True
    sc_points = [
        ("Sharpe & Sortino ($R_f = 6.5\\%$): ", "Mirae Asset Large Cap achieved highest Sharpe (1.448) and Sortino (1.479), minimizing downside semi-deviation on down days."),
        ("CAPM OLS Regression (Nifty 100): ", "Kotak Flexicap (+27.3% alpha) and ICICI Pru Midcap (+29.3% alpha) exhibited high active management alpha with controlled market beta."),
        ("Scorecard Weights (0–100): ", "Score = 30% × 3Y Return Rank + 25% × Sharpe Rank + 20% × Alpha Rank + 15% × TER (inv) + 10% × Max Drawdown (inv). Top fund: Kotak Flexicap (86.2).")
    ]
    for b_title, b_desc in sc_points:
        p = tf_sc.add_paragraph()
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(3)

    # =========================================================================
    # SLIDE 9: DASHBOARD SCREENSHOTS 1 (Overview & Performance)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Power BI Dashboard: Industry Overview & Fund Performance")
    
    # Left: Page 1 Screenshot
    img_p1 = os.path.join(BASE_DIR, "page1_industry_overview.png")
    if os.path.exists(img_p1):
        s9.shapes.add_picture(img_p1, Inches(0.8), Inches(1.5), width=Inches(5.7), height=Inches(3.6))
        
    # Right: Page 2 Screenshot
    img_p2 = os.path.join(BASE_DIR, "page2_fund_performance.png")
    if os.path.exists(img_p2):
        s9.shapes.add_picture(img_p2, Inches(6.8), Inches(1.5), width=Inches(5.7), height=Inches(3.6))

    # Bottom Notes
    add_card(s9, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.7), "Interactive Reporting Highlights")
    tx_d1 = s9.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.2))
    tf_d1 = tx_d1.text_frame
    tf_d1.word_wrap = True
    d1_points = [
        ("Page 1 (Industry Overview): ", "Real-time KPI cards tracking aggregate AUM (₹65+ Lakh Cr), active SIP accounts, top 5 AMC market share, and monthly category inflows."),
        ("Page 2 (Fund Performance): ", "Dynamic risk vs return scatter quadrant, interactive fund comparison slicers, multi-horizon CAGR bar charts, and expense ratio impact sliders.")
    ]
    for b_title, b_desc in d1_points:
        p = tf_d1.add_paragraph()
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 10: DASHBOARD SCREENSHOTS 2 (Demographics & SIP Trends)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Power BI Dashboard: Investor Analytics & SIP Market Trends")
    
    # Left: Page 3 Screenshot
    img_p3 = os.path.join(BASE_DIR, "page3_investor_analytics.png")
    if os.path.exists(img_p3):
        s10.shapes.add_picture(img_p3, Inches(0.8), Inches(1.5), width=Inches(5.7), height=Inches(3.6))
        
    # Right: Page 4 Screenshot
    img_p4 = os.path.join(BASE_DIR, "page4_sip_market_trends.png")
    if os.path.exists(img_p4):
        s10.shapes.add_picture(img_p4, Inches(6.8), Inches(1.5), width=Inches(5.7), height=Inches(3.6))

    # Bottom Notes
    add_card(s10, Inches(0.8), Inches(5.3), Inches(11.7), Inches(1.7), "Behavioral & Channel Distribution Views")
    tx_d2 = s10.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(11.3), Inches(1.2))
    tf_d2 = tx_d2.text_frame
    tf_d2.word_wrap = True
    d2_points = [
        ("Page 3 (Investor Analytics): ", "Age cohort breakdown, gender participation split, and city tier ticket size comparisons enabling wealth managers to tailor marketing outreach."),
        ("Page 4 (SIP Trends): ", "Digital payment mode distribution (UPI AutoPay vs Mandates vs NetBanking), state-wise folio densities, and discontinuation vs retention rates.")
    ]
    for b_title, b_desc in d2_points:
        p = tf_d2.add_paragraph()
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_BLUE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10)
        r2.font.color.rgb = C_DARK
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 11: KEY FINDINGS & STRATEGIC RECOMMENDATIONS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Strategic Recommendations & Actionable Investment Playbook")
    
    # 3 Recommendation Pillars
    pillars = [
        ("Retail Investors", "• Adopt Core & Satellite: 60% in Large/Flexicap anchors, 40% in Mid/Small satellites.\n• Switch to Direct Plans: Save 60-85 bps TER drag (yielding ₹12L+ over 15Y).\n• Use Step-Up SIPs during drawdowns.", C_BLUE),
        ("Wealth Managers", "• Filter by Sortino: Prioritize funds with high downside protection.\n• Monitor Tracking Error: Ensure active risk remains bounded under 20%.\n• Focus on T30/B30 hybrid asset allocation products.", C_EMERALD),
        ("FinTech Platforms", "• Embed 0–100 Scorecard into discovery funnels rather than crude star ratings.\n• Real-Time Drawdown Alerts to prompt value investing entries.\n• One-Click Micro-SIPs via UPI AutoPay integration.", C_AMBER)
    ]
    for i, (p_title, p_body, p_col) in enumerate(pillars):
        cx = Inches(0.8 + i * 3.95)
        add_card(s11, cx, Inches(1.5), Inches(3.8), Inches(4.3), border_color=p_col)
        tx = s11.shapes.add_textbox(cx + Inches(0.15), Inches(1.65), Inches(3.5), Inches(4.0))
        tf = tx.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = p_title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = p_col
        p_t.space_after = Pt(12)
        
        for line in p_body.split("\n"):
            p = tf.add_paragraph()
            p.text = line
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_DARK
            p.space_after = Pt(6)

    # Bottom Summary
    add_card(s11, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.9), border_color=C_NAVY, fill_color=RGBColor(241, 245, 249))
    tx_s11 = s11.shapes.add_textbox(Inches(0.95), Inches(6.08), Inches(11.4), Inches(0.75))
    tf_11 = tx_s11.text_frame
    p_11 = tf_11.paragraphs[0]
    p_11.text = "Execution Takeaway: Objective multi-factor scoring eliminates emotional investing, directing capital toward sustainable alpha generators."
    p_11.font.size = Pt(11)
    p_11.font.bold = True
    p_11.font.color.rgb = C_NAVY

    # =========================================================================
    # SLIDE 12: THANK YOU & Q&A
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, C_NAVY)
    
    # Accent shape
    accent12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    accent12.fill.solid()
    accent12.fill.fore_color.rgb = C_EMERALD
    accent12.line.color.rgb = C_EMERALD

    tbox12 = s12.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.2), Inches(3.8))
    tf12 = tbox12.text_frame
    tf12.word_wrap = True
    
    p0_12 = tf12.paragraphs[0]
    p0_12.text = "BLUESTOCK MUTUAL FUND CAPSTONE PROJECT"
    p0_12.font.size = Pt(13)
    p0_12.font.bold = True
    p0_12.font.color.rgb = C_AMBER
    p0_12.space_after = Pt(12)
    
    p1_12 = tf12.add_paragraph()
    p1_12.text = "Thank You! Questions & Discussion"
    p1_12.font.size = Pt(36)
    p1_12.font.bold = True
    p1_12.font.color.rgb = C_WHITE
    p1_12.space_after = Pt(16)
    
    p2_12 = tf12.add_paragraph()
    p2_12.text = "GitHub Repository: https://github.com/ankithaa08/mutual-fund-analytics  •  Tagged Release: v1.0"
    p2_12.font.size = Pt(14)
    p2_12.font.color.rgb = RGBColor(203, 213, 225)
    p2_12.space_after = Pt(24)
    
    p3_12 = tf12.add_paragraph()
    p3_12.text = "Deliverables: Final_Report.pdf (18 pages)  |  Bluestock_MF_Presentation.pptx (12 slides)  |  Power BI Suite (.pbix)"
    p3_12.font.size = Pt(12)
    p3_12.font.color.rgb = C_EMERALD

    print(f"Saving presentation at {PPTX_PATH}...")
    prs.save(PPTX_PATH)
    
    # Mirror in reports/
    rep_pptx = os.path.join(BASE_DIR, "reports", "Bluestock_MF_Presentation.pptx")
    import shutil
    shutil.copy2(PPTX_PATH, rep_pptx)
    print(f"[SUCCESS] Bluestock_MF_Presentation.pptx generated: {os.path.getsize(PPTX_PATH):,} bytes.")
    print(f"[MIRRORED] {rep_pptx}")

if __name__ == "__main__":
    create_presentation()
