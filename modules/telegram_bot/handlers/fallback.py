from telegram import Update
from telegram.ext import ContextTypes
from modules.telegram_bot.utils.profile_loader import get_profile_by_user_id
from modules.logic.generate_response import generate_response

handled_users = set()

async def handle_free_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    profile = get_profile_by_user_id(user_id)

    if not profile:
        await update.message.reply_text("Я ещё не знаю, кто ты. Введи код доступа, чтобы начать.")
        return

    context.user_data.setdefault("history", [])

    if user_id not in handled_users:
        system_prompt = (
            "Ты — ИИ, настроенный под личность пользователя. Сейчас он впервые написал тебе сообщение напрямую, без команды.\n\n"
            "Твоя задача — дать тёплый, развёрнутый и стилизованный ответ, в рамках активной субличности, с учётом цели, стиля и возраста.\n\n"
            f"Имя пользователя: {profile.get('Имя', '')}\n"
            f"Возраст: {profile.get('Возраст', '')}\n"
            f"Цель: {profile.get('Цель', '')}\n"
            f"Стиль: {profile.get('Стиль', '')}\n"
            f"Субличность: {profile.get('Субличность', '')}\n\n"
            "Расскажи:\n"
            "- что ты уже знаешь о нём (имя, цель, стиль)\n"
            "- как ты будешь взаимодействовать (через команды и свободное общение)\n"
            "- что можно делать (получать задания, разбирать идеи, вести диалог)\n"
            "- что можно менять (субличность, фокус, настроение)\n\n"
            "Обязательно обратись по имени. Стиль — в духе активной субличности. Будь искренним, как будто ты — его внутренний голос."
        )
        handled_users.add(user_id)
        response = generate_response(profile, system_prompt)
        context.user_data["history"].append({"role": "user", "content": system_prompt})
        context.user_data["history"].append({"role": "assistant", "content": response})
    else:
        input_text = update.message.text
        response = generate_response(profile, input_text, context.user_data["history"])
        context.user_data["history"].append({"role": "user", "content": input_text})
        context.user_data["history"].append({"role": "assistant", "content": response})
        context.user_data["history"] = context.user_data["history"][-6:]  # последние 3 пары

    await update.message.reply_text(response)
