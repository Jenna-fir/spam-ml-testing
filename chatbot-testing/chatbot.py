# chatbot-testing/chatbot.py
# Simple wrapper to send questions to the LLM and get responses

import os

from groq import Groq


def get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable is not set")
    return Groq(api_key=api_key)


def ask_chatbot(question, model="llama-3.1-8b-instant"):
    """Sends a question to the LLM and returns its text response"""
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": question}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content


# ── Quick test ────────────────────────────────────────────────
if __name__ == "__main__":
    question = "What is the capital of France?"
    answer = ask_chatbot(question)
    print(f"Q: {question}")
    print(f"A: {answer}")