import streamlit as st
import pandas as pd
from transformers import pipeline
from sklearn.metrics import confusion_matrix

st.set_page_config(page_title="Batch Analysis", layout="wide")
st.header("📁 Batch Review Analysis")

label_map = {"LABEL_0":"negative","LABEL_1":"neutral","LABEL_2":"positive"}

@st.cache_resource
def load_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

model = load_model()

def rating_to_sentiment(r): return "negative" if r<=2 else "neutral" if r==3 else "positive"

file = st.file_uploader("Upload CSV file with reviews", type=["csv"])
if file:
    df = pd.read_csv(file)
    st.dataframe(df.head())

    text_col = st.selectbox("Select Review Column", df.columns)
    rating_col = st.selectbox("Select Rating Column", df.columns)

    if st.button("Analyze Dataset"):
        texts = df[text_col].astype(str).tolist()
        preds = model(texts)

        df["AI Sentiment"] = [label_map[p["label"]] for p in preds]
        df["Rating Sentiment"] = df[rating_col].apply(rating_to_sentiment)

        st.subheader("📊 Batch Summary")
        counts = df["AI Sentiment"].value_counts()
        st.bar_chart(counts)

        st.subheader("⚠️ Confusion Matrix")
        cm = confusion_matrix(df["Rating Sentiment"], df["AI Sentiment"], labels=["negative","neutral","positive"])
        st.dataframe(pd.DataFrame(cm, index=["Rating Neg","Rating Neu","Rating Pos"],
                                  columns=["AI Neg","AI Neu","AI Pos"]))
