#!/usr/bin/env python3
"""[TOOL COURT] — the ledger of the act recomputes, or the page lies; CLOSED WORLD.

A show of the tool world (tools/toolforms.py) is one page of eight frames: a place holds
n things, an act creates / deletes / appends / moves m of them, and the question asks the
count AFTER the act; two frames show an act that CHANGES NOTHING, once and twice.

The court reads each line back through the house's frames. A page is true when every hole
repeated in the frame carries one value (the answer's thing is the story's thing, the
answer's number is the ledger's), when each count form is the form of ITS number, when the
ledger recomputes (create n + m, delete n − m, append n + m, twice n + 2m, move k + m into
the second place and n − m out of the first), when the copula of the place bends with its
number, and when the reading act keeps the count AND says the declared ground of its
constancy. A line of a frame that breaks any of these is a lie; a line of no frame is a lie
of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import toolforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"toolforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): чтение изменило счёт; леджер не сходится; ответ не равен
    # итогу леджера; «дважды» посчитано как один раз; перенос изменил не ту папку; чтение без
    # объявленного основания; счётная форма не по числу; связка места не по числу.
    подсадки = (
        "в папке 3 файла. акт только читает. сколько файлов в папке после акта? в папке 4 файла: чтение ничего не меняет.",
        "there are 3 files in the folder. the act creates 1 file. how many files are in the folder after the act? there are 5 files in the folder: 3 + 1 = 5.",
        "there are 3 files in the folder. the act creates 1 file. how many files are in the folder after the act? there are 5 files in the folder: 3 + 1 = 4.",
        "there are 3 files in the folder. the act creates 1 file twice. how many files are in the folder after the act? there are 4 files in the folder: 3 + 1 + 1 = 4.",
        "folder A contains 12 files, folder B contains 20 files. the act moves 2 files from folder A to folder B. how many files does folder B contain after the act? folder B contains 10 files: 20 + 2 = 10.",
        "в папке 3 файла. акт только читает. сколько файлов в папке после акта? в папке 3 файла: reading changes nothing.",
        "в папке 3 файла. акт создаёт 1 файл. сколько файлов в папке после акта? в папке 4 файлов: 3 + 1 = 4.",
        "there is 3 files in the folder. the act creates 1 file. how many files are in the folder after the act? there are 4 files in the folder: 3 + 1 = 4.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:120]}")
        print(f"ИНСТРУМЕНТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_toolforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_toolforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_toolforms.txt по имени")
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
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ИНСТРУМЕНТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
