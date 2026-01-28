import streamlit as st

st.set_page_config(
    page_title="PureGym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

# ---------- GYM THEME ----------
st.markdown("""
<style>
.stApp { background-color: #0F172A; color: #E5E7EB; }
h1,h2,h3 { color: #22C55E; font-weight: 800; }
section[data-testid="stSidebar"] { background-color:#020617; }
button { background:#22C55E !important; color:black !important; border-radius:12px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:40px;">
<h1>🏋️ PureGym Sentiment Intelligence Dashboard</h1>
<p style="font-size:18px;color:#CBD5E1;">
AI-powered analysis of gym reviews & social media conversations
</p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
c1.metric("💬 Reviews Analyzed", "1,000+")
c2.metric("😊 Overall Sentiment", "Positive")
c3.metric("🔥 Data Sources", "Reviews + Social Media")

st.markdown("## 🚀 Features")
st.markdown("""
- ✍️ **Single Review Sentiment & Emotion**
- 📁 **Batch CSV Review Analysis**
- 🔴 **Social Media Sentiment & Emotion Trends**
""")

st.info("⬅️ Use the sidebar to explore each module")
