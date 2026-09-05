#!/usr/bin/env python3
"""[PROPERTY COMPARISON COURT] — the comparative picks the thing, and the pick is RECHECKED.

A show of the property-comparison world (tools/propcompare.py) is «which is
heavier: a stone or a feather? a stone.» in nine languages — five properties,
each with one declared pair and two comparatives (heavier / lighter), asked
in both orders. The court reads each page through the same house: the
comparative must name a declared property, the two things must be ITS pair,
and the answer must be the thing that comparative picks («a feather is
heavier» is a lie by the table). The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import propcompare as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"propcompare"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): проигравший назван тяжелее; пара чужого свойства;
    # сравнительное «легче» с ответом-победителем
    подсадки = (
        "which is heavier: a stone or a feather? a feather.",
        "что тяжелее: камень или подушка? камень.",
        "was ist leichter: ein Stein oder eine Feder? ein Stein.",
        "co jest szybsze: zając czy żółw? żółw.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"СРАВНЕНИЕ СВОЙСТВ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_propcompare.txt":
            continue
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"СРАВНЕНИЕ СВОЙСТВ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
