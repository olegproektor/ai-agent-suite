import os
from dotenv import load_dotenv

# Загружаем .env один раз на весь проект
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
PROXY_URL = os.getenv("PROXY_URL", None)  # на будущее
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")  # модель по умолчанию

import openai
openai.api_key = OPENAI_API_KEY
