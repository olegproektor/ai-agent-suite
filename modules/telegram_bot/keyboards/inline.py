from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def task_buttons():
    keyboard = [
        [
            InlineKeyboardButton("✅ Выполнил", callback_data="done"),
            InlineKeyboardButton("❌ Пропустить", callback_data="skip"),
            InlineKeyboardButton("🔁 Хочу другое", callback_data="retry")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
