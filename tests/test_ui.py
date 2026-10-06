import matplotlib

matplotlib.use("Agg")  # headless: no window needed

from matplotlib.patches import Circle  # noqa: E402

from patches.puzzle import load_puzzle  # noqa: E402
from patches.ui import PatchesApp  # noqa: E402

from test_rules import PROBLEM1_SOLUTION  # noqa: E402


def make_app():
    return PatchesApp(load_puzzle("puzzles/problem1.json"))


def test_clues_shown_while_unsolved():
    app = make_app()
    assert len(app.ax.texts) == len(app.puzzle.drones)


def test_clues_become_drones_when_solved():
    app = make_app()
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    app.redraw()
    assert len(app.ax.texts) == 0
    circles = [p for p in app.ax.patches if isinstance(p, Circle)]
    assert len(circles) == 5 * len(app.puzzle.drones)


def test_clues_return_after_unsolving():
    app = make_app()
    for rect in PROBLEM1_SOLUTION.values():
        app.board.place(rect)
    app.board.remove_at(0, 0)
    app.redraw()
    assert len(app.ax.texts) == len(app.puzzle.drones)
