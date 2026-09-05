#!/usr/bin/env python3
"""[CLOCK COURT] — the carry is sixty, or the page lies; CLOSED WORLD.

A show of the clock world (tools/clockforms.py) is one journey and one of three questions over
it: the arrival (departure plus duration), the departure (arrival minus duration) and the
duration (the difference of two times). Before this house the свод carried NO time of day at
all: every carry it showed was a carry by ten.

The court reads each line back through the house's frames. A page is true when the hours and
minutes of the ledger are the same time as the clock face, when the sum or difference holds in
MINUTES, when the journey actually crosses the hour (a page whose minutes stay under sixty
teaches nothing the ten-carry did not), when the clock face is a clock — minutes under sixty,
hours under twenty-four, so that «12:75» is a lie and not another spelling of «13:15» — and
when every count form of hour and minute is the form its number takes by the pack's rule. A
line of a frame that breaks any of these is a lie; a line of no frame is a lie of the closed
world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import clockforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"clockforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): перенос по десяти («12:75» вместо «13:15» — на минутах
    # это одно число, и судья, считающий одни минуты, назвал бы ложь истиной); прибытие на
    # час раньше при согласном леджере; леджер, разошедшийся с циферблатом; обратный ход,
    # посчитанный сложением; длительность без переноса.
    подсадки = (
        "the train left at 10:50. the journey takes 2 hours 25 minutes. when will it arrive? at 12:75: 10 hours 50 minutes + 2 hours 25 minutes = 13 hours 15 minutes.",
        "the train left at 10:50. the journey takes 2 hours 25 minutes. when will it arrive? at 12:15: 10 hours 50 minutes + 2 hours 25 minutes = 12 hours 15 minutes.",
        "the train left at 10:50. the journey takes 2 hours 25 minutes. when will it arrive? at 13:15: 10 hours 50 minutes + 2 hours 25 minutes = 12 hours 15 minutes.",
        "the train arrives at 13:15. the journey takes 2 hours 25 minutes. when did it leave? at 15:50: 13 hours 15 minutes − 2 hours 25 minutes = 15 hours 50 minutes.",
        "the train left at 10:50 and arrived at 13:15. how long did it travel? 2 hours 35 minutes: 13 hours 15 minutes − 10 hours 50 minutes = 2 hours 35 minutes.",
        "поезд выехал в 10:50. он идёт 2 часа 25 минут. когда он приедет? в 12:75: 10 часов 50 минут + 2 часа 25 минут = 13 часов 15 минут.",
        "поезд выехал в 10:50. он идёт 2 часа 25 минут. когда он приедет? в 13:15: 10 часов 50 минут + 2 часа 25 минут = 12 часов 15 минут.",
        "pociąg odjechał o 10:50. podróż trwa 2 godziny 25 minut. kiedy przyjedzie? o 13:15: 10 godzin 50 minut + 2 godziny 25 minut = 12 godzin 15 minut.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ЧАСЫ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_clockforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_clockforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_clockforms.txt по имени")
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
    print(f"ЧАСЫ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
