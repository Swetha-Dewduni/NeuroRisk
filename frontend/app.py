import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from styles import inject_styles, hero, section_header, metric_card, info_card, divider

st.set_page_config(
    page_title="NeuroRisk — Dementia Risk Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_styles()

API_URL = "https://swetha2003-dementia-risk-api.hf.space"

import requests
import plotly.graph_objects as go

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <div style='font-size:3rem'>🧠</div>
        <div style='font-size:1.1rem; font-weight:700; color:white;'>NeuroRisk</div>
        <div style='font-size:0.78rem; color:rgba(255,255,255,0.5); margin-top:0.2rem;'>Dementia Risk Predictor</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Model:** XGBoost (tuned)")
    st.markdown("**Dataset:** NACC UDS · 52,537 subjects")
    st.markdown("**Test ROC-AUC:** 0.7306")
    st.markdown("**Threshold:** 39.7% (optimised)")
    st.markdown("---")
    st.caption("⚠️ For educational use only. Not a clinical diagnostic tool.")

# Hero
hero(
    "🧠 Dementia Risk Predictor",
    "Fill in the details below to get a personalised dementia risk score based on lifestyle and social factors — no medical history needed.",
    badges=["Non-Medical Only", "XGBoost · ROC-AUC 0.73", "52,537 Subjects"]
)

# Input form
st.markdown("### Enter Your Information")
col1, col2, col3 = st.columns(3)

with col1:
    section_header("Demographics")
    birthyr  = st.number_input("Birth Year", min_value=1880, max_value=2010, value=1945)
    import datetime
    naccageb = datetime.datetime.now().year - birthyr
    sex      = st.selectbox("Sex", options=[1, 2],
                             format_func=lambda x: "Male" if x == 1 else "Female")
    race     = st.selectbox("Race", options=[1, 2, 3, 4, 5, 50],
                             format_func=lambda x: {1:"White", 2:"Black/African American",
                                                    3:"American Indian/Alaska Native",
                                                    4:"Native Hawaiian/Pacific Islander",
                                                    5:"Asian", 50:"More than one race"}[x])
    educ     = st.slider("Years of Education", min_value=0, max_value=36, value=16)
    hispanic = 0
    primlang = 1
    handed   = 1

with col2:
    section_header("Social & Living")
    maristat = st.selectbox("Marital Status", options=[1, 2, 3, 4, 5, 6],
                             format_func=lambda x: {1:"Married", 2:"Widowed", 3:"Divorced",
                                                    4:"Separated", 5:"Never married",
                                                    6:"Living with partner"}[x])
    nacclivs = st.selectbox("Living Situation", options=[1, 2, 3, 4, 5],
                             format_func=lambda x: {1:"Lives alone", 2:"With spouse/partner",
                                                    3:"With relatives", 4:"With non-relatives",
                                                    5:"Assisted living / memory care"}[x])
    residenc = st.selectbox("Residence Type", options=[1, 2, 3, 4],
                             format_func=lambda x: {1:"Single/multi-family home",
                                                    2:"Retirement community",
                                                    3:"Assisted living",
                                                    4:"Skilled nursing facility"}[x])
    inrelto  = st.selectbox("Relationship to closest contact", options=[1, 2, 3, 4, 5, 6, 7],
                             format_func=lambda x: {1:"Spouse/partner", 2:"Child", 3:"Sibling",
                                                    4:"Other relative", 5:"Paid caregiver",
                                                    6:"Friend", 7:"Other"}[x])
    inlivwth = st.selectbox("Does this person live with you?", options=[0, 1],
                             format_func=lambda x: "No" if x == 0 else "Yes")
    invisits = st.selectbox("How often do you see this person in person?",
                             options=[1, 2, 3, 4, 5, 6, 7],
                             format_func=lambda x: {1:"Daily", 2:"≥3x/week", 3:"Weekly",
                                                    4:"≥3x/month", 5:"Monthly",
                                                    6:"<Monthly", 7:"We live together"}[x])
    incalls  = st.selectbox("How often do you speak on the phone with this person?",
                             options=[1, 2, 3, 4, 5, 6, 7],
                             format_func=lambda x: {1:"Daily", 2:"≥3x/week", 3:"Weekly",
                                                    4:"≥3x/month", 5:"Monthly",
                                                    6:"<Monthly", 7:"We live together"}[x])

with col3:
    section_header("Lifestyle & Smoking")
    never_smoked = st.selectbox("Have you ever smoked?", options=[1, 0],
                                 format_func=lambda x: "No — never smoked" if x == 1 else "Yes — I have smoked")
    if never_smoked == 0:
        tobac30  = st.selectbox("Smoked in last 30 days?", options=[0, 1],
                                 format_func=lambda x: "No" if x == 0 else "Yes")
        tobac100 = st.selectbox("Smoked 100+ cigarettes lifetime?", options=[0, 1],
                                 format_func=lambda x: "No" if x == 0 else "Yes")
        smokyrs  = st.slider("Years smoked", min_value=0, max_value=80, value=10)
        packsper = st.selectbox("Average packs per day", options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
                                 format_func=lambda x: f"{x} pack(s)/day")
    else:
        tobac30 = tobac100 = 0
        smokyrs = 0
        packsper = 0.0
        info_card("Smoking fields not applicable — skipped for never-smokers.", kind="success")

divider()

# Predict button
if st.button("🔍 Predict My Dementia Risk", use_container_width=True, type="primary"):
    payload = {
        "BIRTHYR": birthyr, "NACCAGEB": naccageb, "SEX": sex,
        "HISPANIC": hispanic, "EDUC": educ, "RACE": race,
        "PRIMLANG": primlang, "HANDED": handed, "MARISTAT": maristat,
        "NACCLIVS": nacclivs, "RESIDENC": residenc, "INRELTO": inrelto,
        "INLIVWTH": inlivwth, "INVISITS": invisits, "INCALLS": incalls,
        "NEVER_SMOKED": never_smoked, "TOBAC30": tobac30, "TOBAC100": tobac100,
        "SMOKYRS": smokyrs, "PACKSPER": packsper,
    }

    with st.spinner("Calculating your risk score..."):
        try:
            pred_resp = requests.post(f"{API_URL}/predict", json=payload, timeout=30)
            expl_resp = requests.post(f"{API_URL}/explain", json=payload, timeout=60)
            pred_resp.raise_for_status()
            expl_resp.raise_for_status()
            pred = pred_resp.json()
            expl = expl_resp.json()
        except Exception as e:
            st.error(f"API error: {e}")
            st.stop()

    risk_pct = pred["risk_percent"]
    label    = pred["risk_label"]
    color    = "#ef4444" if pred["prediction"] == 1 else "#34d399"

    st.markdown("---")
    st.markdown("### Your Results")

    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        # Risk gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            title={"text": f"<b style='color:{color}'>{label}</b>",
                   "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1,
                         "tickcolor": "rgba(255,255,255,0.3)"},
                "bar":  {"color": color, "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 39.7], "color": "rgba(52,211,153,0.15)"},
                    {"range": [39.7, 100], "color": "rgba(239,68,68,0.15)"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 2},
                    "thickness": 0.75,
                    "value": 39.7
                },
            },
            number={"suffix": "%", "font": {"size": 36, "color": color}},
        ))
        fig.update_layout(
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=50, b=10, l=20, r=20),
            font={"color": "white"},
        )
        st.plotly_chart(fig, use_container_width=True)

        # Key metrics below gauge
        m1, m2 = st.columns(2)
        with m1:
            metric_card(f"{risk_pct}%", "Risk Score")
        with m2:
            metric_card("39.7%", "Threshold")

    with res_col2:
        st.markdown("#### What drove this prediction?")
        contribs = expl["contributions"][:10]
        features = [c["feature"] for c in contribs]
        values   = [c["shap_value"] for c in contribs]
        colors_bar = ["#ef4444" if v > 0 else "#34d399" for v in values]

        fig2 = go.Figure(go.Bar(
            x=values, y=features,
            orientation="h",
            marker_color=colors_bar,
            text=[f"{v:+.3f}" for v in values],
            textposition="outside",
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="← Decreases risk | Increases risk →",
            xaxis={"color": "rgba(255,255,255,0.6)", "gridcolor": "rgba(255,255,255,0.1)"},
            yaxis={"autorange": "reversed", "color": "rgba(255,255,255,0.8)"},
            font={"color": "white"},
            height=360,
            margin=dict(t=20, b=50, l=150, r=80),
        )
        st.plotly_chart(fig2, use_container_width=True)

    info_card(
        f"<b>How to read this:</b> Your model assigns a <b>{risk_pct}% probability</b> of being "
        f"at risk for dementia based on your non-medical profile. "
        f"Red bars push risk up; green bars push it down. "
        f"The threshold is 39.7% — scores above this are classified as At Risk.",
        kind="info"
    )