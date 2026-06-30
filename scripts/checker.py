import json
from pathlib import Path

DATASET_PATH = Path("data/vedaz_astrologer_finetune.jsonl")


def load_dataset(file_path):
    chats = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                chats.append(json.loads(line))

    return chats


def validate_structure(chat):

    messages = chat.get("messages", [])

    if len(messages) == 0:
        return False

    # First message must be system
    if messages[0]["role"] != "system":
        return False

    expected = "user"

    for message in messages[1:]:

        if message["role"] != expected:
            return False

        expected = "assistant" if expected == "user" else "user"

    return True


# -----------------------------
# Step 5 - Count Words
# -----------------------------
def count_words(chat):

    total_words = 0

    for message in chat["messages"]:
        total_words += len(message["content"].split())

    return total_words


# -----------------------------
# Step 6 - Safety Checker
# -----------------------------
SAFETY_RULES = {

    "Death Prediction": [
        "death",
        "die",
        "mar jaoge",
        "mrityu",
        "life will end"
    ],

    "Medical Prediction": [
        "cancer",
        "heart attack",
        "terminal disease",
        "serious illness",
        "bimari"
    ],

    "Money Guarantee": [
        "100% success",
        "guaranteed money",
        "crorepati",
        "lottery pakka"
    ],

    "Fear Selling": [
        "life ruined",
        "tabah",
        "destroyed",
        "bad luck forever"
    ],

    "Paid Remedy": [
        "51000",
        "21000",
        "paid puja",
        "expensive remedy"
    ]
}


def detect_safety(chat):

    assistant_text = ""

    for message in chat["messages"]:

        if message["role"] == "assistant":
            assistant_text += " " + message["content"].lower()

    violations = []

    for category, keywords in SAFETY_RULES.items():

        for keyword in keywords:

            if keyword.lower() in assistant_text:
                violations.append(category)
                break

    return violations


def main():

    chats = load_dataset(DATASET_PATH)

    print("=" * 70)
    print("VEDAZ CHAT CHECKER")
    print("=" * 70)

    print(f"Total Chats : {len(chats)}")
    print()

    valid = 0
    invalid = 0
    unsafe = 0

    word_counts = []

    for index, chat in enumerate(chats, start=1):

        words = count_words(chat)
        word_counts.append(words)

        violations = detect_safety(chat)

        if validate_structure(chat):

            valid += 1

            if violations:

                unsafe += 1

                print(
                    f"Chat {index:02d} | "
                    f"{words:4d} words | "
                    f"⚠️ UNSAFE | "
                    f"{', '.join(violations)}"
                )

            else:

                print(
                    f"Chat {index:02d} | "
                    f"{words:4d} words | "
                    f"✅ SAFE"
                )

        else:

            invalid += 1

            print(
                f"Chat {index:02d} | "
                f"{words:4d} words | "
                f"❌ INVALID STRUCTURE"
            )

    print()
    print("=" * 70)

    print(f"Valid Chats      : {valid}")
    print(f"Invalid Chats    : {invalid}")
    print(f"Unsafe Chats     : {unsafe}")

    print()

    print(f"Average Words    : {sum(word_counts)/len(word_counts):.2f}")
    print(f"Shortest Chat    : {min(word_counts)} words")
    print(f"Longest Chat     : {max(word_counts)} words")

    print("=" * 70)


if __name__ == "__main__":
    main()