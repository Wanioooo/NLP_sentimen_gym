import streamlit as st

def apply_light_blue_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #F0F9FF;
        color: #0F172A;
    }

    h1, h2, h3 {
        color: #0F172A;
        font-weight: 800;
    }

    section[data-testid="stSidebar"] {
        background-color: #0F172A;
    }

    section[data-testid="stSidebar"] * {
        color: #E0F2FE !important;
    }

    div.stButton > button {
        background-color: #0284C7;
        color: white;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        height: 3em;
    }

    div.stButton > button:hover {
        background-color: #0369A1;
    }

    textarea, input, select {
        background-color: white !important;
        color: #0F172A !important;
        border-radius: 8px !important;
        border: 1px solid #BAE6FD !important;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 16px;
        border-radius: 12px;
        border-left: 6px solid #0284C7;
    }

    [data-testid="stDataFrame"] {
        background-color: white;
        border-radius: 12px;
    }

    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
