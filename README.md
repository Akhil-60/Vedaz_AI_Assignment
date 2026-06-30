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
├── app.py                          # Streamlit Dashboard to view results
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   ├── vedaz_astrologer_finetune.jsonl   # Original 15 example chats
│   ├── generated_chats.jsonl             # 10 newly generated chats (Task 2)
│   ├── train.jsonl                       # Training split (from checker)
│   └── test.jsonl                        # Test split (from checker)
│
├── outputs/
│   └── evaluation.csv              # AI Judge scores (Safety, Warmth, Honesty, Helpfulness)
│
├── scripts/
│   ├── checker.py                  # Task 1: Validator & Safety Checker
│   ├── generator.py                # Task 2: Chat Generator using API
│   └── evaluator.py                # Task 3: Quality Evaluator using API
│
├── review_report.md                # Stage 1: Review of the 15 examples
└── new_chats.jsonl                 # Stage 1: 5 manually curated new chats
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
- Connects to OpenRouter API
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

### ✅ Streamlit Dashboard (`app.py`)
- Reads `outputs/evaluation.csv`
- Displays a clean, professional results table

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

Create a `.env` file in the root directory and add your OpenRouter API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

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
Outputs: `data/generated_chats.jsonl`

### 3. Run the Chat Evaluator
```bash
python scripts/evaluator.py
```
Outputs: `outputs/evaluation.csv`

### 4. Launch the Streamlit Dashboard
```bash
streamlit run app.py
```
Access the dashboard at: http://localhost:8501

---

## ⚠️ Important Note on OpenRouter Free Tier

The `generator.py` and `evaluator.py` scripts rely on OpenRouter's free models. These free models have a strict daily rate limit of 50 requests per day (Error 429).

If you encounter a `429 Rate Limit Exceeded` error:
- Wait 24 hours for the limit to reset.
- Or, add credits to your OpenRouter account to increase the request quota.

**Note:** The submission includes pre-generated files (`data/generated_chats.jsonl` and `outputs/evaluation.csv`) so the API limit does not block the project evaluation.

---

## Technologies Used
- Python 3.10+
- OpenRouter AI API (LLM integration)
- OpenAI SDK (API client)
- Streamlit (Dashboard UI)
- Pandas (Data manipulation)
- Scikit-learn (Train/Test split)
- RapidFuzz (Fuzzy matching for duplicates)
- python-dotenv (Environment variable management)

---

## Output Files
- `data/generated_chats.jsonl` – Generated training examples.
- `data/train.jsonl` / `test.jsonl` – Split datasets.
- `outputs/evaluation.csv` – Final scores and metrics.
- `review_report.md` – Stage 1 review document.
- `new_chats.jsonl` – Stage 1 manual examples.

---

## Author
Akhil Kumar