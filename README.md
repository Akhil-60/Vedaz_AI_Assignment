\# 🔮 Vedaz AI Assignment



\## Overview



This project is developed as part of the Vedaz AI Assignment.



It contains three major modules:



1\. Chat Checker

2\. Chat Generator

3\. Chat Evaluator



The system validates astrology conversations, generates new safe conversations, and evaluates response quality using Large Language Models (LLMs).



\---



\## Project Structure



```

Vedaz\_Assignment/

│

├── app.py

├── README.md

├── requirements.txt

├── .env.example

│

├── data/

│   ├── vedaz\_astrologer\_finetune.jsonl

│   ├── train.jsonl

│   ├── test.jsonl

│   └── generated\_chats.jsonl

│

├── outputs/

│   ├── report.txt

│   └── evaluation.csv

│

├── scripts/

│   ├── checker.py

│   ├── generator.py

│   └── evaluator.py

```



\---



\# Features



\## ✅ Chat Checker



\- Dataset Validation

\- Structure Validation

\- Word Count Analysis

\- Safety Rule Detection

\- Duplicate Detection

\- Train/Test Split

\- Report Generation



\---



\## ✅ Chat Generator



\- Uses OpenRouter API

\- Generates safe astrology conversations

\- Produces JSONL training data

\- Automatic JSON validation



\---



\## ✅ Chat Evaluator



Evaluates responses based on:



\- Safety

\- Warmth

\- Honesty

\- Helpfulness



Results are exported to CSV.



\---



\# Installation



Clone the repository



```bash

git clone <repository-url>

```



Create virtual environment



```bash

python -m venv venv

```



Activate environment



Windows



```bash

venv\\Scripts\\activate

```



Install dependencies



```bash

pip install -r requirements.txt

```



\---



\# Environment Variables



Create a `.env` file



```env

OPENROUTER\_API\_KEY=your\_api\_key

```



\---



\# Run



Chat Checker



```bash

python scripts/checker.py

```



Chat Generator



```bash

python scripts/generator.py

```



Chat Evaluator



```bash

python scripts/evaluator.py

```



Streamlit Dashboard



```bash

streamlit run app.py

```



\---



\# Technologies Used



\- Python

\- OpenRouter API

\- OpenAI SDK

\- Streamlit

\- Pandas

\- Scikit-learn

\- RapidFuzz



\---



\# Output Files



```

outputs/report.txt

outputs/evaluation.csv

data/generated\_chats.jsonl

```



\---



\# Author Akhil Kumar

