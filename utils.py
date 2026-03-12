"""
Utility constants and helpers.
"""

from typing import Tuple

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


def inside_bounds(x: int, y: int, width: int, height: int) -> bool:
    return 0 <= x < width and 0 <= y < height