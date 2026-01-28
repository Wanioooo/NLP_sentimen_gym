import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_models, batch_predict, fetch_tweets, label_map

st.set_page_config(page_title="Social Media Analysis", layout="wide")
st.header("🔴 Social Media Feed Analysis (Simulated)")

sentiment_model, emotion_model = load_models()

query = st.text_input("Search keyword or hashtag:", value="PureGym")
tweet_limit = st.slider("Number of posts to analyze:", min_value=5, max_value=50, value=10, step=5)

if st.button("Analyze Social Media Feed"):
    with st.spinner("Analyzing social media sentiment..."):
        tweets = fetch_tweets(query, tweet_limit)
        sentiment_preds = batch_predict(sentiment_model, tweets)
        sentiments = [label_map[s["label"]] for s in sentiment_preds]

        df_social = pd.DataFrame({"Post": tweets, "Predicted Sentiment": sentiments})

    st.success("Analysis completed!")

    # Pie chart
    st.subheader("📊 Sentiment Distribution")
    sentiment_counts = df_social["Predicted Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig = px.pie(sentiment_counts, names="Sentiment", values="Count",
                 title="Social Media Sentiment Distribution")
    st.plotly_chart(fig, use_container_width=True)

    # Display posts
    st.subheader("📝 Recent Posts & AI Sentiment")
    st.dataframe(df_social)
