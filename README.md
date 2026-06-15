# 🛒 JoShop — AI-Powered E-commerce Intelligence Engine

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

> An end-to-end AI-powered shopping assistant that recommends products, 
> analyzes customer reviews using LLMs, detects fake reviews, and explains 
> recommendations in plain English.

---

## 🚀 Live Demo
🔗 [Click here to try JoShop](#) ← (will update after deployment)

---

## 🧠 Features

- 🔍 **Smart Product Recommendations** — content-based & collaborative filtering
- 💬 **AI Review Summarizer** — summarizes 100s of reviews in 3 lines using GPT
- 🚨 **Fake Review Detector** — LLM-powered suspicious review classification
- 🤖 **Shopping Assistant Chatbot** — ask anything, get intelligent answers
- 📊 **Sentiment Analysis** — visual breakdown of customer opinions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| AI / LLM | OpenAI GPT, LangChain |
| ML | Scikit-learn, Pandas, FAISS |
| NLP | TextBlob, VADER Sentiment |
| UI | Streamlit |
| Dataset | Amazon Product Reviews (Kaggle) |
| Deployment | Hugging Face Spaces |

---

## 📁 Project Structure
JoShop/

├── app.py                  ← Main Streamlit app

├── data/                   ← Dataset

├── utils/

│   ├── llm_handler.py      ← Anthropic Claude API integration

│   ├── recommender.py      ← Recommendation engine

│   ├── sentiment.py        ← Sentiment analysis

│   └── data_loader.py      ← Data preprocessing

├── notebooks/

│   └── EDA.ipynb           ← Exploratory Data Analysis

├── requirements.txt

└── .env.example

---

## ⚙️ Setup & Run Locally

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/JoShop.git
cd JoShop

# Create virtual environment
python -m venv joshop-env
joshop-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run the app
streamlit run app.py
```

---

## 👩‍💻 Author

**Baddala Jhoshna**  
Associate Consultant — AI & Quality Engineering  
[LinkedIn](https://www.linkedin.com/in/jhoshna-baddala-bb1549264/) | [GitHub](https://github.com/Joshnabaddala)

---

## 📄 License
MIT License
