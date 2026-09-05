#!/usr/bin/env python3
"""[NUMBER LINE COURT] — the neighbour, the bigger, the row and the parity are RECOMPUTED.

A show of the number-line world (tools/numberline.py) is a question a person
checks a speaker with and its grounded answer: «what number comes after 9?
after 9 comes 10.», «which is bigger: 7 or 9? 9 is bigger: 9 − 7 = 2.», «count
from 1 to 5. 1, 2, 3, 4, 5.», «is 7 an even or an odd number? odd: 7 = 2 × 3 + 1.»
— in nine languages. The court reads each page through the same house and
walks the line itself: the neighbour by one step, the bigger by the
difference, the row by counting, the parity by the halving. The world is
CLOSED: every honest line of it is a page of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import numberline as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"numberline"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): сосед не на шаг; большее названо меньшим;
    # разность сложена неверно; ряд с пропуском; чётность словом не по числу;
    # половина не по числу
    подсадки = (
        "what number comes after 9? after 9 comes 11.",
        "which is bigger: 7 or 9? 7 is bigger: 7 − 9 = 2.",
        "что больше: 7 или 9? 9 больше: 9 − 7 = 3.",
        "count from 1 to 5. 1, 2, 4, 5.",
        "ist 8 eine gerade oder eine ungerade Zahl? ungerade: 8 = 2 × 3 + 1.",
        "7 — чётное или нечётное число? нечётное: 7 = 2 × 2 + 1.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ЧИСЛОВОЙ РЯД FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_numberline.txt":
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
    print(f"ЧИСЛОВОЙ РЯД {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
