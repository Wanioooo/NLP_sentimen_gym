import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

st.set_page_config(page_title="Single Review Analysis", layout="wide")
st.header("✍️ Single Review Analysis")

label_map = {"LABEL_0": "negative", "LABEL_1": "neutral", "LABEL_2": "positive"}
emoji_map = {"joy":"😄","anger":"😡","sadness":"😢","fear":"😨","surprise":"😲","disgust":"🤢","neutral":"😐"}

@st.cache_resource
def load_models():
    sentiment = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")
    emotion = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=5)
    return sentiment, emotion

sentiment_model, emotion_model = load_models()

review = st.text_area("Enter a customer review:")
user_rating = st.radio(
    "Give a rating:",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x,
    horizontal=True
)


def rating_to_sentiment(r): return "negative" if r<=2 else "neutral" if r==3 else "positive"

if st.button("Analyze Review"):
    if review.strip():
        sent = sentiment_model(review)[0]
        sentiment = label_map[sent["label"]]

        emotions = emotion_model(review)[0]
        emo_df = pd.DataFrame({
            "Emotion": [f"{emoji_map[e['label']]} {e['label'].title()}" for e in emotions],
            "Score (%)": [round(e["score"]*100,2) for e in emotions]
        })

        # Metrics Cards
        col1, col2, col3 = st.columns(3)
        col1.metric("AI Sentiment", sentiment.capitalize())
        col2.metric("Confidence", f"{sent['score']:.2f}")
        col3.metric("Rating Sentiment", rating_to_sentiment(rating).capitalize())

        # Emotion Bar Chart
        fig = px.bar(emo_df.sort_values("Score (%)"), x="Score (%)", y="Emotion",
                     orientation="h", title="🎭 Emotion Detection")
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)

        if sentiment != rating_to_sentiment(rating):
            st.warning("⚠️ AI sentiment does not match rating")
        else:
            st.success("✅ Sentiment matches rating")
