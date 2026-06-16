import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

def summarize_reviews(product_name, reviews):
    """
    Use Groq LLM to summarize customer reviews
    into 3 clear bullet points.
    """
    prompt = f"""
You are a helpful shopping assistant.
Summarize the following customer reviews for "{product_name}" into exactly 3 clear bullet points.
Focus on: quality, value for money, and any issues.
Keep each point under 20 words.

Reviews:
{reviews}

Respond with exactly 3 bullet points starting with •
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def shopping_assistant(user_question, product_context):
    """
    AI shopping assistant that answers user questions
    about products using context from the dataset.
    """
    prompt = f"""
You are JoShop AI, a smart and friendly shopping assistant.
Answer the user's question based on the product information provided.
Be concise, helpful, and always mention price in Indian Rupees (₹).
If you don't know, say so honestly.

Product Information:
{product_context}

User Question: {user_question}

Answer in 2-3 sentences maximum.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def analyze_review_with_ai(review_text):
    """
    Use LLM to deeply analyze a single review —
    extract pros, cons, and overall verdict.
    """
    prompt = f"""
Analyze this product review and extract:
1. Top 2 Pros (positive points)
2. Top 2 Cons (negative points or missing info)
3. One line verdict

Review: "{review_text}"

Format your response exactly like this:
✅ Pro 1: ...
✅ Pro 2: ...
❌ Con 1: ...
❌ Con 2: ...
⭐ Verdict: ...
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250,
        temperature=0.4
    )
    return response.choices[0].message.content.strip()

def get_product_recommendation_reason(user_need, product_name, product_details):
    """
    Generate a personalized reason why a product
    matches what the user is looking for.
    """
    prompt = f"""
A customer is looking for: "{user_need}"
Explain in 2 sentences why "{product_name}" is a great match.
Product details: {product_details}
Be specific, friendly, and mention the price value.
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.6
    )
    return response.choices[0].message.content.strip()