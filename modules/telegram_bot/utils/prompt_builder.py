def build_prompt(profile: dict, instruction: str) -> str:
    return (
        f"Твоя цель: {profile['goal']}.\n"
        f"Твой стиль: {profile['style']}.\n"
        f"Ты говоришь от лица субличности: {profile['subself']}.\n\n"
        f"{instruction}"
    )
