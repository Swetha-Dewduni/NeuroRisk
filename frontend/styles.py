import streamlit as st

def inject_styles():
    st.markdown("""
    <style>
    /* ── Hide default Streamlit header padding ── */
    .block-container { padding-top: 1.5rem !important; }

    /* ── Hero banner ── */
    .hero {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero h1 {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem;
    }
    .hero p {
        color: rgba(255,255,255,0.75) !important;
        font-size: 1rem;
        margin: 0;
    }
    .hero .badge {
        display: inline-block;
        background: rgba(99,102,241,0.3);
        border: 1px solid rgba(99,102,241,0.5);
        color: #a5b4fc;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.78rem;
        margin-right: 0.4rem;
        margin-bottom: 0.8rem;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 12px;
        padding: 1.2rem 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #818cf8;
        line-height: 1.1;
    }
    .metric-card .metric-label {
        font-size: 0.82rem;
        color: rgba(255,255,255,0.55);
        margin-top: 0.3rem;
    }
    .metric-card .metric-delta {
        font-size: 0.78rem;
        color: #34d399;
        margin-top: 0.2rem;
    }

    /* ── Section header with accent ── */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.5rem 0 0.8rem 0;
    }
    .section-header .accent-bar {
        width: 4px;
        height: 28px;
        background: linear-gradient(180deg, #6366f1, #8b5cf6);
        border-radius: 2px;
        flex-shrink: 0;
    }
    .section-header h3 {
        margin: 0 !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: inherit;
    }

    /* ── Info cards ── */
    .info-card {
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.25);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .warning-card {
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.25);
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .success-card {
        background: rgba(52,211,153,0.08);
        border: 1px solid rgba(52,211,153,0.25);
        border-left: 4px solid #34d399;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }
    .danger-card {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.25);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }

    /* ── Feature tag pills ── */
    .tag {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.3);
        color: #a5b4fc;
        padding: 0.15rem 0.6rem;
        border-radius: 12px;
        font-size: 0.78rem;
        margin: 0.15rem;
    }

    /* ── Result gauge container ── */
    .result-container {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid rgba(99,102,241,0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* ── Divider ── */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent);
        margin: 1.5rem 0;
        border: none;
    }

    /* ── Stage cards ── */
    .stage-card {
        border-radius: 12px;
        padding: 1.2rem;
        height: 100%;
        margin-bottom: 0.5rem;
    }
    .stage-mild { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.3); }
    .stage-moderate { background: rgba(249,115,22,0.08); border: 1px solid rgba(249,115,22,0.3); }
    .stage-severe { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.3); }

    /* ── Sidebar improvement ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%) !important;
    }
    [data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }

    /* ── Button styling ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: opacity 0.2s !important;
    }
    .stButton > button:hover { opacity: 0.9 !important; }

    /* ── Form input styling ── */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def hero(title, subtitle, badges=None):
    badge_html = ""
    if badges:
        badge_html = "".join([f'<span class="badge">{b}</span>' for b in badges])
    st.markdown(f"""
    <div class="hero">
        {badge_html}
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def section_header(title):
    st.markdown(f"""
    <div class="section-header">
        <div class="accent-bar"></div>
        <h3>{title}</h3>
    </div>
    """, unsafe_allow_html=True)


def metric_card(value, label, delta=None):
    delta_html = f'<div class="metric-delta">↑ {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def info_card(text, kind="info"):
    css_class = {"info": "info-card", "warning": "warning-card",
                 "success": "success-card", "danger": "danger-card"}.get(kind, "info-card")
    st.markdown(f'<div class="{css_class}">{text}</div>', unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)