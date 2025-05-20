from openai import OpenAI
import os
import httpx  # ← добавлено для ручного клиента
from modules.telegram_bot.config import OPENAI_MODEL  # Подключаем модель из конфигурации

# Инициализируем OpenAI-клиент с принудительным отключением прокси
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client())

def generate_task(profile: dict) -> str:
    subself = profile.get("Субличность", "эксперт")
    goal = profile.get("Цель", "развитие бренда")
    style = profile.get("Стиль", "нейтральный")

    prompt = (
        f"Ты — AI-ассистент по личному бренду. Клиент — в субличности '{subself}', "
        f"его цель — '{goal}', и он предпочитает стиль общения '{style}'. "
        "Придумай одно конкретное задание на сегодня, которое поможет ему проявиться в контенте или укрепить свою позицию."
    )

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка генерации задания: {e}"
