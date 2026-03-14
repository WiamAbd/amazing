"""
Configuration parser for maze project.
"""

from typing import Dict, Tuple, Any


MIN_WIDTH = 9
MIN_HEIGHT = 7


def parse_config(filename: str) -> Dict[str, Any]:
    config: Dict[str, str] = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError("Invalid config line format.")

                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file not found.")

    required = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]

    for key in required:
        if key not in config:
            raise ValueError(f"Missing required key: {key}")

    try:
        width = int(config["WIDTH"])
        height = int(config["HEIGHT"])

        if width < MIN_WIDTH or height < MIN_HEIGHT:
            raise ValueError(
                f"Maze too small for 42 pattern. "
                f"Minimum size is {MIN_WIDTH}x{MIN_HEIGHT}."
            )

        parsed = {
            "WIDTH": width,
            "HEIGHT": height,
            "ENTRY": _parse_coords(config["ENTRY"]),
            "EXIT": _parse_coords(config["EXIT"]),
            "OUTPUT_FILE": config["OUTPUT_FILE"],
            "PERFECT": config["PERFECT"].lower() == "true",
        }

        if "SEED" in config:
            parsed["SEED"] = int(config["SEED"])

    except ValueError as e:
        raise ValueError(f"Invalid configuration values: {e}")

    return parsed


def _parse_coords(value: str) -> Tuple[int, int]:
    parts = value.split(",")

    if len(parts) != 2:
        raise ValueError("Invalid coordinate format.")

    return int(parts[0]), int(parts[1])