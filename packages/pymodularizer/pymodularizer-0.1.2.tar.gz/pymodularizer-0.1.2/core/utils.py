def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "_")

def validate_choice(choices: list, idx: int) -> str:
    try:
        return choices[idx]
    except IndexError:
        raise ValueError("Escolha inválida")
