import os

PROMPT_PATH = os.path.join("data", "prompt.txt")

def build_prompt(profile: dict, input_text: str) -> str:
    try:
        with open(PROMPT_PATH, "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError:
        raise Exception(f"Prompt template not found at {PROMPT_PATH}")
    
    # Маппинг русских названий столбцов на нужные поля
    mapped_profile = {
        "goal": profile.get("Цель", ""),
        "persona": profile.get("Архетип", ""),
        "style": profile.get("Стиль", ""),
        "subself": profile.get("Субличность", ""),
        "mode": profile.get("mode", "base"),
        "name": profile.get("Имя", ""),
        "age": profile.get("Возраст", "")
    }

    prompt = template.format(
        goal=mapped_profile["goal"],
        persona=mapped_profile["persona"],
        style=mapped_profile["style"],
        subself=mapped_profile["subself"],
        mode=mapped_profile["mode"],
        input=input_text,
        name=mapped_profile["name"],
        age=mapped_profile["age"]
    )
    return prompt
