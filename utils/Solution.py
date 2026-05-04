from collections import deque


class Solution:
    def __init__(self, entry: tuple[int, int], exit: tuple[int, int], maze):
        """
        Solves a maze using Breadth-First Search (BFS) to find the
        shortest path between an entry and an exit.

        The maze is expected to be a grid (list of lists) where:
            1 -> wall
            2 -> blocked/special cell (not traversable)
            other values -> traversable cells

        Logical coordinates (row, col) are converted to grid coordinates using:
            (y * 2 + 1, x * 2 + 1)
        """
        ey, ex = entry
        self._entry = (ey * 2 + 1, ex * 2 + 1)
        zy, zx = exit
        self._exit = (zy * 2 + 1, zx * 2 + 1)
        self._maze = maze

    def _neighbors(self, y, x):
        """Retorna células vizinhas acessíveis
        (passo de 2, verifica parede do meio)."""
        rows = len(self._maze)
        cols = len(self._maze[0])
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        result = []
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            my, mx = y + dy // 2, x + dx // 2
            if (0 <= ny < rows and
               0 <= nx < cols and
               self._maze[my][mx] != 1 and
               self._maze[ny][nx] != 1 and
               self._maze[my][mx] != 2 and
               self._maze[ny][nx] != 2):
                result.append((ny, nx))
        return result

    def bfs_resolver(self) -> list[tuple[int, int]]:
        """
        Executes BFS from entry to exit and returns the shortest path.

        Returns:
            list[tuple[int, int]]: Ordered list of coordinates from entry
            to exit, or empty list if no solution exists.
        """
        start = self._entry
        end = self._exit

        came_from: dict[tuple[int, int],
                        tuple[int, int] | None] = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            if current == end:
                path: list[tuple[int, int]] = []
                node: tuple[int, int] | None = current
                while node is not None:
                    path.append(node)
                    node = came_from[node]
                path.reverse()
                return path

            for neighbor in self._neighbors(*current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return []