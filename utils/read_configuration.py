import sys
from .is_valid_keys import is_valid_keys


def read_configuration(path: str) -> dict[str, str] | None:
    configuration: dict[str, str] = {}
    try:
        with open(path, "r") as file:
            for line in file:
                line = line.strip()
                if (not line or line.startswith("#")):
                    continue
                if ("=" not in line):
                    print("Erro: Sintaxe inválida")
                    sys.exit(1)
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()
                configuration[key] = value
        if (not is_valid_keys(configuration)):
            print("Not has all atributes mandatorys")
            return None
        return (configuration)
    except FileNotFoundError:
        print("Erro open the file")
        return None