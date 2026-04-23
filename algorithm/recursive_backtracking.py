
import numpy as np


class backtracking():
    def __init__(self, width: int, height: int, path: str):
        self.width = width
        self.height = height
        self.path = path

    def create_maze(self):
        # creates a 2D array (grid)             example: [[1 1 1 1]
        # size height x width                             [1 1 1 1]
        # fills it with 1s                                [1 1 1 1]]
        maze = np.ones((self.height, self.width), dtype=int)

        for i in range(self.height):
            for j in range(self.width):
                if i % 2 == 1 or j % 2 == 1:
                    maze[i, j] = 0
