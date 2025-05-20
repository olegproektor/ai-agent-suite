import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

CREDENTIALS_PATH = os.getenv("GOOGLE_CREDENTIALS_PATH", "service_account.json")
SPREADSHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_NAME = "user_profiles"

def get_profile_by_user_id(user_id: int) -> dict:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()

    for row in data:
        if str(row.get("ID")) == str(user_id):  # ✅ исправлено с "user_id" на "ID"
            profile = dict(row)
            profile["mode"] = profile.get("mode", "base")  # базовый режим по умолчанию
            return profile

    return None
