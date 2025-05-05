from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def register_gpt_handlers(app):
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = resp.choices[0].message.content.strip()
        await update.message.reply_text(reply)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
