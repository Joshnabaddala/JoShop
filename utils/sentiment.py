from textblob import TextBlob
import pandas as pd

def analyze_sentiment(text):
    """Analyze sentiment of a single review."""
    blob = TextBlob(str(text))
    polarity = blob.sentiment.polarity

    if polarity > 0.2:
        sentiment = "Positive"
        emoji = "😊"
        color = "green"
    elif polarity < -0.1:
        sentiment = "Negative"
        emoji = "😞"
        color = "red"
    else:
        sentiment = "Neutral"
        emoji = "😐"
        color = "orange"

    return {
        "sentiment": sentiment,
        "emoji": emoji,
        "color": color,
        "polarity": round(polarity, 2),
        "subjectivity": round(blob.sentiment.subjectivity, 2)
    }

def analyze_all_reviews(df):
    """Analyze sentiment for all products in dataframe."""
    sentiments = []
    for _, row in df.iterrows():
        result = analyze_sentiment(row["review_text"])
        result["product_name"] = row["product_name"]
        result["rating"] = row["rating"]
        sentiments.append(result)
    return pd.DataFrame(sentiments)

def get_sentiment_summary(df):
    """Get overall sentiment breakdown."""
    sentiment_df = analyze_all_reviews(df)
    summary = sentiment_df["sentiment"].value_counts().to_dict()
    return {
        "Positive": summary.get("Positive", 0),
        "Neutral": summary.get("Neutral", 0),
        "Negative": summary.get("Negative", 0),
        "total": len(sentiment_df)
    }

def detect_fake_review(review_text):
    """
    Basic fake review detection using heuristics.
    Flags reviews that are too short, repetitive, or overly generic.
    """
    text = str(review_text).strip()
    flags = []

    # Too short
    if len(text.split()) < 5:
        flags.append("Review is too short")

    # All caps (shouting = suspicious)
    if text.isupper():
        flags.append("Review is in all caps")

    # Overly generic phrases
    generic_phrases = [
        "good product", "nice product", "best product",
        "very good", "super", "excellent product", "perfect"
    ]
    lower_text = text.lower()
    matches = [p for p in generic_phrases if p in lower_text]
    if len(matches) >= 2:
        flags.append("Review contains generic phrases")

    # Repetitive words
    words = lower_text.split()
    if len(words) > 3:
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio < 0.5:
            flags.append("Review has repetitive words")

    is_fake = len(flags) > 0
    return {
        "is_suspicious": is_fake,
        "flags": flags,
        "verdict": "⚠️ Suspicious Review" if is_fake else "✅ Looks Genuine"
    }