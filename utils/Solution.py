class Solution:
    def __init__(self, entry: tuple[int, int], exit: tuple[int, int], maze):
        """
        Solves a maze using Breadth-First Search (BFS) to find the
        shortest path
        between an entry and an exit.

        The maze is expected to be a grid (e.g., NumPy array) where:
            1 -> wall
            2 -> blocked/special cell (not traversable)
            other values -> traversable cells

        Logical coordinates (row, col) are converted to grid coordinates using:
            (y * 2 + 1, x * 2 + 1)
        """
        # entry/exit estão em coordenadas lógicas (linha, col)
        # mas no maze real as células são (y*2+1, x*2+1)
        ey, ex = entry
        self._entry = (ey * 2 + 1, ex * 2 + 1)
        zy, zx = exit
        self._exit = (zy * 2 + 1, zx * 2 + 1)
        self._maze = maze

    def _neighbors(self, y, x):
        """Retorna células vizinhas acessíveis
        (passo de 2, verifica parede do meio)."""
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        result = []
        for dy, dx in directions:
            ny, nx = y + dy, x + dx
            my, mx = y + dy // 2, x + dx // 2  # célula do meio (parede)
            if (0 <= ny < self._maze.shape[0] and
               0 <= nx < self._maze.shape[1] and
               self._maze[my, mx] != 1 and   # parede entre as células
               self._maze[ny, nx] != 1 and
               self._maze[my, mx] != 2 and   # célula destino não é parede
               self._maze[ny, nx] != 2):     # nem célula especial
                result.append((ny, nx))
        return result

    def bfs_resolver(self) -> list[tuple[int, int]]:
        """
        Return accessible neighboring cells.

        Movement is performed in steps of 2 (skipping walls), while checking
        the intermediate cell to ensure there is no wall between cells.

        Args:
            y (int): Current y-coordinate.
            x (int): Current x-coordinate.

        Returns:
            list[tuple[int, int]]: List of valid neighboring coordinates.

        Notes:
            - A move is valid if:
                * The destination is داخل bounds.
                * The intermediate cell (wall) is not a wall (1) or
                blocked (2).
                * The destination cell is not a wall (1) or blocked (2).
        """
        from collections import deque

        start = self._entry
        end = self._exit

        # came_from rastreia o pai de cada célula visitada
        came_from = {start: None}
        queue = deque([start])

        while queue:
            current = queue.popleft()

            if current == end:
                # reconstrói o caminho de trás pra frente
                path = []
                while current is not None:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path

            for neighbor in self._neighbors(*current):
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    queue.append(neighbor)

        return []  # sem solução
