import json
from pathlib import Path
from sklearn.model_selection import train_test_split

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

    valid_chats = []
    invalid_chats = []
    unsafe_chats = []
    word_counts = []

    for index, chat in enumerate(chats, start=1):

        words = count_words(chat)
        word_counts.append(words)

        violations = detect_safety(chat)

        if validate_structure(chat):

            if violations:
                unsafe_chats.append(chat)
                print(
                    f"Chat {index:02d} | "
                    f"{words:4d} words | "
                    f"⚠️ UNSAFE | "
                    f"{', '.join(violations)}"
                )

            else:
                valid_chats.append(chat)
                print(
                    f"Chat {index:02d} | "
                    f"{words:4d} words | "
                    f"✅ SAFE"
                )

        else:
            invalid_chats.append(chat)
            print(
                f"Chat {index:02d} | "
                f"{words:4d} words | "
                f"❌ INVALID STRUCTURE"
            )

    print()
    print("=" * 70)

    print(f"Valid Chats      : {len(valid_chats)}")
    print(f"Invalid Chats    : {len(invalid_chats)}")
    print(f"Unsafe Chats     : {len(unsafe_chats)}")

    print()

    print(f"Average Words    : {sum(word_counts)/len(word_counts):.2f}")
    print(f"Shortest Chat    : {min(word_counts)} words")
    print(f"Longest Chat     : {max(word_counts)} words")
    
    print("=" * 70)

    # =====================================================
    # ✅ FIX: Train/Test Split and Save files (Added as required)
    # =====================================================
    if len(valid_chats) > 0:
        train_chats, test_chats = train_test_split(valid_chats, test_size=0.2, random_state=42)
        
        with open("train.jsonl", "w", encoding="utf-8") as f:
            for c in train_chats:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
                
        with open("test.jsonl", "w", encoding="utf-8") as f:
            for c in test_chats:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

        print(f"\n✅ Train/Test Split Complete:")
        print(f"   Training set   : {len(train_chats)} chats → saved to train.jsonl")
        print(f"   Test set       : {len(test_chats)} chats → saved to test.jsonl")
    else:
        print("\n⚠️ No valid chats found to split.")
        
    print("=" * 70)


if __name__ == "__main__":
    main()