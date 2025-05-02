from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_task(profile: dict) -> str:
    role = profile.get("role", "эксперт")
    goal = profile.get("goal", "развитие бренда")
    style = profile.get("style", "нейтральный")

    prompt = (
        f"Ты — AI-ассистент по личному бренду. Клиент — в роли '{role}', "
        f"его цель — '{goal}', и он предпочитает стиль общения '{style}'. "
        "Придумай одно конкретное задание на сегодня, которое поможет ему проявиться в контенте или укрепить свою позицию."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Ошибка генерации задания: {e}"
