import asyncio
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN

from handlers.user import send_task, handle_task_button  # ← все функции из user.py

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой AI-ассистент по личному бренду ✨")

# Запуск бота
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Регистрируем команды и обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", send_task))
    app.add_handler(CallbackQueryHandler(handle_task_button))

    print("Бот запущен. Ожидаю команды...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
