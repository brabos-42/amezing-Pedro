import sys
from utils.read_configuration import read_configuration
from dataclasses import dataclass
from algorithm.recursive_backtracking import backtracking


@dataclass
class ValuesConfg:
    width: int
    height: int
    path: bool


def main() -> None:
    values_config: dict[str, str] | None = None
    if (len(sys.argv) != 2):
        print("Error need the file for generate")
        return
    values_config = read_configuration(sys.argv[1])
    print(f"{values_config} valores")
    if values_config is None:
        return None
    ValuesConfg(
        width=int(values_config["WIDTH"]),
        height=int(values_config["HEIGHT"]),
        path=bool(values_config["PERFECT"])
    )
    test = backtracking(ValuesConfg.width, ValuesConfg.height, path="")
    test.create_maze()


if __name__ == "__main__":
    main()
