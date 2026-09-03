#!/usr/bin/env python3
"""[CHAINS IN TWENTY-NINE LANGUAGES COURT] — every step counts, the seam holds.

A line of the chains world is two or three equalities of one pack's own
declared templates. The court reads them back through the same templates
(tools/chainforms.py), reads every numeral to its number by the pack,
recounts each step, and checks the SEAM: the number that leaves a step is
an operand of the next. A chain whose seam is broken, whose step miscounts,
or whose numeral the pack never declared, is a lie."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import chainforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name
# THE WORLD IS CLOSED: every honest line of «chains_langs» is a chain of this
# court (built so, 03.09), so a line of it this court does not recognise is a lie.
ЗАМКНУТЫЕ_МИРЫ = frozenset({"chains_langs"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_chains_langs.txt":
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
    print(f"ЦЕПОЧКИ НА ЯЗЫКАХ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
