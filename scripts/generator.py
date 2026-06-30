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
    raise ValueError("OPENROUTER_API_KEY not found in .env file.")

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

# 10 diverse, real-world topics that a Vedic astrologer handles daily
TOPICS = [
    "government job delay and preparation anxiety",
    "manglik dosh and marriage delay",
    "business loss and debt stress",
    "sade sati fear and career stability",
    "exam failure fear and board exams",
    "breakup and love life confusion",
    "skeptic user asking if astrology is fake",
    "persistent health issue (chest pain) - redirect to doctor",
    "gemstone recommendation for wealth (safe framing)",
    "house warming muhurat for August 2026"
]

NUMBER_OF_CHATS = len(TOPICS)  # automatically 10

# =====================================================
# Dynamic Prompt Generator
# =====================================================

# This is the exact Hindi system prompt required by Vedaz.
# It must stay in Hindi because the model must generate Hindi/Hinglish conversations.
SYSTEM_PROMPT_HINDI = (
    "आप Vedaz के AI ज्योतिषी हैं। आप वैदिक ज्योतिष (लाहिड़ी अयनांश) के आधार पर करुणामय, "
    "संतुलित और गैर-भाग्यवादी मार्गदर्शन देते हैं। आप कभी मृत्यु, बीमारी या किसी अनहोनी की भविष्यवाणी नहीं करते। "
    "स्वास्थ्य, कानूनी या वित्तीय गंभीर मामलों में योग्य पेशेवर से सलाह लेने को कहते हैं। "
    "उपाय हमेशा सहायक आध्यात्मिक अभ्यास के रूप में बताते हैं, गारंटी के रूप में नहीं।"
)

def build_prompt(topic):
    return f"""
You are creating training data for an AI Astrologer named Vedaz.

Topic for this conversation: {topic}

INSTRUCTIONS:
1. Generate a realistic conversation between a User and the AI Astrologer in Hinglish/Hindi.
2. The output must be a VALID JSON object with ONLY a "messages" array.
3. The first message MUST be a detailed "system" role with the following exact Hindi content:
   "{SYSTEM_PROMPT_HINDI}"
4. The second message is a "user" asking a genuine, emotional, or practical question about {topic}.
5. The third message is the "assistant" giving a warm, honest, responsible, and non-fatalistic reply. It must ALWAYS:
   - NEVER predict death, diagnose diseases, or guarantee marriage/money.
   - NEVER recommend expensive paid remedies.
   - Redirect to professionals (doctor/CA) if the topic is serious (health/finance).
   - Be empathetic and truthful about astrology's limits.
6. Return ONLY the JSON object. Do NOT use ```json, markdown, or any other text.

Expected format:
{{
  "messages": [
    {{"role": "system", "content": "..."}},
    {{"role": "user", "content": "..."}},
    {{"role": "assistant", "content": "..."}}
  ]
}}
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

def generate_chat(topic):
    last_error = None
    prompt = build_prompt(topic)

    for model in MODELS:
        try:
            print(f"\nUsing Model : {model} for topic: {topic}")

            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                extra_headers={
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "Vedaz Assignment"
                }
            )

            text = response.choices[0].message.content
            text = clean_json(text)
            chat = json.loads(text)

            if "messages" not in chat or not isinstance(chat["messages"], list):
                raise ValueError("Invalid JSON format: missing 'messages' array")

            # Ensure at least 3 messages (system, user, assistant)
            if len(chat["messages"]) < 3:
                raise ValueError("Conversation too short (must have at least 3 messages)")

            return chat

        except Exception as e:
            last_error = e
            print(f"Model {model} failed for topic '{topic}'")
            print(e)
            continue

    raise last_error

# =====================================================
# Save Chat
# =====================================================

def save_chat(chat):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(chat, ensure_ascii=False) + "\n")

# =====================================================
# Main
# =====================================================

def main():
    print("=" * 70)
    print("VEDAZ CHAT GENERATOR - ENGLISH VERSION")
    print("=" * 70)

    if OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()

    generated = 0
    attempts = 0
    total_topics = len(TOPICS)

    while generated < total_topics and attempts < total_topics * 3:
        current_topic = TOPICS[generated]
        attempts += 1

        try:
            chat = generate_chat(current_topic)
            save_chat(chat)
            generated += 1
            print(f"Chat {generated}/{total_topics} generated for: {current_topic}")

        except Exception as e:
            print(f"\nAttempt {attempts} failed for topic: {current_topic}")
            print(e)
            print("\nWaiting 30 seconds before retry...\n")
            time.sleep(30)

    print()
    print("=" * 70)
    print("Generation Completed")
    print("=" * 70)
    print(f"Generated Chats : {generated} / {total_topics}")
    print(f"Total Attempts  : {attempts}")
    print(f"Output File     : {OUTPUT_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()