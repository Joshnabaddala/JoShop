import streamlit as st
import pandas as pd
from utils.data_loader import load_data, get_categories, filter_by_category, search_products
from utils.sentiment import analyze_sentiment, detect_fake_review, get_sentiment_summary
from utils.recommender import get_content_based_recommendations, get_top_rated_products, get_budget_recommendations, explain_recommendation
from utils.llm_handler import summarize_reviews, shopping_assistant, analyze_review_with_ai

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="JoShop AI",
    page_icon="🛒",
    layout="wide"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #FF6B35;
        text-align: center;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF6B35;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: #fff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ── HEADER ──
st.markdown('<p class="main-header">🛒 JoShop AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered E-commerce Intelligence Engine</p>', unsafe_allow_html=True)

# ── LOAD DATA ──
df = load_data()

# ── SIDEBAR ──
st.sidebar.image("https://img.icons8.com/color/96/shopping-cart.png", width=80)
st.sidebar.title("JoShop AI")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🔍 Search & Recommend", "💬 AI Review Analyzer", "🤖 Shopping Assistant", "📊 Insights"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Baddala Jhoshna**")
st.sidebar.markdown("AI Engineer | Python Developer")

# ════════════════════════════════
# PAGE 1 — HOME
# ════════════════════════════════
if page == "🏠 Home":
    st.subheader("Welcome to JoShop AI 👋")
    st.write("Your intelligent shopping companion powered by AI and Machine Learning.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Products", len(df))
    with col2:
        st.metric("Categories", df["category"].nunique())
    with col3:
        st.metric("Avg Rating", f"{df['rating'].mean():.1f} ⭐")
    with col4:
        st.metric("Total Reviews", f"{df['num_reviews'].sum():,}")

    st.markdown("---")
    st.subheader("🔥 Top Rated Products")
    top_products = get_top_rated_products(df, top_n=5)
    for _, row in top_products.iterrows():
        with st.container():
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1:
                st.markdown(f"**{row['product_name']}**")
            with c2:
                st.markdown(f"📦 {row['category']}")
            with c3:
                st.markdown(f"⭐ {row['rating']}")
            with c4:
                st.markdown(f"₹{row['price']:,}")
        st.divider()

    st.subheader("✨ What JoShop AI Can Do")
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.info("🔍 **Smart Search**\nFind products instantly")
    with f2:
        st.success("🤖 **AI Recommendations**\nPersonalized suggestions")
    with f3:
        st.warning("💬 **Review Analysis**\nAI-powered insights")
    with f4:
        st.error("🚨 **Fake Detection**\nSpot suspicious reviews")

# ════════════════════════════════
# PAGE 2 — SEARCH & RECOMMEND
# ════════════════════════════════
elif page == "🔍 Search & Recommend":
    st.subheader("🔍 Search Products & Get AI Recommendations")

    tab1, tab2, tab3 = st.tabs(["Search Products", "Similar Products", "Budget Finder"])

    with tab1:
        search_query = st.text_input("Search for a product...", placeholder="e.g. headphones, smartwatch")
        category_filter = st.selectbox("Filter by Category", ["All"] + list(get_categories(df)))

        if search_query:
            results = search_products(df, search_query)
        else:
            results = filter_by_category(df, category_filter)

        st.markdown(f"**{len(results)} products found**")
        for _, row in results.iterrows():
            with st.expander(f"🛍️ {row['product_name']} — ₹{row['price']:,} | ⭐ {row['rating']}"):
                sentiment = analyze_sentiment(row["review_text"])
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Category:** {row['category']}")
                    st.write(f"**Price:** ₹{row['price']:,}")
                    st.write(f"**Rating:** ⭐ {row['rating']}")
                    st.write(f"**Reviews:** {row['num_reviews']:,}")
                with col2:
                    st.write(f"**Sentiment:** {sentiment['emoji']} {sentiment['sentiment']}")
                    st.write(f"**Polarity Score:** {sentiment['polarity']}")
                    st.write(f"**Review:** {row['review_text'][:150]}...")

    with tab2:
        st.write("Select a product to get AI-powered similar product recommendations")
        selected = st.selectbox("Choose a product", df["product_name"].tolist())

        if st.button("🔍 Find Similar Products"):
            recs = get_content_based_recommendations(df, selected, top_n=3)
            if not recs.empty:
                st.success(f"Products similar to **{selected}**:")
                for _, row in recs.iterrows():
                    explanation = explain_recommendation(
                        selected, row["product_name"],
                        row["category"], row["rating"], row["price"]
                    )
                    with st.expander(f"✅ {row['product_name']} — {row['similarity_%']}% match"):
                        st.markdown(explanation)
                        st.write(f"⭐ Rating: {row['rating']} | 💰 Price: ₹{row['price']:,}")
            else:
                st.warning("No similar products found.")

    with tab3:
        st.write("Find the best products within your budget")
        budget = st.slider("Your Budget (₹)", min_value=500, max_value=50000,
                          value=5000, step=500)
        if st.button("🎯 Find Best Products in Budget"):
            budget_recs = get_budget_recommendations(df, budget, top_n=3)
            if not budget_recs.empty:
                st.success(f"Best products under ₹{budget:,}:")
                st.dataframe(budget_recs, use_container_width=True)
            else:
                st.warning(f"No products found under ₹{budget:,}")

