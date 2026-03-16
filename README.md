*This project has been created as part of the 42 curriculum by <kel-hadd> and <wabdella>.*

# A-Maze-ing

## Description

A-Maze-ing is a maze generator written in Python 3.  
The program generates a random maze based on a configuration file, ensures compliance with strict structural rules, integrates a visible “42” pattern inside the maze, and outputs both a hexadecimal representation and an interactive ASCII visualization.

The maze can be either:

- **Perfect** (exactly one path between entry and exit)
- **Imperfect** (contains cycles but remains fully connected)

The project strictly follows the mandatory requirements defined in the subject.

---

# Features

- Random maze generation using DFS (recursive backtracker)
- Reproducibility via seed
- Perfect / Imperfect mode
- Structural “42” pattern integrated in the maze
- No 3x3 open areas
- Wall coherence validation
- Border closure validation
- Hexadecimal file output
- Interactive ASCII visualization
- Color rotation
- Shortest path visualization
- Reusable pip-installable module (`mazegen`)

---

# How to Run

python3 a_maze_ing.py config.txt

## How to intall mazegen package

python -m build
pip install dist/mazegen-1.0.0-py3-none-any.whl
pip show mazegen

## Install dependencies

```bash
make install

export PATH="$HOME/.local/bin:$PATH"
source ~/.zshrc