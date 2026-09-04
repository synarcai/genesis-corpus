#!/usr/bin/env python3
"""[EVERYDAY SPEECH COURT] — the everyday is declared, or the line is a lie.

A show of the dialogue world is a pair of the everyday, a definition of the
everyday, the name, the answer to «who are you?» or a polite ignorance. The
court reads it back through the same house (tools/dialogueforms.py): the set
of shows is FINITE and declared, so a line of the world is true when it is
one of them. A line that sits in a declared FRAME but carries a foreign word
(«что такое привет? привет — это прощание.», «что такое привет? я не знаю,
что такое привет.») is a LIE, not silence: the frame is the house's, and the
house knows what stands in it.

The world is CLOSED: every honest line of it is a line of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import dialogueforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"dialogue"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_dialogue.txt":
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
    print(f"РЕЧЕВОЙ ОБИХОД {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
