#!/usr/bin/env python3
"""[ACTION MEASURE COURT] — the number measures the act, or counts the bearers; the line is the table, or it is a lie.

A show of the action-measure world (tools/actionmeasure.py) is one of four pages:
a measured act and its question («the frog jumped 12 inches. how far did the frog
jump? 12 inches.»), two measures summed with their ledger, or bearers counted
before the subject with an arrival or a departure («6 birds were sitting on the
fence. 4 more birds came. how many birds are on the fence now? 10 birds: 6 + 4 = 10.»).

The court reads each page back through the same house: the unit must be of the
kind the verb measures (jump — length, weigh — weight: «jumped 12 pounds» is a lie
by unit, before any number is checked), the count form must answer its number,
the sum and the bearer arithmetic must recompute. The world is CLOSED: every
honest line of it is a line of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import actionmeasure as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"action_measure"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): единица не по глаголу; сумма сложена неверно;
    # носители сложены неверно; счётная форма не по числу (ru).
    подсадки = (
        "the frog jumped 12 pounds. how far did the frog jump? 12 pounds.",
        "the frog jumped 12 inches and then 8 inches. how far did the frog jump in all? 20 inches: 12 + 8 = 21.",
        "6 birds were sitting on the fence. 4 more birds came. how many birds are on the fence now? 10 birds: 6 + 4 = 11.",
        "лягушка прыгнула на 12 сантиметр. на сколько сантиметров прыгнула лягушка? на 12 сантиметр.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"МЕРА ДЕЙСТВИЯ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_action_measure.txt":
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
    print(f"МЕРА ДЕЙСТВИЯ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
