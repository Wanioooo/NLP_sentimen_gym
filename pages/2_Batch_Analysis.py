import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import confusion_matrix
from utils import load_models, batch_predict, clean_text, label_map, rating_to_sentiment

st.set_page_config(page_title="Batch Review Analysis", layout="wide")
st.header("📁 Batch Review Analysis (CSV Upload)")

# Load models
sentiment_model, emotion_model = load_models()

uploaded_file = st.file_uploader("Upload a CSV file containing reviews:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded dataset:")
    st.dataframe(df.head())

    text_column = st.selectbox("Select the review text column:", df.columns)
    rating_column = st.selectbox("Select the rating column:", df.columns)

    max_rows = st.slider("Limit number of reviews to analyze:", min_value=100,
                         max_value=min(2000, len(df)), value=500, step=100)

    if st.button("Analyze Dataset"):
        with st.spinner("Analyzing reviews..."):
            texts = df[text_column].astype(str).apply(clean_text).tolist()[:max_rows]
            sentiment_preds = batch_predict(sentiment_model, texts)

            df_result = df.head(max_rows).copy()
            df_result["ai_sentiment"] = [label_map[s["label"]] for s in sentiment_preds]
            df_result["ai_sentiment_score"] = [s["score"] for s in sentiment_preds]
            df_result["rating_sentiment"] = df_result[rating_column].apply(rating_to_sentiment)

        st.success("Batch analysis completed!")
        st.dataframe(df_result.head())

        # Summary
        st.subheader("📊 Batch Summary")
        sentiment_counts = df_result["ai_sentiment"].value_counts(normalize=True) * 100
        st.write(f"Total reviews analyzed: {len(df_result)}")
        st.write(f"Positive reviews: {sentiment_counts.get('positive', 0):.2f}%")
        st.write(f"Negative reviews: {sentiment_counts.get('negative', 0):.2f}%")

        # Confusion Matrix
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

        # Download results
        csv = df_result.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Results as CSV", csv, "sentiment_results.csv", "text/csv")
else:
    st.info("⬆️ Upload a CSV file to begin analysis"
