LEXICON = {
    "urgent": 4, "asap": 4, "immediately": 4, "emergency": 4,
    "rush": 3, "today": 3, "late": 3, "delay": 3, "delayed": 3,
    "broken": 2, "wrong": 2, "tomorrow": 2, "soon": 2,
    "flexible": -2, "whenever": -2, "later": -1,
}
NEGATIONS = {"not", "no", "never", "hardly"}
INTENSIFIERS = {"very": 2, "really": 2, "so": 2, "extremely": 3}
USE_BUT_RULE = False       
USE_NEGATION_WINDOW = True    
NEGATION_WINDOW = 3
PUNCTUATION = ".,!?:;\"'()"
def clean_word(word):
    return word.lower().strip(PUNCTUATION)
def tokenize(message):
    """Split the message into tokens, keeping the original spelling."""
    return message.split()
def is_negation(word):
    return word in NEGATIONS or word.endswith("n't")
def analyse(message):
    """Return a list of (original_word, points) pairs."""
    pairs = []
    negate_for = 0
    boost = 1
    but_weight = 1
    for original in tokenize(message):
        word = clean_word(original)
        points = 0
        if is_negation(word):
            negate_for = NEGATION_WINDOW if USE_NEGATION_WINDOW else 999
            pairs.append((original, 0))
            continue
        if word == "but" and USE_BUT_RULE:
            but_weight = 2
        elif word in INTENSIFIERS:
            boost = INTENSIFIERS[word]
        elif word in LEXICON:
            points = LEXICON[word] * boost * but_weight
            if negate_for > 0:
                points = -points
            negate_for = 0
            boost = 1
        negate_for = max(0, negate_for - 1)
        pairs.append((original, points))
    return pairs
def message_score(message):
    return sum(points for _, points in analyse(message))
def classify(message):
    score = message_score(message)
    if score >= 2:
        return "URGENT"
    return "NORMAL"
def keywords(message):
    """Return the words from the urgency list that appear in the message."""
    found = []
    for original, _ in analyse(message):
        if clean_word(original) in LEXICON and original not in found:
            found.append(original)
    return found
TEST_MESSAGES = [
    ("I need my cake today", "URGENT"),
    ("Please deliver ASAP", "URGENT"),
    ("My order is delayed", "URGENT"),
    ("This is an emergency, call me immediately", "URGENT"),
    ("I need it very soon", "URGENT"),
    ("Please make the order later", "NORMAL"),
    ("I am flexible about delivery", "NORMAL"),
    ("The menu looks nice", "NORMAL"),
    ("It is not urgent", "NORMAL"),
    ("No rush, please deliver whenever", "NORMAL"),
]
def run_tests():
    correct = 0
    for message, expected in TEST_MESSAGES:
        result = classify(message)
        mark = "OK" if result == expected else "XX"
        correct += result == expected
        print(f"{mark}  {result:<7} score={message_score(message):>3}  {message}")
    print(f"\nAccuracy: {correct}/{len(TEST_MESSAGES)}")
if __name__ == "__main__":
    run_tests()
    print("\nType a bakery message, or 'quit' to stop.")
    while True:
        message = input("\n> ")
        if message.strip().lower() == "quit":
            break
        scored_words = [(word, points) for word, points in analyse(message) if points]
        print(f"{classify(message)} | score: {message_score(message)}")
        print(f"Keywords: {keywords(message)} | words: {scored_words}")
