import streamlit as st
import pandas as pd
from transformers import pipeline
from sklearn.metrics import confusion_matrix
from theme import apply_light_blue_theme

st.set_page_config(page_title="Batch Analysis", layout="wide")
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

def rating_to_sentiment(r):
    return "negative" if r <= 2 else "neutral" if r == 3 else "positive"

st.header("📁 Batch Review Analysis")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    text_col = st.selectbox("Review column", df.columns)
    rating_col = st.selectbox("Rating column", df.columns)

    if st.button("Analyze Dataset"):
        texts = df[text_col].astype(str).tolist()
        preds = model(texts)

        df["AI Sentiment"] = [label_map[p["label"]] for p in preds]
        df["Rating Sentiment"] = df[rating_col].apply(rating_to_sentiment)

        st.dataframe(df.head())

        cm = confusion_matrix(
            df["Rating Sentiment"],
            df["AI Sentiment"],
            labels=["negative","neutral","positive"]
        )

        st.subheader("⚠️ Confusion Matrix")
        st.dataframe(pd.DataFrame(
            cm,
            index=["Rating Neg","Rating Neu","Rating Pos"],
            columns=["AI Neg","AI Neu","AI Pos"]
        ))
