#!/usr/bin/env python3
"""[DATE COURT] — the month is asked how long it is, or the page lies; CLOSED WORLD.

A show of the date world (tools/dateforms.py) crosses from one month into the next, and that
crossing is the only carry in the corpus WHOSE BASE CHANGES: thirty-one days in March, thirty
in April, twenty-eight in February. A carry with a fixed base can be learnt as a habit; this
one can only be learnt as a law that asks the month.

The court reads each line back through the house's frames. A page is true when the length it
names is the length THAT month has (a page calling March thirty days is a lie however well its
arithmetic then follows), when the step actually carries past the end of the month, when the
day of the new month is the remainder, when the numbers of the dates and of the step are the
same numbers as the ledger's, and when the count form of the day is the form its number takes.
A line of a frame that breaks any of these is a lie; a line of no frame is a lie of the closed
world. German is a DECLARED GAP of the house: it writes the day with a full stop («5. März»),
and a full stop followed by a space ends a sentence for every court of this corpus.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import dateforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"dateforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): длина месяца взята чужая; число нового месяца не сходится;
    # февраль сочтён тридцатиоднодневным; промежуток не сходится; обратный ход не сходится.
    подсадки = (
        "28 March. 6 days later. what date will it be? 3 April: March has 30 days, 28 + 6 = 34, 34 − 30 = 3.",
        "28 March. 6 days later. what date will it be? 4 April: March has 31 days, 28 + 6 = 34, 34 − 31 = 4.",
        "26 February. 5 days later. what date will it be? 3 March: February has 31 days, 26 + 5 = 31, 31 − 31 = 3.",
        "from 27 April to 5 May. how many days passed? 9 days: April has 30 days, 30 − 27 = 3, 3 + 5 = 9.",
        "28 марта. через 6 дней. какое будет число? 3 апреля: в марте 30 дней, 28 + 6 = 34, 34 − 30 = 3.",
        "28 марта. через 6 дней. какое будет число? 4 апреля: в марте 31 день, 28 + 6 = 34, 34 − 31 = 4.",
        "28 marca. 6 dni później. jaka będzie data? 4 kwietnia: marzec ma 31 dni, 28 + 6 = 34, 34 − 31 = 4.",
        "3 aprile. 6 giorni prima. che data era? 27 marzo: marzo ha 31 giorni, 31 − 3 = 28, 6 − 3 = 3.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ДАТА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_dateforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_dateforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_dateforms.txt по имени")
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
    print(f"ДАТА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
