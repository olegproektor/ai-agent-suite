import os
import httpx
from openai import OpenAI
from .prompt_builder import build_prompt

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client())

def generate_response(profile: dict, input_text: str, history: list = None) -> str:
    prompt = build_prompt(profile, input_text)

    messages = [{"role": "system", "content": "Ты — ИИ-собеседник на основе субличностей пользователя."}]
    
    if history:
        messages.extend(history)

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.8,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[Ошибка генерации ответа: {e}]"
