import streamlit as st

st.set_page_config(
    page_title="Dementia Risk Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Config — update API_URL to your deployed Render backend URL
# ---------------------------------------------------------------------------
API_URL = "https://swetha2003-dementia-risk-api.hf.space"   # <-- update after deploying backend

import requests
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.sidebar.title("🧠 Dementia Risk Predictor")
st.sidebar.markdown(
    "This tool predicts dementia risk using only **non-medical variables** "
    "(demographics, lifestyle, social engagement) — no clinical tests required."
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Model:** XGBoost (tuned)")
st.sidebar.markdown("**Dataset:** NACC Uniform Data Set")
st.sidebar.markdown("**Subjects:** 52,537 baseline visits")
st.sidebar.markdown("**Test ROC-AUC:** 0.7306")

# ---------------------------------------------------------------------------
# Page: Risk Predictor
# ---------------------------------------------------------------------------
st.title("🧠 Dementia Risk Predictor")
st.markdown(
    "Enter the subject's information below. The model will estimate their "
    "probability of being at risk for dementia based on non-medical factors only."
)
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Demographics")
    birthyr   = st.number_input("Birth Year", min_value=1880, max_value=2010, value=1945)
    #naccageb  = st.number_input("Age at Baseline Visit", min_value=0, max_value=120, value=75)
    import datetime

    naccageb = datetime.datetime.now().year - birthyr  # derived from birth year
    sex       = st.selectbox("Sex", options=[1, 2], format_func=lambda x: "Male" if x == 1 else "Female")
    #hispanic  = st.selectbox("Hispanic/Latino", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    hispanic = 0  # default: Non-Hispanic
    race      = st.selectbox("Primary Race", options=[1, 2, 3, 4, 5, 50],
                              format_func=lambda x: {1:"White", 2:"Black/African American",
                                                     3:"American Indian/Alaska Native",
                                                     4:"Native Hawaiian/Pacific Islander",
                                                     5:"Asian", 50:"More than one race"}[x])
    primlang  = st.selectbox("Primary Language", options=[1, 2, 3, 4, 5, 6],
                              format_func=lambda x: {1:"English", 2:"Spanish", 3:"Mandarin/Cantonese",
                                                     4:"Russian", 5:"Japanese", 6:"Other"}[x])
    handed    = st.selectbox("Handedness", options=[1, 2, 3],
                              format_func=lambda x: {1:"Right", 2:"Left", 3:"Ambidextrous"}[x])
    educ      = st.slider("Years of Education", min_value=0, max_value=36, value=16)

with col2:
    st.subheader("Social & Living")
    maristat  = st.selectbox("Marital Status", options=[1, 2, 3, 4, 5, 6],
                              format_func=lambda x: {1:"Married", 2:"Widowed", 3:"Divorced",
                                                     4:"Separated", 5:"Never married",
                                                     6:"Living with partner"}[x])
    nacclivs  = st.selectbox("Living Situation", options=[1, 2, 3, 4, 5],
                              format_func=lambda x: {1:"Lives alone", 2:"With spouse/partner",
                                                     3:"With relatives", 4:"With non-relatives",
                                                     5:"Assisted living / memory care"}[x])
    residenc  = st.selectbox("Residence Type", options=[1, 2, 3, 4],
                              format_func=lambda x: {1:"Single/multi-family home",
                                                     2:"Retirement community",
                                                     3:"Assisted living",
                                                     4:"Skilled nursing facility"}[x])
    inrelto   = st.selectbox("Co-participant Relationship", options=[1, 2, 3, 4, 5, 6, 7],
                              format_func=lambda x: {1:"Spouse/partner", 2:"Child", 3:"Sibling",
                                                     4:"Other relative", 5:"Paid caregiver",
                                                     6:"Friend", 7:"Other"}[x])
    inlivwth  = st.selectbox("Co-participant Lives With Subject", options=[0, 1],
                              format_func=lambda x: "No" if x == 0 else "Yes")
    invisits  = st.selectbox("How often does your closest contact visit you in person?", options=[1, 2, 3, 4, 5, 6, 7],
                              format_func=lambda x: {1:"Daily", 2:"≥3x/week", 3:"Weekly",
                                                     4:"≥3x/month", 5:"Monthly",
                                                     6:"<Monthly", 7:"Lives with subject"}[x])
    incalls   = st.selectbox("Phone Call Frequency", options=[1, 2, 3, 4, 5, 6, 7],
                              format_func=lambda x: {1:"Daily", 2:"≥3x/week", 3:"Weekly",
                                                     4:"≥3x/month", 5:"Monthly",
                                                     6:"<Monthly", 7:"Lives with subject"}[x])

with col3:
    st.subheader("Lifestyle / Smoking")
    never_smoked = st.selectbox("Never Smoked", options=[1, 0],
                                 format_func=lambda x: "Yes (never smoked)" if x == 1 else "No (has smoked)")
    if never_smoked == 0:
        tobac30   = st.selectbox("Smoked in Last 30 Days", options=[0, 1],
                                  format_func=lambda x: "No" if x == 0 else "Yes")
        tobac100  = st.selectbox("Smoked 100+ Cigarettes Lifetime", options=[0, 1],
                                  format_func=lambda x: "No" if x == 0 else "Yes")
        smokyrs   = st.slider("Years Smoked", min_value=0, max_value=80, value=10)
        packsper  = st.selectbox("Average Packs Per Day", options=[0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
                                  format_func=lambda x: f"{x} pack(s)/day")
    else:
        tobac30  = 0
        tobac100 = 0
        smokyrs  = 0
        packsper = 0.0
        st.info("Smoking fields not applicable for never-smokers.")

st.markdown("---")

# ---------------------------------------------------------------------------
# Predict button
# ---------------------------------------------------------------------------
if st.button("🔍 Predict Dementia Risk", use_container_width=True, type="primary"):
    payload = {
        "BIRTHYR": birthyr, "NACCAGEB": naccageb, "SEX": sex,
        "HISPANIC": hispanic, "EDUC": educ, "RACE": race,
        "PRIMLANG": primlang, "HANDED": handed, "MARISTAT": maristat,
        "NACCLIVS": nacclivs, "RESIDENC": residenc, "INRELTO": inrelto,
        "INLIVWTH": inlivwth, "INVISITS": invisits, "INCALLS": incalls,
        "NEVER_SMOKED": never_smoked, "TOBAC30": tobac30, "TOBAC100": tobac100,
        "SMOKYRS": smokyrs, "PACKSPER": packsper,
    }

    with st.spinner("Computing risk score..."):
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

    # --- Result ---
    risk_pct = pred["risk_percent"]
    label    = pred["risk_label"]
    color    = "#e74c3c" if pred["prediction"] == 1 else "#2ecc71"

    res_col1, res_col2 = st.columns([1, 2])

    with res_col1:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_pct,
            title={"text": f"Dementia Risk Score<br><span style='color:{color};font-size:1.2em'><b>{label}</b></span>"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar":  {"color": color},
                "steps": [
                    {"range": [0, 40],  "color": "#d5f5e3"},
                    {"range": [40, 65], "color": "#fdebd0"},
                    {"range": [65, 100],"color": "#fadbd8"},
                ],
                "threshold": {"line": {"color": "black", "width": 3}, "value": 39.7},
            },
            number={"suffix": "%"},
        ))
        fig.update_layout(height=300, margin=dict(t=60, b=10, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

    with res_col2:
        st.markdown("#### What drove this prediction?")
        contribs = expl["contributions"][:10]
        features = [c["feature"] for c in contribs]
        values   = [c["shap_value"] for c in contribs]
        colors_bar = ["#e74c3c" if v > 0 else "#2ecc71" for v in values]

        fig2 = go.Figure(go.Bar(
            x=values, y=features,
            orientation="h",
            marker_color=colors_bar,
            text=[f"{v:+.3f}" for v in values],
            textposition="outside",
        ))
        fig2.update_layout(
            title="Top 10 Feature Contributions (SHAP)",
            xaxis_title="SHAP value (→ increases risk, ← decreases risk)",
            yaxis={"autorange": "reversed"},
            height=380,
            margin=dict(t=50, b=40, l=160, r=60),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown(
        f"> **Interpretation:** The model assigns this subject a **{risk_pct}% probability** "
        f"of being at risk for dementia. The threshold for classification is 39.7% (optimised for recall). "
        f"Red bars increase risk; green bars decrease it."
    )