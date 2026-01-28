import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from theme import apply_light_blue_theme

st.set_page_config(page_title="Social Media Analysis", layout="wide")
apply_light_blue_theme()

label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

model = load_model()

st.header("📱 Live Social Media Feed Analysis (Twitter)")

st.info("⚠️ Currently using sample tweets CSV. Replace with live scraping if allowed.")

# Upload CSV with tweets
file = st.file_uploader("Upload CSV of tweets (with column 'tweet')", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    tweet_col = st.selectbox("Select the column containing tweets", df.columns)

    if st.button("Analyze Tweets"):
        texts = df[tweet_col].astype(str).tolist()
        preds = model(texts)
        df["AI Sentiment"] = [label_map[p["label"]] for p in preds]

        st.subheader("📊 Sentiment Summary")
        counts = df["AI Sentiment"].value_counts()
        st.bar_chart(counts)

        st.subheader("Detailed Results")
        st.dataframe(df.head())
else:
    st.info("Upload a CSV file containing tweets to start analysis")
