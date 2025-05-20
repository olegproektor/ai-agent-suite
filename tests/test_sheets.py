# tests/test_sheets.py

from modules.telegram_bot.sheets.sheets import (
    get_profile_by_user_id,
    get_full_profile,
    check_code_valid,
    insert_user_by_code
)

test_user_id = 514847371
test_code = "OLG-1001"  # Убедись, что этот код есть в access_codes_oleg

print("\n🔍 Тест 1: get_profile_by_user_id")
profile = get_profile_by_user_id(test_user_id)
print("Базовый профиль:", profile)

print("\n🔍 Тест 2: get_full_profile")
full_profile = get_full_profile(test_user_id)
print("Полный профиль:", full_profile)

print(f"\n🔍 Тест 3: check_code_valid('{test_code}')")
is_valid = check_code_valid(test_code)
print("Код валиден:", is_valid)

if is_valid:
    print("\n🔧 Тест 4: insert_user_by_code(...)")
    insert_user_by_code(test_user_id, test_code)
    print("✅ Код применён, профиль должен быть добавлен.")
else:
    print("⛔ Пропущен insert_user_by_code — код недействителен.")
