import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_content_features(df):
    """Combine product features into one text for similarity matching."""
    df = df.copy()
    df["features"] = (
        df["product_name"] + " " +
        df["category"] + " " +
        df["review_text"]
    )
    return df

def get_content_based_recommendations(df, product_name, top_n=3):
    """
    Content-based filtering:
    Recommends products similar to the selected product
    based on name, category, and review text.
    """
    df = build_content_features(df)

    # Build TF-IDF matrix
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["features"])

    # Compute cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find index of selected product
    indices = pd.Series(df.index, index=df["product_name"])

    if product_name not in indices:
        return pd.DataFrame()

    idx = indices[product_name]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Exclude the product itself, get top N
    sim_scores = [s for s in sim_scores if s[0] != idx][:top_n]
    product_indices = [s[0] for s in sim_scores]
    similarity_scores = [round(s[1] * 100, 1) for s in sim_scores]

    result = df.iloc[product_indices][
        ["product_name", "category", "price", "rating"]
    ].copy()
    result["similarity_%"] = similarity_scores
    return result.reset_index(drop=True)

def get_top_rated_products(df, category="All", top_n=5):
    """
    Popularity-based recommendation:
    Returns top rated products, optionally filtered by category.
    """
    if category != "All":
        df = df[df["category"] == category]

    top = df.sort_values(
        by=["rating", "num_reviews"],
        ascending=False
    ).head(top_n)

    return top[["product_name", "category", "price", "rating", "num_reviews"]].reset_index(drop=True)

def get_budget_recommendations(df, max_price, top_n=3):
    """
    Budget-based recommendation:
    Returns best rated products within a price range.
    """
    budget_df = df[df["price"] <= max_price]

    if budget_df.empty:
        return pd.DataFrame()

    result = budget_df.sort_values(
        by=["rating", "num_reviews"],
        ascending=False
    ).head(top_n)

    return result[["product_name", "category", "price", "rating"]].reset_index(drop=True)

def explain_recommendation(product_name, recommended_name, category, rating, price):
    """
    Generate a human-readable explanation for why a product was recommended.
    No LLM needed — rule-based explanation.
    """
    explanation = (
        f"We recommended **{recommended_name}** because:\n"
        f"- It belongs to the same category: **{category}**\n"
        f"- It has a strong customer rating of **{rating}/5**\n"
        f"- It is priced at **₹{price:,}**\n"
        f"- Customers who viewed **{product_name}** also liked this product"
    )
    return explanation