import numpy as np
from enum import Enum
import random
import cv2  # type: ignore


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
        self.path = "path.jpg"
        self.maze: np.ndarray | None = None

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
        self.maze = maze
        self.add_42_maze()
        # select from [2, 4, 6, ...] which is guaranteed to be unvisited
        # to choose a starting point
        # Only even indices are valid “cells”
        # 0 and width-1 are borders so we start at 2
        sx = random.choice(range(2, self.width - 2, 2))
        sy = random.choice(range(2, self.height - 2, 2))

        self.generator(sx, sy, maze)
        # cleanup step at the end of the algorithm
        # Anywhere I see 0.5 (visited), turn it into 1 (wall)
        #   Before: 0.5 0.5 0.5 0.5 0.5       After: 1 1 1 1 1
        #           0.5 0   0.5 0   0.5              1 0 1 0 1
        #           0.5 0   0.5 0   0.5              1 0 1 0 1
        #           0.5 0   0   0   0.5              1 0 0 0 1
        #           0.5 0.5 0.5 0.5 0.5              1 1 1 1 1
        for i in range(self.height):
            for j in range(self.width):
                if maze[i, j] == 0.5:
                    if (i == 0 or j == 0 or
                       i == self.height - 1 or j == self.width - 1):
                        maze[i, j] = 0   # keep borders as walls
                else:
                    maze[i, j] = 1   # internal visited → path
        # set entry and exit of the maze
        # !! we need to change it to the parameters they give
        maze[1, 2] = 0.5
        maze[self.height - 2, self.width - 3] = 0.5
        # save the maze!
        # makes it into an immage
        # 0 -> black pixels
        # 1 becomes 255 -> white pixels
        maze = (maze * 255).astype('uint8')
        cv2.imwrite(self.path, maze)

    def generator(self, coord_x, coord_y, grid):
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
        if (self.is_visited(coord_x, coord_y - 2, grid) and
           self.is_visited(coord_x, coord_y + 2, grid) and
           self.is_visited(coord_x - 2, coord_y, grid) and
           self.is_visited(coord_x + 2, coord_y, grid)):
            return
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

                # checks if the next cell is unvisited
                if (0 <= next_cell_x < self.width and
                   0 <= next_cell_y < self.height and
                   grid[next_cell_y, next_cell_x] != 0.5):
                    # breaks the wall
                    grid[middle_cell_y, middle_cell_x] = 0.5
                    # moves recursively
                    self.generator(next_cell_x, next_cell_y, grid)

    def is_visited(self, x, y, grid):
        if 0 <= y < self.height and 0 <= x < self.width:
            return grid[y, x] == 0.5
        return True  # treat out-of-bounds as visited

    def add_42_maze(self) -> None:
        if (self.maze is not None):
            coord_x = self.width // 2
            coord_y = self.height // 2
            offsets: list[tuple[int, int]] = [
                (-2, -3),
                (-1, -3),
                (0, -3),
                (0, -2),
                (0, -1),
                (1, -1),
                (2, -1),
            ]
            for dy, dx in offsets:
                self.maze[coord_y + dy, coord_x + dx] = 0
            print(f"célula: [{coord_y - 2}, {coord_x + 3}]")
            print(f"{self.maze} \n")


# remembering which number is up, and which one is down isn’t optimal
# Instead, we will use enums to save the directions.
class Directions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
