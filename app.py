import streamlit as st
from theme import apply_light_blue_theme

st.set_page_config(
    page_title="PureGym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

apply_light_blue_theme()

st.markdown("""
<div style="text-align:center; padding:40px;">
<h1>🏋️ PureGym Sentiment Analysis Dashboard</h1>
<p style="font-size:17px; color:#334155;">
AI-powered dashboard to analyze customer reviews using NLP
</p>
</div>
""", unsafe_allow_html=True)

st.subheader("📌 Dashboard Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Sentiment Types", "3", "Positive / Neutral / Negative")
col2.metric("Emotion Classes", "6", "Joy, Anger, Sadness, etc.")
col3.metric("Input Types", "2", "Text & CSV")

st.markdown("""
### 🔍 Features
- ✍️ Single customer review sentiment & emotion analysis  
- 📁 Batch CSV review analysis  
- ⚠️ Sentiment vs rating mismatch detection  
- 📊 Visual emotion breakdown  

➡️ Use the **sidebar** to navigate between pages.
""")
