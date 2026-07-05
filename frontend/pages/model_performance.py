import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Model Performance", page_icon="📊", layout="wide")

API_URL = "https://your-backend.onrender.com"   # <-- update after deploying backend

st.title("📊 Model Performance")
st.markdown(
    "Comprehensive evaluation of all three tuned models on the held-out test set (10,508 subjects). "
    "XGBoost is the primary model; Logistic Regression and Random Forest are comparison baselines."
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Load metrics from API
# ---------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_metrics():
    resp = requests.get(f"{API_URL}/metrics", timeout=30)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

try:
    metrics_df = load_metrics()
except Exception as e:
    st.error(f"Could not load metrics from API: {e}")
    st.stop()

# ---------------------------------------------------------------------------
# Section 1 — Model comparison table
# ---------------------------------------------------------------------------
st.subheader("Model Comparison — All Three Tuned Models")

# Style the dataframe
def highlight_best(df):
    styled = df.style
    for col in ["ROC-AUC", "PR-AUC", "F1 (0.5)", "F1 (optimal)"]:
        if col in df.columns:
            max_val = df[col].max()
            styled = styled.apply(
                lambda s, c=col: [
                    "background-color: #d5f5e3; font-weight: bold" if v == max_val else ""
                    for v in s
                ],
                subset=[col],
            )
    for col in ["Brier Score"]:
        if col in df.columns:
            min_val = df[col].min()
            styled = styled.apply(
                lambda s, c=col: [
                    "background-color: #d5f5e3; font-weight: bold" if v == min_val else ""
                    for v in s
                ],
                subset=[col],
            )
    return styled

st.dataframe(
    highlight_best(metrics_df.set_index("Model")),
    use_container_width=True,
)
st.caption("Green = best value in each column. Brier Score: lower is better. All others: higher is better.")

# ---------------------------------------------------------------------------
# Section 2 — Metric comparison bar charts
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Visual Comparison")

metric_cols = ["ROC-AUC", "PR-AUC", "F1 (0.5)", "F1 (optimal)"]
available   = [c for c in metric_cols if c in metrics_df.columns]

colors = ["#2471a3", "#1abc9c", "#e67e22"]

col1, col2 = st.columns(2)
for i, metric in enumerate(available):
    fig = go.Figure()
    for j, row in metrics_df.iterrows():
        fig.add_trace(go.Bar(
            name=row["Model"],
            x=[row["Model"]],
            y=[row[metric]],
            marker_color=colors[j % len(colors)],
            text=[f"{row[metric]:.4f}"],
            textposition="outside",
            showlegend=(i == 0),
        ))
    fig.update_layout(
        title=metric,
        yaxis=dict(range=[0.6, 0.82]),
        height=320,
        margin=dict(t=50, b=40, l=40, r=20),
        barmode="group",
    )
    if i % 2 == 0:
        col1.plotly_chart(fig, use_container_width=True)
    else:
        col2.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Section 3 — Performance interpretation
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Performance Interpretation")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("XGBoost ROC-AUC", "0.7306", delta="+0.006 vs baseline")
    st.markdown(
        "**ROC-AUC of 0.73** on purely non-medical variables is competitive. "
        "Studies using full clinical NACC data typically achieve 0.80–0.90 — "
        "the gap represents the cost of the non-medical constraint, which is "
        "the point of this project."
    )
with c2:
    st.metric("Optimal Threshold", "0.397", delta="vs default 0.5")
    st.markdown(
        "Lowering the threshold to **0.397** increases recall to 0.87 — "
        "the model catches 87% of at-risk subjects. For a screening tool, "
        "high recall is more important than high precision: missing a true "
        "at-risk person is worse than a false alarm."
    )
with c3:
    st.metric("Brier Score", "0.2081", delta="-0.04 vs random (0.25)")
    st.markdown(
        "Brier score of **0.208** confirms the model produces well-calibrated "
        "probability estimates, not just ordinal rankings. This matters when "
        "the output is interpreted as a risk percentage."
    )

st.markdown("---")
st.subheader("Why Three Models?")
st.markdown("""
Training multiple model families is standard practice in ML — each makes different 
assumptions about the data:

- **Logistic Regression** assumes linear relationships between features and log-odds. 
  Its near-identical performance before and after tuning confirms the data has 
  a strong linear component. The L1 penalty (selected by tuning) performs implicit 
  feature selection by zeroing out weak coefficients.

- **Random Forest** showed the largest improvement from tuning (+0.039 ROC-AUC). 
  The default unconstrained trees overfitted badly; constraining depth and 
  minimum leaf size recovered substantial generalisation.

- **XGBoost** was the strongest model throughout — gradient boosting's sequential 
  error correction suits tabular demographic data better than a single ensemble 
  of independent trees.
""")