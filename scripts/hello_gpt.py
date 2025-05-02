import os
from dotenv import load_dotenv

load_dotenv()

import sys
import time
from openai import OpenAI

# Инициализируем клиент (читаем ключ из переменных окружения)
client = OpenAI()

# Собираем вопрос из аргументов CLI
question = " ".join(sys.argv[1:]) or "Ping?"

t0 = time.time()
# Новый синтаксис: client.chat.completions.create
resp = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": question}]
)

# Берём ответ и статистику
answer = resp.choices[0].message.content.strip()
tokens = resp.usage.total_tokens

print(answer)
print(f"\n---\nTokens: {tokens}  Cost≈${tokens*0.00001:.4f}  Time:{time.time()-t0:.1f}s")
