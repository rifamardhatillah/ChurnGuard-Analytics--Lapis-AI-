import io
import hashlib
import datetime
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# ─────────────────────────────────────────
# PAGE CONFIG  (harus paling atas)
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ChurnGuard Pro | Retention Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def run_churnguard_app():

    # ─────────────────────────────────────────
    # DESIGN SYSTEM — CSS
    # ─────────────────────────────────────────
    st.markdown("""
    <style>
    /* ── Google Fonts ─────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

    /* ── Base ─────────────────────────────────────────────────── */
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stApp { background: #F0F4FF; color: #0F172A; }

    /* ── Remove Streamlit chrome ──────────────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 2rem 3rem 2rem; max-width: 1400px; }

    /* ── Scrollbar ────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #F0F4FF; }
    ::-webkit-scrollbar-thumb { background: #BFDBFE; border-radius: 3px; }

    /* ── Sidebar ──────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    /* ── Brand Bar ────────────────────────────────────────────── */
    .brand-bar {
        display: flex; align-items: center; gap: 16px;
        padding: 22px 0 18px 0; margin-bottom: 4px;
        border-bottom: 1px solid #E2E8F0;
    }
    .brand-logo {
        width: 46px; height: 46px; border-radius: 12px;
        background: linear-gradient(135deg,#2563EB,#0EA5E9);
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; flex-shrink: 0;
        box-shadow: 0 4px 12px rgba(37,99,235,0.25);
    }
    .brand-name {
        font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 800;
        background: linear-gradient(90deg,#2563EB,#0EA5E9);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }
    .brand-sub { font-size: 0.72rem; color: #94A3B8; letter-spacing: .12em; text-transform: uppercase; }

    /* ── Section Heading ──────────────────────────────────────── */
    .section-heading {
        font-family: 'Syne', sans-serif; font-size: 1.05rem; font-weight: 700;
        color: #64748B; letter-spacing: .08em; text-transform: uppercase;
        margin: 28px 0 14px 0; display: flex; align-items: center; gap: 8px;
    }
    .section-heading::after {
        content:''; flex: 1; height: 1px;
        background: linear-gradient(90deg,rgba(37,99,235,0.25),transparent);
    }

    /* ── Section Header (inline page subtitle) ────────────────── */
    .section-header {
        font-family: 'DM Sans', sans-serif; color: #2563EB; font-size: .75rem;
        letter-spacing: .15em; text-transform: uppercase;
        border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; margin-bottom: 20px;
    }

    /* ── KPI Cards ────────────────────────────────────────────── */
    .kpi-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 16px; padding: 22px 20px; position: relative; overflow: hidden;
        transition: border-color .25s, transform .2s;
        box-shadow: 0 1px 6px rgba(37,99,235,0.06);
    }
    .kpi-card:hover { border-color: #2563EB; transform: translateY(-3px); }
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
        background: var(--accent);
    }
    .kpi-label {
        font-size: 0.72rem; font-weight: 600; color: #94A3B8;
        letter-spacing: .1em; text-transform: uppercase; margin-bottom: 10px;
    }
    .kpi-value {
        font-family: 'DM Mono', monospace; font-size: 2rem; font-weight: 500;
        color: var(--accent); line-height: 1; margin-bottom: 8px;
    }
    .kpi-delta { font-size: 0.75rem; color: #94A3B8; }

    /* ── Model Metric Card ────────────────────────────────────── */
    .model-metric-card {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 16px; padding: 18px; text-align: center;
        box-shadow: 0 1px 6px rgba(37,99,235,0.06);
        transition: border-color .25s, transform .2s;
    }
    .model-metric-card:hover { border-color: #2563EB; transform: translateY(-2px); }
    .model-metric-label {
        font-size: .72rem; color: #94A3B8; text-transform: uppercase;
        letter-spacing: .08em; margin-bottom: 8px;
    }
    .model-metric-value {
        font-family: 'DM Mono', monospace; font-size: 1.6rem; font-weight: 500; line-height: 1;
    }

    /* ── Accuracy Badge (sidebar) ─────────────────────────────── */
    .accuracy-badge {
        background: #EFF6FF; border: 1px solid #BFDBFE;
        border-radius: 12px; padding: 12px 14px; text-align: center; margin-bottom: 8px;
    }

    /* ── Alert Banners ────────────────────────────────────────── */
    .alert-critical {
        background: linear-gradient(90deg,rgba(239,68,68,.08),rgba(239,68,68,.03));
        border: 1px solid rgba(239,68,68,.25); border-left: 4px solid #EF4444;
        border-radius: 10px; padding: 14px 18px; margin-bottom: 12px;
        font-size: 0.85rem; color: #991B1B;
    }
    .alert-warning {
        background: linear-gradient(90deg,rgba(245,158,11,.08),rgba(245,158,11,.03));
        border: 1px solid rgba(245,158,11,.25); border-left: 4px solid #F59E0B;
        border-radius: 10px; padding: 14px 18px; margin-bottom: 12px;
        font-size: 0.85rem; color: #92400E;
    }
    .alert-ok {
        background: linear-gradient(90deg,rgba(16,185,129,.08),rgba(16,185,129,.03));
        border: 1px solid rgba(16,185,129,.25); border-left: 4px solid #10B981;
        border-radius: 10px; padding: 14px 18px; margin-bottom: 12px;
        font-size: 0.85rem; color: #065F46;
    }

    /* ── Risk Cards ───────────────────────────────────────────── */
    .risk-card-high {
        background: linear-gradient(90deg,rgba(239,68,68,.08),rgba(239,68,68,.03));
        border: 1px solid rgba(239,68,68,.25); border-left: 4px solid #EF4444;
        border-radius: 10px; padding: 14px 18px; margin: 6px 0; color: #0F172A;
    }
    .risk-card-medium {
        background: linear-gradient(90deg,rgba(245,158,11,.08),rgba(245,158,11,.03));
        border: 1px solid rgba(245,158,11,.25); border-left: 4px solid #F59E0B;
        border-radius: 10px; padding: 14px 18px; margin: 6px 0; color: #0F172A;
    }
    .risk-card-low {
        background: linear-gradient(90deg,rgba(16,185,129,.08),rgba(16,185,129,.03));
        border: 1px solid rgba(16,185,129,.25); border-left: 4px solid #10B981;
        border-radius: 10px; padding: 14px 18px; margin: 6px 0; color: #0F172A;
    }

    /* ── Customer Detail Box ──────────────────────────────────── */
    .customer-detail-box {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 12px; padding: 18px 22px; margin-bottom: 12px;
        box-shadow: 0 1px 6px rgba(37,99,235,0.06);
    }

    /* ── Metric Widget Override ───────────────────────────────── */
    .stMetric {
        background: #FFFFFF; border: 1px solid #E2E8F0;
        border-radius: 12px; padding: 16px 20px;
        box-shadow: 0 1px 6px rgba(37,99,235,0.06);
    }
    .stMetric label {
        color: #94A3B8 !important; font-size: .72rem !important;
        letter-spacing: .08em; text-transform: uppercase;
        font-family: 'DM Sans', sans-serif !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 1.6rem !important;
    }
    .stMetric [data-testid="stMetricDelta"] { font-size: .8rem !important; }

    /* ── Buttons ──────────────────────────────────────────────── */
    .stButton > button {
        background: linear-gradient(135deg,#2563EB,#0EA5E9);
        color: white; border: none; border-radius: 8px;
        font-family: 'DM Sans', sans-serif; font-weight: 600;
        padding: .5rem 1.5rem; transition: all .2s;
    }
    .stButton > button:hover { opacity: 0.9; transform: translateY(-1px); }
    div.stDownloadButton > button {
        background: linear-gradient(135deg,#2563EB,#0EA5E9);
        color: white; border: none; border-radius: 8px;
        font-family: 'DM Sans', sans-serif; font-weight: 600;
        padding: .5rem 1.5rem; transition: all .2s; width: 100%;
    }
    div.stDownloadButton > button:hover { opacity: 0.9; transform: translateY(-1px); }

    /* ── Tabs ─────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: #F8FAFC; border-radius: 12px 12px 0 0;
        border-bottom: 1px solid #E2E8F0; gap: 0; padding: 4px 8px 0 8px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #64748B; font-weight: 600; font-size: .85rem;
        padding: 10px 20px; border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #60A5FA !important;
        background: rgba(30,86,160,.12) !important;
        border-bottom: 2px solid #1E56A0 !important;
    }

    /* ── Selectbox / Multiselect ──────────────────────────────── */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        color: #0F172A !important;
    }
    .stSelectbox [data-baseweb="select"] span,
    .stSelectbox [data-baseweb="select"] div,
    .stSelectbox [data-baseweb="select"] input { color: #0F172A !important; }
    .stMultiSelect [data-baseweb="select"] input { color: #0F172A !important; }
    [data-baseweb="tag"] { color: #FFFFFF !important; }
    [data-baseweb="tag"] span, [data-baseweb="tag"] div,
    [data-baseweb="tag"] p, [data-baseweb="tag"] button svg {
        color: #FFFFFF !important; fill: #FFFFFF !important;
    }
    [data-baseweb="menu"] {
        background: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important; box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;
    }
    [data-baseweb="menu"] li { color: #0F172A !important; background: #FFFFFF !important; }
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [aria-selected="true"] {
        background: #EFF6FF !important; color: #2563EB !important;
    }

    /* ── Dataframe ────────────────────────────────────────────── */
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

    /* ── Nav default ──────────────────────────────────────────── */
    .nav-link { color: #64748B !important; }

    /* ── Nav selected ─────────────────────────────────────────── */
    .nav-link-selected {
        background: linear-gradient(135deg,#2563EB,#0EA5E9) !important;
        color: white !important;
        border: 1px solid transparent !important;
        box-shadow: 0 4px 12px rgba(37,99,235,0.25) !important;
    }
    .nav-link-selected span,
    [data-testid="stSidebar"] .nav-link-selected span { color: white !important; }

    /* ── Icon warna ───────────────────────────────────────────── */
    /* Tidak set color di key "icon" styles dict → icon inherit   */
    /* dari parent <a>. Abu saat non-active, putih saat active.   */
    [data-testid="stSidebar"] .nav-link:not(.active) i.icon { color: #6B7280; }
    [data-testid="stSidebar"] .nav-link.active i.icon { color: inherit; }

    /* ── User badge sidebar ───────────────────────────────────── */
    .user-badge {
        background: #EFF6FF; border: 1px solid #DBEAFE;
        border-radius: 12px; padding: 12px 14px; margin-bottom: 16px;
    }
    .user-badge-label { font-size: 11px; color: #94A3B8; margin-bottom: 2px; }
    .user-badge-name { font-weight: 700; color: #2563EB; font-family: 'DM Sans', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # PLOTLY LAYOUT HELPER
    # ─────────────────────────────────────────
    PLOTLY_BASE = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color="#94A3B8", size=12),
        margin=dict(l=10, r=10, t=36, b=10),
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#0F172A", bordercolor="#2563EB"),
    )
    def pl(**kw):
        base = dict(PLOTLY_BASE)
        base.update(kw)
        return base

    # ─────────────────────────────────────────
    # LOAD ARTIFACTS
    # ─────────────────────────────────────────
    MODEL_PATH = "models"

    @st.cache_resource
    def load_model():
        model         = joblib.load(f"{MODEL_PATH}/churnguard_model.joblib")
        forward_feats = joblib.load(f"{MODEL_PATH}/forward_features.joblib")
        oe_plan       = joblib.load(f"{MODEL_PATH}/encoder_plan.joblib")
        oe_nps        = joblib.load(f"{MODEL_PATH}/encoder_nps.joblib")
        return model, forward_feats, oe_plan, oe_nps

    @st.cache_data
    def load_data():
        return pd.read_csv("churnguard_predictions.csv")

    @st.cache_data
    def load_saved_metrics():
        try:
            return joblib.load(f"{MODEL_PATH}/model_metrics.joblib")
        except FileNotFoundError:
            return None

    try:
        model, forward_features, oe_plan, oe_nps = load_model()
        MODEL_LOADED = True
    except FileNotFoundError:
        MODEL_LOADED = False

    try:
        df = load_data()
        DATA_LOADED = True
    except FileNotFoundError:
        DATA_LOADED = False
        df = pd.DataFrame()

    saved_metrics = load_saved_metrics()

    # ─────────────────────────────────────────
    # HELPER: ENCODING
    # ─────────────────────────────────────────
    CONTRACT_CATEGORIES = ['annual', 'monthly', 'quarterly']

    def encode_input(raw: dict) -> pd.DataFrame:
        df_in = pd.DataFrame([raw])
        df_in['plan_type_enc']    = oe_plan.transform(df_in[['plan_type']])[0]
        df_in['nps_category_enc'] = oe_nps.transform(df_in[['nps_category']])[0]
        for cat in CONTRACT_CATEGORIES:
            df_in[f'contract_type_{cat}'] = (df_in['contract_type'] == cat).astype(int)
        _pm = {'starter': 0, 'professional': 1, 'enterprise': 2}
        df_in['_plan_num']            = df_in['plan_type'].map(_pm)
        df_in['nps_x_adoption']       = df_in['avg_nps_score'] * df_in['avg_feature_adoption']
        df_in['usage_x_tech_tickets'] = df_in['avg_monthly_usage_hrs'] * df_in['technical_tickets']
        df_in['plan_x_usage']         = df_in['_plan_num'] * df_in['avg_monthly_usage_hrs']
        df_in['tenure_x_engagement']  = df_in['tenure_days'] * df_in['engagement_score']
        df_in['usage_per_tenure']     = df_in['avg_monthly_usage_hrs'] / (df_in['tenure_days'] / 30 + 0.01)
        df_in['tickets_per_month']    = df_in['total_tickets'] / (df_in['tenure_days'] / 30 + 0.01)
        df_in['late_x_dunning']       = df_in['payment_delay_rate'] * df_in['dunning_rate']
        df_in['inactive_level']       = (df_in['days_since_last_login'] > 30).astype(int)
        df_in['usage_consistency']    = 1 / (df_in.get('std_monthly_usage_hrs', pd.Series([0])) + 1)
        df_in['usage_drop_ratio']     = 1 - (df_in['min_monthly_usage_hrs'] / (df_in['max_monthly_usage_hrs'] + 0.001))
        df_in['engagement_score']     = (
            df_in['avg_feature_adoption'] * 0.4 +
            df_in['avg_monthly_usage_hrs'] * 0.4 +
            (1 / (df_in['days_since_last_login'] + 1)) * 100 * 0.2
        )
        df_in['risk_score'] = (
            df_in['usage_drop_ratio'] * 0.5 +
            df_in['inactive_level'] * 0.3 +
            (1 - df_in['avg_feature_adoption'] / 100) * 0.2
        )
        df_in['payment_cv'] = df_in.get('std_payment_value', pd.Series([0])) / (df_in['avg_payment_value'] + 1)
        for col in [f for f in forward_features if f not in df_in.columns]:
            df_in[col] = 0
        return df_in[forward_features]

    # ─────────────────────────────────────────
    # HELPER: GAUGE + RISK
    # ─────────────────────────────────────────
    def make_gauge(proba, risk_color, height=260):
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=proba * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Churn Probability", 'font': {'color': '#94A3B8', 'size': 13, 'family': 'DM Sans'}},
            number={'suffix': '%', 'font': {'color': '#0F172A', 'size': 36, 'family': 'DM Mono'}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#94A3B8'},
                'bar': {'color': risk_color, 'thickness': 0.28},
                'bgcolor': '#E2E8F0',
                'borderwidth': 0,
                'steps': [
                    {'range': [0,  40],  'color': 'rgba(16,185,129,.08)'},
                    {'range': [40, 70],  'color': 'rgba(245,158,11,.06)'},
                    {'range': [70, 100], 'color': 'rgba(239,68,68,.06)'},
                ],
                'threshold': {
                    'line': {'color': risk_color, 'width': 2},
                    'thickness': .8, 'value': proba * 100
                }
            }
        ))
        fig.update_layout(**pl(height=height))
        return fig

    def risk_info(proba):
        if proba >= 0.7: return "🔴 HIGH RISK",   "#EF4444", "risk-card-high"
        if proba >= 0.4: return "🟡 MEDIUM RISK",  "#F59E0B", "risk-card-medium"
        return                   "🟢 LOW RISK",    "#10B981", "risk-card-low"

    def fmt(v, fmt_str=None, suffix='', prefix='', default='—'):
        if v is None or (isinstance(v, float) and np.isnan(v)): return default
        if fmt_str: return f"{prefix}{v:{fmt_str}}{suffix}"
        return f"{prefix}{v}{suffix}"

    # ─────────────────────────────────────────
    # PDF REPORT GENERATOR
    # ─────────────────────────────────────────
    def generate_pdf_report(df_data: pd.DataFrame, saved_m: dict) -> bytes:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
            HRFlowable, PageBreak
        )
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm
        )

        C_DARK   = colors.HexColor("#F8FAFC")
        C_PANEL  = colors.HexColor("#EFF6FF")
        C_BORDER = colors.HexColor("#CBD5E1")
        C_BLUE   = colors.HexColor("#2563EB")
        C_GREEN  = colors.HexColor("#10B981")
        C_YELLOW = colors.HexColor("#F59E0B")
        C_RED    = colors.HexColor("#EF4444")
        C_TEXT   = colors.HexColor("#0F172A")
        C_MUTED  = colors.HexColor("#64748B")

        styles = getSampleStyleSheet()
        def S(name, **kw):
            return ParagraphStyle(name, parent=styles['Normal'], **kw)

        sTitle   = S('T',  fontSize=22, textColor=C_BLUE, fontName='Helvetica-Bold', spaceAfter=4,  alignment=TA_CENTER)
        sSub     = S('S',  fontSize=10, textColor=C_MUTED, spaceAfter=2,              alignment=TA_CENTER)
        sH1      = S('H1', fontSize=13, textColor=C_BLUE, fontName='Helvetica-Bold', spaceBefore=14, spaceAfter=6)
        sBody    = S('B',  fontSize=9,  textColor=C_TEXT, leading=14)
        sCaption = S('C',  fontSize=8,  textColor=C_MUTED, spaceAfter=6)

        story = []
        now   = datetime.datetime.now().strftime("%d %B %Y, %H:%M")

        story.append(Spacer(1, 1.5*cm))
        story.append(Paragraph("🛡️ ChurnGuard Pro", sTitle))
        story.append(Paragraph("Customer Churn Analysis Report", sSub))
        story.append(Paragraph(f"Generated: {now}  |  User: {st.session_state.get('username','—')}", sCaption))
        story.append(HRFlowable(width="100%", thickness=1, color=C_BORDER, spaceAfter=16))

        story.append(Paragraph("1. Ringkasan Eksekutif", sH1))
        total = len(df_data)
        if 'churn_proba' in df_data.columns:
            high_n   = int((df_data['churn_proba'] >= 0.7).sum())
            med_n    = int(((df_data['churn_proba'] >= 0.4) & (df_data['churn_proba'] < 0.7)).sum())
            low_n    = int((df_data['churn_proba'] < 0.4).sum())
            avg_prob = df_data['churn_proba'].mean()
        else:
            high_n = med_n = low_n = 0; avg_prob = 0.0
        churned = int(df_data['churn'].sum()) if 'churn' in df_data.columns else 0

        exec_data = [
            ['Metrik', 'Nilai', 'Keterangan'],
            ['Total Customer',        f"{total:,}",                         'Seluruh data dalam sistem'],
            ['Churn Aktual',          f"{churned:,} ({churned/total*100:.1f}%)", 'Label ground truth'],
            ['Avg Churn Probability', f"{avg_prob:.1%}",                    'Rata-rata probabilitas model'],
            ['High Risk (≥70%)',      f"{high_n:,} ({high_n/total*100:.1f}%)", 'Perlu tindakan segera'],
            ['Medium Risk (40-70%)',  f"{med_n:,} ({med_n/total*100:.1f}%)",   'Perlu monitoring'],
            ['Low Risk (<40%)',       f"{low_n:,} ({low_n/total*100:.1f}%)",    'Aman'],
        ]
        t_exec = Table(exec_data, colWidths=[5*cm, 3.5*cm, 8.5*cm])
        t_exec.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_PANEL),  ('TEXTCOLOR', (0,0), (-1,0), C_BLUE),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE',   (0,0), (-1,-1), 8.5),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [C_DARK, C_PANEL]),
            ('TEXTCOLOR',  (0,1), (-1,-1), C_TEXT), ('GRID', (0,0), (-1,-1), 0.4, C_BORDER),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),8), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('TEXTCOLOR',  (1,4),(1,4), C_RED), ('TEXTCOLOR',(1,5),(1,5), C_YELLOW), ('TEXTCOLOR',(1,6),(1,6), C_GREEN),
        ]))
        story.append(t_exec)
        story.append(Spacer(1, 0.4*cm))

        story.append(Paragraph("2. Performa Model XGBoost", sH1))
        story.append(Paragraph(
            "Model dilatih menggunakan XGBoost dengan hyperparameter tuning via Optuna dan "
            "feature selection menggunakan Forward Selection. Metrik dihitung pada data test set.", sBody))
        story.append(Spacer(1, 0.3*cm))

        if saved_m:
            perf_data = [
                ['Metrik', 'Nilai', 'Interpretasi'],
                ['Accuracy',       f"{saved_m.get('Accuracy',0):.1%}",  'Persentase prediksi yang benar'],
                ['F1-Score',       f"{saved_m.get('F1-Score',0):.1%}",  'Harmonic mean precision & recall'],
                ['Precision',      f"{saved_m.get('Precision',0):.1%}", 'Dari prediksi churn, berapa yang benar-benar churn'],
                ['Recall',         f"{saved_m.get('Recall',0):.1%}",    'Dari yang churn, berapa berhasil terdeteksi'],
                ['Train-Test Gap', f"{saved_m.get('Gap',0):.4f}",       f"Status: {saved_m.get('Status','—')}"],
            ]
        else:
            perf_data = [['Metrik','Nilai','Keterangan'],['—','—','model_metrics.joblib tidak ditemukan']]

        t_perf = Table(perf_data, colWidths=[3.5*cm, 3*cm, 10.5*cm])
        t_perf.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),C_PANEL), ('TEXTCOLOR',(0,0),(-1,0),C_BLUE),
            ('FONTNAME',  (0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,-1),8.5),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_DARK,C_PANEL]),
            ('TEXTCOLOR',(0,1),(-1,-1),C_TEXT),
            ('TEXTCOLOR',(1,1),(1,-1),C_GREEN), ('FONTNAME',(1,1),(1,-1),'Helvetica-Bold'),
            ('GRID',(0,0),(-1,-1),0.4,C_BORDER), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('LEFTPADDING',(0,0),(-1,-1),8), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ]))
        story.append(t_perf)
        story.append(Spacer(1, 0.4*cm))

        story.append(Paragraph("3. Distribusi Risiko per Plan Type", sH1))
        if 'plan_type' in df_data.columns and 'churn_proba' in df_data.columns:
            plan_rows = [['Plan Type','Total','High Risk','Medium Risk','Low Risk','Avg Prob']]
            for plan in sorted(df_data['plan_type'].unique()):
                sub = df_data[df_data['plan_type']==plan]; n = len(sub)
                plan_rows.append([
                    plan.title(), str(n),
                    f"{(sub['churn_proba']>=0.7).sum()} ({(sub['churn_proba']>=0.7).mean():.0%})",
                    f"{((sub['churn_proba']>=0.4)&(sub['churn_proba']<0.7)).sum()} ({((sub['churn_proba']>=0.4)&(sub['churn_proba']<0.7)).mean():.0%})",
                    f"{(sub['churn_proba']<0.4).sum()} ({(sub['churn_proba']<0.4).mean():.0%})",
                    f"{sub['churn_proba'].mean():.1%}",
                ])
            t_plan = Table(plan_rows, colWidths=[2.8*cm,1.8*cm,3.2*cm,3.2*cm,3.2*cm,2.8*cm])
            t_plan.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),C_PANEL), ('TEXTCOLOR',(0,0),(-1,0),C_BLUE),
                ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,-1),8.5),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_DARK,C_PANEL]), ('TEXTCOLOR',(0,1),(-1,-1),C_TEXT),
                ('GRID',(0,0),(-1,-1),0.4,C_BORDER), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('LEFTPADDING',(0,0),(-1,-1),8), ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ]))
            story.append(t_plan)
        story.append(Spacer(1, 0.4*cm))

        story.append(PageBreak())
        story.append(Paragraph("4. Top 20 Customer Berisiko Tertinggi", sH1))
        story.append(Paragraph(
            "Customer dengan probabilitas churn tertinggi. Prioritaskan untuk segera dihubungi tim Customer Success.", sBody))
        story.append(Spacer(1, 0.3*cm))

        if 'churn_proba' in df_data.columns:
            top20     = df_data.sort_values('churn_proba', ascending=False).head(20)
            cols_show = ['customer_id','churn_proba','plan_type','contract_type','tenure_days']
            cols_show = [c for c in cols_show if c in top20.columns]
            headers   = {'customer_id':'Customer ID','churn_proba':'Churn Prob','plan_type':'Plan',
                         'contract_type':'Contract','tenure_days':'Tenure (hari)'}
            rows = [[headers.get(c,c) for c in cols_show]]
            for _,r in top20.iterrows():
                row_data = []
                for c in cols_show:
                    v = r[c]
                    if c=='churn_proba':   row_data.append(f"{v:.1%}")
                    elif c=='tenure_days': row_data.append(f"{int(v)} hari")
                    else:                  row_data.append(str(v))
                rows.append(row_data)
            col_w = [17/len(cols_show)*cm]*len(cols_show)
            t_top = Table(rows, colWidths=col_w)
            t_top.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),C_PANEL), ('TEXTCOLOR',(0,0),(-1,0),C_BLUE),
                ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,-1),8),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_DARK,C_PANEL]), ('TEXTCOLOR',(0,1),(-1,-1),C_TEXT),
                ('TEXTCOLOR',(1,1),(1,-1),C_RED), ('FONTNAME',(1,1),(1,-1),'Helvetica-Bold'),
                ('GRID',(0,0),(-1,-1),0.4,C_BORDER), ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                ('LEFTPADDING',(0,0),(-1,-1),7), ('TOPPADDING',(0,0),(-1,-1),5), ('BOTTOMPADDING',(0,0),(-1,-1),5),
            ]))
            story.append(t_top)

        story.append(Spacer(1, 0.6*cm))
        story.append(Paragraph("5. Rekomendasi Tindakan", sH1))
        reco_data = [
            ['Segment','Tindakan yang Disarankan','Prioritas'],
            ['High Risk\n(≥70%)',    'Hubungi langsung dalam 48 jam. Tawarkan diskon retention,\nreview kontrak, atau dedicated support.','🔴 Segera'],
            ['Medium Risk\n(40-70%)','Kirim email nurturing & survei kepuasan. Monitor usage\nmingguan dan jadwalkan check-in bulanan.','🟡 Minggu ini'],
            ['Low Risk\n(<40%)',     'Lanjutkan program loyalty & upsell. Libatkan dalam\nbeta feature untuk meningkatkan engagement.','🟢 Rutin'],
            ['Detractor NPS',       'Eskalasi ke Customer Success Manager.\nLakukan root cause analysis tiket yang belum terselesaikan.','🔴 Segera'],
            ['Feature Adoption <30%','Jadwalkan sesi onboarding ulang.\nKirim tutorial targeted sesuai plan.','🟡 Minggu ini'],
        ]
        t_reco = Table(reco_data, colWidths=[3*cm,10.5*cm,3.5*cm])
        t_reco.setStyle(TableStyle([
            ('BACKGROUND',(0,0),(-1,0),C_PANEL), ('TEXTCOLOR',(0,0),(-1,0),C_BLUE),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'), ('FONTSIZE',(0,0),(-1,-1),8.5),
            ('ROWBACKGROUNDS',(0,1),(-1,-1),[C_DARK,C_PANEL]), ('TEXTCOLOR',(0,1),(-1,-1),C_TEXT),
            ('GRID',(0,0),(-1,-1),0.4,C_BORDER), ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('LEFTPADDING',(0,0),(-1,-1),8), ('TOPPADDING',(0,0),(-1,-1),7), ('BOTTOMPADDING',(0,0),(-1,-1),7),
        ]))
        story.append(t_reco)
        story.append(Spacer(1, 1*cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER))
        story.append(Paragraph(
            f"ChurnGuard Pro Report  ·  {now}  ·  Confidential",
            S('foot', fontSize=7, textColor=C_MUTED, alignment=TA_CENTER, spaceBefore=6)))
        doc.build(story)
        return buf.getvalue()

    # ─────────────────────────────────────────
    # SIDEBAR
    # ─────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div class="brand-bar">
            <div class="brand-logo">🛡️</div>
            <div>
                <div class="brand-name">ChurnGuard</div>
                <div class="brand-sub">Retention Intelligence</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        username = st.session_state.get('username', '—')
        st.markdown(f"""
        <div class="user-badge">
            <div class="user-badge-label">Logged in as</div>
            <div class="user-badge-name">{username}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">Navigation</div>', unsafe_allow_html=True)

        page = option_menu(
            menu_title=None,
            options=["Overview", "Prediksi Customer", "Semua Data", "Detail Customer", "Feature Importance"],
            icons=["bar-chart-fill", "search", "table", "person-fill", "graph-up-arrow"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"font-size": "16px"},
                "nav-link": {
                    "font-size": "14px", "font-weight": "600", "text-align": "left",
                    "margin": "6px 0", "padding": "12px 14px", "border-radius": "10px",
                    "background-color": "#FFFFFF", "color": "#64748B",
                    "border": "1px solid #E2E8F0", "transition": "all .2s ease",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(135deg,#2563EB,#0EA5E9)",
                    "color": "white", "border": "1px solid transparent",
                    "box-shadow": "0 4px 12px rgba(37,99,235,0.25)",
                },
            }
        )

        # ── Icon fix: inherit dari parent <a.active> ──
        st.markdown("""
        <style>
        [data-testid="stSidebar"] .nav-link.active i.icon,
        [data-testid="stSidebar"] .nav-link.active i.bi {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
        }
        [data-testid="stSidebar"] .nav-link:not(.active) i.icon,
        [data-testid="stSidebar"] .nav-link:not(.active) i.bi {
            color: #6B7280 !important;
            -webkit-text-fill-color: #6B7280 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-heading">Dataset</div>', unsafe_allow_html=True)
        if DATA_LOADED:
            total   = len(df)
            churned = int(df['churn'].sum()) if 'churn' in df.columns else 0
            st.markdown(f'<div class="alert-ok">📊 {total:,} customers loaded</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="alert-warning">⚠️ Churn aktual: {churned:,} ({churned/total*100:.1f}%)</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-critical">❌ churnguard_predictions.csv tidak ditemukan</div>', unsafe_allow_html=True)

        if saved_metrics:
            st.markdown('<div class="section-heading">Performa Model</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="accuracy-badge">
                <div style="font-family:'DM Mono',monospace;font-size:1.5rem;color:#2563EB;font-weight:500">
                    {saved_metrics.get('Accuracy',0):.1%}
                </div>
                <div style="font-size:.7rem;color:#94A3B8;text-transform:uppercase;letter-spacing:.08em">Accuracy</div>
            </div>
            <div class="accuracy-badge">
                <div style="font-family:'DM Mono',monospace;font-size:1.5rem;color:#10B981;font-weight:500">
                    {saved_metrics.get('F1-Score',0):.3f}
                </div>
                <div style="font-size:.7rem;color:#94A3B8;text-transform:uppercase;letter-spacing:.08em">F1-Score</div>
            </div>
            """, unsafe_allow_html=True)

        if DATA_LOADED:
            st.markdown('<div class="section-heading">Laporan PDF</div>', unsafe_allow_html=True)
            if st.button("📄 Generate & Download PDF", use_container_width=True):
                with st.spinner("Membuat laporan PDF..."):
                    pdf_bytes = generate_pdf_report(df, saved_metrics)
                fname = f"churnguard_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=fname,
                                   mime="application/pdf", use_container_width=True)

        st.markdown('<div class="section-heading">System Status</div>', unsafe_allow_html=True)
        if MODEL_LOADED:
            st.markdown('<div class="alert-ok">✅ churnguard_model.joblib · Active</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-critical">❌ churnguard_model.joblib · Not Found</div>', unsafe_allow_html=True)
        st.caption(f"Last refresh: {datetime.datetime.now().strftime('%H:%M:%S')}")

    # ═══════════════════════════════════════════════════════
    # PAGE 1: OVERVIEW
    # ═══════════════════════════════════════════════════════
    if page == "Overview":
        st.markdown('<div class="section-heading">📊 Overview</div>', unsafe_allow_html=True)
        st.markdown("<p class='section-header'>ringkasan performa model & distribusi data</p>", unsafe_allow_html=True)

        if not DATA_LOADED:
            st.info("Load `churnguard_predictions.csv` untuk melihat halaman ini.")
            st.stop()

        # ── KPI Cards ──
        if 'churn_proba' in df.columns:
            high_n   = (df['churn_proba'] >= 0.7).sum()
            med_n    = ((df['churn_proba'] >= 0.4) & (df['churn_proba'] < 0.7)).sum()
            low_n    = (df['churn_proba'] < 0.4).sum()
            avg_prob = df['churn_proba'].mean()
            total    = len(df)

            kpis = [
                ("#3B82F6", "Total Customer",      f"{total:,}",    "All-time data"),
                ("#EF4444", "🔴 High Risk (≥70%)", f"{high_n:,}",   f"{high_n/total*100:.1f}% dari total"),
                ("#F59E0B", "🟡 Medium Risk",       f"{med_n:,}",    f"{med_n/total*100:.1f}% dari total"),
                ("#10B981", "🟢 Low Risk",          f"{low_n:,}",    f"{low_n/total*100:.1f}% dari total"),
            ]
            cols = st.columns(4)
            for col, (accent, label, value, sub) in zip(cols, kpis):
                with col:
                    st.markdown(f"""
                    <div class="kpi-card" style="--accent:{accent}">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                        <div class="kpi-delta">{sub}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            neg_pct = high_n / total * 100
            if neg_pct >= 30:
                st.markdown(f'<div class="alert-critical">🚨 <strong>CRITICAL:</strong> {high_n:,} customer berisiko tinggi ({neg_pct:.1f}%). Segera tindak lanjuti.</div>', unsafe_allow_html=True)
            elif med_n / total * 100 >= 30:
                st.markdown(f'<div class="alert-warning">⚠️ <strong>WARNING:</strong> Proporsi medium risk cukup tinggi. Monitor secara aktif.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-ok">✅ <strong>SEHAT:</strong> Profil risiko dalam batas normal. Pertahankan kualitas layanan.</div>', unsafe_allow_html=True)

        # ── Model Performance ──
        if saved_metrics:
            st.markdown('<div class="section-heading">📐 Performa Model</div>', unsafe_allow_html=True)
            m_cols = st.columns(5)
            metric_items = [
                ("Accuracy",       saved_metrics.get('Accuracy',0), ".1%", "#2563EB"),
                ("F1-Score",       saved_metrics.get('F1-Score',0), ".3f", "#10B981"),
                ("Precision",      saved_metrics.get('Precision',0), ".3f", "#F59E0B"),
                ("Recall",         saved_metrics.get('Recall',0), ".3f", "#F59E0B"),
                ("Train-Test Gap", saved_metrics.get('Gap',0), ".4f",
                 "#10B981" if saved_metrics.get('Status','') == 'OK' else "#EF4444"),
            ]
            for col, (label, val, fmt_s, color) in zip(m_cols, metric_items):
                with col:
                    st.markdown(f"""
                    <div class="model-metric-card">
                        <div class="model-metric-label">{label}</div>
                        <div class="model-metric-value" style="color:{color}">{val:{fmt_s}}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Charts ──
        col_hist, col_bar = st.columns([1.5, 1])
        with col_hist:
            st.markdown("#### Distribusi Churn Probability")
            if 'churn_proba' in df.columns:
                fig = px.histogram(df, x='churn_proba', nbins=40,
                    color_discrete_sequence=['#2563EB'], template='plotly_white',
                    labels={'churn_proba': 'Churn Probability'})
                fig.add_vline(x=0.4, line_dash='dot', line_color='#F59E0B', annotation_text="Medium")
                fig.add_vline(x=0.7, line_dash='dot', line_color='#EF4444', annotation_text="High")
                fig.update_layout(**pl(height=300,
                    xaxis=dict(gridcolor='#E2E8F0'), yaxis=dict(gridcolor='#E2E8F0')))
                st.plotly_chart(fig, use_container_width=True)

        with col_bar:
            st.markdown("#### Churn Rate by Plan")
            if 'plan_type' in df.columns and 'churn' in df.columns:
                pc = df.groupby('plan_type')['churn'].mean().reset_index()
                pc.columns = ['Plan','Rate']
                pc['Rate %'] = pc['Rate'] * 100
                fig2 = px.bar(pc, x='Plan', y='Rate %',
                    color='Rate %', color_continuous_scale=['#10B981','#F59E0B','#EF4444'],
                    template='plotly_white', text_auto='.1f')
                fig2.update_traces(textposition='outside')
                fig2.update_layout(**pl(height=300, coloraxis_showscale=False,
                    xaxis=dict(gridcolor='#E2E8F0'), yaxis=dict(gridcolor='#E2E8F0')))
                st.plotly_chart(fig2, use_container_width=True)

        if 'tenure_days' in df.columns and 'churn_proba' in df.columns:
            st.markdown("#### Avg Churn Probability vs Tenure")
            df['tenure_bucket'] = pd.cut(df['tenure_days'],
                bins=[0,90,180,365,730,9999],
                labels=['< 3 bln','3-6 bln','6-12 bln','1-2 thn','> 2 thn'])
            tc = df.groupby('tenure_bucket', observed=True)['churn_proba'].mean().reset_index()
            fig3 = px.line(tc, x='tenure_bucket', y='churn_proba', markers=True,
                template='plotly_white', color_discrete_sequence=['#2563EB'],
                labels={'churn_proba':'Avg Churn Prob','tenure_bucket':'Tenure'})
            fig3.update_layout(**pl(height=260,
                xaxis=dict(gridcolor='#E2E8F0'), yaxis=dict(gridcolor='#E2E8F0', tickformat='.0%')))
            st.plotly_chart(fig3, use_container_width=True)

    # ═══════════════════════════════════════════════════════
    # PAGE 2: PREDIKSI
    # ═══════════════════════════════════════════════════════
    elif page == "Prediksi Customer":
        st.markdown('<div class="section-heading">🔍 Prediksi Churn Customer</div>', unsafe_allow_html=True)
        st.markdown("<p class='section-header'>masukkan data customer untuk prediksi real-time</p>", unsafe_allow_html=True)

        if not MODEL_LOADED:
            st.markdown('<div class="alert-critical">❌ Model belum di-load. Pastikan file .joblib ada di folder models/</div>', unsafe_allow_html=True)
            st.stop()

        with st.form("predict_form"):
            st.markdown("#### 📋 Informasi Akun")
            c1,c2,c3 = st.columns(3)
            with c1: plan_type     = st.selectbox("Plan Type", ['starter','professional','enterprise'])
            with c2: contract_type = st.selectbox("Contract Type", CONTRACT_CATEGORIES)
            with c3: total_users   = st.number_input("Total Users", min_value=1, value=5)
            tenure_days = st.slider("Tenure (hari)", 0, 2000, 365)

            st.markdown("#### 💳 Billing")
            c1,c2,c3 = st.columns(3)
            with c1:
                avg_payment_value  = st.number_input("Avg Payment Value", value=500.0)
                payment_delay_rate = st.slider("Payment Delay Rate", 0.0, 1.0, 0.1)
            with c2:
                total_payments = st.number_input("Total Payments", min_value=0, value=12)
                max_delay_days = st.number_input("Max Delay Days", min_value=0, value=5)
            with c3:
                dunning_rate   = st.slider("Dunning Rate", 0.0, 1.0, 0.05)
                avg_delay_days = st.number_input("Avg Delay Days", min_value=0.0, value=2.0)

            st.markdown("#### 📱 Usage")
            c1,c2,c3 = st.columns(3)
            with c1:
                avg_monthly_usage_hrs = st.number_input("Avg Monthly Usage (hrs)", value=20.0)
                min_monthly_usage_hrs = st.number_input("Min Monthly Usage (hrs)", value=5.0)
            with c2:
                max_monthly_usage_hrs = st.number_input("Max Monthly Usage (hrs)", value=40.0)
                avg_feature_adoption  = st.slider("Avg Feature Adoption (%)", 0.0, 100.0, 50.0)
            with c3:
                days_since_last_login = st.number_input("Days Since Last Login", min_value=0, value=7)

            st.markdown("#### 💬 NPS & Support")
            c1,c2,c3 = st.columns(3)
            with c1:
                avg_nps_score    = st.slider("Avg NPS Score", 0.0, 10.0, 7.0)
                latest_nps_score = st.slider("Latest NPS Score", 0.0, 10.0, 7.0)
            with c2:
                nps_category  = st.selectbox("NPS Category", ['Detractor','Passive','Promoter'])
                total_tickets = st.number_input("Total Support Tickets", min_value=0, value=2)
            with c3:
                technical_tickets = st.number_input("Technical Tickets", min_value=0, value=1)
                unresolved_ratio  = st.slider("Unresolved Ticket Ratio", 0.0, 1.0, 0.2)

            submitted = st.form_submit_button("🔮 Prediksi Sekarang", use_container_width=True)

        if submitted:
            raw_input = {
                'plan_type': plan_type, 'contract_type': contract_type, 'total_users': total_users,
                'tenure_days': tenure_days, 'total_payments': total_payments,
                'total_revenue': avg_payment_value * total_payments,
                'avg_payment_value': avg_payment_value, 'std_payment_value': avg_payment_value * 0.1,
                'payment_delay_rate': payment_delay_rate, 'max_delay_days': max_delay_days,
                'avg_delay_days': avg_delay_days, 'dunning_count': int(dunning_rate * total_payments),
                'dunning_rate': dunning_rate, 'payment_cv': 0.1,
                'late_x_dunning': payment_delay_rate * dunning_rate,
                'avg_monthly_usage_hrs': avg_monthly_usage_hrs, 'max_monthly_usage_hrs': max_monthly_usage_hrs,
                'min_monthly_usage_hrs': min_monthly_usage_hrs,
                'std_monthly_usage_hrs': (max_monthly_usage_hrs - min_monthly_usage_hrs) / 4,
                'avg_feature_adoption': avg_feature_adoption, 'min_feature_adoption': avg_feature_adoption * 0.7,
                'days_since_last_login': days_since_last_login,
                'engagement_score': avg_feature_adoption*0.4 + avg_monthly_usage_hrs*0.4 + (1/(days_since_last_login+1))*100*0.2,
                'usage_drop_ratio': 1 - (min_monthly_usage_hrs / (max_monthly_usage_hrs + 0.001)),
                'inactive_level': int(days_since_last_login > 30),
                'usage_consistency': 1 / ((max_monthly_usage_hrs - min_monthly_usage_hrs) / 4 + 1),
                'risk_score': (1-min_monthly_usage_hrs/(max_monthly_usage_hrs+0.001))*0.5 + int(days_since_last_login>30)*0.3 + (1-avg_feature_adoption/100)*0.2,
                'avg_nps_score': avg_nps_score, 'min_nps_score': avg_nps_score * 0.7,
                'latest_nps_score': latest_nps_score, 'nps_response_count': 3, 'nps_std': 1.0,
                'nps_trend': latest_nps_score - avg_nps_score, 'nps_category': nps_category,
                'total_tickets': total_tickets, 'high_priority_tickets': 0,
                'open_tickets': int(total_tickets * unresolved_ratio),
                'billing_tickets': 0, 'technical_tickets': technical_tickets,
                'unresolved_ratio': unresolved_ratio, 'high_priority_ratio': 0.0, 'billing_ticket_ratio': 0.0,
                'nps_x_adoption': avg_nps_score * avg_feature_adoption,
                'usage_x_tech_tickets': avg_monthly_usage_hrs * technical_tickets,
                'plan_x_usage': {'starter':0,'professional':1,'enterprise':2}[plan_type] * avg_monthly_usage_hrs,
                'tenure_x_engagement': tenure_days * (avg_feature_adoption*0.4 + avg_monthly_usage_hrs*0.4),
                'usage_per_tenure': avg_monthly_usage_hrs / (tenure_days / 30 + 0.01),
                'tickets_per_month': total_tickets / (tenure_days / 30 + 0.01),
            }
            try:
                X_input = encode_input(raw_input)
                proba   = model.predict_proba(X_input)[0][1]
                rl, rc, rclass = risk_info(proba)

                st.markdown("---")
                st.markdown('<div class="section-heading">Hasil Prediksi</div>', unsafe_allow_html=True)
                cg, cd = st.columns([1, 1.5])
                with cg:
                    st.plotly_chart(make_gauge(proba, rc), use_container_width=True)
                with cd:
                    st.markdown(f"""
                    <div class="{rclass}">
                        <h4 style="margin:0;color:{rc}">{rl}</h4>
                        <p style="margin:4px 0 0;color:#64748B;font-size:.85rem">
                            Probabilitas churn: <strong style="color:#0F172A;font-family:'DM Mono',monospace">{proba:.1%}</strong>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("**Signal yang terdeteksi:**")
                    sigs = []
                    if days_since_last_login > 30: sigs.append(f"⚠️ Tidak login selama {days_since_last_login} hari")
                    if payment_delay_rate > 0.3:   sigs.append(f"⚠️ Keterlambatan bayar {payment_delay_rate:.0%}")
                    if avg_feature_adoption < 30:  sigs.append(f"⚠️ Feature adoption rendah ({avg_feature_adoption:.0f}%)")
                    if nps_category == 'Detractor': sigs.append("⚠️ Customer adalah Detractor")
                    if unresolved_ratio > 0.5:     sigs.append(f"⚠️ {unresolved_ratio:.0%} tiket belum terselesaikan")
                    if tenure_days < 90:           sigs.append(f"⚠️ Customer baru ({tenure_days} hari)")
                    for s in sigs:
                        st.markdown(f'<div class="alert-warning">{s}</div>', unsafe_allow_html=True)
                    if not sigs:
                        st.markdown('<div class="alert-ok">✅ Tidak ada sinyal risiko yang menonjol</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error saat prediksi: {e}")
                st.exception(e)

    # ═══════════════════════════════════════════════════════
    # PAGE 3: SEMUA DATA
    # ═══════════════════════════════════════════════════════
    elif page == "Semua Data":
        st.markdown('<div class="section-heading">📋 Semua Data Customer</div>', unsafe_allow_html=True)
        st.markdown("<p class='section-header'>seluruh data dengan semua kolom</p>", unsafe_allow_html=True)

        if not DATA_LOADED:
            st.info("Load `churnguard_predictions.csv` untuk melihat halaman ini.")
            st.stop()

        c1,c2,c3,c4 = st.columns(4)
        with c1:
            risk_filter = st.multiselect("Risk Level",
                ['🔴 High (≥70%)', '🟡 Medium (40-70%)', '🟢 Low (<40%)'],
                default=['🔴 High (≥70%)', '🟡 Medium (40-70%)', '🟢 Low (<40%)'])
        with c2:
            plan_filter = st.multiselect("Plan", df['plan_type'].unique().tolist(),
                default=df['plan_type'].unique().tolist()) if 'plan_type' in df.columns else []
        with c3:
            contract_filter = st.multiselect("Contract", df['contract_type'].unique().tolist(),
                default=df['contract_type'].unique().tolist()) if 'contract_type' in df.columns else []
        with c4:
            search_id = st.text_input("Cari Customer ID", placeholder="ketik sebagian ID...")

        mask = pd.Series([True]*len(df), index=df.index)
        if 'churn_proba' in df.columns:
            if '🔴 High (≥70%)'     not in risk_filter: mask &= (df['churn_proba'] < 0.7)
            if '🟡 Medium (40-70%)' not in risk_filter: mask &= ~((df['churn_proba'] >= 0.4) & (df['churn_proba'] < 0.7))
            if '🟢 Low (<40%)'      not in risk_filter: mask &= (df['churn_proba'] >= 0.4)
        if plan_filter     and 'plan_type'     in df.columns: mask &= df['plan_type'].isin(plan_filter)
        if contract_filter and 'contract_type' in df.columns: mask &= df['contract_type'].isin(contract_filter)
        if search_id       and 'customer_id'   in df.columns:
            mask &= df['customer_id'].astype(str).str.contains(search_id, case=False, na=False)

        df_f = df[mask].copy()
        st.caption(f"Menampilkan {len(df_f):,} dari {len(df):,} customer")

        dd = df_f.copy()
        if 'churn_proba' in dd.columns:
            risk_values = dd['churn_proba'].apply(
                lambda x: '🔴 High' if x >= 0.7 else ('🟡 Medium' if x >= 0.4 else '🟢 Low'))
            if 'risk_level' in dd.columns:
                dd['risk_level'] = risk_values
            else:
                dd.insert(dd.columns.tolist().index('churn_proba') + 1, 'risk_level', risk_values)
            dd['churn_proba'] = dd['churn_proba'].apply(lambda x: f"{x:.1%}")
        if 'churn'      in dd.columns: dd['churn']      = dd['churn'].map({1:'✅ Yes', 0:'—'})
        if 'churn_pred' in dd.columns: dd['churn_pred'] = dd['churn_pred'].map({1:'✅ Yes', 0:'—'})

        prio  = ['customer_id','churn_proba','risk_level','churn','churn_pred','plan_type','contract_type','tenure_days']
        other = [c for c in dd.columns if c not in prio]
        st.dataframe(dd[[c for c in prio if c in dd.columns]+other],
                     use_container_width=True, height=540, hide_index=True)
        st.download_button("⬇️ Download CSV (semua kolom)",
            df_f.to_csv(index=False), "churnguard_all_data.csv", "text/csv")

    # ═══════════════════════════════════════════════════════
    # PAGE 4: DETAIL CUSTOMER
    # ═══════════════════════════════════════════════════════
    elif page == "Detail Customer":
        st.markdown('<div class="section-heading">👤 Detail Customer</div>', unsafe_allow_html=True)
        st.markdown("<p class='section-header'>profil lengkap dan analisis risiko per customer</p>", unsafe_allow_html=True)

        if not DATA_LOADED:
            st.info("Load `churnguard_predictions.csv` untuk melihat halaman ini.")
            st.stop()

        cs, csort = st.columns([2,1])
        with csort:
            sort_by = st.selectbox("Urutkan berdasarkan",
                ['Churn Prob (tertinggi)','Churn Prob (terendah)','Customer ID'])
        with cs:
            search_q = st.text_input("🔍 Filter Customer ID", placeholder="ketik sebagian ID...")

        if 'customer_id' in df.columns:
            if sort_by == 'Churn Prob (tertinggi)' and 'churn_proba' in df.columns:
                id_list = df.sort_values('churn_proba', ascending=False)['customer_id'].astype(str).tolist()
            elif sort_by == 'Churn Prob (terendah)' and 'churn_proba' in df.columns:
                id_list = df.sort_values('churn_proba', ascending=True)['customer_id'].astype(str).tolist()
            else:
                id_list = sorted(df['customer_id'].astype(str).tolist())
            if search_q: id_list = [i for i in id_list if search_q.lower() in i.lower()]
            if not id_list: st.warning("Tidak ada customer yang cocok."); st.stop()
            selected_id = st.selectbox(f"Pilih Customer ({len(id_list):,} tersedia)", id_list)
        else:
            st.warning("Kolom `customer_id` tidak ditemukan."); st.stop()

        row = df[df['customer_id'].astype(str) == str(selected_id)]
        if row.empty: st.warning(f"Customer `{selected_id}` tidak ditemukan."); st.stop()
        row = row.iloc[0]

        def _g(col, default=None): return row[col] if col in row.index else default

        proba = _g('churn_proba')
        rl, rc, rclass = risk_info(proba) if proba is not None else ("—","#64748B","risk-card-low")

        st.markdown("---")
        c1,c2,c3 = st.columns([2.2,1.2,1])
        with c1:
            st.markdown(f"### 👤 `{selected_id}`")
            pb = {'starter':'🥉 Starter','professional':'🥈 Professional','enterprise':'🥇 Enterprise'}
            st.markdown(
                f"**Plan:** {pb.get(str(_g('plan_type','')),str(_g('plan_type','—')))} &nbsp;|&nbsp; "
                f"**Contract:** {str(_g('contract_type','—')).title()} &nbsp;|&nbsp; "
                f"**Users:** {int(_g('total_users',0)) if _g('total_users') is not None else '—'}")
            t = _g('tenure_days')
            if t is not None:
                t = int(t)
                st.markdown(f"**Tenure:** {t} hari ({'~'+str(t//30)+' bulan' if t<365 else '~'+f'{t/365:.1f} tahun'})")
            actual = _g('churn'); pred = _g('churn_pred')
            if actual is not None and pred is not None:
                al = "✅ Churn" if actual==1 else "— Tidak Churn"
                plb = "✅ Churn" if pred==1   else "— Tidak Churn"
                mi = "✔️ Benar" if actual==pred else "❌ Salah prediksi"
                st.markdown(f"""
                <div class="customer-detail-box" style="margin-top:12px">
                    <span style="font-size:.72rem;color:#94A3B8;text-transform:uppercase;letter-spacing:.08em">Aktual vs Prediksi</span><br><br>
                    Aktual: <strong>{al}</strong> &nbsp;|&nbsp; Prediksi: <strong>{plb}</strong> &nbsp;|&nbsp; {mi}
                </div>
                """, unsafe_allow_html=True)
        with c2:
            if proba is not None: st.plotly_chart(make_gauge(proba, rc, height=220), use_container_width=True)
        with c3:
            if proba is not None:
                st.markdown(f"""
                <div class="{rclass}" style="margin-top:30px;text-align:center">
                    <div style="font-size:1rem;color:{rc};font-weight:700">{rl}</div>
                    <div style="font-size:2rem;color:#0F172A;font-family:'DM Mono',monospace;font-weight:500;margin-top:4px">{proba:.1%}</div>
                    <div style="font-size:.72rem;color:#94A3B8;margin-top:4px">churn probability</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('<div class="section-heading">⚠️ Signal Risiko yang Terdeteksi</div>', unsafe_allow_html=True)
        sigs = []
        if (_g('days_since_last_login') or 0) > 30:
            sigs.append(f"Tidak login selama <strong>{int(_g('days_since_last_login',0))} hari</strong>")
        if (_g('payment_delay_rate') or 0) > 0.3:
            sigs.append(f"Keterlambatan bayar <strong>{_g('payment_delay_rate',0):.0%}</strong>")
        if (_g('avg_feature_adoption') or 100) < 30:
            sigs.append(f"Feature adoption sangat rendah (<strong>{_g('avg_feature_adoption',0):.1f}%</strong>)")
        if str(_g('nps_category','')).lower() == 'detractor':
            sigs.append("Customer adalah <strong>Detractor</strong> (NPS rendah)")
        if (_g('unresolved_ratio') or 0) > 0.5:
            sigs.append(f"<strong>{_g('unresolved_ratio',0):.0%}</strong> tiket belum terselesaikan")
        if 0 < (_g('tenure_days') or 999) < 90:
            sigs.append(f"Customer baru (<strong>{int(_g('tenure_days',0))} hari</strong>)")
        if (_g('dunning_rate') or 0) > 0.2:
            sigs.append(f"Dunning rate tinggi (<strong>{_g('dunning_rate',0):.0%}</strong>)")
        if (_g('nps_trend') or 0) < -1:
            sigs.append(f"NPS menurun (trend: <strong>{_g('nps_trend',0):.1f}</strong>)")

        if sigs:
            sc = st.columns(2)
            for i, s in enumerate(sigs):
                with sc[i%2]:
                    st.markdown(f'<div class="risk-card-medium">⚠️ {s}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-ok">✅ Tidak ada sinyal risiko yang menonjol</div>', unsafe_allow_html=True)

        st.markdown("---")
        tb, tu, tn, tt, tr = st.tabs([
            "💳 Billing", "📱 Usage", "💬 NPS", "🎫 Support Tickets", "🗂️ Semua Kolom"])

        def mrow(items):
            cols = st.columns(len(items))
            for col,(label,val) in zip(cols,items): col.metric(label,val)

        with tb:
            st.markdown("<p class='section-header'>data pembayaran & tagihan</p>", unsafe_allow_html=True)
            mrow([("Total Payments",    fmt(_g('total_payments'),'.0f')),
                  ("Total Revenue",     fmt(_g('total_revenue'),',.0f',prefix='$')),
                  ("Avg Payment Value", fmt(_g('avg_payment_value'),',.0f',prefix='$'))])
            mrow([("Payment Delay Rate", fmt(_g('payment_delay_rate'),'.1%')),
                  ("Avg Delay Days",     fmt(_g('avg_delay_days'),'.1f',suffix=' hari')),
                  ("Max Delay Days",     fmt(_g('max_delay_days'),'.0f',suffix=' hari'))])
            mrow([("Dunning Count", fmt(_g('dunning_count'),'.0f')),
                  ("Dunning Rate",  fmt(_g('dunning_rate'),'.1%')),
                  ("Payment CV",    fmt(_g('payment_cv'),'.3f'))])
        with tu:
            st.markdown("<p class='section-header'>pola penggunaan produk</p>", unsafe_allow_html=True)
            mrow([("Avg Monthly Usage", fmt(_g('avg_monthly_usage_hrs'),'.1f',suffix=' hrs')),
                  ("Min Monthly Usage", fmt(_g('min_monthly_usage_hrs'),'.1f',suffix=' hrs')),
                  ("Max Monthly Usage", fmt(_g('max_monthly_usage_hrs'),'.1f',suffix=' hrs'))])
            mrow([("Avg Feature Adoption", fmt(_g('avg_feature_adoption'),'.1f',suffix='%')),
                  ("Days Since Last Login", fmt(_g('days_since_last_login'),'.0f',suffix=' hari')),
                  ("Usage Drop Ratio",      fmt(_g('usage_drop_ratio'),'.1%'))])
            mrow([("Engagement Score", fmt(_g('engagement_score'),'.2f')),
                  ("Usage per Tenure", fmt(_g('usage_per_tenure'),'.2f')),
                  ("Inactive Level",   "Ya ⚠️" if _g('inactive_level')==1 else "Tidak ✅")])
        with tn:
            st.markdown("<p class='section-header'>net promoter score & sentimen</p>", unsafe_allow_html=True)
            nc  = str(_g('nps_category','—'))
            ncc = {'Promoter':'#10B981','Passive':'#F59E0B','Detractor':'#EF4444'}.get(nc,'#94A3B8')
            st.markdown(f"**NPS Category:** <span style='color:{ncc};font-weight:700;font-size:1.1rem'>{nc}</span>", unsafe_allow_html=True)
            mrow([("Avg NPS Score",    fmt(_g('avg_nps_score'),'.1f',suffix=' / 10')),
                  ("Latest NPS Score", fmt(_g('latest_nps_score'),'.1f',suffix=' / 10')),
                  ("Min NPS Score",    fmt(_g('min_nps_score'),'.1f',suffix=' / 10'))])
            mrow([("NPS Trend",          fmt(_g('nps_trend'),'+.2f')),
                  ("NPS Std Dev",        fmt(_g('nps_std'),'.2f')),
                  ("NPS Response Count", fmt(_g('nps_response_count'),'.0f'))])
        with tt:
            st.markdown("<p class='section-header'>support ticket & prioritas</p>", unsafe_allow_html=True)
            mrow([("Total Tickets",     fmt(_g('total_tickets'),'.0f')),
                  ("Open (Unresolved)", fmt(_g('open_tickets'),'.0f')),
                  ("Unresolved Ratio",  fmt(_g('unresolved_ratio'),'.1%'))])
            mrow([("Technical Tickets",     fmt(_g('technical_tickets'),'.0f')),
                  ("Billing Tickets",       fmt(_g('billing_tickets'),'.0f')),
                  ("High Priority Tickets", fmt(_g('high_priority_tickets'),'.0f'))])
            mrow([("High Priority Ratio",  fmt(_g('high_priority_ratio'),'.1%')),
                  ("Billing Ticket Ratio", fmt(_g('billing_ticket_ratio'),'.1%')),
                  ("Tickets per Month",    fmt(_g('tickets_per_month'),'.2f'))])
        with tr:
            st.markdown("<p class='section-header'>seluruh kolom data mentah</p>", unsafe_allow_html=True)
            raw_df = row.to_frame(name='Nilai').reset_index()
            raw_df.columns = ['Kolom','Nilai']
            st.dataframe(raw_df, use_container_width=True, height=520)

    # ═══════════════════════════════════════════════════════
    # PAGE 5: FEATURE IMPORTANCE
    # ═══════════════════════════════════════════════════════
    elif page == "Feature Importance":
        st.markdown('<div class="section-heading">📈 Feature Importance</div>', unsafe_allow_html=True)
        st.markdown("<p class='section-header'>fitur yang paling mempengaruhi prediksi model</p>", unsafe_allow_html=True)

        if not MODEL_LOADED:
            st.markdown('<div class="alert-critical">❌ Model belum di-load.</div>', unsafe_allow_html=True)
            st.stop()

        try:
            importances = model.named_steps['clf'].feature_importances_
            fi = pd.DataFrame({'Feature': list(forward_features), 'Importance': importances}
                              ).sort_values('Importance', ascending=True)
            top_n = st.slider("Tampilkan Top N Fitur", 5, len(fi), min(20, len(fi)))
            fis   = fi.tail(top_n)

            fig = go.Figure(go.Bar(
                x=fis['Importance'], y=fis['Feature'], orientation='h',
                marker=dict(
                    color=fis['Importance'],
                    colorscale=[[0,'#DBEAFE'],[0.5,'#2563EB'],[1,'#1E3A8A']]
                )
            ))
            fig.update_layout(**pl(
                height=max(400, top_n * 28),
                xaxis=dict(gridcolor='#E2E8F0', title='Importance Score'),
                yaxis=dict(gridcolor='#E2E8F0'),
            ))
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div class="section-heading">Tabel Detail</div>', unsafe_allow_html=True)
            fit = fi.sort_values('Importance', ascending=False).copy()
            fit['Rank']       = range(1, len(fit)+1)
            fit['Importance'] = fit['Importance'].apply(lambda x: f"{x:.4f}")
            st.dataframe(fit[['Rank','Feature','Importance']], use_container_width=True, hide_index=True)

        except Exception as e:
            st.error(f"Gagal mengambil feature importance: {e}")
            st.info("Pastikan model pipeline memiliki named step 'clf' dengan `feature_importances_`.")