import pandas as pd
from transformers import pipeline

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

def batch_predict(model, texts, batch_size=8):
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        preds = model(batch, truncation=True, max_length=256)
        results.extend(preds)
    return results

def rating_to_sentiment(r):
    if r <= 2:
        return "negative"
    elif r == 3:
        return "neutral"
    else:
        return "positive"

def clean_text(t):
    return str(t).strip()

def fetch_tweets(query, limit=20):
    try:
        df = pd.read_csv("sample_tweets.csv")
        tweets = df["tweet"].astype(str).tolist()
    except:
        tweets = [
            "PureGym has amazing equipment and friendly staff!",
            "Too crowded during peak hours.",
            "Affordable membership and clean gym.",
            "Terrible customer service experience.",
            "Love the 24/7 access!",
            "Machines broken for weeks.",
            "Great value for money.",
            "Staff were rude and unhelpful.",
            "Best gym experience so far.",
            "Gym is okay but overcrowded."
        ]
    return tweets[:limit]
