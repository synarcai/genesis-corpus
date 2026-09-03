#!/usr/bin/env python3
"""[ACTION PAGES COURT] — the page is regenerated and compared.

A line of the action pages world is a page of the house of action pages
(tools/actionpages.py): a fact, an act, a question and a chain of
primitives. The court reads the holes back (the bearer and its Russian
genitive, the thing in its count form, the numbers, the word of the share,
the word of multiplicity), writes the page again as the house writes it and
compares letter by letter: a step that miscounts, a share taken from the
wrong denominator, a Russian verb whose gender does not follow the name — a
page the house would not write."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import actionpages as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name
# THE WORLD IS CLOSED: every honest line of «action_pages» is a page of this
# court (built so, 03.09), so a line of it this court does not recognise is a lie.
ЗАМКНУТЫЕ_МИРЫ = frozenset({"action_pages"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_action_pages.txt":
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
    print(f"СТРАНИЦЫ ДЕЙСТВИЯ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
