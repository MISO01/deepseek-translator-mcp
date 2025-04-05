import os
import requests

def run(input: dict) -> dict:
    text = input.get("text")
    api_key = os.getenv("DEEPSEEK_API_KEY")

    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "Translate Korean to Simplified Chinese."},
                {"role": "user", "content": text}
            ]
        }
    )

    result = response.json()
    translated = result["choices"][0]["message"]["content"]
    return {"translated_text": translated.strip()}
