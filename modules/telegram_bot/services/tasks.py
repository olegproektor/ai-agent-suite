from telegram import Update
from telegram.ext import ContextTypes

from modules.logic.prompt_builder import build_prompt
from modules.telegram_bot.config import OPENAI_MODEL
from modules.telegram_bot.utils.profile_loader import get_profile_by_user_id

import logging
import os
import httpx
from openai import OpenAI

# Инициализация OpenAI-клиента с ручным http_client (без прокси)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client())

async def send_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    profile = get_profile_by_user_id(user_id)
    if not profile:
        await update.message.reply_text("Профиль не найден. Обратитесь к куратору.")
        return

    prompt = build_prompt(profile, "Сформулируй задание дня")
    logging.info(f"[PROMPT GPT]: {prompt}")

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )
        reply = response.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"[OPENAI ERROR] {e}")
        await update.message.reply_text(f"Ошибка генерации: {e}")
