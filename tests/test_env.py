import os
from dotenv import load_dotenv

load_dotenv()

print("GOOGLE_CREDENTIALS_PATH:", os.getenv("GOOGLE_CREDENTIALS_PATH"))
print("GOOGLE_SHEET_ID:", os.getenv("GOOGLE_SHEET_ID"))
