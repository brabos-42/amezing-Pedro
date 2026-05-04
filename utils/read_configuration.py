import sys
from .is_valid_keys import is_valid_keys


def read_configuration(path: str) -> dict[str, str]:
    """
    Function for the read file that receive in sys.args

    The function return a Dict[str, str].
    If the mmandatory fields no has in the file the program is stop
    """
    # variable configuration of type Dict[str, str]
    configuration: dict[str, str] = {}
    # 'Try' block is used to run code if it the fails her run 'Exept'
    try:
        # Open the file. The file read line for line
        with open(path, "r") as file:
            for line in file:
                # remove the white spaces in start and end file
                line = line.strip()
                # if the line for white or start the #
                if (not line or line.startswith("#")):
                    continue
                # if the line not have = in your caractes break the program
                if ("=" not in line):
                    print("Erro: Sintaxe inválida")
                    sys.exit(1)
                # create the variavles key and value and get the field in order
                key, value = line.split("=", 1)
                key, value = key.strip(), value.strip()
                # add the value in the prop {'width':"50"}
                configuration[key] = value
        # verify if the file contains all the condiguration mandatory
        if (not is_valid_keys(configuration)):
            print("Not has all atributes mandatorys")
            sys.exit()
        return (configuration)
    except FileNotFoundError:
        print("Erro open the file")
        sys.exit()
