#!/usr/bin/env python3
"""[SUFFICIENCY COURT] — the yes-or-no bought by a subtraction; CLOSED WORLD.

A show of the purse world (tools/enoughforms.py) is a price, a purse and a decision. The court
recomputes the whole page: the cost is the count times the price, the verdict is the DIRECTION of
the subtraction (purse minus cost when the answer is yes, cost minus purse when it is no), the
remainder and the shortfall are that difference, and the boundary case — the purse exactly equal
to the cost — is true only where the equality is exact and the zero is named by the word its
language uses. A page that says yes with the numbers of a no, or names a shortfall it did not
subtract, is a lie however right its arithmetic looks.

The census found zero lines carrying «хватит ли» or «is that enough» in the whole свод before
this house: the corpus computed and never decided.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import enoughforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"enough"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): произведение неверно; ДА при вычитании наоборот;
    # нехватка не равна разности; граница объявлена без равенства; родительный после
    # «brakuje» подменён именительным; счётная форма товара от чужого числа; ответ о
    # нехватке разошёлся с леджером; остаток назван, но не посчитан.
    подсадки = (
        "одно яблоко стоит 2 рубля. у меня 10 рублей. хватит ли на 4 яблока? да: 4 × 2 = 6, 10 − 6 = 4, останется 4 рубля.",
        "one apple costs 2 dollars. i have 10 dollars. is that enough for 6 apples? yes: 6 × 2 = 12, 10 − 12 = 2, 2 dollars will be left.",
        "ein Apfel kostet 2 Euro. ich habe 10 Euro. ist das genug für 6 Äpfel? nein: 6 × 2 = 12, 12 − 10 = 3, 3 Euro fehlen.",
        "одна книга стоит 3 рубля. у меня 12 рублей. хватит ли на 5 книг? да: 5 × 3 = 15, 12 − 15 = 0, ничего не останется.",
        "jedno jabłko kosztuje 2 złote. mam 10 złotych. czy wystarczy na 6 jabłek? nie: 6 × 2 = 12, 12 − 10 = 2, trzeba jeszcze 2 złotych.",
        "jedno jabłko kosztuje 2 złote. mam 10 złotych. czy wystarczy na 6 jabłka? nie: 6 × 2 = 12, 12 − 10 = 2, trzeba jeszcze 2 złote.",
        "ein Bleistift kostet 5 Euro. ich habe 20 Euro. wie viel fehlt noch für 5 Bleistifte? 4 Euro: 5 × 5 = 25, 25 − 20 = 5.",
        "одно яблоко стоит 2 рубля. у меня 10 рублей. хватит ли на 4 яблока? да: 4 × 2 = 8, 10 − 8 = 2, останется 3 рубля.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ХВАТИТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_enough.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_enough.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_enough.txt по имени")
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
    print(f"ХВАТИТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
