import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

def ask_next_question(conversation: str) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "http://localhost",  # optional but recommended
        "X-Title": "Credit Card Advisor"
    }

    payload = {
        "model": "meta-llama/llama-3-8b-instruct",  # ✅ Your model
        "messages": [
            {"role": "system", "content": "You are a helpful and polite credit card advisor."},
            {"role": "user", "content": f"Conversation so far:\n{conversation}\n\nAsk the next best question to recommend a credit card."}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        return response.json()["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("OpenRouter LLM error:", e)
        return "⚠️ Sorry, the assistant is currently unavailable."
