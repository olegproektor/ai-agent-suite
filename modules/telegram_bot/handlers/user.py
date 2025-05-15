# handlers/user.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from telegram_bot.sheets.sheets import (
    get_profile_by_user_id,
    insert_user_by_code,
    check_code_valid
)
from ai.generator import generate_task
from keyboards.inline import task_buttons
import logging

# Временное хранилище пользователей, ожидающих ввод кода
user_pending_verification = {}

logging.basicConfig(level=logging.INFO)

# -----------------------------------
# /start → Запрашивает код доступа
# -----------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"[START] user_id: {user_id}")

    profile = get_profile_by_user_id(user_id)
    if profile:
        await update.message.reply_text("✅ Профиль уже активирован. Используйте /task.")
        return

    await update.message.reply_text("🔐 Введите код доступа, полученный от куратора:")
    user_pending_verification[user_id] = True

# -----------------------------------
# Обработка текста как access-кода
# -----------------------------------
async def handle_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    code = update.message.text.strip()

    if user_id not in user_pending_verification:
        return  # Не в режиме ожидания

    if check_code_valid(code):
        insert_user_by_code(user_id, code)
        await update.message.reply_text("✅ Доступ подтверждён. Используйте /task.")
    else:
        await update.message.reply_text("❌ Неверный код. Попробуйте ещё раз или обратитесь к куратору.")

    user_pending_verification.pop(user_id, None)

# -----------------------------------
# /task → Генерация задания
# -----------------------------------
async def send_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"[TASK] /task от user_id: {user_id}")

    profile = get_profile_by_user_id(user_id)
    if not profile:
        await update.message.reply_text("🔐 Профиль не найден. Обратитесь к куратору.")
        return

    task_text = generate_task(profile)
    await update.message.reply_text(
        text=f"📌 Ваше задание:\n\n{task_text}",
        reply_markup=task_buttons()
    )

# -----------------------------------
# Обработка кнопок под сообщением
# -----------------------------------
async def handle_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "done":
        await query.edit_message_text("👍 Задание выполнено!")
    elif query.data == "skip":
        await query.edit_message_text("⏭ Задание пропущено.")
    elif query.data == "retry":
        profile = get_profile_by_user_id(user_id)
        if not profile:
            await context.bot.send_message(
                chat_id=query.message.chat.id,
                text="🔐 Профиль не найден. Обратитесь к куратору."
            )
            return

        task_text = generate_task(profile)
        await context.bot.send_message(
            chat_id=query.message.chat.id,
            text=f"🔁 Новое задание:\n\n{task_text}",
            reply_markup=task_buttons()
        )
