import numpy as np


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
        grid[coord_y, coord_x] = 0.5

        if (grid[coord_y - 2, coord_x] == 0.5 and grid[coord_y + 2, coord_x]
           == 0.5 and grid[coord_y, coord_x - 2] == 0.5
           and grid[coord_y, coord_x + 2] == 0.5):
            pass
        else:
            pass
