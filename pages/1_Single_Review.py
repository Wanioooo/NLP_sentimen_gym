import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from theme import apply_light_blue_theme

st.set_page_config(page_title="Single Review Analysis", layout="wide")
apply_light_blue_theme()

label_map = {
    "LABEL_0": "negative",
    "LABEL_1": "neutral",
    "LABEL_2": "positive"
}

emoji_map = {
    "joy": "😄",
    "anger": "😡",
    "sadness": "😢",
    "fear": "😨",
    "surprise": "😲",
    "disgust": "🤢",
    "neutral": "😐"
}

@st.cache_resource
def load_models():
    return (
        pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment"),
        pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=5)
    )

sentiment_model, emotion_model = load_models()

st.header("✍️ Single Review Analysis")

review = st.text_area("Enter customer review:")
rating = st.radio("Rating:", [1,2,3,4,5], horizontal=True)

def rating_to_sentiment(r):
    return "negative" if r <= 2 else "neutral" if r == 3 else "positive"

if st.button("Analyze"):
    sent = sentiment_model(review)[0]
    sentiment = label_map[sent["label"]]

    emotions = emotion_model(review)[0]
    emo_df = pd.DataFrame({
        "Emotion": [f"{emoji_map[e['label']]} {e['label'].title()}" for e in emotions],
        "Score (%)": [round(e["score"]*100,2) for e in emotions]
    })

    col1, col2, col3 = st.columns(3)
    col1.metric("AI Sentiment", sentiment.capitalize())
    col2.metric("Confidence", f"{sent['score']:.2f}")
    col3.metric("Rating Sentiment", rating_to_sentiment(rating).capitalize())

    fig = px.bar(
        emo_df.sort_values("Score (%)"),
        x="Score (%)",
        y="Emotion",
        orientation="h",
        title="Emotion Detection"
    )
    st.plotly_chart(fig, use_container_width=True)
