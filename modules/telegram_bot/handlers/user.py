from telegram import Update
from telegram.ext import ContextTypes
from ai.generator import generate_task
from keyboards.inline import task_buttons

# Команда /task — отправка задания с кнопками
async def send_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    profile = {
        "role": "Наставник",
        "goal": "Повысить экспертность",
        "style": "тёплый"
    }

    task_text = generate_task(profile)

    await update.message.reply_text(
        text=f"Вот твоё задание:\n\n{task_text}",
        reply_markup=task_buttons()
    )

# Обработка нажатий кнопок
async def handle_task_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "done":
        await query.edit_message_text("Отлично! Задание выполнено 💪")

    elif query.data == "skip":
        await query.edit_message_text("Ок, пропустили. Завтра попробуем ещё раз.")

    elif query.data == "retry":
        await query.edit_message_text("Генерирую новое задание... 🔄")

        profile = {
            "role": "Наставник",
            "goal": "Повысить экспертность",
            "style": "тёплый"
        }

        task_text = generate_task(profile)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Вот новое задание для тебя:\n\n{task_text}",
            reply_markup=task_buttons()
        )

