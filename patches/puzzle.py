"""Loading a puzzle definition from JSON.

File coordinates use x = column, y = row, with (0, 0) the top-left cell.
"""

import json
from dataclasses import dataclass

SHAPES = ("vertical-rectangle", "horizontal-rectangle", "square", "any")


@dataclass(frozen=True)
class Drone:
    id: str
    row: int
    col: int
    shape: str          # one of SHAPES
    size: int | None    # required cell count, or None for "any"
    color: str


@dataclass(frozen=True)
class Puzzle:
    grid_size: int
    drones: tuple[Drone, ...]

    def drone_at(self, row, col):
        """Return the drone whose seed is at (row, col), or None."""
        for drone in self.drones:
            if (drone.row, drone.col) == (row, col):
                return drone
        return None


def parse_puzzle(data):
    """Build a Puzzle from an already-decoded JSON dict, validating it."""
    n = data["grid_size"]
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"grid_size must be a positive integer, got {n!r}")

    drones = []
    seen_ids, seen_seeds = set(), set()
    for d in data["drones"]:
        drone_id = d["id"]
        col, row = d["x"], d["y"]
        if not (0 <= row < n and 0 <= col < n):
            raise ValueError(f"{drone_id}: seed ({col}, {row}) is off the {n}x{n} grid")
        if drone_id in seen_ids:
            raise ValueError(f"duplicate drone id {drone_id!r}")
        if (row, col) in seen_seeds:
            raise ValueError(f"{drone_id}: another drone already starts at ({col}, {row})")
        if d["shape"] not in SHAPES:
            raise ValueError(f"{drone_id}: unknown shape {d['shape']!r}")
        size = None if d["size"] == "any" else d["size"]
        if size is not None and (not isinstance(size, int) or size < 1):
            raise ValueError(f"{drone_id}: size must be a positive integer or \"any\"")

        seen_ids.add(drone_id)
        seen_seeds.add((row, col))
        drones.append(Drone(drone_id, row, col, d["shape"], size, d["color"]))

    return Puzzle(n, tuple(drones))


def load_puzzle(path):
    """Read and validate a puzzle file."""
    with open(path) as f:
        return parse_puzzle(json.load(f))
