import os
import sys
import asyncio

# Добавляем путь к корневой папке проекта (если нужно)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Импорты
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from config import BOT_TOKEN
from handlers.user import send_task, handle_task_button
from handlers.gpt import register_gpt_handlers

# Загрузка ключей
load_dotenv()
client = OpenAI()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-ассистент по личному бренду ✨")

# Точка запуска
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", send_task))
    app.add_handler(CallbackQueryHandler(handle_task_button))
    register_gpt_handlers(app)

    print("Бот запущен. Ожидаю команды...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
