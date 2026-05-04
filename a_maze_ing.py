import sys
import copy
from utils import read_configuration, Solution
from dataclasses import dataclass
from algorithm import MazeGenerator
import random
from typing import Optional

COLORS = {
    "white":   "\033[48;2;200;200;200m",
    "red":     "\033[48;2;180;50;50m",
    "green":   "\033[48;2;50;150;50m",
    "yellow":  "\033[48;2;180;180;50m",
    "blue":    "\033[48;2;50;50;180m",
    "magenta": "\033[48;2;150;50;150m",
    "cyan":    "\033[48;2;50;180;180m",
}
RESET = "\033[0m"


@dataclass
class ValuesConfg:
    width: int
    height: int
    path: str
    perfect: bool
    entry: tuple
    exit: tuple
    seed: str


def entry_tuples(value: str) -> tuple[int, int]:
    """
        Pega o os valores em strings de tuples e transforma para tuples de fato
    """
    parts = [
        int(x.strip())
        for x in value.replace('(', '').replace(')', '').split(',')
        if x.strip()
    ]
    return (parts[0], parts[1])


def parse_bool(value: str) -> bool:
    """
        Pega o valor de entrada e virifica, transformando em boolean de acordo
    """
    return value.strip().lower() in ("true", "1", "yes")


def generate_maze(valuesReceiver, seed: str):
    if valuesReceiver.seed == "":
        random.seed()
    else:
        random.seed(valuesReceiver.seed)

    gen = MazeGenerator(
        valuesReceiver.width,
        valuesReceiver.height,
        valuesReceiver.path,
        valuesReceiver.entry,
        valuesReceiver.exit,
        valuesReceiver.perfect
    )
    gen.create_maze()
    return gen


def apply_solution(gen, valuesReceiver) -> tuple[MazeGenerator, Optional[list[tuple[int, int]]]]:
    """
        função que aplica a solução do labirito chamando a Class Solution.
        A class recebe valor de entrada e valor e o maze
        e usar a função bfs_resolver para concluir. 

        Essa função usa o algoritimo de bfs para resolver o labirinto, e ele retorna um lista
        de tuplas para indicando o caminho.

        pegamos o maze e usamos a nossa lista indicando a posiçao dos caminhos para 
        mudar o valor das celular assim mudando a cor do caminho

    """
    solution = Solution(valuesReceiver.entry, valuesReceiver.exit, gen.maze)
    resolution = solution.bfs_resolver()
    if resolution is None:
        return gen, None

    for i, (y, x) in enumerate(resolution):
        gen.maze[y, x] = 3
        if i + 1 < len(resolution):
            ny, nx = resolution[i + 1]
            my, mx = resolution[i]
            gen.maze[(y + ny) // 2, (x + nx) // 2] = 3
            gen.maze[(y + my) // 2, (x + mx) // 2] = 3

    return gen, resolution


def display_maze(gen, maze_color) -> None:
    """
        fução para exibir o maze passa a cor da parede como parametro
    """
    maze_lines = gen.generate_final_maze(wall_color=maze_color)
    for line in maze_lines:
        print(line)
    print(RESET)


def main() -> None:
    """
        Função inicial do nosso programa, ele rodar as validações dos valores inicias
        Pega o arquivo  valida as campos, entradas, se passou o arquivo,
        converte em parametro de um objeto

        Roda o Ui no terminal para interação do usuario

    """
    if len(sys.argv) != 2:
        print("Error need the file for generate")
        return

    values_config = read_configuration(sys.argv[1])
    valuesReceiver = ValuesConfg(
        width=int(values_config["WIDTH"]),
        height=int(values_config["HEIGHT"]),
        path=str(values_config["OUTPUT_FILE"]),
        perfect=parse_bool(values_config['PERFECT']),
        entry=entry_tuples(values_config['ENTRY']),
        exit=entry_tuples(values_config['EXIT']),
        seed=str(values_config['SEED'])
    )

    gen = generate_maze(valuesReceiver, valuesReceiver.seed)
    original_maze = copy.deepcopy(gen.maze)
    show_solution = False
    color_names = list(COLORS.keys())
    color_index = 0
    maze_color = COLORS[color_names[color_index]]

    display_maze(gen, maze_color)

    while True:
        print("=====  A-MAZE-ING  =====")
        print("1) Regenerate a New Maze")
        print(f"2) {'Hide' if show_solution else 'Show'} Solution")
        print("3) Rotate Maze Colors")
        print(f"0) Quit{RESET}\n")

        try:
            raw = input(f"Choice from 0-3 \n $ {RESET}").strip()
            choice = int(raw)
        except ValueError:
            print("\n[!] Invalid choice, please choose from 0-3")
            continue

        if not 0 <= choice <= 3:
            print("\n[!] Invalid choice, please choose from 0-3")
            continue

        if choice == 1:
            gen = generate_maze(valuesReceiver, valuesReceiver.seed)
            original_maze = copy.deepcopy(gen.maze)
            show_solution = False
            display_maze(gen, maze_color)
            print("\n[+] Maze Regenerated!")

        elif choice == 2:
            show_solution = not show_solution
            gen.maze = copy.deepcopy(original_maze)
            if show_solution:
                gen, resolution = apply_solution(gen, valuesReceiver)
                if resolution is None:
                    print("\n[!] No solution found!")
                    show_solution = False
                else:
                    display_maze(gen, maze_color)
                    print("\n[+] Solution Shown!")
            else:
                display_maze(gen, maze_color)
                print("\n[+] Solution Hidden!")

        elif choice == 3:
            color_index = (color_index + 1) % len(color_names)
            maze_color = COLORS[color_names[color_index]]
            gen.maze = copy.deepcopy(original_maze)
            if show_solution:
                gen, resolution = apply_solution(gen, valuesReceiver)
            display_maze(gen, maze_color)
            print(f"\n[+] Color changed to {color_names[color_index]}!")

        elif choice == 0:
            print(f"{RESET}Quitting...")
            break


if __name__ == "__main__":
    main()