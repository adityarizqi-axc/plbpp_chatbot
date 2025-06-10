import requests
from ..core.config import settings

def ask_gemini(question: str, context: str = "") -> str:
    # This is a mockup, adjust as necessary for Gemini API integration.
    headers = {"Authorization": f"Bearer {settings.GEMINI_API_KEY}"}
    data = {
        "model": "gemini-pro",
        "messages": [
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(settings.GEMINI_API_URL, json=data, headers=headers)
    if response.status_code == 200:
        result = response.json()
        # Adjust according to actual Gemini API response format
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")
    return "Maaf, AI tidak dapat menjawab pertanyaan Anda saat ini."