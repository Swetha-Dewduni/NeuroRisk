import streamlit as st

st.set_page_config(page_title="About Dementia", page_icon="📖", layout="wide")

st.title("📖 About Dementia")
st.markdown("Understanding dementia, its risk factors, and how this tool can help.")
st.markdown("---")

# ---------------------------------------------------------------------------
# Section 1 — What is dementia
# ---------------------------------------------------------------------------
st.subheader("What is Dementia?")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown("""
Dementia is not a single disease — it is an umbrella term for a group of symptoms 
affecting memory, thinking, and social abilities severely enough to interfere with 
daily life. It is caused by damage to brain cells that affects their ability to 
communicate with each other.

The most common types include:
- **Alzheimer's disease** — accounts for 60–80% of cases. Characterised by the 
  buildup of amyloid plaques and tau tangles in the brain.
- **Vascular dementia** — caused by reduced blood flow to the brain, often following 
  a stroke.
- **Lewy body dementia** — caused by abnormal protein deposits called Lewy bodies 
  that disrupt brain chemistry.
- **Frontotemporal dementia** — affects the frontal and temporal lobes, causing 
  changes in personality and language before memory is affected.

Dementia is progressive — symptoms worsen over time. It currently affects over 
**55 million people worldwide** and this number is expected to triple by 2050.
    """)

with col2:
    st.info("""
**Key facts**

🌍 55 million people worldwide live with dementia

📈 10 million new cases diagnosed every year

👵 Age is the strongest risk factor — risk doubles every 5 years after age 65

🔬 There is currently no cure, but early identification enables better management
    """)

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 2 — Stages
# ---------------------------------------------------------------------------
st.subheader("Stages of Dementia")

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown("""
**🟡 Mild Cognitive Impairment (MCI)**

The transition stage between normal ageing and dementia. People with MCI notice 
memory lapses but can still carry out daily activities independently.

Not everyone with MCI develops dementia — but it is a recognised risk factor. 
This stage is the focus of early intervention.
    """)
with s2:
    st.markdown("""
**🟠 Mild Dementia**

Memory loss and confusion become noticeable to others. The person may need 
help with complex tasks like managing finances or planning. Personality changes 
may begin to appear.

Many people live independently at this stage with some support.
    """)
with s3:
    st.markdown("""
**🔴 Moderate to Severe Dementia**

Significant memory loss, difficulty recognising family members, and loss of 
independent function. Full-time care is typically required at the severe stage.

Communication becomes increasingly difficult as the disease progresses.
    """)

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 3 — Risk factors
# ---------------------------------------------------------------------------
st.subheader("Risk Factors")
st.markdown(
    "Dementia risk factors fall into two categories: those you cannot change, "
    "and those you can actively address."
)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("#### 🔒 Non-modifiable risk factors")
    st.markdown("""
These factors increase risk but cannot be changed:

| Factor | Detail |
|---|---|
| **Age** | The strongest single risk factor. Risk roughly doubles every 5 years after 65. |
| **Sex** | Women have a higher lifetime risk than men, partly due to longer life expectancy. |
| **Genetics** | The APOE ε4 gene variant significantly increases Alzheimer's risk. |
| **Family history** | Having a first-degree relative with dementia increases risk. |
| **Down syndrome** | Associated with higher risk of early-onset Alzheimer's. |

> These factors are captured in this model through **age, birth year, and sex**.
    """)

with col_b:
    st.markdown("#### 🔓 Modifiable risk factors")
    st.markdown("""
Research suggests up to **40% of dementia cases** could be prevented or delayed 
by addressing these factors:

| Factor | Detail |
|---|---|
| **Social isolation** | Low social contact is one of the strongest modifiable risk factors. |
| **Education** | Higher education builds cognitive reserve — the brain's resilience against decline. |
| **Smoking** | Smoking increases risk by damaging blood vessels in the brain. |
| **Physical inactivity** | Regular exercise reduces risk by up to 35%. |
| **Excessive alcohol** | Heavy drinking damages brain cells directly. |
| **Depression** | Untreated depression is associated with increased dementia risk. |
| **Hearing loss** | Unaddressed hearing loss increases cognitive load and social withdrawal. |

> This model focuses specifically on **social engagement, education, and smoking** 
> as the key modifiable predictors.
    """)

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 4 — Why non-medical prediction matters
# ---------------------------------------------------------------------------
st.subheader("Why Non-Medical Prediction?")

