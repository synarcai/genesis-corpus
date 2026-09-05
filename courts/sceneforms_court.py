#!/usr/bin/env python3
"""[SCENE COURT] — the frame's holes agree, or the page lies; CLOSED WORLD.

A show of the scene world (tools/sceneforms.py) is one of seven frames held by a copula and a
preposition, with no verb of action: a place holding two kinds (the question naming the second),
a class of a thing, two places with the question «where are there more», the colour of the
things, the belonging of things to a place, and «is there» with its negative twin.

The court reads each line through the house's frames: a page whose repeated holes carry one
value (the answer's place is the story's place, the answer's colour is the story's colour, the
answer's polarity is the question's), whose count form is the form of its number, whose copula
agrees with its number, whose «more» names the place of the greater number and whose class is
the class the world-facts house declares — is true; a line of a frame that breaks any of these
is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import sceneforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"sceneforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): вопрос о втором роде, отвеченный числом первого; «где больше»
    # с местом меньшего числа; чужой цвет в ответе; чужое место в ответе; чужой класс; счётная
    # форма не по числу; связка места не по числу
    подсадки = (
        "there are 12 coins and 5 books on the shelf. how many books are on the shelf? there are 12 books on the shelf.",
        "there are 12 coins on the shelf and there are 5 coins on the table. where are there more coins? on the table.",
        "Ann has 2 red coins. what colour are the coins? blue.",
        "12 coins are on the shelf. where are the 12 coins? in the box.",
        "a spider is an animal. what is a spider? a spider is a tree.",
        "there are 12 coins on the shelf. are there any coins on the shelf? yes, there are 12 coin on the shelf.",
        "there is 12 coins on the shelf. are there any coins on the shelf? yes, there is 12 coins on the shelf.",
        "на полке 12 книг, а на столе 5 книг. где книг больше? на столе.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"СЦЕНА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_sceneforms.txt"]
    if not пути:  # the world is not in the manifest yet — the court reads its file by name
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_sceneforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_sceneforms.txt по имени")
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
    print(f"СЦЕНА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
