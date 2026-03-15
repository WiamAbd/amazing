"""
Maze generation logic with structural 42,
clean DFS handling and controlled imperfect mode.
"""

import random
from typing import List, Tuple, Optional
from utils import DIRECTIONS, OPPOSITE, inside_bounds


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

        # Cells forming the 42 shape
        self.pattern_cells = set()

        self._prepare_42_structure()

        self._validate_positions()

    # --------------------------------------------------
    # Basic validation
    # --------------------------------------------------

    def _validate_positions(self) -> None:
        if not inside_bounds(*self.entry, self.width, self.height):
            raise ValueError("Entry outside maze bounds.")

        if not inside_bounds(*self.exit, self.width, self.height):
            raise ValueError("Exit outside maze bounds.")

        if self.entry == self.exit:
            raise ValueError("Entry and Exit must differ.")

        if self.entry in self.pattern_cells:
            raise ValueError("Entry cannot be inside the 42 pattern.")

        if self.exit in self.pattern_cells:
            raise ValueError("Exit cannot be inside the 42 pattern.")
        

    # --------------------------------------------------
    # Prepare 42 coordinates
    # --------------------------------------------------

    def _prepare_42_structure(self) -> None:
        pattern = [
            "X   XXX",
            "X     X",
            "XXX XXX",
            "  X X  ",
            "  X XXX",
        ]
        # pattern = [
        #     "XX XXX XXX XXXX",
        #     " X   X   X    X",
        #     " X XXX XXX   X ",
        #     " X   X   X  X  ",
        #     " X XXX XXX X   ",]
        
        ph = len(pattern)
        pw = max(len(row) for row in pattern)

        start_x = self.width // 2 - pw // 2
        start_y = self.height // 2 - ph // 2

        for y in range(ph):
            for x in range(len(pattern[y])):
            #for x in range(pw):
                if pattern[y][x] == "X":
                    cx = start_x + x
                    cy = start_y + y
                    if inside_bounds(cx, cy, self.width, self.height):
                        self.pattern_cells.add((cx, cy))

    # --------------------------------------------------
    # DFS Maze Generation
    # --------------------------------------------------

    def generate(self) -> None:
        # Reset full grid
        self.maze = [
            [0b1111 for _ in range(self.width)]
            for _ in range(self.height)
        ]

        visited = []
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append(False)
            visited.append(row)

        # Mark 42 cells as already visited (treated as obstacles)
        for (x, y) in self.pattern_cells:
            visited[y][x] = True

        stack = [self.entry]
        visited[self.entry[1]][self.entry[0]] = True

        while stack:
            x, y = stack[-1]
            neighbors = []

            for d, (dx, dy, _) in DIRECTIONS.items():
                nx, ny = x + dx, y + dy

                if inside_bounds(nx, ny, self.width, self.height):
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

        # Ensure 42 cells remain fully closed
        for (x, y) in self.pattern_cells:
            self.maze[y][x] = 0b1111

        # Add controlled cycles if imperfect
        if not self.perfect:
            self._add_cycles()

    def _remove_wall(self, x: int, y: int, d: str) -> None:
        _, _, bit = DIRECTIONS[d]
        self.maze[y][x]=self.maze[y][x] & ~(1 << bit)
    # --------------------------------------------------
    # Controlled Imperfect Mode
    # --------------------------------------------------

    def _add_cycles(self) -> None:
        candidates = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue

                for d, (dx, dy, bit) in DIRECTIONS.items():
                    nx, ny = x + dx, y + dy

                    if not inside_bounds(nx, ny, self.width, self.height):
                        continue

                    if (nx, ny) in self.pattern_cells:
                        continue

                    if self.maze[y][x] & (1 << bit):
                        candidates.append((x, y, d))

        random.shuffle(candidates)

        max_cycles = (self.width * self.height) // 15
        cycles_added = 0

        for x, y, d in candidates:
            if cycles_added >= max_cycles:
                break

            dx, dy, bit = DIRECTIONS[d]
            nx, ny = x + dx, y + dy

            # Temporarily remove wall
            self.maze[y][x] &= ~(1 << bit)
            _, _, opposite_bit = DIRECTIONS[OPPOSITE[d]]
            self.maze[ny][nx] &= ~(1 << opposite_bit)

            if self._has_large_open_area():
                # Revert
                self.maze[y][x] |= (1 << bit)
                self.maze[ny][nx] |= (1 << opposite_bit)
                continue

            cycles_added += 1

    # --------------------------------------------------
    # Room size validation
    # --------------------------------------------------

    def _has_large_open_area(self) -> bool:
        # Check 3x3 fully open
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                open_count = 0
                for dy in range(3):
                    for dx in range(3):
                        if self.maze[y + dy][x + dx] == 0:
                            open_count += 1
                if open_count == 9:
                    return True

        return False

    # --------------------------------------------------
    # Shortest path (BFS)
    # --------------------------------------------------

    def shortest_path(self) -> str:
        """Find shortest path from entry to exit using BFS."""
        queue = [(self.entry, "")]
        visited = {self.entry}

        while queue:
            (x, y), path = queue.pop(0)  # ← only change from deque version

            if (x, y) == self.exit:
                return path

            for d, (dx, dy, bit) in DIRECTIONS.items():
                if not (self.maze[y][x] & (1 << bit)):
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + d))

        return ""

    # --------------------------------------------------
    # Output file
    # --------------------------------------------------

    def write_output(self, filename: str) -> None:
        path = self.shortest_path()

        with open(filename, "w", encoding="utf-8") as f:
            for row in self.maze:
                f.write("".join(f"{cell:X}" for cell in row) + "\n")

            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            f.write(f"{path}\n")