import streamlit as st

st.set_page_config(
    page_title="PureGym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

# ---- GYM THEME STYLE ----
st.markdown("""
<style>
.stApp { background-color: #0F172A; color: #E5E7EB; }
h1, h2, h3 { color: #22C55E; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# ---- HERO SECTION ----
st.markdown("""
<div style="text-align:center; padding:40px;">
    <h1>🏋️ PureGym Sentiment Intelligence Dashboard</h1>
    <p style="font-size:18px; color:#CBD5E1;">
        AI-powered insight into customer reviews & social media conversations
    </p>
</div>
""", unsafe_allow_html=True)

# ---- KPI CARDS ----
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 Reviews Analyzed", "1,000+", delta="Live")
with col2:
    st.metric("😊 Avg Sentiment", "Positive", delta="+12%")
with col3:
    st.metric("🔥 Data Sources", "Reviews + Social Media")

# ---- FEATURES ----
st.markdown("## 🚀 Dashboard Features")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    ### ✍️ Single Review Analysis
    - Sentiment polarity  
    - Emotion detection  
    - Rating vs AI comparison
    """)

with col5:
    st.markdown("""
    ### 📁 Batch Review Analysis
    - CSV upload  
    - Confusion matrix  
    - Downloadable results
    """)

with col6:
    st.markdown("""
    ### 🔴 Social Media Intelligence
    - Simulated live feed  
    - Sentiment & emotion trends  
    - Public opinion insights
    """)

st.info("⬅️ Use the sidebar to explore different analysis modules")
