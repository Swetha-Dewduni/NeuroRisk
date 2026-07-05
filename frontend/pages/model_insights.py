import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Model Insights", page_icon="🔍", layout="wide")

API_URL = "https://swetha2003-dementia-risk-api.hf.space"   # <-- update after deploying backend

st.title("🔍 Model Insights")
st.markdown(
    "Global explanation of what the XGBoost model has learned — "
    "which non-medical factors drive dementia risk predictions and in what direction."
)
st.markdown("---")

# ---------------------------------------------------------------------------
# Load feature importance from API
# ---------------------------------------------------------------------------
@st.cache_data(ttl=3600)
def load_feature_importance():
    resp = requests.get(f"{API_URL}/feature-importance", timeout=30)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

try:
    fi_df = load_feature_importance()
except Exception as e:
    st.error(f"Could not load feature importance from API: {e}")
    st.stop()

fi_df = fi_df.rename(columns={"Unnamed: 0": "feature"})
fi_df = fi_df.sort_values("mean_abs_shap", ascending=True)

# ---------------------------------------------------------------------------
# Section 1 — Feature importance bar chart
# ---------------------------------------------------------------------------
st.subheader("Global Feature Importance (Mean |SHAP Value|)")
st.markdown(
    "Each bar shows the average absolute SHAP value for that feature across all test subjects. "
    "Larger = more influence on predictions overall."
)

fig = go.Figure(go.Bar(
    x=fi_df["mean_abs_shap"],
    y=fi_df["feature"],
    orientation="h",
    marker=dict(
        color=fi_df["mean_abs_shap"],
        colorscale="Blues",
        showscale=False,
    ),
    text=fi_df["mean_abs_shap"].round(4),
    textposition="outside",
))
fig.update_layout(
    xaxis_title="Mean |SHAP Value|",
    yaxis_title="Feature",
    height=700,
    margin=dict(t=30, b=40, l=160, r=80),
)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Section 2 — Feature group breakdown
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("Importance by Feature Group")
st.markdown("Aggregated SHAP importance across the four non-medical feature domains.")

GROUP_MAP = {
    "INCALLS":       "Social Engagement",
    "INVISITS":      "Social Engagement",
    "INLIVWTH":      "Social Engagement",
    "EDUC":          "Demographics",
    "SEX":           "Demographics",
    "NACCAGEB":      "Demographics",
    "BIRTHYR":       "Demographics",
    "HISPANIC":      "Demographics",
    "RACE_2.0":      "Demographics",
    "RACE_3.0":      "Demographics",
    "RACE_4.0":      "Demographics",
    "RACE_5.0":      "Demographics",
    "RACE_50.0":     "Demographics",
    "PRIMLANG_2.0":  "Demographics",
    "PRIMLANG_3.0":  "Demographics",
    "PRIMLANG_4.0":  "Demographics",
    "PRIMLANG_5.0":  "Demographics",
    "PRIMLANG_6.0":  "Demographics",
    "HANDED_2.0":    "Demographics",
    "HANDED_3.0":    "Demographics",
    "PACK_YEARS":    "Lifestyle / Smoking",
    "TOBAC100":      "Lifestyle / Smoking",
    "TOBAC30":       "Lifestyle / Smoking",
    "SMOKYRS":       "Lifestyle / Smoking",
    "PACKSPER":      "Lifestyle / Smoking",
    "NEVER_SMOKED":  "Lifestyle / Smoking",
    "MARISTAT_2.0":  "Social",
    "MARISTAT_3.0":  "Social",
    "MARISTAT_4.0":  "Social",
    "MARISTAT_5.0":  "Social",
    "MARISTAT_6.0":  "Social",
    "NACCLIVS_2.0":  "Social",
    "NACCLIVS_3.0":  "Social",
    "NACCLIVS_4.0":  "Social",
    "NACCLIVS_5.0":  "Social",
    "RESIDENC_2.0":  "Social",
    "RESIDENC_3.0":  "Social",
    "RESIDENC_4.0":  "Social",
    "INRELTO_2.0":   "Social",
    "INRELTO_3.0":   "Social",
    "INRELTO_4.0":   "Social",
    "INRELTO_5.0":   "Social",
    "INRELTO_6.0":   "Social",
    "INRELTO_7.0":   "Social",
}

fi_df["group"] = fi_df["feature"].map(GROUP_MAP).fillna("Other")
group_importance = (
    fi_df.groupby("group")["mean_abs_shap"]
    .sum()
    .reset_index()
    .sort_values("mean_abs_shap", ascending=False)
)

col1, col2 = st.columns([1, 1])
with col1:
    fig2 = px.pie(
        group_importance,
        values="mean_abs_shap",
        names="group",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4,
    )
    fig2.update_layout(title="Feature Group Share of Total SHAP Importance", height=400)
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = go.Figure(go.Bar(
        x=group_importance["group"],
        y=group_importance["mean_abs_shap"],
        marker_color=px.colors.qualitative.Set2[:len(group_importance)],
        text=group_importance["mean_abs_shap"].round(3),
        textposition="outside",
    ))
    fig3.update_layout(
        title="Total SHAP Importance by Group",
        yaxis_title="Sum of Mean |SHAP|",
        height=400,
        margin=dict(t=50, b=40),
    )
    st.plotly_chart(fig3, use_container_width=True)

# ---------------------------------------------------------------------------
# Section 3 — Key findings narrative
# ---------------------------------------------------------------------------
st.markdown("---")
st.subheader("📋 Key Findings")

st.markdown("""
**Social engagement is the strongest signal.** `INCALLS` (telephone contact frequency) 
is the single most important feature, followed by `INVISITS` (in-person visits). 
Lower contact frequency is associated with higher dementia risk — consistent with 
the established literature linking social isolation to cognitive decline.

**Education is the strongest demographic predictor.** `EDUC` (years of education) 
is the second most important feature overall. Higher education is widely theorised 
to build cognitive reserve — the brain's resilience against neurodegeneration.

**Age and sex matter, but don't dominate.** `NACCAGEB` and `SEX` rank third and fourth. 
Notably, social and lifestyle factors collectively outweigh raw demographic risk, 
suggesting these are actionable targets unlike age.

**PACK_YEARS validates the feature engineering decision.** The engineered cumulative 
smoking exposure variable outperforms the raw smoking indicators (`TOBAC30`, `TOBAC100`), 
confirming that a single combined measure captures more signal than its components separately.

**Co-participant relationship type matters.** `INRELTO_5.0` (paid caregiver as co-participant) 
is a strong risk signal — subjects relying on paid care likely have pre-existing functional 
dependencies that correlate with dementia risk.
""")