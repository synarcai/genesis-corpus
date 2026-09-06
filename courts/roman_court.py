#!/usr/bin/env python3
"""[ROMAN COURT] — the canonical numeral and the law of the order of two signs; CLOSED WORLD.

A show of the roman world (tools/romanforms.py) is one number in three frames: the numeral asked
for, the numeral read, and the subtractive law itself. The court renders the number greedily by
the table and demands the shown numeral be exactly that — «XIIII» is a lie for 14 though its
letters add up, because the market has one spelling of a number. Then it cuts the numeral into
tokens and demands the ledger be their values in their order, summing to the number; and for the
law it demands the named pair be the numeral's own pair, the smaller sign first, and the
difference their difference.

The census found zero roman numerals in the whole свод before this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import romanforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"roman"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): неканоническая запись, чужая запись, доля леджера,
    # СУММА, КОТОРАЯ СХОДИТСЯ ПО ЧИСЛУ И ЛЖЁТ ПО ЗНАКАМ, разность пары, пара не из этой
    # записи, порядок знаков наоборот, чтение чужого числа — на восьми языках.
    подсадки = (
        "как записать 14 римскими цифрами? XIIII: 10 + 1 + 1 + 1 + 1 = 14.",
        "how is 44 written in roman numerals? XLVI: 40 + 4 = 44.",
        "римская запись XXVII. какое это число? 27: 10 + 10 + 6 + 1 = 27.",
        "jak zapisać 44 cyframi rzymskimi? XLIV: 40 + 4 = 45.",
        "in XC the smaller sign X stands before the larger sign C and is subtracted: 100 − 10 = 80.",
        "w XIV mniejszy znak I stoi przed większym znakiem X i odejmuje się: 10 − 1 = 9.",
        "en XIV el signo menor V está delante del signo mayor I y se resta: 5 − 1 = 4.",
        "het Romeinse getal XIX. welk getal is dit? 21: 10 + 9 = 21.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"РИМСКОЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_roman.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_roman.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_roman.txt по имени")
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
    print(f"РИМСКОЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