# ════════════════════════════════
# PAGE 3 — AI REVIEW ANALYZER
# ════════════════════════════════
elif page == "💬 AI Review Analyzer":
    st.subheader("💬 AI-Powered Review Analyzer")

    tab1, tab2 = st.tabs(["Analyze a Review", "Fake Review Detector"])

    with tab1:
        selected_product = st.selectbox("Select Product", df["product_name"].tolist())
        product_row = df[df["product_name"] == selected_product].iloc[0]

        st.write(f"**Review:** {product_row['review_text']}")
        sentiment = analyze_sentiment(product_row["review_text"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sentiment", f"{sentiment['emoji']} {sentiment['sentiment']}")
        with col2:
            st.metric("Polarity", sentiment["polarity"])
        with col3:
            st.metric("Subjectivity", sentiment["subjectivity"])

        if st.button("🤖 Deep AI Analysis"):
            with st.spinner("AI is analyzing the review..."):
                ai_analysis = analyze_review_with_ai(product_row["review_text"])
                st.markdown("### AI Analysis Result:")
                st.markdown(ai_analysis)

        if st.button("📝 Summarize Review with AI"):
            with st.spinner("Summarizing..."):
                summary = summarize_reviews(selected_product, product_row["review_text"])
                st.markdown("### AI Summary:")
                st.info(summary)

    with tab2:
        st.write("Paste any review below to check if it looks suspicious")
        user_review = st.text_area("Paste a review here...", height=100)
        if st.button("🚨 Check Review"):
            if user_review:
                result = detect_fake_review(user_review)
                if result["is_suspicious"]:
                    st.error(f"**{result['verdict']}**")
                    for flag in result["flags"]:
                        st.warning(f"⚠️ {flag}")
                else:
                    st.success(f"**{result['verdict']}**")
            else:
                st.warning("Please paste a review first.")

# ════════════════════════════════
# PAGE 4 — SHOPPING ASSISTANT
# ════════════════════════════════
elif page == "🤖 Shopping Assistant":
    st.subheader("🤖 JoShop AI Shopping Assistant")
    st.write("Ask me anything about products!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Show chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    user_input = st.chat_input("Ask me about products, prices, recommendations...")

    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Build product context
        product_context = df[["product_name", "category", "price", "rating"]].to_string()

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = shopping_assistant(user_input, product_context)
                st.write(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})

# ════════════════════════════════
# PAGE 5 — INSIGHTS
# ════════════════════════════════
elif page == "📊 Insights":
    st.subheader("📊 Product Insights Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Price Distribution by Category")
        price_data = df.groupby("category")["price"].mean().reset_index()
        st.bar_chart(price_data.set_index("category"))

    with col2:
        st.markdown("#### Average Rating by Category")
        rating_data = df.groupby("category")["rating"].mean().reset_index()
        st.bar_chart(rating_data.set_index("category"))

    st.markdown("---")
    st.markdown("#### Sentiment Overview")
    summary = get_sentiment_summary(df)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success(f"😊 Positive Reviews: {summary['Positive']}")
    with c2:
        st.warning(f"😐 Neutral Reviews: {summary['Neutral']}")
    with c3:
        st.error(f"😞 Negative Reviews: {summary['Negative']}")

    st.markdown("---")
    st.markdown("#### Full Product Table")
    st.dataframe(df[["product_name", "category", "price", "rating", "num_reviews"]], use_container_width=True)