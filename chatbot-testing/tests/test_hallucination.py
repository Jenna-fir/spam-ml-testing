# chatbot-testing/tests/test_hallucination.py
# Automated hallucination & accuracy testing for the LLM chatbot

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import pytest
from chatbot import ask_chatbot
from test_questions import TEST_QUESTIONS


# ── Helper: check if any expected keyword is in the response ──
def contains_expected_answer(response, expected_keywords):
    response_lower = response.lower()
    return any(keyword.lower() in response_lower for keyword in expected_keywords)


# ── TEST 1: Run all factual + math questions ───────────────────
@pytest.mark.parametrize("q", [
    q for q in TEST_QUESTIONS if q["category"] in ["factual", "math"]
])
def test_factual_accuracy(q):
    response = ask_chatbot(q["question"])
    passed = contains_expected_answer(response, q["expected_keywords"])
    print(f"\nQ: {q['question']}")
    print(f"A: {response}")
    print(f"Result: {'✅ PASS' if passed else '❌ FAIL (possible hallucination)'}")
    assert passed, f"Expected one of {q['expected_keywords']} in response"


# ── TEST 2: Trick questions — model should NOT make things up ──
@pytest.mark.parametrize("q", [
    q for q in TEST_QUESTIONS if q["category"] == "trick"
])
def test_trick_questions_no_hallucination(q):
    response = ask_chatbot(q["question"])
    passed = contains_expected_answer(response, q["expected_keywords"])
    print(f"\nQ: {q['question']}")
    print(f"A: {response}")
    print(f"Result: {'✅ PASS - correctly identified false premise' if passed else '🚨 HALLUCINATION DETECTED'}")
    assert passed, f"Model hallucinated an answer to a false-premise question!"


# ── TEST 3: Made-up entities — model should admit uncertainty ──
@pytest.mark.parametrize("q", [
    q for q in TEST_QUESTIONS if q["category"] == "fictional"
])
def test_fictional_entities(q):
    response = ask_chatbot(q["question"])
    passed = contains_expected_answer(response, q["expected_keywords"])
    print(f"\nQ: {q['question']}")
    print(f"A: {response}")
    print(f"Result: {'✅ PASS - admitted uncertainty' if passed else '🚨 HALLUCINATION DETECTED'}")
    assert passed, f"Model made up information about a fictional entity!"


# ── TEST 4: Consistency — same question, different phrasing ────
def test_consistency():
    q1 = "What is the capital city of Japan?"
    q2 = "Which city serves as Japan's capital?"

    response1 = ask_chatbot(q1)
    response2 = ask_chatbot(q2)

    print(f"\nQ1: {q1}\nA1: {response1}")
    print(f"\nQ2: {q2}\nA2: {response2}")

    both_mention_tokyo = "tokyo" in response1.lower() and "tokyo" in response2.lower()
    assert both_mention_tokyo, "Inconsistent answers for the same underlying question!"
