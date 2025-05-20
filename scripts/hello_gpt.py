import os
from dotenv import load_dotenv

load_dotenv()

import sys
import time
from openai import OpenAI

# Инициализируем клиента (читаем ключ из переменных окружения)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

client = OpenAI(api_key=OPENAI_API_KEY)

# Собираем вопрос из аргументов CLI
question = " ".join(sys.argv[1:]) or "Ping?"

t0 = time.time()

# Запрос к OpenAI
resp = client.chat.completions.create(
    model=OPENAI_MODEL,
    messages=[{"role": "user", "content": question}]
)

# Ответ и статистика
answer = resp.choices[0].message.content.strip()
tokens = resp.usage.total_tokens

print(answer)
print(f"\n---\nTokens: {tokens}  Cost≈${tokens*0.00001:.4f}  Time:{time.time()-t0:.1f}s")
