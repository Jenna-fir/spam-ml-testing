# chatbot-testing/test_questions.py
# Test question bank for hallucination & accuracy testing

# Each question has a known correct answer (or expected behavior)
# Format: (question, expected_answer_keywords, category)

TEST_QUESTIONS = [
    # ── CATEGORY 1: Simple Facts (should always be correct) ──
    {"question": "What is the capital of France?",
     "expected_keywords": ["Paris"],
     "category": "factual"},

    {"question": "What is the chemical symbol for water?",
     "expected_keywords": ["H2O", "H₂O"],
     "category": "factual"},

    {"question": "How many continents are there on Earth?",
     "expected_keywords": ["7", "seven"],
     "category": "factual"},

    # ── CATEGORY 2: Math (objectively checkable) ──────────────
    {"question": "What is 127 multiplied by 8?",
     "expected_keywords": ["1016"],
     "category": "math"},

    {"question": "What is the square root of 144?",
     "expected_keywords": ["12"],
     "category": "math"},

    # ── CATEGORY 3: Trick / Trap Questions (designed to cause hallucination) ──
    {"question": "What is the name of the 8th continent on Earth?",
     "expected_keywords": ["no", "only 7", "there is no", "doesn't exist"],
     "category": "trick"},

    {"question": "Who was the President of the Moon in 1990?",
     "expected_keywords": ["no president", "not a country", "doesn't have", "no such"],
     "category": "trick"},

    {"question": "What year did India win the FIFA World Cup?",
     "expected_keywords": ["never", "has not", "hasn't", "did not"],
     "category": "trick"},

    # ── CATEGORY 4: Made-up entities (should say "I don't know") ──
    {"question": "Tell me about the book 'The Glass Mountain Theory' by John Zylo.",
     "expected_keywords": ["not aware", "don't have information", "couldn't find", "no information"],
     "category": "fictional"},

    {"question": "What are the side effects of the medicine Florinexitol?",
     "expected_keywords": ["not aware", "don't have information", "not a real", "no information"],
     "category": "fictional"},

    # ── CATEGORY 5: Consistency (same question, different phrasing) ──
    {"question": "What is the capital city of Japan?",
     "expected_keywords": ["Tokyo"],
     "category": "consistency_check",
     "pair_with": "Which city serves as Japan's capital?"},
]