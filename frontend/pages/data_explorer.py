import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import os

st.set_page_config(page_title="Data Explorer", page_icon="📈", layout="wide")

st.title("📈 Data Explorer")
st.markdown(
    "Explore the distributions of key non-medical features in the training dataset, "
    "broken down by dementia risk class. Based on 52,537 baseline visits from the "
    "NACC Uniform Data Set."
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Load the processed dataset
# Note: for deployment, store step2_final_clean.csv in frontend/data/
# ---------------------------------------------------------------------------
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "step3_full.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Risk Class"] = df["dementia_binary"].map({0: "Not at Risk", 1: "At Risk"})
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "Dataset file not found. Copy `step2_final_clean.csv` to `frontend/data/` "
        "before deploying."
    )
    st.stop()

RISK_COLORS = {"Not at Risk": "#2ecc71", "At Risk": "#e74c3c"}

# ---------------------------------------------------------------------------
# Section 1 — Dataset overview
# ---------------------------------------------------------------------------
st.subheader("Dataset Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Subjects",  f"{len(df):,}")
col2.metric("At Risk",         f"{df['dementia_binary'].sum():,}", delta=f"{df['dementia_binary'].mean()*100:.1f}%")
col3.metric("Not at Risk",     f"{(1-df['dementia_binary']).sum():,}", delta=f"{(1-df['dementia_binary']).mean()*100:.1f}%")
col4.metric("Features Used",   "21 non-medical variables")

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 2 — Age distribution
# ---------------------------------------------------------------------------
st.subheader("Age at Baseline by Risk Class")

fig = go.Figure()
for label, color in RISK_COLORS.items():
    subset = df[df["Risk Class"] == label]["NACCAGEB"].dropna()
    fig.add_trace(go.Histogram(
        x=subset, name=label, opacity=0.7,
        marker_color=color, nbinsx=40,
        histnorm="probability density",
    ))
fig.update_layout(
    barmode="overlay",
    xaxis_title="Age at Baseline Visit",
    yaxis_title="Density",
    height=380,
    legend=dict(x=0.02, y=0.98),
)
st.plotly_chart(fig, use_container_width=True)
st.caption(
    f"At-risk subjects: mean age {df[df['dementia_binary']==1]['NACCAGEB'].mean():.1f} | "
    f"Not-at-risk: mean age {df[df['dementia_binary']==0]['NACCAGEB'].mean():.1f}"
)

# ---------------------------------------------------------------------------
# Section 3 — Education distribution
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Years of Education by Risk Class")

fig2 = go.Figure()
for label, color in RISK_COLORS.items():
    subset = df[df["Risk Class"] == label]["EDUC"].dropna()
    fig2.add_trace(go.Histogram(
        x=subset, name=label, opacity=0.7,
        marker_color=color, nbinsx=30,
        histnorm="probability density",
    ))
fig2.update_layout(
    barmode="overlay",
    xaxis_title="Years of Education",
    yaxis_title="Density",
    height=380,
    legend=dict(x=0.02, y=0.98),
)
st.plotly_chart(fig2, use_container_width=True)
st.caption(
    f"At-risk subjects: mean education {df[df['dementia_binary']==1]['EDUC'].mean():.1f} years | "
    f"Not-at-risk: {df[df['dementia_binary']==0]['EDUC'].mean():.1f} years"
)

# ---------------------------------------------------------------------------
# Section 4 — Social engagement (INCALLS / INVISITS)
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Social Engagement by Risk Class")

FREQ_MAP = {1:"Daily", 2:"≥3x/week", 3:"Weekly", 4:"≥3x/month", 5:"Monthly", 6:"<Monthly", 7:"Lives with"}

col_a, col_b = st.columns(2)

for col_widget, col_name, title in [
    (col_a, "INCALLS",  "Phone Call Frequency"),
    (col_b, "INVISITS", "In-Person Visit Frequency"),
]:
    freq_data = (
        df.groupby(["Risk Class", col_name])
        .size()
        .reset_index(name="count")
    )
    freq_data[col_name] = freq_data[col_name].map(FREQ_MAP)
    order = list(FREQ_MAP.values())
    freq_data[col_name] = pd.Categorical(freq_data[col_name], categories=order, ordered=True)
    freq_data = freq_data.sort_values(col_name)

    fig3 = px.bar(
        freq_data, x=col_name, y="count", color="Risk Class",
        color_discrete_map=RISK_COLORS,
        barmode="group", title=title,
        labels={col_name: "Frequency", "count": "Number of Subjects"},
    )
    fig3.update_layout(height=380, margin=dict(t=50))
    col_widget.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Section 5 — Smoking (PACK_YEARS)
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Cumulative Smoking Exposure (Pack-Years) by Risk Class")

# Exclude never-smokers for this view to focus on smokers only
smokers = df[df["NEVER_SMOKED"] == 0].copy()

fig4 = go.Figure()
for label, color in RISK_COLORS.items():
    subset = smokers[smokers["Risk Class"] == label]["PACK_YEARS"].dropna()
    subset = subset[subset <= 150]   # cap at 150 for readability
    fig4.add_trace(go.Box(
        y=subset, name=label,
        marker_color=color,
        boxmean=True,
    ))
fig4.update_layout(
    yaxis_title="Pack-Years (capped at 150 for display)",
    height=400,
    showlegend=True,
)
st.plotly_chart(fig4, use_container_width=True)
st.caption(f"Smokers only (n={len(smokers):,}). Never-smokers excluded from this chart.")

# ---------------------------------------------------------------------------
# Section 6 — Sex breakdown
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Sex Distribution by Risk Class")

sex_data = (
    df.groupby(["Risk Class", "SEX"])
    .size()
    .reset_index(name="count")
)
sex_data["SEX"] = sex_data["SEX"].map({1: "Male", 2: "Female"})

fig5 = px.bar(
    sex_data, x="Risk Class", y="count", color="SEX",
    color_discrete_map={"Male": "#2471a3", "Female": "#e74c3c"},
    barmode="group",
    labels={"count": "Number of Subjects"},
    title="Sex Distribution by Risk Class",
)
fig5.update_layout(height=380)
st.plotly_chart(fig5, use_container_width=True)

# ---------------------------------------------------------------------------
# Section 7 — Key data insights
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Key Data Insights")
st.markdown(f"""
- **Age gap:** At-risk subjects are on average 
  **{df[df['dementia_binary']==1]['NACCAGEB'].mean() - df[df['dementia_binary']==0]['NACCAGEB'].mean():.1f} years older** 
  than not-at-risk subjects at baseline.

- **Education gap:** At-risk subjects have on average 
  **{df[df['dementia_binary']==0]['EDUC'].mean() - df[df['dementia_binary']==1]['EDUC'].mean():.1f} fewer years of education** 
  than not-at-risk subjects — consistent with the cognitive reserve hypothesis.

- **Social isolation:** The at-risk group shows notably lower telephone and in-person 
  contact frequency with their co-participant, supporting social engagement as a 
  modifiable protective factor.

- **Never-smokers:** {df['NEVER_SMOKED'].mean()*100:.1f}% of subjects never smoked. 
  Among smokers, pack-year distributions are similar across risk classes, 
  suggesting smoking's effect is moderate relative to age and social factors in this dataset.
""")