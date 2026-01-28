import streamlit as st
import pandas as pd

# 1️⃣ PAGE CONFIG — MUST COME FIRST
st.set_page_config(
    page_title="PureGym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

# 2️⃣ PUT YOUR CSS THEME HERE ⬇️⬇️⬇️
st.markdown("""
<style>
/* MAIN BACKGROUND */
.stApp {
    background-color: #F8FAFC;
    color: #111827;
}

/* TITLES */
h1, h2, h3 {
    color: #111827;
    font-weight: 800;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
    color: white;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* BUTTONS */
div.stButton > button {
    background-color: #DC2626;
    color: white;
    font-weight: 700;
    border-radius: 10px;
    border: none;
    height: 3em;
}
div.stButton > button:hover {
    background-color: #B91C1C;
}

/* INPUT BOXES */
textarea, input, select {
    background-color: white !important;
    color: #111827 !important;
    border-radius: 8px !important;
    border: 1px solid #CBD5E1 !important;
}

/* METRIC CARDS */
[data-testid="stMetric"] {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* DATAFRAMES */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
}

/* ALERTS */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# 3️⃣ ONLY AFTER THIS — YOUR UI CODE
st.title("🏋️ PureGym Sentiment Analysis Dashboard")
