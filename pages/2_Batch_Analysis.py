import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from sklearn.metrics import confusion_matrix

st.set_page_config(page_title="Batch Review Analysis", layout="wide")
st.header("📁 Batch Review Analysis (CSV Upload)")

# -------------------------------
# Load Models
# -------------------------------
@st.cache_resource
def load_models():
    sentiment_model = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment"
    )
    emotion_model = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=5
    )
    return sentiment_model, emotion_model

sentiment_model, emotion_model = load_models()

# -------------------------------
# Helper Functions
# -------------------------------
label_map = {"LABEL_0":"negative","LABEL_1":"neutral","LABEL_2":"positive"}
emoji_map = {
    "joy": "😄",
    "anger": "😡",
    "sadness": "😢",
    "fear": "😨",
    "surprise": "😲",
    "disgust": "🤢",
    "neutral": "😐"
}

def rating_to_sentiment(r):
    if r <= 2:
        return "negative"
    elif r == 3:
        return "neutral"
    else:
        return "positive"

def clean_text(text):
    return str(text).strip()

def batch_predict(pipeline_model, texts, batch_size=8):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        preds = pipeline_model(batch, truncation=True, max_length=256)
        results.extend(preds)
    return results

def batch_emotion_predict(pipeline_model, texts, batch_size=8):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        preds = pipeline_model(batch, truncation=True, max_length=256)
        results.extend(preds)
    return results

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload a CSV file containing reviews:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded dataset:")
    st.dataframe(df.head())

    text_column = st.selectbox("Select the review text column:", df.columns)
    rating_column = st.selectbox("Select the rating column:", df.columns)

    # Slider to limit rows
    max_rows = st.slider(
        "Limit number of reviews to analyze (for performance):",
        min_value=100,
        max_value=min(2000, len(df)),
        value=500,
        step=100
    )

    if st.button("Analyze Dataset"):
        with st.spinner("Analyzing reviews... This may take a few moments."):
            # Prepare text
            texts = df[text_column].astype(str).apply(clean_text).tolist()[:max_rows]

            # Predict sentiment
            sentiment_preds = batch_predict(sentiment_model, texts)

            # Predict emotions
            emotion_preds = batch_emotion_predict(emotion_model, texts)

            # Prepare results dataframe
            df_result = df.head(max_rows).copy()
            df_result["ai_sentiment"] = [label_map[s["label"]] for s in sentiment_preds]
            df_result["ai_sentiment_score"] = [s["score"] for s in sentiment_preds]
            df_result["rating_sentiment"] = df_result[rating_column].apply(rating_to_sentiment)

            # Top emotion per review
            df_result["emotion"] = [max(e, key=lambda x: x["score"])["label"] for e in emotion_preds]
            df_result["emotion_score"] = [max(e, key=lambda x: x["score"])["score"] for e in emotion_preds]

        st.success("Batch analysis completed!")
        st.dataframe(df_result.head())

        # -------------------------------
        # Sentiment Distribution Charts
        # -------------------------------
        st.subheader("📊 Sentiment Distribution")
        sentiment_counts = df_result["ai_sentiment"].value_counts()
        sentiment_percent = df_result["ai_sentiment"].value_counts(normalize=True)*100

        # Pie chart
        fig_pie = px.pie(
            names=sentiment_counts.index,
            values=sentiment_counts.values,
            title="AI Sentiment Distribution (Pie Chart)"
        )
        st.plotly_chart(fig_pie, use_container_width=True)


        # -------------------------------
        # Emotion Distribution Chart
        # -------------------------------
        st.subheader("🎭 Dominant Emotion Distribution")
        emotion_counts = df_result["emotion"].value_counts()
        emotion_percent = df_result["emotion"].value_counts(normalize=True)*100
        df_emotion_chart = pd.DataFrame({
            "Emotion": [f"{emoji_map.get(e,'')} {e}" for e in emotion_counts.index],
            "Count": emotion_counts.values,
            "Percentage": emotion_percent.values*100
        })

        fig_emotion = px.bar(
            df_emotion_chart,
            x="Emotion",
            y="Count",
            text=df_emotion_chart["Percentage"].apply(lambda x: f"{x:.1f}%"),
            title="Emotion Counts (%)"
        )
        fig_emotion.update_traces(textposition="outside")
        st.plotly_chart(fig_emotion, use_container_width=True)

        # -------------------------------
        # Confusion Matrix
        # -------------------------------
        st.subheader("⚠️ Rating vs AI Sentiment Confusion Matrix")
        cm = confusion_matrix(
            df_result["rating_sentiment"],
            df_result["ai_sentiment"],
            labels=["negative", "neutral", "positive"]
        )
        cm_df = pd.DataFrame(
            cm,
            index=["Rating Negative", "Rating Neutral", "Rating Positive"],
            columns=["AI Negative", "AI Neutral", "AI Positive"]
        )
        st.dataframe(cm_df)

        mismatch_rate = (df_result["rating_sentiment"] != df_result["ai_sentiment"]).mean() * 100
        st.warning(f"{mismatch_rate:.1f}% of reviews show sentiment–rating mismatch")

        # -------------------------------
        # Download CSV
        # -------------------------------
        csv = df_result.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Results as CSV",
            csv,
            "sentiment_emotion_results.csv",
            "text/csv"
        )
else:
    st.info("⬆️ Upload a CSV file to begin analysis")
