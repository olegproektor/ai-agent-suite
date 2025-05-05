import os
from dotenv import load_dotenv

load_dotenv()
print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("TELEGRAM_TOKEN =", os.getenv("TELEGRAM_TOKEN"))
