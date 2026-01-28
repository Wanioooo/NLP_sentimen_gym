import streamlit as st
from utils import load_models, batch_predict, rating_to_sentiment, clean_text, label_map, emoji_map

st.set_page_config(page_title="Single Review Analysis", layout="wide")

st.header("✍️ Single Review Analysis")

sentiment_model, emotion_model = load_models()

user_review = st.text_area("Enter your review:")

user_rating = st.radio(
    "Give a rating:",
    options=[1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x,
    horizontal=True
)

if st.button("Analyze Review"):
    if user_review.strip():
        sentiment_result = sentiment_model(user_review)[0]
        sentiment_label = label_map[sentiment_result["label"]]
        sentiment_score = sentiment_result["score"]

        emotion_results = emotion_model(user_review)[0]
        emotion_dict = {e["label"]: round(e["score"] * 100, 2) for e in emotion_results}

        rating_sentiment = rating_to_sentiment(user_rating)

        st.subheader("🧠 Sentiment Result")
        st.write(f"**Predicted Sentiment:** {sentiment_label}")
        st.write(f"**Confidence:** {sentiment_score:.2f}")
        st.write(f"**Rating-based Sentiment:** {rating_sentiment}")

        st.subheader("🎭 Emotion Detection")
        import pandas as pd
        import plotly.express as px

        df_emotion = pd.DataFrame({
            "Emotion": [f"{emoji_map.get(k,'')} {k.capitalize()}" for k in emotion_dict],
            "Score (%)": list(emotion_dict.values())
        }).sort_values("Score (%)")

        fig = px.bar(
            df_emotion,
            x="Score (%)",
            y="Emotion",
            orientation="h",
            text="Score (%)",
            title="Emotion Confidence (%)"
        )
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig.update_layout(xaxis_range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("⚠️ Sentiment vs Rating Check")
        if sentiment_label != rating_sentiment:
            st.warning("Mismatch detected between AI sentiment and user rating!")
        else:
            st.success("Sentiment matches rating.")
