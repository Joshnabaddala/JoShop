---
title: JoShop
emoji: 🛒
colorFrom: orange
colorTo: red
sdk: docker
app_file: app.py
pinned: false
---

# 🛒 JoShop — AI-Powered E-commerce Intelligence Engine

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Groq](https://img.shields.io/badge/Groq-LLM-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> An end-to-end AI-powered shopping assistant that recommends products,
> analyzes customer reviews using LLMs, detects fake reviews, and explains
> recommendations in plain English.

---

## 🚀 Live Demo
🔗 [Click here to try JoShop](https://huggingface.co/spaces/joshna1910/JoShop)

---

## 🧠 Features

- 🔍 **Smart Product Recommendations** — content-based & collaborative filtering
- 💬 **AI Review Summarizer** — summarizes 100s of reviews in 3 lines using Groq LLM
- 🚨 **Fake Review Detector** — LLM-powered suspicious review classification
- 🤖 **Shopping Assistant Chatbot** — ask anything, get intelligent answers
- 📊 **Sentiment Analysis** — visual breakdown of customer opinions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| AI / LLM | Groq API, LangChain |
| ML | Scikit-learn, Pandas, FAISS |
| NLP | TextBlob, Sentiment Analysis |
| UI | Streamlit |
| Deployment | Hugging Face Spaces |

---

## 📁 Project Structure
JoShop/

├── app.py                  ← Main Streamlit app

├── data/                   ← Dataset

├── utils/

│   ├── llm_handler.py      ← Groq LLM API integration

│   ├── recommender.py      ← Recommendation engine

│   ├── sentiment.py        ← Sentiment analysis

│   └── data_loader.py      ← Data preprocessing

├── requirements.txt

└── .env.example
---

## ⚙️ Setup & Run Locally

```bash
git clone https://github.com/Joshnabaddala/JoShop.git
cd JoShop
python -m venv joshop-env
joshop-env\Scripts\activate
pip install -r requirements.txt
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