import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

from modules.telegram_bot.main import main

if __name__ == "__main__":
    main()
