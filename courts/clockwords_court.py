#!/usr/bin/env python3
"""[SPOKEN-CLOCK COURT] — the words name that very minute, or the page lies; CLOSED WORLD.

A show of the spoken-clock world (tools/clockwords.py) names one quarter-hour twice: in figures
and in the words of its language — and the languages disagree about which hour to count from.
English, French, Spanish, Italian and Portuguese count from the hour that has passed; Russian,
German, Dutch and Polish count toward the hour that is coming, and German does one for the
quarter and the other for the half.

The court reads each line back through the house's frames, both of which hold the figures AND
the words as holes. A page is true when the phrase is a phrase of THAT language and names
exactly the minute the figures show — so a page reading «half past two» over 3:30 (the very
mistake of a reader that learnt one of the two halves of the world) is a lie, and so is
«a quarter past two» over 2:30. A line of a frame that breaks this is a lie; a line of no
frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import clockwords as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"clockwords"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): час сдвинут (та половина мира, что считает иначе);
    # четверть названа половиной; обратный ход с чужими цифрами; чужой час в словах.
    подсадки = (
        "the clock shows 3:30. how do you say it in words? half past two.",
        "the clock shows 2:30. how do you say it in words? a quarter past two.",
        "часы показывают 3:30. как сказать это словами? половина третьего.",
        "часы показывают 2:30. как сказать это словами? четверть третьего.",
        "die Uhr zeigt 3:30. wie sagt man das in Worten? halb drei.",
        "die Uhr zeigt 2:30. wie sagt man das in Worten? Viertel nach zwei.",
        "zegar wskazuje 3:30. jak to powiedzieć słowami? wpół do trzeciej.",
        "zegar wskazuje 2:30. jak to powiedzieć słowami? kwadrans po drugiej.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ЧАСЫ СЛОВОМ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_clockwords.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_clockwords.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_clockwords.txt по имени")
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
    print(f"ЧАСЫ СЛОВОМ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
