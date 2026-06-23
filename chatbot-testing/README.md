# LLM Chatbot Testing — Hallucination & Accuracy Suite

Automated testing framework for evaluating an LLM chatbot's factual accuracy,
hallucination tendency, and answer consistency using Python, pytest, and the Groq API.

## What This Project Covers
- Built a chatbot wrapper using Groq's Llama 3 API
- Designed 11 test cases across 5 categories: factual, math, trick questions,
  fictional entities, and consistency checks
- Achieved a **90% pass rate** (10/11 tests)
- Identified and documented **1 confirmed edge case** where keyword-based
  grading misclassified a reasonably hedged response as a hallucination

## Tech Stack
Python · Groq API (Llama 3) · pytest

## Test Categories
| Category | Purpose | Result |
|---|---|---|
| Factual | Baseline sanity checks (e.g. capital cities) | ✅ All passed |
| Math | Objectively verifiable answers | ✅ All passed |
| Trick questions | False-premise questions (e.g. "8th continent") | ✅ All passed — no hallucination |
| Fictional entities | Made-up books/medications | ⚠️ 1 of 2 flagged — see finding below |
| Consistency | Same question, different phrasing | ✅ Passed |

## Key Finding
When asked about a fictional medication ("Florinexitol"), the model did not
confidently invent side effects. Instead, it suggested the name might be
misspelled and recommended consulting a medical professional — a reasonably
safe response. The automated test flagged this as a failure because it used
exact keyword matching (expecting phrases like "not aware" or "no information"),
which didn't account for this valid alternative phrasing.

**Takeaway:** Simple keyword-based grading has limitations for evaluating
open-ended LLM responses. A more robust approach would use **"LLM-as-judge"**
— having a second LLM evaluate whether a response appropriately expressed
uncertainty, rather than relying on exact string matching.

## Project Structure