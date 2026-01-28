import streamlit as st
import pandas as pd
from transformers import pipeline
import plotly.express as px

st.set_page_config(page_title="Social Media Analysis", layout="wide")
st.header("📱 Social Media Feed Analysis (CSV-based)")

label_map = {"LABEL_0":"negative","LABEL_1":"neutral","LABEL_2":"positive"}

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

model = load_model()

file = st.file_uploader("Upload CSV of tweets", type=["csv"])
if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    tweet_col = st.selectbox("Select Tweet Column", df.columns)

    if st.button("Analyze Tweets"):
        texts = df[tweet_col].astype(str).tolist()
        preds = model(texts)
        df["AI Sentiment"] = [label_map[p["label"]] for p in preds]

        st.subheader("📊 Sentiment Summary")
        counts = df["AI Sentiment"].value_counts()
        st.bar_chart(counts)

        st.subheader("Detailed Results")
        st.dataframe(df.head())
