import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_models, label_map, emoji_map, rating_to_sentiment

st.set_page_config(page_title="Single Review", layout="wide")

st.markdown("""<style>...</style>""", unsafe_allow_html=True)

st.header("✍️ Single Review Analysis")

sentiment_model, emotion_model = load_models()

review = st.text_area("Enter customer review:")
rating = st.radio("Rating", [1,2,3,4,5], horizontal=True)

if st.button("Analyze Review"):
    s = sentiment_model(review)[0]
    e = emotion_model(review)[0]

    st.subheader("🧠 Sentiment")
    st.success(f"{label_map[s['label']]} ({s['score']:.2f})")

    df = pd.DataFrame({
        "Emotion": [emoji_map[x["label"]] + " " + x["label"] for x in e],
        "Score (%)": [x["score"]*100 for x in e]
    })

    fig = px.bar(df, x="Score (%)", y="Emotion", orientation="h")
    fig.update_layout(plot_bgcolor="#020617", paper_bgcolor="#020617",
                      font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    if label_map[s["label"]] != rating_to_sentiment(rating):
        st.warning("Mismatch between rating and sentiment")
