import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_models, batch_predict, fetch_tweets, label_map, emoji_map

st.set_page_config(page_title="Social Media", layout="wide")

st.markdown("""
<style>
.stApp { background-color:#0F172A; color:#E5E7EB; }
h1,h2,h3 { color:#22C55E; }
</style>
""", unsafe_allow_html=True)

st.header("🔴 Social Media Sentiment & Emotion Analysis")

sentiment_model, emotion_model = load_models()

limit = st.slider("Number of posts", 5, 30, 10)

if st.button("Analyze Social Media"):
    posts = fetch_tweets("PureGym", limit)

    s_preds = batch_predict(sentiment_model, posts)
    e_preds = batch_predict(emotion_model, posts)

    sentiments = [label_map[x["label"]] for x in s_preds]
    emotions = [max(e, key=lambda x: x["score"])["label"] for e in e_preds]

    df = pd.DataFrame({
        "Post": posts,
        "Sentiment": sentiments,
        "Emotion": emotions
    })

    st.subheader("📊 Sentiment Distribution")
    fig1 = px.pie(df, names="Sentiment")
    fig1.update_layout(plot_bgcolor="#020617", paper_bgcolor="#020617",
                       font_color="white")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🎭 Emotion Distribution")
    emo_df = df["Emotion"].value_counts().reset_index()
    emo_df.columns = ["Emotion","Count"]
    emo_df["Emotion"] = emo_df["Emotion"].apply(lambda x: emoji_map[x] + " " + x)

    fig2 = px.bar(emo_df, x="Emotion", y="Count")
    fig2.update_layout(plot_bgcolor="#020617", paper_bgcolor="#020617",
                       font_color="white")
    st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(df)
