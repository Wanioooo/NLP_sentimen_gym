import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_models, batch_predict, fetch_tweets, label_map, emoji_map

st.set_page_config(page_title="Social Media Analysis", layout="wide")
st.header("📱 Social Media Feed Analysis (Simulated Twitter/X)")

st.caption(
    "Social media posts are simulated using pre-collected data due to API and platform limitations."
)

# -------------------------------
# Load models
# -------------------------------
sentiment_model, emotion_model = load_models()

# -------------------------------
# User inputs
# -------------------------------
query = st.text_input("Search keyword or hashtag:", value="PureGym")
tweet_limit = st.slider(
    "Number of posts to analyze:",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

if st.button("Analyze Social Media Feed"):
    with st.spinner("Analyzing social media sentiment and emotions..."):
        # Fetch posts (simulate Twitter/X)
        posts = fetch_tweets(query, tweet_limit)

        # -------------------------------
        # Sentiment Prediction
        # -------------------------------
        sentiment_preds = batch_predict(sentiment_model, posts)
        sentiments = [label_map[s["label"]] for s in sentiment_preds]

        # -------------------------------
        # Emotion Prediction
        # -------------------------------
        emotion_preds = batch_predict(emotion_model, posts)
        dominant_emotions = []
        for emo_list in emotion_preds:
            top_emotion = max(emo_list, key=lambda x: x["score"])
            dominant_emotions.append(top_emotion["label"])

        # -------------------------------
        # Create DataFrame
        # -------------------------------
        df_social = pd.DataFrame({
            "Post": posts,
            "Sentiment": sentiments,
            "Dominant Emotion": dominant_emotions
        })

    st.success("Social media analysis completed!")

    # ===============================
    # SENTIMENT DISTRIBUTION
    # ===============================
    st.subheader("📊 Sentiment Distribution")
    sent_dist = df_social["Sentiment"].value_counts().reset_index()
    sent_dist.columns = ["Sentiment", "Count"]

    fig_sent = px.pie(
        sent_dist,
        names="Sentiment",
        values="Count",
        title="Social Media Sentiment Distribution"
    )
    st.plotly_chart(fig_sent, use_container_width=True)

    # ===============================
    # EMOTION DISTRIBUTION
    # ===============================
    st.subheader("🎭 Emotion Distribution")
    emo_dist = df_social["Dominant Emotion"].value_counts().reset_index()
    emo_dist.columns = ["Emotion", "Count"]

    emo_dist["Emotion"] = emo_dist["Emotion"].apply(
        lambda x: f"{emoji_map.get(x,'')} {x.capitalize()}"
    )

    fig_emo = px.bar(
        emo_dist,
        x="Emotion",
        y="Count",
        text="Count",
        title="Dominant Emotions in Social Media Posts"
    )
    fig_emo.update_traces(textposition="outside")
    st.plotly_chart(fig_emo, use_container_width=True)

    # ===============================
    # DOMINANT INSIGHT
    # ===============================
    st.subheader("🧠 Key Insight")
    dominant_sentiment = sent_dist.iloc[0]["Sentiment"]
    dominant_emotion = emo_dist.iloc[0]["Emotion"]

    st.info(
        f"Overall social media discussion is *{dominant_sentiment.upper()}*, "
        f"with dominant emotion *{dominant_emotion}*."
    )

    # ===============================
    # DISPLAY POSTS
    # ===============================
    st.subheader("📝 Social Media Posts with AI Analysis")
    st.dataframe(df_social)
