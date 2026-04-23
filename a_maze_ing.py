import sys
from utils.read_configuration import read_configuration


def main():
    values_config: dict
    if (len(sys.argv) != 2):
        print("Error need the file for generate")
        return
    values_config = read_configuration(sys.argv[1])
    print(f"{values_config} valores")


if __name__ == "__main__":
    main()
