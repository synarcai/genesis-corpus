#!/usr/bin/env python3
"""[SPEED COURT] — three questions, one law; CLOSED WORLD.

A show of the speed world (tools/speedforms.py) is one journey and one of three questions over
it: the distance (speed times time), the time (distance over speed) and the speed (distance
over time). The census found ZERO lines in the свод writing a unit that is a RATIO of two units
(«km/h»), and the reader's silence atlas names the money-and-rate road as its second-largest
gate.

The court reads each line back through the house's frames. A page is true when speed times
time is the distance — the same law read three ways, so a page that adds instead of multiplying
or divides by the wrong side is a lie — and when the counted hour is the form its number takes
by the pack's rule while the ledger carries that same number. A line of a frame that breaks
this is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import speedforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"speedforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): путь сложен вместо умножения; время делено неверно;
    # скорость делена неверно; счётное слово часа — форма чужого числа.
    подсадки = (
        "the train goes 60 km/h. how far will it go in 3 hours? 63 km: 60 × 3 = 63.",
        "the train went 160 km at 80 km/h. in how many hours did it go that far? in 4 hours: 160 ÷ 80 = 4.",
        "the train went 180 km in 4 hours. how many kilometres per hour does it go? 90 km/h: 180 ÷ 4 = 90.",
        "поезд идёт 60 км/ч. сколько километров он пройдёт за 3 часа? 63 км: 60 × 3 = 63.",
        "поезд прошёл 160 км со скоростью 80 км/ч. за сколько часов он прошёл этот путь? за 4 часа: 160 ÷ 80 = 4.",
        "поезд идёт 60 км/ч. сколько километров он пройдёт за 3 час? 180 км: 60 × 3 = 180.",
        "pociąg jedzie 60 km/h. ile kilometrów przejedzie w 3 godziny? 63 km: 60 × 3 = 63.",
        "der Zug fährt 60 km/h. wie weit fährt er in 3 Stunden? 63 km: 60 × 3 = 63.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"СКОРОСТЬ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_speedforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_speedforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_speedforms.txt по имени")
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
    print(f"СКОРОСТЬ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
