#!/usr/bin/env python3
"""[NO-MENTION COURT] — the refusal names what the story never said, or the page lies; CLOSED WORLD.

A show of the no-mention world (tools/nomention.py) is the fourth gate of the silence atlas by
d5's measure: the question names a place or a kind of thing the story never carried, and the
honest answer is a refusal WITH ITS GROUND — «I do not know: nothing is said about the box».
Beside it stands its positive twin (the question about the place the story DID name, answered
by the count), because a market shown only refusals buys refusal.

The court reads each line back through the house's frames, and every frame says which places
the story named and which place the question asked. A page is true when a refusal stands over
a place the story did NOT name, when an answer stands over a place it DID, when the ground
names the very place (or kind) the question asked, when each count form is the form of ITS
number and all forms are of one thing, and when the copula of a place bends with its number.
A page that refuses about a named place, or answers about an unnamed one, is a lie the court
names. A line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import nomention as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"nomention"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): отказ о месте, которое история назвала; ответ о месте,
    # которого не называла; отказ о названном из двух; ответ о третьем, неназванном; счётная
    # форма чужого числа.
    подсадки = (
        "there are 5 files in the folder. how many files are in the folder? I do not know: nothing is said about the folder.",
        "there are 5 files in the folder. how many files are in the box? there are 5 files in the box.",
        "в папке 5 файлов. сколько файлов в папке? не знаю: о папке не сказано.",
        "в папке 5 файлов. сколько файлов в ящике? в ящике 5 файлов.",
        "im Ordner sind 5 Dateien. in der Kiste sind 7 Dateien. wie viele Dateien sind in der Kiste? ich weiß es nicht: über die Kiste ist nichts gesagt.",
        "w folderze jest 5 plików. w pudełku jest 7 plików. ile plików jest na liście? na liście jest 5 plików.",
        "there are 5 file in the folder. how many files are in the folder? there are 5 file in the folder.",
        "в папке 5 файла. сколько файлов в папке? в папке 5 файла.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"НЕНАЗВАННОЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_nomention.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_nomention.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_nomention.txt по имени")
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
    print(f"НЕНАЗВАННОЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
