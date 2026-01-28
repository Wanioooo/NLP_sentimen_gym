import streamlit as st
import pandas as pd
from sklearn.metrics import confusion_matrix
from utils import load_models, batch_predict, label_map, rating_to_sentiment, clean_text

st.set_page_config(page_title="Batch Analysis", layout="wide")

st.markdown("""
<style>
.stApp { background-color:#0F172A; color:#E5E7EB; }
h1,h2,h3 { color:#22C55E; }
</style>
""", unsafe_allow_html=True)

st.header("📁 Batch Review Analysis")

sentiment_model, _ = load_models()

file = st.file_uploader("Upload CSV", type="csv")

if file:
    df = pd.read_csv(file)
    text_col = st.selectbox("Review column", df.columns)
    rate_col = st.selectbox("Rating column", df.columns)

    if st.button("Analyze"):
        texts = df[text_col].apply(clean_text).tolist()
        preds = batch_predict(sentiment_model, texts)

        df["AI Sentiment"] = [label_map[p["label"]] for p in preds]
        df["Rating Sentiment"] = df[rate_col].apply(rating_to_sentiment)

        st.dataframe(df.head())

        cm = confusion_matrix(
            df["Rating Sentiment"],
            df["AI Sentiment"],
            labels=["negative","neutral","positive"]
        )

        st.subheader("⚠️ Confusion Matrix")
        st.dataframe(cm)
