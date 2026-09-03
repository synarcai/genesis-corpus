#!/usr/bin/env python3
"""[MEASURED STORIES COURT] — the line is the table, or it is a lie.

A show of the measured-story world names two measured acts and their
difference, or a pair priced one by the other and its division. The court
reads it back through the same house (tools/measurestory.py): the actor, the
verb with its declared past tense and preposition, the measure with the count
form its number asks for, the multiplier word, and the ledger of primitive
steps. A line of these shapes the table does not hold is a lie — a wrong
difference, a verb that does not agree with its actor, a measure form that
does not answer its count, a division that does not divide.

The world is CLOSED: every honest line of it is a line of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import measurestory as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"measure_story"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_measure_story.txt":
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
    print(f"ИСТОРИИ С МЕРОЙ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
