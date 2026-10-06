"""The rules of Patches: what makes a region valid and when the puzzle is solved.

A solution assigns each drone one rectangular search region such that:
  * the region contains that drone's seed cell and no other seed,
  * the region matches the drone's shape and size requirements,
  * no two regions overlap, and
  * together the regions cover every cell of the grid.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rect:
    top: int
    left: int
    height: int
    width: int

    @classmethod
    def from_corners(cls, r1, c1, r2, c2):
        """Rectangle spanning two opposite corner cells (inclusive)."""
        top, left = min(r1, r2), min(c1, c2)
        return cls(top, left, abs(r1 - r2) + 1, abs(c1 - c2) + 1)

    @property
    def area(self):
        return self.height * self.width

    def contains(self, row, col):
        return (self.top <= row < self.top + self.height
                and self.left <= col < self.left + self.width)

    def cells(self):
        return {(r, c)
                for r in range(self.top, self.top + self.height)
                for c in range(self.left, self.left + self.width)}

    def overlaps(self, other):
        return bool(self.cells() & other.cells())


def shape_ok(shape, rect):
    if shape == "square":
        return rect.height == rect.width
    if shape == "vertical-rectangle":
        return rect.height > rect.width
    if shape == "horizontal-rectangle":
        return rect.width > rect.height
    return True  # "any"


def size_ok(size, rect):
    return size is None or rect.area == size


def region_errors(puzzle, drone, rect):
    """List the reasons `rect` is not a valid region for `drone` (empty if valid)."""
    errors = []
    n = puzzle.grid_size
    if rect.top < 0 or rect.left < 0 or rect.top + rect.height > n or rect.left + rect.width > n:
        errors.append("region extends off the grid")
    if not rect.contains(drone.row, drone.col):
        errors.append("region does not contain the drone's seed")
    others = [d.id for d in puzzle.drones if d is not drone and rect.contains(d.row, d.col)]
    if others:
        errors.append(f"region contains other drones: {', '.join(others)}")
    if not shape_ok(drone.shape, rect):
        errors.append(f"region is not a {drone.shape}")
    if not size_ok(drone.size, rect):
        errors.append(f"region covers {rect.area} cells, needs {drone.size}")
    return errors


def is_solved(puzzle, regions):
    """True if `regions` (drone id -> Rect) is a complete, valid solution."""
    covered = set()
    for drone in puzzle.drones:
        rect = regions.get(drone.id)
        if rect is None or region_errors(puzzle, drone, rect):
            return False
        cells = rect.cells()
        if cells & covered:
            return False
        covered |= cells
    return len(covered) == puzzle.grid_size ** 2
