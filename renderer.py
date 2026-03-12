"""
Renderer with color rotation and menu.
"""

from maze import MazeGenerator

RESET = "\033[0m"

# Color themes
COLOR_THEMES = [
    {"walls": "\033[97m", "path": "\033[96m", "pattern": "\033[93m"},
    {"walls": "\033[92m", "path": "\033[94m", "pattern": "\033[91m"},
    {"walls": "\033[95m", "path": "\033[92m", "pattern": "\033[96m"},
]

current_theme_index = 0


def render(maze: MazeGenerator, show_path: bool = False) -> None:
    theme = COLOR_THEMES[current_theme_index]

    wall_color = theme["walls"]
    path_color = theme["path"]
    pattern_color = theme["pattern"]

    width = maze.width
    height = maze.height

    path_positions = set()

    if show_path:
        x, y = maze.entry
        path_positions.add((x, y))

        for move in maze.shortest_path():
            if move == "N":
                y -= 1
            elif move == "S":
                y += 1
            elif move == "E":
                x += 1
            elif move == "W":
                x -= 1
            path_positions.add((x, y))

    # Top border
    print(wall_color + "+" + "---+" * width + RESET)

    for j in range(height):
        row = wall_color + "|" + RESET

        for i in range(width):
            cell = maze.maze[j][i]

            if (i, j) == maze.entry:
                content = path_color + " E " + RESET
            elif (i, j) == maze.exit:
                content = path_color + " X " + RESET
            elif show_path and (i, j) in path_positions:
                content = path_color + " . " + RESET
            elif (i, j) in maze.pattern_cells:
                content = pattern_color + "███" + RESET
            else:
                content = "   "

            row += content

            if cell & (1 << 1):
                row += wall_color + "|" + RESET
            else:
                row += " "

        print(row)

        row = wall_color + "+"
        for i in range(width):
            cell = maze.maze[j][i]
            if cell & (1 << 2):
                row += "---+"
            else:
                row += "   +"

        print(row + RESET)


def run_menu(maze: MazeGenerator) -> None:
    global current_theme_index

    show_path = False

    while True:
        print("\n=== A-Maze-ing ===")
        render(maze, show_path)

        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice = input("Choice (1-4): ").strip()

        if choice == "1":
            maze.generate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            current_theme_index = (
                current_theme_index + 1
            ) % len(COLOR_THEMES)
        elif choice == "4":
            break
        else:
            print("Invalid choice.")