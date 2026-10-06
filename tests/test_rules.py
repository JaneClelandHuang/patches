import pytest

from patches.puzzle import load_puzzle, parse_puzzle
from patches.rules import Rect, is_solved, region_errors, shape_ok, size_ok

# Known solution to puzzles/sample.json, as (top, left, height, width).
SAMPLE_SOLUTION = {
    "drone_1": Rect(0, 0, 4, 2),
    "drone_2": Rect(0, 2, 4, 3),
    "drone_3": Rect(0, 5, 4, 2),
    "drone_4": Rect(4, 0, 2, 2),
    "drone_5": Rect(4, 2, 3, 3),
    "drone_6": Rect(4, 5, 1, 2),
    "drone_7": Rect(5, 5, 2, 1),
    "drone_8": Rect(5, 6, 2, 1),
    "drone_9": Rect(6, 0, 1, 2),
}


@pytest.fixture
def sample():
    return load_puzzle("puzzles/sample.json")


def test_rect_from_corners_any_order():
    assert Rect.from_corners(3, 4, 1, 2) == Rect(1, 2, 3, 3)


@pytest.mark.parametrize("shape,rect,ok", [
    ("square", Rect(0, 0, 2, 2), True),
    ("square", Rect(0, 0, 1, 2), False),
    ("vertical-rectangle", Rect(0, 0, 3, 1), True),
    ("vertical-rectangle", Rect(0, 0, 1, 3), False),
    ("horizontal-rectangle", Rect(0, 0, 1, 3), True),
    ("horizontal-rectangle", Rect(0, 0, 2, 2), False),
    ("any", Rect(0, 0, 2, 5), True),
])
def test_shape_ok(shape, rect, ok):
    assert shape_ok(shape, rect) is ok


def test_size_ok():
    assert size_ok(None, Rect(0, 0, 3, 3))
    assert size_ok(6, Rect(0, 0, 2, 3))
    assert not size_ok(5, Rect(0, 0, 2, 3))


def test_region_must_contain_only_its_own_seed(sample):
    drone_1 = sample.drones[0]
    assert region_errors(sample, drone_1, SAMPLE_SOLUTION["drone_1"]) == []
    errors = region_errors(sample, drone_1, Rect(0, 0, 4, 4))
    assert any("other drones" in e for e in errors)


def test_sample_solution_is_solved(sample):
    assert is_solved(sample, SAMPLE_SOLUTION)


def test_missing_region_is_not_solved(sample):
    partial = dict(SAMPLE_SOLUTION)
    del partial["drone_9"]
    assert not is_solved(sample, partial)


# Known solution to puzzles/problem1.json.
PROBLEM1_SOLUTION = {
    "drone_1": Rect(0, 0, 2, 3),
    "drone_2": Rect(0, 3, 1, 3),
    "drone_3": Rect(2, 1, 2, 2),
    "drone_4": Rect(1, 3, 3, 3),
    "drone_5": Rect(2, 0, 3, 1),
    "drone_6": Rect(4, 1, 1, 5),
    "drone_7": Rect(5, 0, 1, 3),
    "drone_8": Rect(5, 3, 1, 3),
}


def test_class_puzzle_solution_is_solved():
    puzzle = load_puzzle("puzzles/problem1.json")
    assert puzzle.grid_size == 6
    assert is_solved(puzzle, PROBLEM1_SOLUTION)


def test_parse_rejects_bad_shape():
    with pytest.raises(ValueError):
        parse_puzzle({"grid_size": 3, "drones": [
            {"id": "a", "x": 0, "y": 0, "shape": "circle", "size": 1, "color": "red"}]})


def test_parse_rejects_off_grid_seed():
    with pytest.raises(ValueError):
        parse_puzzle({"grid_size": 3, "drones": [
            {"id": "a", "x": 3, "y": 0, "shape": "any", "size": 1, "color": "red"}]})
