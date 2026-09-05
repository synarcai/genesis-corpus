#!/usr/bin/env python3
"""[EPISODE COURT] — the tape recomputes step by step, or the page lies; CLOSED WORLD.

A show of the episode world (tools/episodeforms.py) is one page of a TAPE: a place holds n
things, three acts follow one another, and the question asks the count after all of them,
after the second one, which act moved the count most, how many acts moved it at all, or
what the count was before against what it is now.

The court reads each line back through the house's frames. A page is true when every hole
repeated in the frame carries one value, when each count form is the form of ITS number and
all forms of the page are forms of ONE thing, when the ledger of the whole tape recomputes
and its PREFIX recomputes for the answer about the second step, when no intermediate count
falls below one, when the copula of the place bends with the number it stands at (the final
count, or the prefix count for the answer about a step), when the named winner is the act
whose change is greatest and that greatest is unique, when the named count of changing acts
is the count of acts whose change is not nought (a reading act moves nothing and says so),
and when the named verdict of comparison agrees with the numbers. A line of a frame that
breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import episodeforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"episodeforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): леджер ленты не сходится; итог не равен концу леджера;
    # префикс шага посчитан по всей ленте; назван не тот шаг; чтение сочтено изменяющим;
    # вердикт сравнения против чисел; счётная форма чужого числа; связка не по числу.
    подсадки = (
        "в папке 10 файлов. первый акт создаёт 2 файла. второй акт удаляет 1 файл. третий акт создаёт 3 файла. сколько файлов в папке после всех актов? в папке 15 файлов: 10 + 2 − 1 + 3 = 15.",
        "в папке 10 файлов. первый акт создаёт 2 файла. второй акт удаляет 1 файл. третий акт создаёт 3 файла. сколько файлов в папке после всех актов? в папке 15 файлов: 10 + 2 − 1 + 3 = 14.",
        "в папке 10 файлов. первый акт создаёт 2 файла. второй акт удаляет 1 файл. третий акт создаёт 3 файла. сколько файлов в папке после второго акта? после второго акта в папке 14 файлов: 10 + 2 − 1 = 14.",
        "there are 10 files in the folder. the first act creates 2 files. the second act deletes 1 file. the third act creates 3 files. which act changed the count most? the first act: it added 2 files.",
        "there are 10 files in the folder. the first act creates 2 files. the second act only reads. the third act creates 3 files. how many acts changed the count? three acts: reading changes nothing.",
        "there are 10 files in the folder. the first act creates 2 files. the second act deletes 1 file. the third act deletes 3 files. how many were there before and after? before 10, after 8: more.",
        "в папке 10 файлов. первый акт создаёт 2 файла. второй акт удаляет 1 файл. третий акт создаёт 3 файла. сколько файлов в папке после всех актов? в папке 14 файл: 10 + 2 − 1 + 3 = 14.",
        "there are 10 files in the folder. the first act creates 2 files. the second act deletes 1 file. the third act creates 3 files. how many files are in the folder after all the acts? there is 14 files in the folder: 10 + 2 − 1 + 3 = 14.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:160]}")
        print(f"ЭПИЗОД FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_episodeforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_episodeforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_episodeforms.txt по имени")
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
        print(f"  ЛОЖЬ: {п[:160]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ЭПИЗОД {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
