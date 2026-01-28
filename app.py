import streamlit as st

st.set_page_config(
    page_title="Gym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ Gym Sentiment Analysis Dashboard")
st.write("AI-powered dashboard to analyze customer reviews using NLP.")

st.markdown("""
<div style="
    border: 2px solid #0284C7; 
    border-radius: 12px; 
    padding: 15px; 
    background-color: #E0F2FE;
">
<h2 style="color: #0F172A; margin:0;">📊 Dashboard Overview</h2>
</div>
""", unsafe_allow_html=True)


st.subheader("📌 Dashboard Overview")


col1, col2, col3 = st.columns(3)

col1.markdown("""
<div style="
    border: 2px solid #0284C7;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    background-color: #E0F2FE;
">
<h3 style="margin:0; color:#0F172A;">Sentiment Types</h3>
<p style="font-size:20px; font-weight:700; color:#0369A1;">3</p>
<p style="margin:0; color:#0F172A;">Positive / Neutral / Negative</p>
</div>
""", unsafe_allow_html=True)

col2.markdown("""
<div style="
    border: 2px solid #0284C7;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    background-color: #E0F2FE;
">
<h3 style="margin:0; color:#0F172A;">Emotion Classes</h3>
<p style="font-size:20px; font-weight:700; color:#0369A1;">6</p>
<p style="margin:0; color:#0F172A;">Joy, Anger, Sadness, etc.</p>
</div>
""", unsafe_allow_html=True)

col3.markdown("""
<div style="
    border: 2px solid #0284C7;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    background-color: #E0F2FE;
">
<h3 style="margin:0; color:#0F172A;">Input Types</h3>
<p style="font-size:20px; font-weight:700; color:#0369A1;">2</p>
<p style="margin:0; color:#0F172A;">Text & CSV</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
### 🔍 Features
- ✍️ Single customer review sentiment & emotion analysis  
- 📁 Batch CSV review analysis  
- ⚠️ Sentiment vs rating mismatch detection  
- 📊 Visual emotion breakdown  
- 📱 Social media feed analysis (CSV-based)
""")
