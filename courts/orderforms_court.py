#!/usr/bin/env python3
"""[ORDER COURT] — the answer is a SEQUENCE, and it recomputes; CLOSED WORLD.

A show of the order world (tools/orderforms.py) puts a set of three or four numbers in order,
up and down, and asks two questions that no maximum can answer: which is the SECOND largest,
and which stands BETWEEN the other two. The census found zero lines of ordering in the свод:
the corpus compared pairs and named extremes, but never ordered a set.

The court reads each line back through the house's frames. A page is true when the sequence it
writes is the sorted set (in that direction), when the second largest is the second of the
descending order — not the maximum and not the minimum — and when the number called «between»
is the middle one and the chain of signs names its two edges. Sets with equal members are not
written by the house and are false in it: an equal pair has no second place. A line of no frame
is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import orderforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"orderforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): порядок не тот; убывание записано возрастанием; второе по
    # величине названо наибольшим; «между» названо крайним; четвёрка упорядочена неверно.
    подсадки = (
        "the numbers: 7, 3, 9. how do they go in ascending order? 3, 9, 7.",
        "the numbers: 7, 3, 9. how do they go in descending order? 3, 7, 9.",
        "the numbers: 7, 3, 9. which number is the second largest? 9.",
        "the numbers: 7, 3, 9. which number is between the other two? 9: 3 < 9 < 9.",
        "the numbers: 7, 3, 9, 5. how do they go in ascending order? 3, 5, 9, 7.",
        "числа: 7, 3, 9. как они идут по возрастанию? 3, 9, 7.",
        "числа: 7, 3, 9. какое число второе по величине? 9.",
        "liczby: 7, 3, 9. jak idą malejąco? 3, 7, 9.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ПОРЯДОК FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_orderforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_orderforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_orderforms.txt по имени")
    for путь in пути:
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = _судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:150]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ПОРЯДОК {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
