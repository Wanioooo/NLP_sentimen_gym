# ==============================
# app.py (Homepage)
# ==============================

import streamlit as st

st.set_page_config(
    page_title="PureGym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ PureGym Customer Sentiment Dashboard")
st.markdown("""
Welcome to the **PureGym Sentiment Analysis Dashboard**.  
This dashboard allows you to:
- Analyze single reviews
- Analyze batch reviews via CSV
- Analyze social media sentiment (simulated live feed)
""")

st.subheader("Dashboard Overview")
st.markdown("""
1. **Single Review Analysis:** Input a review and see AI-predicted sentiment and emotion.  
2. **Batch Review Analysis:** Upload a CSV file of reviews and get AI sentiment with rating comparison.  
3. **Social Media Feed Analysis:** Simulated live Twitter/X posts analyzed for sentiment.  
""")

st.info("Use the sidebar to navigate to different analysis pages.")
