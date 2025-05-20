import os
import json
import logging
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Загрузка переменных из .env
from dotenv import load_dotenv
load_dotenv()

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID")

# Пути
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
CREDS_PATH = os.path.join(BASE_DIR, "service_account.json")
CURATORS_PATH = os.path.join(BASE_DIR, "curators.json")

# Загрузка кураторов
with open(CURATORS_PATH, "r", encoding="utf-8") as f:
    CURATORS = json.load(f)

# Авторизация Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_PATH, SCOPE)
client = gspread.authorize(creds)

def extract_prefix_from_code(code):
    return code.split('-')[0].strip()

def get_curator_name_by_prefix(prefix):
    return CURATORS.get(prefix, {}).get("name", prefix)

def get_access_codes_worksheet(code: str):
    prefix = extract_prefix_from_code(code)
    if prefix not in CURATORS:
        raise ValueError(f"Неизвестный префикс кода: {prefix}")
    sheet_id = CURATORS[prefix]["sheet_id"]
    sheet_name = CURATORS[prefix]["sheet_name"]
    logging.info(f"[DEBUG] Префикс: {prefix}, Sheet ID: {sheet_id}, Sheet Name: {sheet_name}")
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return sheet, prefix

def insert_user_by_code(user_id: int, code: str) -> None:
    try:
        access_sheet, curator_id = get_access_codes_worksheet(code)
        user_profiles = client.open_by_key(GOOGLE_SHEET_ID).worksheet("user_profiles")

        rows = access_sheet.get_all_records()
        for i, row in enumerate(rows, start=2):
            if str(row.get("Код доступа", "")).strip() == code.strip():
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                code_prefix = extract_prefix_from_code(code)
                curator_name = get_curator_name_by_prefix(code_prefix)

                profile_row = {
                    "ID": str(user_id),
                    "Куратор": curator_name,
                    "Имя": row.get("Имя", ""),
                    "Возраст": row.get("Возраст", ""),  # ← ✅ добавлено
                    "Фамилия": row.get("Фамилия", ""),
                    "Цель": row.get("Цель", ""),
                    "Архетип": row.get("Архетип", ""),
                    "Стиль": row.get("Стиль", ""),
                    "Субличность": row.get("Субличность", ""),
                    "Маска": row.get("Маска", ""),
                    "Сценарий": row.get("Сценарий", ""),
                    "Аватар": row.get("Аватар", ""),
                    "Визуал": row.get("Визуал", ""),
                    "created_at": now,
                    "last_interaction": now
                }

                # Обновлённый список колонок с учётом "Возраст"
                columns = [
                    "ID", "Куратор", "Имя", "Возраст", "Фамилия", "Цель", "Архетип",
                    "Стиль", "Субличность", "Маска", "Сценарий", "Аватар", "Визуал",
                    "created_at", "last_interaction"
                ]

                user_profiles.append_row([profile_row.get(col, "") for col in columns])

                # Обновляем статус в access_sheet
                access_sheet.update_cell(i, list(row.keys()).index("Статус") + 1, "Использован")
                access_sheet.update_cell(i, list(row.keys()).index("Когда использован") + 1, now)
                return
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при добавлении пользователя: {e}")
        return


def check_code_valid(code: str) -> bool:
    try:
        sheet, _ = get_access_codes_worksheet(code)
        data = sheet.get_all_records()
        for row in data:
            logging.info(f"[DEBUG] Проверка строки: {row}")
            code_cell = str(row.get("Код доступа", "")).strip()
            status_cell = str(row.get("Статус", "")).strip().lower()
            if code_cell == code.strip() and status_cell != "использован":
                logging.info(f"[DEBUG] ✅ Код найден: {code_cell}, статус: {status_cell}")
                return True
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при проверке кода: {e}")
    return False    

def get_profile_by_user_id(user_id: int):
    """
    Получить профиль пользователя по его Telegram user_id из таблицы user_profiles.
    """
    try:
        user_profiles = client.open_by_key(GOOGLE_SHEET_ID).worksheet("user_profiles")
        records = user_profiles.get_all_records()
        for row in records:
            if str(row.get("ID", "")) == str(user_id):
                return row
        return None
    except Exception as e:
        logging.error(f"[SHEETS] Ошибка при получении профиля пользователя: {e}")
        return None
