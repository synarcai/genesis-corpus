#!/usr/bin/env python3
"""[PRICE COURT] — the total is the product, and every count form is the pack's, RECHECKED.

A show of the price world (tools/priceforms.py) is «one apple costs 2 dollars.
how much do 3 apples cost? 6 dollars: 3 × 2 = 6.» in nine languages. The court
reads each page through the same house: the thing must be a declared one, the
total must be the product, and the count forms of the thing and the currency
must be those the pack's agreement rule selects for the number («3 яблок»,
«6 рубля» are lies before the product is checked). The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import priceforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"price"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): итог не произведение; счётная форма вещи не по числу;
    # счётная форма валюты не по числу; польские формы
    подсадки = (
        "one apple costs 2 dollars. how much do 3 apples cost? 7 dollars: 3 × 2 = 7.",
        "одно яблоко стоит 2 рубля. сколько стоят 3 яблок? 6 рублей: 3 × 2 = 6.",
        "одно яблоко стоит 2 рубля. сколько стоят 3 яблока? 6 рубля: 3 × 2 = 6.",
        "jedno jabłko kosztuje 2 złote. ile kosztują 3 jabłka? 6 złote: 3 × 2 = 6.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ЦЕНА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_price.txt":
            continue
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ЦЕНА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
