import streamlit as st

st.set_page_config(
    page_title="Gym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ Gym Sentiment Analysis Dashboard")
st.write("AI-powered dashboard to analyze customer reviews using NLP.")

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
- 📱 Social media feed analysis (CSV-based)
""")
