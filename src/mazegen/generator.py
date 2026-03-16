import random
from typing import List, Tuple, Optional
from collections import deque


DIRECTIONS = {
    "N": (0, -1, 0),
    "E": (1, 0, 1),
    "S": (0, 1, 2),
    "W": (-1, 0, 3),
}

OPPOSITE = {
    "N": "S",
    "S": "N",
    "E": "W",
    "W": "E",
}


class MazeGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        perfect: bool = True,
        seed: Optional[int] = None,
    ) -> None:

        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive.")

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit_
        self.perfect = perfect

        if seed is not None:
            random.seed(seed)

        self.maze: List[List[int]] = []

    # --------------------------------------------------

    def generate(self) -> None:
        self.maze = [
            [0b1111 for _ in range(self.width)]
            for _ in range(self.height)
        ]

        visited = [[False] * self.width for _ in range(self.height)]
        stack = [self.entry]
        visited[self.entry[1]][self.entry[0]] = True

        while stack:
            x, y = stack[-1]
            neighbors = []

            for d, (dx, dy, _) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if not visited[ny][nx]:
                        neighbors.append((d, nx, ny))

            if neighbors:
                d, nx, ny = random.choice(neighbors)
                self._remove_wall(x, y, d)
                self._remove_wall(nx, ny, OPPOSITE[d])
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        if not self.perfect:
            self._add_cycles()

    def _remove_wall(self, x: int, y: int, d: str) -> None:
        _, _, bit = DIRECTIONS[d]
        self.maze[y][x] &= ~(1 << bit)

    def _add_cycles(self) -> None:
        extra = (self.width * self.height) // 15

        for _ in range(extra):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            d = random.choice(list(DIRECTIONS.keys()))

            dx, dy, bit = DIRECTIONS[d]
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                self.maze[y][x] &= ~(1 << bit)
                _, _, opposite_bit = DIRECTIONS[OPPOSITE[d]]
                self.maze[ny][nx] &= ~(1 << opposite_bit)

    def shortest_path(self) -> str:
        queue = deque([(self.entry, "")])
        visited = {self.entry}

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == self.exit:
                return path

            for d, (dx, dy, bit) in DIRECTIONS.items():
                if not (self.maze[y][x] & (1 << bit)):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + d))

        return ""
