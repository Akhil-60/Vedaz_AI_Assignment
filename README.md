# 🔮 Vedaz AI Astrologer Assignment

## Overview
This project is developed as part of the Vedaz AI Assignment. It contains the full pipeline for training data validation, safe conversation generation, and quality evaluation for an AI Vedic Astrologer.

It consists of three major modules:
1. **Chat Checker**: Validates structure, ensures safety rules, and splits data.
2. **Chat Generator**: Generates new, safe Hinglish/Hindi astrology conversations.
3. **Chat Evaluator**: Tests response quality using an AI judge.

---

## Project Structure

```
Vedaz_Assignment/
│
├── app.py                                  # Streamlit Live Chat & Dashboard
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   ├── vedaz_astrologer_finetune.jsonl     # Original 15 example chats
│   ├── generated_chats.jsonl               # 10 newly generated chats (Task 2)
│   ├── train.jsonl                         # Training split (from checker)
│   └── test.jsonl                          # Test split (from checker)
│
├── outputs/
│   └── evaluation.csv                      # AI Judge scores (Safety, Warmth, Honesty, Helpfulness)
│
├── scripts/
│   ├── checker.py                          # Task 1: Validator & Safety Checker
│   ├── generator.py                        # Task 2: Chat Generator using API
│   └── evaluator.py                        # Task 3: Quality Evaluator using API
│
├── review_report.md                        # Stage 1: Review of the 15 examples
└── new_chats.jsonl                         # Stage 1: 5 manually curated new chats
```

---

## Features

### ✅ Chat Checker (`checker.py`)
- Structure validation (`system` → `user` → `assistant`)
- Word count analysis
- Safety rule violation detection (death, medical diagnosis, money guarantees, fear-selling, paid remedies)
- Duplicate detection
- Train/Test split (80/20 ratio) saving to `train.jsonl` and `test.jsonl`

### ✅ Chat Generator (`generator.py`)
- Connects to **Groq API** using the OpenAI SDK
- Uses dynamic topics to generate diverse, safe astrology conversations
- Automatically validates output JSON format
- Outputs to `data/generated_chats.jsonl`

### ✅ Chat Evaluator (`evaluator.py`)
- Runs real-user questions through the AI model
- Uses a secondary "Judge" LLM to evaluate responses on 4 criteria:
  - Safety (1-10)
  - Warmth (1-10)
  - Honesty (1-10)
  - Helpfulness (1-10)
- Exports results to `outputs/evaluation.csv`

### ✅ Streamlit Dashboard & Live Chat (`app.py`)
- Provides a live chat interface to talk to the AI Astrologer
- Displays a clean, professional evaluation results table in the sidebar

---

## Installation

Clone the repository:
```bash
git clone <repository-url>
```

Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```
Get your free API key from [console.groq.com](https://console.groq.com)

---

## How to Run

### 1. Run the Chat Checker
```bash
python scripts/checker.py
```
Outputs: `data/train.jsonl`, `data/test.jsonl`, and a console validation report.

### 2. Run the Chat Generator
```bash
python scripts/generator.py
```
Outputs: `data/generated_chats.jsonl` (10 new safe chats)

### 3. Run the Chat Evaluator
```bash
python scripts/evaluator.py
```
Outputs: `outputs/evaluation.csv`

### 4. Launch the Streamlit Dashboard & Live Chat
```bash
streamlit run app.py
```
Access the dashboard at: http://localhost:8501

---

## ⚠️ Important Note on API Usage

All API-based scripts (`generator.py`, `evaluator.py`, and `app.py`) use Groq's high-speed inference API with the `llama-3.3-70b-versatile` model.

Groq's Free Tier is very generous:
- Provides thousands of requests per day (30 requests per minute)
- No strict daily token limit, making it perfect for assignments and demos
- The project no longer relies on OpenRouter's 50 requests/day limit

The repository includes pre-generated files (`data/generated_chats.jsonl` and `outputs/evaluation.csv`) so the project works even if you don't have an API key immediately.

---

## Technologies Used
- Python 3.10+
- Groq API (High-speed LLM inference)
- OpenAI SDK (API client)
- Streamlit (Dashboard UI)
- Pandas (Data manipulation)
- Scikit-learn (Train/Test split)
- RapidFuzz (Fuzzy matching for duplicates)
- python-dotenv (Environment variable management)

---

## Output Files
- `data/generated_chats.jsonl` – Generated training examples
- `data/train.jsonl` / `test.jsonl` – Split datasets
- `outputs/evaluation.csv` – Final scores and metrics
- `review_report.md` – Stage 1 review document
- `new_chats.jsonl` – Stage 1 manual examples

---

## Author
Akhil Kumar
