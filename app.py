# ===============================
# PureGym Sentiment Analysis Dashboard
# Light Blue Theme (Readable & Clean)
# ===============================

import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from sklearn.metrics import confusion_matrix

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="PureGym Sentiment Dashboard",
    page_icon="🏋️",
    layout="wide"
)

# -------------------------------
# LIGHT BLUE THEME (PUT HERE)
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F0F9FF;
    color: #0F172A;
}

h1, h2, h3 {
    color: #0F172A;
    font-weight: 800;
}

section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: #E0F2FE !important;
}

div.stButton > button {
    background-color: #0284C7;
    color: white;
    font-weight: 700;
    border-radius: 10px;
    border: none;
    height: 3em;
}

div.stButton > button:hover {
    background-color: #0369A1;
}

textarea, input, select {
    background-color: white !important;
    color: #0F172A !important;
    border-radius: 8px !important;
    border: 1px solid #BAE6FD !important;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    border-left: 6px solid #0284C7;
}

[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 12px;
}

.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<div style="text-align:center; padding:30px;">
<h1>🏋️ PureGym Sentiment Analysis Dashboard</h1>
<p style="font-size:16px; color:#334155;">
AI-powered analysis of customer reviews using NLP
</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# LABEL MAPS
# -------------------------------
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

# -------------------------------
# LOAD MODELS
# -------------------------------
@st.cache_resource
def load_models():
    sentiment = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment"
    )

    emotion = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=5
    )
    return sentiment, emotion

sentiment_model, emotion_model = load_models()

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def rating_to_sentiment(r):
    if r <= 2:
        return "negative"
    elif r == 3:
        return "neutral"
    else:
        return "positive"

def batch_predict(model, texts, batch_size=8):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        preds = model(batch, truncation=True, max_length=256)
        results.extend(preds)
    return results

# ======================================================
# ✍️ SINGLE REVIEW ANALYSIS
# ======================================================
st.header("✍️ Single Review Analysis")

review = st.text_area("Enter a PureGym customer review:")

rating = st.radio(
    "Give a rating:",
    [1, 2, 3, 4, 5],
    format_func=lambda x: "⭐" * x,
    horizontal=True
)

if st.button("Analyze Review"):
    if review.strip():
        sent = sentiment_model(review)[0]
        sent_label = label_map[sent["label"]]
        sent_score = sent["score"]

        emotions = emotion_model(review)[0]
        emo_df = pd.DataFrame({
            "Emotion": [f"{emoji_map.get(e['label'],'')} {e['label'].title()}" for e in emotions],
            "Score (%)": [round(e["score"] * 100, 2) for e in emotions]
        })

        col1, col2, col3 = st.columns(3)
        col1.metric("AI Sentiment", sent_label.capitalize())
        col2.metric("Confidence", f"{sent_score:.2f}")
        col3.metric("Rating Sentiment", rating_to_sentiment(rating).capitalize())

        fig = px.bar(
            emo_df.sort_values("Score (%)"),
            x="Score (%)",
            y="Emotion",
            orientation="h",
            text="Score (%)",
            title="Emotion Detection"
        )
        fig.update_traces(texttemplate="%{text:.1f}%")
        st.plotly_chart(fig, use_container_width=True)

        if sent_label != rating_to_sentiment(rating):
            st.warning("⚠️ Sentiment does not match rating")
        else:
            st.success("✅ Sentiment matches rating")

# ======================================================
# 📁 BATCH CSV ANALYSIS
# ======================================================
st.header("📁 Batch Review Analysis")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    text_col = st.selectbox("Review text column", df.columns)
    rating_col = st.selectbox("Rating column (1–5)", df.columns)

    limit = st.slider("Limit rows", 100, min(2000, len(df)), 500, step=100)

    if st.button("Analyze Dataset"):
        texts = df[text_col].astype(str).tolist()[:limit]
        preds = batch_predict(sentiment_model, texts)

        result = df.head(limit).copy()
        result["ai_sentiment"] = [label_map[p["label"]] for p in preds]
        result["rating_sentiment"] = result[rating_col].apply(rating_to_sentiment)

        st.success("Batch analysis completed")
        st.dataframe(result.head())

        st.subheader("📊 Summary")
        counts = result["ai_sentiment"].value_counts()
        st.bar_chart(counts)

        st.subheader("⚠️ Confusion Matrix")
        cm = confusion_matrix(
            result["rating_sentiment"],
            result["ai_sentiment"],
            labels=["negative", "neutral", "positive"]
        )

        cm_df = pd.DataFrame(
            cm,
            index=["Rating Neg", "Rating Neu", "Rating Pos"],
            columns=["AI Neg", "AI Neu", "AI Pos"]
        )

        st.dataframe(cm_df)

else:
    st.info("⬆️ Upload a CSV file to start")
