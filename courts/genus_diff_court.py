#!/usr/bin/env python3
"""[GENUS AND DIFFERENCE COURT] — the line is the table, or it is a lie.

A show of the genus_diff world is one line: the statement of a definition,
a question about it, and the answer. The court reads it back through the
same table the house writes from (tools/defforms.py): the thing, its genus,
its difference, the relative word that agrees with the genus, and the answer
that must be exactly the part of the fact the question asks for.

A line of this SHAPE that the table does not hold is a lie — a genus
borrowed from another thing, a difference that is not this thing's, a
relative word that does not agree, a choice question answered by the genus
it is not, an inversion answered by another thing. The world is CLOSED:
every honest line of it is a line of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import defforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"genus_diff"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_genus_diff.txt":
            continue
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip() or с.startswith("\x0c"):
                continue
            судимо, истинно = судить(с)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(с)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"РОД И ОТЛИЧИЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
