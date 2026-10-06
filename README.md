# Patches — UAV Search-Area Puzzle

A Python + Matplotlib version of LinkedIn's *Patches* puzzle, reframed for UAVs:
each seed cell is a drone, and the rectangle you draw around it is that drone's
search area. Cover the whole grid so that every cell is searched exactly once.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Matplotlib needs a GUI toolkit to open a window. On Ubuntu/WSL, if
`python -m patches` exits without showing anything, install Tk:
`sudo apt install python3-tk`.

## Play

```bash
python -m patches                       # loads puzzles/sample.json
python -m patches puzzles/other.json    # any puzzle file
```

| Action      | Effect                                          |
|-------------|-------------------------------------------------|
| left-drag   | draw a region from one corner cell to the other |
| right-click | remove the region under the cursor              |
| `r`         | reset the board                                 |

Seed labels show the required size (`?` = any size) and shape:
`□` square, `↕` vertical rectangle (taller than wide),
`↔` horizontal rectangle (wider than tall), no symbol = any rectangle.
A region that breaks its drone's shape or size rule is drawn hatched.

## Rules

A puzzle is solved when every drone has one rectangular region that

1. contains its own seed and no other seed,
2. matches its shape and size requirements,
3. doesn't overlap any other region,

and together the regions cover every cell.

## Puzzle file format

```json
{
  "grid_size": 7,
  "drones": [
    {"id": "drone_1", "x": 0, "y": 2, "shape": "vertical-rectangle", "size": 8, "color": "teal"}
  ]
}
```

- `x` is the column, `y` is the row, and `(0, 0)` is the top-left cell.
- `shape` is one of `vertical-rectangle`, `horizontal-rectangle`, `square`, or `any`.
- `size` is a cell count, or `"any"`.
- `color` is any Matplotlib color name.

Included puzzles:
- `puzzles/sample.json` is a 7x7 puzzle with a unique solution.
- `puzzles/problem1.json` is a 6x6 class puzzle with a unique solution.

## Code layout

| File                  | Responsibility                                   |
|-----------------------|--------------------------------------------------|
| `patches/puzzle.py`   | load and validate puzzle files                   |
| `patches/rules.py`    | `Rect`, shape/size checks, `is_solved`           |
| `patches/board.py`    | game state: place/remove regions (no drawing)    |
| `patches/ui.py`       | Matplotlib window and mouse/keyboard handling    |
| `patches/__main__.py` | command-line entry point                         |

## Tests

```bash
pytest
```
