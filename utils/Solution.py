class Solution:
    def __init__(self, entry: tuple[int, int], exit: tuple[int, int], maze):
        self._entry = entry
        self._exit = exit
        self._maze = maze

    def bfs_resolver(self):
        cost = 0
        visited: list = []
        possibles_positios: list = []
        solution_router: list = []

        visited.append(self._entry)
        possibles_positios.append(self._entry)

        while possibles_positios:
            current_position = possibles_positios.pop(0)

            if current_position == self._exit:
                solution_router.append(current_position)
                return solution_router

            for neighbor in self.maze[current_position]:
                if neighbor not in visited:
                    possibles_positios.append(neighbor)
                    visited.append(neighbor)

            cost += 1
        return cost,
