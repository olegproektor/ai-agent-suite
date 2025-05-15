import gspread
import os
import json
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

# Загрузка переменных окружения
load_dotenv()

# Пути
BASE_DIR = Path(__file__).resolve().parents[3]
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")
CURATORS_PATH = os.path.join(BASE_DIR, "curators.json")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")  # ID таблицы с user_profiles

print(f"[DEBUG] BASE_DIR: {BASE_DIR}")
print(f"[DEBUG] CREDS_PATH: {CREDS_PATH}")
print(f"[DEBUG] CURATORS_PATH: {CURATORS_PATH}")

# Подключение к Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
client = gspread.authorize(creds)

# Загрузка curators.json
with open(CURATORS_PATH, "r", encoding="utf-8") as f:
    CURATORS = json.load(f)

# --------------------------------------
#          ПРОФИЛИ И ДОСТУП
# --------------------------------------

def get_profile_by_user_id(user_id: int) -> dict:
    """Возвращает базовый профиль пользователя по user_id."""
    try:
        main_sheet = client.open_by_key(SHEET_ID).worksheet("user_profiles")
        rows = main_sheet.get_all_records()
        for row in rows:
            if str(row.get("ID")) == str(user_id):
                return {
                    "goal": row.get("Цель", ""),
                    "persona": row.get("Архетип", ""),
                    "style": row.get("Стиль", ""),
                    "subself": row.get("Субличность", "")
                }
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при получении базового профиля: {e}")
    return None


def get_full_profile(user_id: int) -> dict:
    """Возвращает всю строку профиля пользователя по user_id."""
    try:
        main_sheet = client.open_by_key(SHEET_ID).worksheet("user_profiles")
        rows = main_sheet.get_all_records()
        for row in rows:
            if str(row.get("ID")) == str(user_id):
                return row
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при получении полного профиля: {e}")
    return {}

# --------------------------------------
#          ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# --------------------------------------

def get_curator_config_by_code(code: str):
    prefix = code.split("-")[0]
    for curator_id, config in CURATORS.items():
        if config["prefix"] == prefix:
            return config, curator_id
    raise ValueError(f"Неизвестный префикс кода: {prefix}")


def get_access_codes_worksheet(code: str):
    config, curator_id = get_curator_config_by_code(code)
    creds_path = os.path.join(BASE_DIR, config["credentials"])
    scope = SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client_local = gspread.authorize(creds)

    spreadsheet = client_local.open_by_url(config["sheet_url"])
    worksheet = spreadsheet.worksheet(f"access_codes_{curator_id}")
    return worksheet, curator_id

# --------------------------------------
#        ПРОВЕРКА И ДОБАВЛЕНИЕ
# --------------------------------------

def check_code_valid(code: str) -> bool:
    try:
        sheet, _ = get_access_codes_worksheet(code)
        data = sheet.get_all_records()
        for row in data:
            if str(row.get("Код доступа", "")).strip() == code.strip() and row.get("Статус", "").lower() != "использован":
                return True
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при проверке кода: {e}")
    return False


def insert_user_by_code(user_id: int, code: str) -> None:
    try:
        # доступ к двум таблицам
        access_sheet, curator_id = get_access_codes_worksheet(code)
        user_profiles = client.open_by_key(SHEET_ID).worksheet("user_profiles")

        rows = access_sheet.get_all_records()
        for i, row in enumerate(rows, start=2):  # строка 2 — первая после заголовков
            if str(row.get("Код доступа", "")).strip() == code.strip():
                now = datetime.now().strftime("%Y-%m-%d %H:%M")

                # Запись в user_profiles
                profile_row = {
                    "ID": str(user_id),
                    "Имя": row.get("Имя", ""),
                    "Фамилия": row.get("Фамилия", ""),
                    "Цель": row.get("Цель", ""),
                    "Архетип": row.get("Архетип", ""),
                    "Стиль": row.get("Стиль", ""),
                    "Субличность": row.get("Субличность", ""),
                    "Маска": row.get("Маска", ""),
                    "Сценарий": row.get("Сценарий", ""),
                    "Аватар": row.get("Аватар", ""),
                    "Визуал": row.get("Визуал", ""),
                    "curator_id": curator_id,
                    "created_at": now,
                    "last_interaction": now
                }

                user_profiles.append_row(list(profile_row.values()))

                # Обновление строки кода
                access_sheet.update_cell(i, list(row.keys()).index("ID") + 1, str(user_id))
                access_sheet.update_cell(i, list(row.keys()).index("Статус") + 1, "использован")
                access_sheet.update_cell(i, list(row.keys()).index("Когда использован") + 1, now)

                logging.info(f"[SHEETS] Код {code} активирован, user_id={user_id}")
                return
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при вставке пользователя: {e}")
