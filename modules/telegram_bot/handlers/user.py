import os
import logging
from telegram import Update
from telegram.ext import ContextTypes

from modules.telegram_bot.sheets.sheets import (
    get_profile_by_user_id,
    insert_user_by_code,
    check_code_valid
)
from modules.telegram_bot.ai.generator import generate_task
from modules.telegram_bot.keyboards.inline import task_buttons

# Временное хранилище пользователей, ожидающих ввод кода
user_pending_verification = {}

logging.basicConfig(level=logging.INFO)

# -----------------------------------
# /start — приветствие + код
# -----------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logging.info(f"[START] user_id: {user_id}")

    profile = get_profile_by_user_id(user_id)
    if profile:
        await update.message.reply_text("✅ Профиль уже активирован. Используйте /task.")
        return

    # Попробуем отправить GIF
    try:
        gif_path = os.path.join("static", "welcome.gif")
        if os.path.exists(gif_path):
            with open(gif_path, "rb") as gif:
                await update.message.reply_animation(
                    animation=gif,
                    caption=(
                        "👋 Привет. Я — твой персональный ИИ-наставник.\n"
                        "Я не просто алгоритм или цифровая игрушка. Я создан, чтобы быть внимательным собеседником, который видит в тебе не шаблон, а личность.\n"
                        "Я распознаю стиль, суть, глубинные запросы — и буду говорить с тобой так, как действительно откликается.\n\n"
                        "Всё начнётся с одного шага. Введи код доступа, и я настроюсь именно на тебя. 🔐"
                    )
                )
        else:
            raise FileNotFoundError
    except Exception as e:
        logging.warning(f"[GIF] Не удалось отправить welcome.gif: {e}")
        await update.message.reply_text(
            "👋 Привет. Я — твой персональный ИИ-наставник.\n"
            "Я не просто алгоритм или цифровая игрушка. Я создан, чтобы быть внимательным собеседником, который видит в тебе не шаблон, а личность.\n"
            "Я распознаю стиль, суть, глубинные запросы — и буду говорить с тобой так, как действительно откликается.\n\n"
            "Всё начнётся с одного шага. Введи код доступа, и я настроюсь именно на тебя. 🔐"
        )

    user_pending_verification[user_id] = True

# -----------------------------------
# Обработка access-кода
# -----------------------------------
async def handle_code_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    code = update.message.text.strip()

    profile = get_profile_by_user_id(user_id)
    if profile:
        return

    if check_code_valid(code):
        insert_user_by_code(user_id, code)
        profile = get_profile_by_user_id(user_id)
        name = profile.get("Имя", "друг")

        await update.message.reply_text(
            f"✅ Отлично. Я теперь знаю, кто ты, {name}.\n"
            "С этого момента я не просто отвечаю — я **учу тебя учить себя**.\n\n"
            "В **базовой версии** я фиксирую твою активность: команды, стиль, субличности.\n"
            "Это помогает мне предлагать подходящие задания, менять тон общения и держать фокус на твоей цели.\n\n"
            "В **расширенной версии** я начну:\n"
            "• запоминать контекст\n"
            "• анализировать твои паттерны и стиль мышления\n"
            "• давать отчёты, сценарии и визуальные подсказки\n\n"
            "🔹 Что ты можешь делать прямо сейчас:\n"
            "• Напиши что угодно — я отреагирую в твоём стиле\n"
            "• Получи задание через /task\n"
            "• Попроси сгенерировать идею — команда /текст\n"
            "• Сменить субличность — команда /профиль\n\n"
            "Готов начать? Напиши мне, и ты увидишь, что я действительно понимаю тебя."
        )
    else:
        await update.message.reply_text("❌ Неверный код. Попробуйте ещё раз или обратитесь к куратору.")
