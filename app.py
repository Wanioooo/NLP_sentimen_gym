import streamlit as st

st.set_page_config(
    page_title="GymPulse: NLP Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide",
)

# ============================
# Homepage Header Box
# ============================
st.markdown("""
<div style="
    border: 3px solid #0284C7;
    border-radius: 15px;
    padding: 25px;
    background-color: #E0F2FE;
    text-align: center;">
<h1 style="margin:0; color:#0F172A;">🏋️ GymPulse: NLP Sentiment Dashboard</h1>
<p style="color:#0F172A; font-size:16px;">AI-powered analysis of customer reviews & social media sentiment</p>
</div>
""", unsafe_allow_html=True)

# ============================
# Metrics Cards
# ============================
st.markdown("### 📌 Dashboard Overview")
col1, col2, col3 = st.columns(3)

card_style = """
<div style="
    border: 2px solid #0284C7;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    background-color: #E0F2FE;
">
<h3 style="margin:0; color:#0F172A;">{title}</h3>
<p style="font-size:20px; font-weight:700; color:#0369A1;">{value}</p>
<p style="margin:0; color:#0F172A;">{desc}</p>
</div>
"""

col1.markdown(card_style.format(title="Sentiment Types", value="3", desc="Positive / Neutral / Negative"), unsafe_allow_html=True)
col2.markdown(card_style.format(title="Emotion Classes", value="6", desc="Joy, Anger, Sadness..."), unsafe_allow_html=True)
col3.markdown(card_style.format(title="Input Types", value="2", desc="Text & CSV"), unsafe_allow_html=True)

# ============================
# Features List
# ============================
st.markdown("""
### 🔍 Features
- ✍️ Single customer review sentiment & emotion analysis  
- 📁 Batch CSV review analysis  
- ⚠️ Sentiment vs rating mismatch detection  
- 📊 Visual emotion breakdown  
- 📱 Social media feed analysis (CSV-based)
""")
