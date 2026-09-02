"""LINE → WORLD: the index of the full corpus by its worlds.

The full corpus is the worlds of the manifest welded by seams in manifest
order (`gen_genesis_full.собрать`); the worlds are not marked inside the
text, so an instrument reading the full file cannot say which world a line
came from (holon 03.09: the «world» column of UNOWNED-REASON stayed empty).
This prints one row per world — name, first line, last line (1-based, in
the assembled file) — derived from the same assembly, never from a second
list; the last row is checked against the file's length.

    python3 tools/line_world.py [full|school] > LINE-WORLD.tsv
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen_genesis_full  # noqa: E402


def диапазоны(сборка="full"):
    """[(мир, первая, последняя)] — строки мира в собранном своде."""
    пары = gen_genesis_full.куски_сборки(сборка)
    тело, _ = gen_genesis_full.собрать(сборка)
    # LINES ARE CUT BY «\n» ONLY: str.splitlines() would also cut at the
    # form feed of a seam and count every seam twice.
    всего = тело.count("\n")
    вон, поз = [], 0
    for имя, кусок in пары:
        n = кусок.count("\n") + 1
        вон.append((имя, поз + 1, поз + n))
        поз += n + 1                     # one seam line between worlds
    assert поз - 1 == всего, f"index {поз - 1} ≠ file {всего} lines"
    return вон


def main():
    сборка = sys.argv[1] if len(sys.argv) > 1 else "full"
    print("мир\tпервая\tпоследняя")
    for имя, a, b in диапазоны(сборка):
        print(f"{имя}\t{a}\t{b}")


if __name__ == "__main__":
    main()
