from typing import Set


def is_valid_keys(configs: dict) -> bool:
    mandatory_keys:  Set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "DISPLAY_MAZE",
        "SEED"
    }
    current_keys: Set[str] = set(configs.keys())
    missing_keys: Set[str] = mandatory_keys - current_keys
    if missing_keys:
        print(f"Erro: Chaves obrigatórias ausentes: {', '.join(missing_keys)}")
        return False
    return configs.__contains__("WIDTH")
