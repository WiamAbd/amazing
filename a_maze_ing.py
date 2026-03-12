#!/usr/bin/env python3

import sys
from config_parser import parse_config
from maze import MazeGenerator
from renderer import run_menu


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        config = parse_config(sys.argv[1])

        maze = MazeGenerator(
            width=config["WIDTH"],
            height=config["HEIGHT"],
            entry=config["ENTRY"],
            exit_=config["EXIT"],
            perfect=config["PERFECT"],
            seed=config.get("SEED"),
        )

        maze.generate()
        maze.write_output(config["OUTPUT_FILE"])

        run_menu(maze)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()