st.markdown("""
Most dementia risk assessment tools require clinical inputs — cognitive test scores, 
blood biomarkers, or neuroimaging. These are powerful but have significant limitations:

- They require a **trained clinician** to administer
- They are **expensive** and not universally accessible
- By the time clinical markers appear, **significant brain changes have already occurred**

This tool takes a different approach. By focusing exclusively on **demographic, 
lifestyle, and social factors** — information anyone can report — it aims to:

1. **Lower the barrier** to risk awareness. No clinic visit needed.
2. **Identify modifiable risks early**, before clinical symptoms emerge.
3. **Highlight social isolation** as an actionable, underappreciated risk factor.

A model trained purely on non-medical variables achieving **ROC-AUC of 0.73** 
demonstrates that meaningful risk stratification is possible from everyday 
information — an important finding for public health screening.
""")

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 5 — How to use this tool
# ---------------------------------------------------------------------------
st.subheader("How to Use This Tool")

st.markdown("""
Navigate to the **Risk Predictor** page and fill in the form. The model will return:

- A **risk percentage** (0–100%) — the model's estimated probability of being at risk
- A **classification** — At Risk or Not At Risk, based on an optimised threshold of 39.7%
- A **SHAP explanation** — showing which of your specific inputs drove the prediction 
  up or down

**Interpreting the score:**
- The threshold of 39.7% was chosen to maximise recall — the model prioritises 
  catching at-risk individuals over avoiding false alarms
- A high score is not a diagnosis — it indicates elevated risk based on lifestyle 
  and social factors only
- A low score does not mean dementia cannot develop — it means the non-medical 
  risk factors assessed here are not elevated
""")

st.info("""
💡 **Tip:** The most actionable insight from this tool is often not the score itself, 
but the SHAP explanation — it shows exactly which factors are contributing most to 
your individual risk estimate, and many of those factors are within your control.
""")

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 6 — When to seek help
# ---------------------------------------------------------------------------
st.subheader("When to Seek Help")

st.warning("""
**This tool is not a diagnostic instrument.** It is a risk screening tool based on 
non-medical variables. A high risk score should prompt a conversation with a healthcare 
professional — not self-diagnosis.
""")

st.markdown("""
**Speak to a doctor if you or someone you know experiences:**

- Frequent memory loss that disrupts daily life
- Difficulty completing familiar tasks
- Confusion about time, place, or people
- Trouble with language — struggling to find words or follow conversations
- Poor judgement or decision-making
- Withdrawal from social activities
- Changes in mood or personality

**Early diagnosis matters.** While there is no cure, early identification enables:
- Access to medications that can slow symptom progression
- Planning and legal/financial arrangements while the person has capacity
- Access to support services for the person and their family
- Opportunity to participate in clinical trials
""")

st.markdown("---")

# ---------------------------------------------------------------------------
# Section 7 — Resources
# ---------------------------------------------------------------------------
st.subheader("Further Resources")

r1, r2, r3 = st.columns(3)
with r1:
    st.markdown("""
**🌐 Alzheimer's Association**

The world's leading voluntary health organisation in Alzheimer's care and research.

[alz.org](https://www.alz.org)
    """)
with r2:
    st.markdown("""
**🌐 Alzheimer's Disease International**

Global federation of Alzheimer's associations, representing 100+ countries.

[alzint.org](https://www.alzint.org)
    """)
with r3:
    st.markdown("""
**🌐 NACC — National Alzheimer's Coordinating Center**

The source of the dataset used to train this model.

[naccdata.org](https://naccdata.org)
    """)

st.markdown("---")
st.caption(
    "NeuroRisk is a research and educational tool. It is not a medical device and should not "
    "be used as a substitute for professional medical advice, diagnosis, or treatment."
)