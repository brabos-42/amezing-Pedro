from typing import Set


def is_valid_keys(configs: dict) -> bool:
    """
    Validate that a configuration dictionary contains all required keys.

    Args:
        configs (dict): Dictionary containing configuration parameters.

    Returns:
        bool: True if all mandatory keys are present, False otherwise.

    Notes:
        - Required keys are:
            WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT, SEED
        - Prints an error message listing missing keys if validation fails.
        - The final return checks for "WIDTH", which is redundant if all
        keys exist.
    """
    mandatory_keys:  Set[str] = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
        "SEED"
    }
    current_keys: Set[str] = set(configs.keys())
    missing_keys: Set[str] = mandatory_keys - current_keys
    if missing_keys:
        print(f"Erro: Chaves obrigatórias ausentes: {', '.join(missing_keys)}")
        return False
    return configs.__contains__("WIDTH")
