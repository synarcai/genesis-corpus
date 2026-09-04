#!/usr/bin/env python3
"""[JOINTS COURT] — the joint stands in a declared place, or the line is a lie.

A show of the joints world names two or three numeric phrases of ONE clause,
the word (or the bare comma) standing between them, and the sum with its
ledger. The court reads the line back through the same house
(tools/jointforms.py): the bearer, each good with the count form its number
asks for, the joint among those the language declares, the sum and the
primitive steps. A joint the language never declared is not judged here at
all — the house speaks only of its own fan — but a declared joint carrying a
wrong sum, a wrong count form or a broken ledger is named a lie.

The world is CLOSED: every honest line of it is a line of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import jointforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"joints"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_joints.txt":
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
    print(f"СОЧЛЕНЕНИЯ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
