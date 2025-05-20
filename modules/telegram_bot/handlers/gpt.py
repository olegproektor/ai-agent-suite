from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters

from modules.telegram_bot.config import BOT_TOKEN, OPENAI_API_KEY, OPENAI_MODEL
from modules.logic.prompt_builder import build_prompt
from modules.telegram_bot.utils.profile_loader import get_profile_by_user_id

from openai import OpenAI
import httpx
import os

# Инициализируем клиента с ручным http_client (чистый, без прокси)
client = OpenAI(api_key=OPENAI_API_KEY, http_client=httpx.Client())

def register_gpt_handlers(app):
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        user_id = update.effective_user.id

        profile = get_profile_by_user_id(user_id)
        if not profile:
            await update.message.reply_text("Профиль не найден. Обратитесь к куратору.")
            return

        prompt = build_prompt(profile, user_input)

        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
                max_tokens=800
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Ошибка при обращении к GPT: {e}"

        await update.message.reply_text(reply)

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
