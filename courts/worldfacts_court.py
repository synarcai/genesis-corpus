#!/usr/bin/env python3
"""[ФАКТЫ МИРА COURT] — the line is a show of the house, or it is a lie.

The set of shows is FINITE and declared (tools/worldfacts.py): a fact of the
world, its GROUND, its CONSEQUENCE, a class membership, and the two agreement
frames. A line of this world is true when the house names it; the world is
CLOSED, so a ground moved onto another fact («ice floats in water. why?
because a stone is heavier than water.») is caught as a lie, not as silence.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import worldfacts as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"worldfacts"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ЧУЖОЙ ПОКАЗ НЕ ПОВТОРЯЕТСЯ (М-172, вторая грань): строка, уже стоящая
    # в другом мире свода, есть не знание, а вес. Первая волна дома написала
    # «iron is a metal.» и «the sun is a star.» вслед за genesis_l4.
    чужие = set()
    for путь in worlds(kind="shows"):
        if путь.name == "genesis_worldfacts.txt":
            continue
        for с in путь.read_text(encoding="utf-8", errors="replace").splitlines():
            с = с.strip()
            if с and not с.startswith("\x0c"):
                чужие.add(с)
    двойники = sorted(с for с in F.ПОКАЗЫ if с in чужие)
    for с in двойники[:5]:
        print(f"  ДВОЙНИК ЧУЖОГО МИРА: {с[:110]}")
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_worldfacts.txt":
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
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 and not двойники else "FAIL"
    print(f"ФАКТЫ МИРА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}, двойников чужих миров {len(двойники)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
