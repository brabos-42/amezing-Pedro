import sys
from utils import read_configuration
from dataclasses import dataclass
from algorithm import backtracking
import random

"""
Add Decorator DataClasss on a Class. He help us add the propieties Class for
the use with the batter usebility
Ex: Before DataClass
    values_config["<NameProp>"]
after DataClass
    values_config.<nameProp>
"""


@dataclass
class ValuesConfg:
    width: int
    height: int
    path: str
    display_maze: bool
    perfect: bool
    entry: tuple
    exit: tuple


def entry_tuples(value: str) -> tuple[int, int]:
    return tuple(int(x) for x in value.replace('(', '').split(','))


def parse_bool(value: str) -> bool:
    return value.strip().lower() in ("true", "1", "yes")


def main() -> None:
    """

    """
    # create the variable for to receiver values the file config
    if (len(sys.argv) != 2):
        print("Error need the file for generate")
        return
    # This function get and return a Dict with the configs
    values_config = read_configuration(sys.argv[1])
    # Use the ValueConfig class
    valuesReceiver = ValuesConfg(
        width=int(values_config["WIDTH"]),
        height=int(values_config["HEIGHT"]),
        path=str(values_config["OUTPUT_FILE"]),
        perfect=parse_bool(values_config['PERFECT']),
        entry=entry_tuples(values_config['ENTRY']),
        exit=entry_tuples(values_config['EXIT']),
        display_maze=parse_bool(values_config['DISPLAY_MAZE'])
    )
    random.seed(42)
    test = backtracking(valuesReceiver.width,
                        valuesReceiver.height,
                        valuesReceiver.path,
                        valuesReceiver.display_maze,
                        valuesReceiver.entry,
                        valuesReceiver.entry)

    test.create_maze()


if __name__ == "__main__":
    main()
