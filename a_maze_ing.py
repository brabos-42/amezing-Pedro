import sys
from utils import read_configuration, Solution
from dataclasses import dataclass
from algorithm import MazeGenerator
import random

COLORS = {
    "white":   "\033[97m",
    "red":     "\033[91m",
    "green":   "\033[92m",
    "yellow":  "\033[93m",
    "blue":    "\033[94m",
    "magenta": "\033[95m",
    "cyan":    "\033[96m",
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
    """
    Data container for maze configuration values.

    Attributes:
        width (int): Maze width (logical units).
        height (int): Maze height (logical units).
        path (str): Output file path.
        perfect (bool): Whether to generate a perfect maze.
        entry (tuple): Entry coordinates (row, col).
        exit (tuple): Exit coordinates (row, col).
        seed (str): Random seed for reproducibility.
    """


def entry_tuples(value: str) -> tuple[int, int]:
    """
    Convert a string representation of coordinates into a tuple.

    Args:
        value (str): Coordinate string in the format "(y,x)".

    Returns:
        tuple[int, int]: Parsed (y, x) coordinates.
    """
    return tuple(int(x) for x in value.replace('(', '').split(','))


def parse_bool(value: str) -> bool:
    """
    Convert a string to a boolean value.

    Args:
        value (str): Input string.

    Returns:
        bool: True if value represents a truthy string ("true", "1", "yes"),
        False otherwise.
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
        valuesReceiver.display_maze,
        valuesReceiver.entry,
        valuesReceiver.exit,
        valuesReceiver.perfect
    )
    gen.create_maze()
    return gen


def apply_solution(gen, valuesReceiver):
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


def display_maze(gen, maze_color):
    gen._set_color_wall(maze_color)
    print(RESET)


def main() -> None:
    """
    Main entry point for maze generation and solving.

    Workflow:
        1. Read configuration file from command-line argument.
        2. Parse configuration into a structured dataclass.
        3. Validate dimensions and seed randomness.
        4. Generate the maze.
        5. Solve the maze using BFS.
        6. Mark the solution path in the maze.
        7. Print the colored maze.
        8. Append movement directions (N, S, E, W) to the output file.

    Notes:
        - Entry and exit positions are given in logical coordinates.
        - The solution path is written as directional steps.
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
    show_solution = False
    color_names = list(COLORS.keys())
    color_index = 0
    maze_color = COLORS[color_names[color_index]]


    gen._set_color_wall("033[92m")
    gen._cell._set_color_wall("\033[92m")
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
            show_solution = False
            display_maze(gen, maze_color)
            print("\n[+] Maze Regenerated!")

        elif choice == 2:
            show_solution = not show_solution
            gen = generate_maze(valuesReceiver, valuesReceiver.seed)
            if show_solution:
                gen, resolution = apply_solution(gen, valuesReceiver)
                if resolution is None:
                    print("\n[!] No solution found!")
                    show_solution = False
                else:
                    display_maze(gen, maze_color)
                    print(f"\n[+] Solution Shown!")
            else:
                display_maze(gen, maze_color)
                print(f"\n[+] Solution Hidden!")

        elif choice == 3:
            color_index = (color_index + 1) % len(color_names)
            maze_color = COLORS[color_names[color_index]]
            display_maze(gen, maze_color)
            print(f"\n[+] Color changed to {color_names[color_index]}!")

        elif choice == 0:
            print(f"{RESET}Quitting...")
            break

if __name__ == "__main__":
    main()