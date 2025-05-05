import sys
import os

# Добавляем путь к modules/telegram_bot
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "modules", "telegram_bot")))

from main import main

if __name__ == "__main__":
    main()
