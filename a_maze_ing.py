import sys
from utils.read_configuration import read_configuration
# from algorithm.recursive_backtracking import backtracking


def main() -> None:
    values_config: dict[str, str] | None = None
    if (len(sys.argv) != 2):
        print("Error need the file for generate")
        return
    values_config = read_configuration(sys.argv[1])
    print(f"{values_config} valores")


if __name__ == "__main__":
    main()
