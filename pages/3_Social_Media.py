# ======================================================
# 🔴 SIMULATED LIVE SOCIAL MEDIA FEED ANALYSIS
# ======================================================

import streamlit as st
from utils import load_models, batch_predict, rating_to_sentiment, clean_text, label_map, emoji_map

st.set_page_config(page_title="Social Media Analysis", layout="wide")

st.header("🔴 Live Social Media Feed Analysis (Simulated Twitter/X)")

st.caption(
    "⚠️ Live tweets are simulated using a pre-collected dataset due to API and platform limitations."
)

query = st.text_input(
    "Search keyword or hashtag:",
    value="PureGym"
)

tweet_limit = st.slider(
    "Number of social media posts to analyze:",
    min_value=5,
    max_value=50,
    value=10,
    step=5
)

if st.button("Analyze Social Media Feed"):
    with st.spinner("Analyzing social media sentiment..."):
        tweets = fetch_tweets(query, tweet_limit)
        sentiment_preds = batch_predict(sentiment_model, tweets)

        sentiments = [label_map[s["label"]] for s in sentiment_preds]

        df_social = pd.DataFrame({
            "Post": tweets,
            "Predicted Sentiment": sentiments
        })

    st.success("Social media sentiment analysis completed!")

    # -------------------------------
    # Sentiment Distribution
    # -------------------------------
    st.subheader("📊 Social Media Sentiment Distribution")

    sentiment_counts = df_social["Predicted Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]

    fig = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Sentiment Distribution from Social Media Posts"
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # Display Posts
    # -------------------------------
    st.subheader("📝 Social Media Posts & AI Sentiment")
    st.dataframe(df_social)
