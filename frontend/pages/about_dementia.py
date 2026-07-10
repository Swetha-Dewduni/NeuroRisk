import streamlit as st
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from styles import inject_styles, hero, section_header, metric_card, info_card, divider

st.set_page_config(page_title="About Dementia", page_icon="📖", layout="wide")
inject_styles()

hero(
    "📖 About Dementia",
    "Understanding dementia, its risk factors, and how this tool can help you take action early.",
    badges=["Educational", "Evidence-Based", "WHO Data"]
)

# Key stats
section_header("Global Impact")
c1, c2, c3, c4 = st.columns(4)
with c1: metric_card("55M+", "People living with dementia", "10M new cases/year")
with c2: metric_card("2x", "Risk increase every 5 yrs after 65")
with c3: metric_card("40%", "Cases potentially preventable")
with c4: metric_card("$1.3T", "Annual global cost")

divider()

# What is dementia
section_header("What is Dementia?")
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
Dementia is not a single disease — it is an umbrella term for a group of symptoms
affecting memory, thinking, and social abilities severely enough to interfere with
daily life. It is caused by damage to brain cells that affects their ability to
communicate with each other.

**The most common types include:**
- **Alzheimer's disease** — 60–80% of cases. Caused by amyloid plaques and tau tangles.
- **Vascular dementia** — caused by reduced blood flow, often following a stroke.
- **Lewy body dementia** — caused by abnormal protein deposits disrupting brain chemistry.
- **Frontotemporal dementia** — affects personality and language before memory.

Dementia is progressive — symptoms worsen over time. There is currently no cure,
but early identification enables better planning and management.
    """)
with col2:
    info_card("""
<b>Did you know?</b><br><br>
Dementia is the <b>7th leading cause</b> of death globally and one of the major causes of
disability among older people.<br><br>
Women are disproportionately affected — they represent <b>65% of total dementia deaths</b>.
    """, kind="warning")

divider()

# Stages
section_header("Stages of Dementia")
s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
<div class="stage-card stage-mild">
<h4 style="color:#f59e0b">🟡 Mild Cognitive Impairment (MCI)</h4>
The transition stage between normal ageing and dementia. People notice memory
lapses but can still carry out daily activities independently.<br><br>
Not everyone with MCI develops dementia — but it is a recognised risk factor.
This stage is the focus of early intervention.
</div>
    """, unsafe_allow_html=True)
with s2:
    st.markdown("""
<div class="stage-card stage-moderate">
<h4 style="color:#f97316">🟠 Mild Dementia</h4>
Memory loss and confusion become noticeable to others. The person may need
help with complex tasks like managing finances or planning.<br><br>
Many people live independently at this stage with some support.
Personality changes may begin to appear.
</div>
    """, unsafe_allow_html=True)
with s3:
    st.markdown("""
<div class="stage-card stage-severe">
<h4 style="color:#ef4444">🔴 Moderate to Severe Dementia</h4>
Significant memory loss, difficulty recognising family members, and loss of
independent function. Full-time care is typically required.<br><br>
Communication becomes increasingly difficult as the disease progresses.
</div>
    """, unsafe_allow_html=True)

divider()

# Risk factors
section_header("Risk Factors")
col_a, col_b = st.columns(2)
with col_a:
    st.markdown("#### 🔒 Non-modifiable risk factors")
    st.markdown("""
| Factor | Detail |
|---|---|
| **Age** | Risk doubles every 5 years after 65 |
| **Sex** | Women have higher lifetime risk |
| **Genetics** | APOE ε4 variant increases Alzheimer's risk |
| **Family history** | First-degree relative increases risk |
    """)
    info_card("These factors are captured in this model through <b>age, birth year, and sex</b>.", kind="info")

with col_b:
    st.markdown("#### 🔓 Modifiable risk factors")
    st.markdown("""
| Factor | Risk reduction |
|---|---|
| **Social engagement** | Up to 60% lower risk with high social contact |
| **Education** | Each year reduces risk ~7% |
| **Smoking cessation** | Reduces risk to near non-smoker levels |
| **Physical activity** | 35% reduction with regular exercise |
| **Hearing treatment** | 8% of dementia cases linked to untreated hearing loss |
    """)
    info_card("This model focuses on <b>social engagement, education, and smoking</b> as key modifiable predictors.", kind="success")

divider()

# Why this tool
section_header("Why Non-Medical Prediction?")
st.markdown("""
Most dementia risk tools require clinical inputs — cognitive test scores, blood biomarkers,
or neuroimaging. These are powerful but have significant limitations:
""")
w1, w2, w3 = st.columns(3)
with w1:
    info_card("🏥 Require a <b>trained clinician</b> to administer", kind="warning")
with w2:
    info_card("💰 Are <b>expensive</b> and not universally accessible", kind="warning")
with w3:
    info_card("⏱️ By the time markers appear, <b>significant brain changes</b> have already occurred", kind="warning")

st.markdown("""
This tool takes a different approach — using only **demographic, lifestyle, and social factors**
that anyone can report. Achieving **ROC-AUC of 0.73** on purely non-medical variables demonstrates
that meaningful risk stratification is possible from everyday information.
""")

divider()

# How to use
section_header("How to Use This Tool")
h1, h2, h3 = st.columns(3)
with h1:
    info_card("1️⃣ Go to <b>Risk Predictor</b> and fill in the form with your demographic and lifestyle information.", kind="info")
with h2:
    info_card("2️⃣ Click <b>Predict</b> to get your personalised risk score and SHAP explanation.", kind="info")
with h3:
    info_card("3️⃣ Review which factors are driving your score — many are <b>within your control</b>.", kind="success")

divider()

# Warning
info_card("""
⚠️ <b>Important Disclaimer</b><br><br>
This tool is <b>not a diagnostic instrument</b>. A high risk score should prompt a conversation
with a healthcare professional — not self-diagnosis. This model was trained on a research cohort
and should be used for educational and awareness purposes only.
""", kind="danger")

# Resources
section_header("Further Resources")
r1, r2, r3 = st.columns(3)
with r1:
    st.markdown("""
**🌐 Alzheimer's Association**

World's leading voluntary health organisation in Alzheimer's care and research.

[alz.org](https://www.alz.org)
    """)
with r2:
    st.markdown("""
**🌐 Alzheimer's Disease International**

Global federation representing 100+ national Alzheimer's associations.

[alzint.org](https://www.alzint.org)
    """)
with r3:
    st.markdown("""
**🌐 NACC — National Alzheimer's Coordinating Center**

Source of the dataset used to train this model.

[naccdata.org](https://naccdata.org)
    """)

st.caption("NeuroRisk is a research and educational tool. Not a medical device.")