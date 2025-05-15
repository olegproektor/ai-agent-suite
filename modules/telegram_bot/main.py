import sys
import os
import asyncio

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

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
from services.tasks import send_task
from handlers.user import start, send_task, handle_task_button, handle_code_input
from handlers.gpt import register_gpt_handlers

# Загрузка ключей
load_dotenv()
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-ассистент по личному бренду ✨")

# Точка запуска
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", send_task))
    app.add_handler(CallbackQueryHandler(handle_task_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code_input))
    register_gpt_handlers(app)

    print("Бот запущен. Ожидаю команды...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
