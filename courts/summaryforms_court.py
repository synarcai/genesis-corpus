#!/usr/bin/env python3
"""[SUMMARY COURT] — the note checks out against its episode, or the page lies; CLOSED WORLD.

A show of the summary world (tools/summaryforms.py) is one page of a COMPACTED record: an
episode of states (or a tape of acts), a note that keeps some of it, and a question about
THE NOTE — what it says of a place it keeps, what it says of a place it dropped, how many
places it names, which one it left out, and whether it is right.

The court reads each line back through the house's frames. A page is true when every hole
repeated in the frame carries one value (so a truthful note cannot drift from its episode),
when each count form is the form of ITS number and all forms of the page are forms of ONE
thing, when the copula of a place bends with the number it stands at, when the place named
by an answer is the place the question asked, when a claim of silence is made about the
dropped place and only it, when an answer from the note is given about a kept place and
only it, when the counting word is the word of the number of kept places and the list is
their names in order, when the distortion the «no» names DIFFERS from the truth (a «no»
over a faithful note is a lie), and when the tape's ledger recomputes and the note's number
agrees with it (for «yes») or differs from it (for «no»). A line of a frame that breaks any
of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import summaryforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"summaryforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): ответ о хранимом месте с чужим числом; молчание о месте,
    # которое сводка держит; число вместо молчания о выкинутом месте; счёт мест не по
    # заметкам; ушедшим названо хранимое место; «да» над искажённой заметкой; «нет» над
    # верной; леджер ленты не сходится.
    подсадки = (
        "в папке 3 файла. в ящике 6 файлов. в списке 9 файлов. сводка: 3 файла в папке, 6 файлов в ящике. что сводка говорит о папке? в папке 6 файлов.",
        "в папке 3 файла. в ящике 6 файлов. в списке 9 файлов. сводка: 3 файла в папке, 6 файлов в ящике. что сводка говорит о папке? ничего: сводка молчит о папке.",
        "в папке 3 файла. в ящике 6 файлов. в списке 9 файлов. сводка: 3 файла в папке, 6 файлов в ящике. что сводка говорит о списке? в списке 9 файлов.",
        "there are 3 files in the folder. there are 6 files in the box. there are 9 files in the list. the summary: 3 files in the folder, 6 files in the box. how many places does the summary name? three places: the folder and the box.",
        "there are 3 files in the folder. there are 6 files in the box. there are 9 files in the list. the summary: 3 files in the folder, 6 files in the box. about which place is the summary silent? about the folder.",
        "there are 3 files in the folder. there are 6 files in the box. there are 9 files in the list. the summary: 3 files in the folder, 8 files in the box. is the summary right? yes: there are 3 files in the folder, and the summary says 3.",
        "there are 3 files in the folder. there are 6 files in the box. there are 9 files in the list. the summary: 3 files in the folder, 6 files in the box. is the summary right? no: there are 6 files in the box, but the summary says 6.",
        "в папке 10 файлов. первый акт создаёт 2 файла. второй акт удаляет 1 файл. третий акт создаёт 3 файла. сводка: 14 файлов в папке. верна ли сводка? да: 10 + 2 − 1 + 3 = 15, и сводка говорит 14.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:160]}")
        print(f"СВОДКА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_summaryforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_summaryforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_summaryforms.txt по имени")
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
    print(f"СВОДКА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
