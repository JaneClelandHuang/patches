"""Run with:  python -m patches [puzzle.json]"""

import sys

from .puzzle import load_puzzle
from .ui import PatchesApp

DEFAULT_PUZZLE = "puzzles/sample.json"


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = argv[0] if argv else DEFAULT_PUZZLE
    PatchesApp(load_puzzle(path)).run()


if __name__ == "__main__":
    main()
