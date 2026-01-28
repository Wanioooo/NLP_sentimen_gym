# ======================================================
# 📁 BATCH REVIEW ANALYSIS
# ======================================================

import streamlit as st
from utils import load_models, batch_predict, rating_to_sentiment, clean_text, label_map, emoji_map

st.set_page_config(page_title="Batch Analysis", layout="wide")

st.header("📁 Batch Review Analysis (CSV Upload)")

uploaded_file = st.file_uploader("Upload a CSV file containing reviews:", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of uploaded dataset:")
    st.dataframe(df.head())

    # Select review text column
    text_column = st.selectbox(
        "Select the column that contains review text:",
        df.columns
    )

    # Select rating column
    rating_column = st.selectbox(
        "Select the column that contains ratings (1–5):",
        df.columns
    )

    # Slider to limit rows for performance
    max_rows = st.slider(
        "Limit number of reviews to analyze (for performance):",
        min_value=100,
        max_value=min(2000, len(df)),
        value=500,
        step=100
    )

    if st.button("Analyze Dataset"):
        with st.spinner("Analyzing reviews... Please wait."):
            # Prepare text for prediction
            texts = df[text_column].astype(str).apply(clean_text).tolist()[:max_rows]

            # Predict AI sentiment
            sentiment_preds = batch_predict(sentiment_model, texts)

            # Create result dataframe
            df_result = df.head(max_rows).copy()
            df_result["ai_sentiment"] = [label_map[s["label"]] for s in sentiment_preds]
            df_result["ai_sentiment_score"] = [s["score"] for s in sentiment_preds]

            # Create rating sentiment
            df_result["rating_sentiment"] = df_result[rating_column].apply(rating_to_sentiment)

        st.success("Batch analysis completed!")
        st.dataframe(df_result.head())

        # -------------------------------
        # Batch Summary Statistics
        # -------------------------------
        st.subheader("📊 Batch Analysis Summary")
        total_reviews = len(df_result)
        sentiment_counts = df_result["ai_sentiment"].value_counts(normalize=True) * 100

        positive_pct = sentiment_counts.get("positive", 0)
        negative_pct = sentiment_counts.get("negative", 0)
        dominant_emotion = "N/A"  # Optional: can compute if emotion predictions are added

        st.write(f"*Total reviews analyzed:* {total_reviews}")
        st.write(f"*Positive reviews:* {positive_pct:.2f}%")
        st.write(f"*Negative reviews:* {negative_pct:.2f}%")
        st.write(f"*Dominant emotion:* {dominant_emotion}")

        if positive_pct > negative_pct:
            st.info("📌 Overall sentiment trend: Mostly Positive")
        else:
            st.info("📌 Overall sentiment trend: Mostly Negative")

        csv = df_result.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Results as CSV",
            csv,
            "sentiment_emotion_results.csv",
            "text/csv"
        )

        # -------------------------------
        # CONFUSION MATRIX
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

else:
    st.info("⬆️ Upload a CSV file to begin analysis")
