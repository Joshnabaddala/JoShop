import pandas as pd
import os

def load_data():
    """Load and clean the product dataset."""
    data_path = os.path.join("data", "products.csv")
    
    # If real data not available, use sample data
    if not os.path.exists(data_path):
        return get_sample_data()
    
    df = pd.read_csv(data_path)
    df = df.dropna(subset=["product_name", "review_text"])
    df = df.reset_index(drop=True)
    return df

def get_sample_data():
    """Sample e-commerce data for demo purposes."""
    data = {
        "product_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "product_name": [
            "boAt Rockerz 450 Bluetooth Headphones",
            "Samsung Galaxy Buds2 Pro",
            "Sony WH-1000XM5 Noise Cancelling",
            "JBL Tune 510BT Wireless",
            "Apple AirPods Pro 2nd Gen",
            "Noise ColorFit Pro 4 Smartwatch",
            "Fire-Boltt Phoenix Smart Watch",
            "Samsung Galaxy Watch 5",
            "Apple Watch Series 9",
            "Amazfit GTR 4 Smartwatch"
        ],
        "category": [
            "Headphones", "Headphones", "Headphones", "Headphones", "Headphones",
            "Smartwatch", "Smartwatch", "Smartwatch", "Smartwatch", "Smartwatch"
        ],
        "price": [1299, 12999, 29990, 2999, 24900, 3999, 2499, 27999, 41900, 14999],
        "rating": [4.2, 4.5, 4.7, 4.1, 4.8, 4.0, 3.9, 4.4, 4.9, 4.3],
        "review_text": [
            "Great sound quality for the price. Battery life is excellent. Comfortable to wear for long hours.",
            "Amazing sound, great ANC. A bit expensive but worth it. Fits perfectly in ears.",
            "Best noise cancelling headphones I have used. Premium build quality. Highly recommended.",
            "Good budget headphones. Sound is decent. Battery lasts long. Good value for money.",
            "Perfect sound, seamless Apple integration. Noise cancellation is top notch. Premium product.",
            "Good smartwatch for the price. Health tracking is accurate. Battery life could be better.",
            "Decent budget smartwatch. Many features at low price. Build quality is average.",
            "Excellent smartwatch. Smooth performance. Health features are very accurate and reliable.",
            "Best smartwatch available. Seamless integration with iPhone. Premium build and great display.",
            "Great battery life. Accurate health tracking. Good display. Value for money smartwatch."
        ],
        "num_reviews": [15420, 3210, 8930, 12100, 25600, 9870, 18340, 5620, 31200, 7890]
    }
    return pd.DataFrame(data)

def get_categories(df):
    """Get unique product categories."""
    return list(df["category"].unique())

def filter_by_category(df, category):
    """Filter products by category."""
    if category == "All":
        return df
    return df[df["category"] == category].reset_index(drop=True)

def search_products(df, query):
    """Search products by name or category."""
    query = query.lower()
    mask = (
        df["product_name"].str.lower().str.contains(query) |
        df["category"].str.lower().str.contains(query)
    )
    return df[mask].reset_index(drop=True)