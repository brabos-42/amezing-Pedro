import sys


def is_valid_keys(configs: dict) -> bool:
    return configs.__contains__("WIDTH")


def read_configuration(path: str) -> dict:
    configuration: dict = {}
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


def main():
    values_config: dict
    if (len(sys.argv) != 2):
        print("Error need the file for generate")
        return
    values_config = read_configuration(sys.argv[1])
    print(f"{values_config} valores")


if __name__ == "__main__":
    main()
