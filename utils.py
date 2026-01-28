# ==============================
# utils.py
# ==============================

import pandas as pd
from transformers import pipeline

# -------------------------------
# LABEL & EMOJI MAPS
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

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def batch_predict(pipeline_model, texts, batch_size=8):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        preds = pipeline_model(batch, truncation=True, max_length=256)
        results.extend(preds)
    return results

def rating_to_sentiment(rating):
    if rating <= 2:
        return "negative"
    elif rating == 3:
        return "neutral"
    else:
        return "positive"

def clean_text(text):
    return str(text).strip()

def fetch_tweets(query, limit=50):
    try:
        df = pd.read_csv("sample_tweets.csv")
        tweets = df["tweet"].astype(str).tolist()
    except FileNotFoundError:
        # fallback simulated tweets
        tweets = [
            "PureGym has amazing equipment and friendly staff!",
            "Too crowded during peak hours, very frustrating.",
            "Affordable gym membership and clean facilities.",
            "Terrible customer service, very disappointed.",
            "Love the 24/7 access, makes life so much easier.",
            "Machines were broken for weeks.",
            "Great value for money and motivating environment.",
            "Staff were rude and unhelpful.",
            "Best gym experience I've had so far!",
            "Gym is okay but can be overcrowded sometimes."
        ]
    return tweets[:limit]
