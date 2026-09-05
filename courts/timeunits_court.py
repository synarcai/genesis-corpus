#!/usr/bin/env python3
"""[TIME UNITS COURT] — the conversion is a declared pair, and the product is RECOMPUTED.

A show of the time-units world (tools/timeunits.py) is «сколько минут в двух
часах? 120: 2 × 60 = 120.» in nine languages — hour → minutes, minute →
seconds, week → days, day → hours, for two to five of the larger unit, the
count in words for two to four. The court reads each page through the same
house: the two units must be a declared pair with its factor, the count in
words must be the digit's, the larger unit's form must be the pack's, and the
product must hold. The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import timeunits as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"timeunits"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): произведение не сходится; множитель чужой пары; слово не по цифре
    подсадки = (
        "сколько минут в двух часах? 130: 2 × 60 = 130.",
        "how many days are there in two weeks? 14: 2 × 60 = 14.",
        "ile minut jest w trzech godzinach? 120: 2 × 60 = 120.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ЕДИНИЦЫ ВРЕМЕНИ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_timeunits.txt":
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
    print(f"ЕДИНИЦЫ ВРЕМЕНИ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
