from telegram import Update
from telegram.ext import ContextTypes

from telegram_bot.utils.prompt_builder import build_prompt
from telegram_bot.sheets.sheets import get_profile_by_user_id

import openai
import os
from dotenv import load_dotenv

load_dotenv()

async def send_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    profile = get_profile_by_user_id(user_id)
    if not profile:
        await update.message.reply_text("Профиль не найден. Обратитесь к куратору.")
        return

    prompt = build_prompt(profile, "Сформулируй задание дня")
    print("🔹 PROMPT GPT:")
    print(prompt)


    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"Ошибка генерации: {e}")
