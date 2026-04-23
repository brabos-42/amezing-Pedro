import numpy as np
from enum import Enum
import random


class backtracking():
    def __init__(self, width: int, height: int, path: str):
        # adjust the width and height for the grid
        # if the size is even the mesh would turn broken ending in path
        # instead of wall so we create a 'invisible layer'
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.path = path

    # creates the base of the maze, the mesh
    # cell types:
    # 1 → untouched / potential path
    # 0 → wall
    # 0.5 → already visited (or reserved / blocked)

    def create_maze(self):
        # creates a 2D array (grid)             example: [[1 1 1 1]
        # size height x width                             [1 1 1 1]
        # fills it with 1s                                [1 1 1 1]]
        maze = np.ones((self.height, self.width), dtype=float)
        # loops through rolls                   example: [[1 0 1 0 1]
        # loops through columns                           [0 0 0 0 0]
        # if row or column is odd change to 0             [1 0 1 0 1]
        # that creates a grid skeleton                    [0 0 0 0 0]
        # a mesh that will be used as base                [1 0 1 0 1]]
        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0  # walls
                # we set the borders            example: 0.5 0.5 0.5 0.5 0.5
                # as visited so the                      0.5  0   0   0  0.5
                # creator wont go past it                0.5  0   1   0  0.5
                #                                        0.5  0   0   0  0.5
                #                                        0.5 0.5 0.5 0.5 0.5
                if (i == 0 or j == 0
                   or i == self.height - 1 or j == self.width - 1):
                    maze[i, j] = 0.5  # visited
                    maze[i, j] = 0

    def generate(self, coord_x, coord_y, grid):
        # mark the current cell as visited
        grid[coord_y, coord_x] = 0.5

        # these are the equivalent to UP DOWN LEFT RIGHT
        # but we skip one cell because of the structure
        # of our grid    ->   Cell   Wall   Cell
        # so this if means "are ALL neighboring cells already visited?”

        # logic breakdown:
        # 1. From current cell → try random directions
        # 2. If a neighbor hasn’t been visited →
        #   break the wall
        #   move there (recursively)
        # 3. If all neighbors visited → stop (backtrack)
        if (grid[coord_y - 2, coord_x] == 0.5 and grid[coord_y + 2, coord_x]
           == 0.5 and grid[coord_y, coord_x - 2] == 0.5
           and grid[coord_y, coord_x + 2] == 0.5):
            pass
        # explore:
        else:
            # create direction list
            li = [1, 2, 3, 4]
            # Picks a random direction
            # Removes it so it won't be tried again
            while len(li) > 0:
                dir = random.choice(li)
                li.remove(dir)

                # Convert direction into movement
                if dir == Directions.UP.value:
                    next_cell_x = coord_x
                    middle_cell_x = coord_x
                    next_cell_y = coord_y - 2
                    middle_cell_y = coord_y - 1
                elif dir == Directions.DOWN.value:
                    next_cell_x = coord_x
                    middle_cell_x = coord_x
                    next_cell_y = coord_y + 2
                    middle_cell_y = coord_y + 1
                elif dir == Directions.LEFT.value:
                    next_cell_x = coord_x - 2
                    middle_cell_x = coord_x - 1
                    next_cell_y = coord_y
                    middle_cell_y = coord_y
                elif dir == Directions.RIGHT.value:
                    next_cell_x = coord_x + 2
                    middle_cell_x = coord_x + 1
                    next_cell_y = coord_y
                    middle_cell_y = coord_y
                else:
                    next_cell_x = coord_x
                    middle_cell_x = coord_x
                    next_cell_y = coord_y
                    middle_cell_y = coord_y

                # checks if the next cell 
                if grid[next_cell_y, next_cell_x] != 0.5:
                    grid[middle_cell_y, middle_cell_x] = 0.5
                    self.generator(next_cell_x, next_cell_y, grid)

    def add_42_maze(self):
        current_maze = self.generate()
        print(f"{current_maze}")


# remembering which number is up, and which one is down isn’t optimal
# Instead, we will use enums to save the directions.
class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
