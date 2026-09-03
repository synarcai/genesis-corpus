#!/usr/bin/env python3
"""[SEARCH IN TEN LANGUAGES COURT] — the walk is walked again.

A line of the search world is a template of the house of search phrases
(tools/searchforms.py) with its holes filled; the court turns the same
template into a pattern, reads the holes back, walks the same walk (to the
next prime, to the smallest multiplier, from the part to the number) and
compares the ledger step by step: a skipped witness, a wrong divisor, a
prime declared one step early — a lie."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import searchforms as F  # noqa: E402

ПРАВИЛА = {язык: F.образцы(язык) for язык in F.ЯЗЫКИ}


import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name
# THE WORLD IS CLOSED: every honest line of «search_langs» is a shape of this
# court (built so, 03.09), so a line of it this court does not recognise is a lie.
ЗАМКНУТЫЕ_МИРЫ = frozenset({"search_langs"})


def _судить(строка):
    с = строка.strip()
    for язык, правила in ПРАВИЛА.items():
        for образец, род, спрошено in правила:
            м = образец.match(с)
            if м:
                return True, F.судить_группы(язык, род, спрошено, м.groups())
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_search_langs.txt":
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
        print(f"  ЛОЖЬ: {п[:110]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ПОИСК НА ЯЗЫКАХ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
