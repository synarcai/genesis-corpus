#!/usr/bin/env python3
"""[UNREAD-NUMBER COURT] — the number reads back from where it hid, or the page lies; CLOSED WORLD.

A show of the unread-number world (tools/readnum.py) puts a number in one of the four places
the atlas of silence names as unread — a list without commas, after a copula, first in the
sentence, under a currency sign — or lets a pro-form («5 new ones») count the goods.

The court reads each line back through the house's frames. A page is true when each count
form is the form of ITS number (so the list cannot be segmented wrong and still pass), when
the total of a list is the sum of its three numbers, when the answer about one goods is that
goods' own number, when the price under the sign is that number and the count times the price
is the ledger's product, and when the pro-form's sum is the sum of its two numbers with the
colour and pro-form words in the count forms their language bends them into. A line of a frame
that breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import readnum as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"readnum"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): в списке без запятых взято число соседа (сам замеренный
    # дефект: 179 немых строк рощи); итог списка не сходится; счётная форма чужого числа;
    # число после связки прочитано иначе; ведущее число прочитано иначе; цена под знаком не
    # та; леджер цены не сходится; про-форма сложена неверно.
    подсадки = (
        "i have 3 apples 4 books 5 pencils. how many apples do i have? 4.",
        "у меня 3 яблока 4 книги 5 карандашей. сколько у меня яблок? 4.",
        "i have 3 apples 4 books 5 pencils. how many things do i have? 13: 3 + 4 + 5 = 13.",
        "ich habe 3 Äpfel 1 Bücher 5 Bleistifte. wie viele Äpfel habe ich? 3.",
        "i have apples. there are 7. how many apples do i have? 9.",
        "9 books are on the table. how many books are on the table? 8.",
        "one apple costs $5. how much do 3 apples cost? $16: 3 × 5 = 16.",
        "i have 3 red apples and 5 new ones. how many apples do i have? 9: 3 + 5 = 9.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:160]}")
        print(f"ЧИСЛО FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_readnum.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_readnum.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_readnum.txt по имени")
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
    print(f"ЧИСЛО {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
