from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from openai import OpenAI
from dotenv import load_dotenv

from telegram_bot.sheets.sheets import get_profile_by_user_id
from telegram_bot.utils.prompt_builder import build_prompt

load_dotenv()
client = OpenAI()

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
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            reply = f"Ошибка при обращении к GPT: {e}"

        await update.message.reply_text(reply)

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
