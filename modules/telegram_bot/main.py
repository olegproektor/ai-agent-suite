import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from modules.telegram_bot.config import BOT_TOKEN
from modules.telegram_bot.services.tasks import send_task
from modules.telegram_bot.handlers.user import (
    start,
    handle_code_input
)
from modules.telegram_bot.handlers.gpt import register_gpt_handlers
from modules.telegram_bot.handlers.fallback import handle_free_message

# Загрузка .env
load_dotenv()

# --------------------------
# Основной запуск бота
# --------------------------
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("task", send_task))
    app.add_handler(CallbackQueryHandler(handle_task_button))

    app.add_handler(
        MessageHandler(filters.TEXT & filters.Regex(r"^[A-Z]{3}-\d{3}$"), handle_code_input)
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_free_message)
    )

    register_gpt_handlers(app)

    print("🤖 Бот запущен. Ожидаю команды...")
    app.run_polling()

# --------------------------
# Обработчик кнопок задания
# --------------------------
async def handle_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    if data == "accept_task":
        await query.edit_message_text("🚀 Отлично! Выполни задание и сообщи, как прошло.")
    elif data == "decline_task":
        await query.edit_message_text("⏳ Хорошо, вернёмся к заданию позже.")
    else:
        await query.edit_message_text("🤖 Неизвестная команда.")

# --------------------------
# Точка входа
# --------------------------
if __name__ == "__main__":
    asyncio.run(main())
