import sys
from utils import read_configuration
from dataclasses import dataclass
from algorithm import backtracking

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


def main() -> None:
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
        path=str(values_config["PERFECT"]),
    )
    test = backtracking(valuesReceiver.width,
                        valuesReceiver.height,
                        valuesReceiver.path)
    test.create_maze()
    print(f"{test.maze}! \n")


if __name__ == "__main__":
    main()
