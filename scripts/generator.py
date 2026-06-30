import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# =====================================================
# Load Environment Variables
# =====================================================

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError(
        "OPENROUTER_API_KEY not found in .env file."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# =====================================================
# Configuration
# =====================================================

MODELS = [

    "google/gemma-4-31b-it:free",

    "qwen/qwen3-next-80b-a3b-instruct:free",

    "meta-llama/llama-3.3-70b-instruct:free"

]

OUTPUT_FILE = Path("data/generated_chats.jsonl")

NUMBER_OF_CHATS = 10

# =====================================================
# Prompt
# =====================================================

PROMPT = """
You are creating training data for an AI Astrologer.

Generate ONE conversation.

Return ONLY ONE valid JSON object.

Do NOT return markdown.
Do NOT return explanation.
Do NOT use ```json.

Format:

{
    "messages":[
        {
            "role":"system",
            "content":"You are Vedaz AI Astrologer."
        },
        {
            "role":"user",
            "content":"..."
        },
        {
            "role":"assistant",
            "content":"..."
        }
    ]
}

Rules:

- Never predict death.
- Never diagnose diseases.
- Never guarantee marriage.
- Never guarantee money.
- Never create fear.
- Never recommend paid remedies.
- Always be warm.
- Always be honest.
- Encourage professional help whenever appropriate.

Return JSON only.
"""

# =====================================================
# Clean JSON
# =====================================================


def clean_json(text: str):

    text = text.replace("```json", "")
    text = text.replace("```", "")
    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found.")

    return text[start:end + 1]


# =====================================================
# Generate Chat
# =====================================================
def generate_chat():

    last_error = None

    for model in MODELS:

        try:

            print(f"\nUsing Model : {model}")

            response = client.chat.completions.create(

                model=model,

                messages=[
                    {
                        "role": "user",
                        "content": PROMPT
                    }
                ],

                temperature=0.5,

                extra_headers={
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "Vedaz Assignment"
                }

            )

            text = response.choices[0].message.content

            text = clean_json(text)

            chat = json.loads(text)

            if "messages" not in chat:
                raise ValueError("Invalid JSON format")

            return chat

        except Exception as e:

            last_error = e

            print(f"❌ {model} Failed")

            print(e)

            continue

    raise last_error




# =====================================================
# Save Chat
# =====================================================


def save_chat(chat):

    with open(
        OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(
                chat,
                ensure_ascii=False
            )
        )

        file.write("\n")


# =====================================================
# Main
# =====================================================


def main():

    print("=" * 70)
    print("VEDAZ CHAT GENERATOR")
    print("=" * 70)

    # Remove old generated file
    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    generated = 0
    attempts = 0

    while generated < NUMBER_OF_CHATS and attempts < NUMBER_OF_CHATS * 2:

        attempts += 1

        try:

            chat = generate_chat()

            save_chat(chat)

            generated += 1

            print(f"✅ Chat {generated} Generated")

        
        except Exception as e:

            print(f"\n❌ Attempt {attempts} Failed")

            print(e)

            print("\n⏳ Waiting 30 seconds...\n")

            time.sleep(30)
        

    print()
    print("=" * 70)
    print("Generation Completed")
    print("=" * 70)
    print(f"Generated Chats : {generated}")
    print(f"Attempts        : {attempts}")
    print(f"Output File     : {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()