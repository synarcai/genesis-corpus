#!/usr/bin/env python3
"""[DISCOUNT-ROAD COURT] — the money recomputes on the road it names; CLOSED WORLD.

A show of the discount road (tools/discountroad.py) is a price, a discount ON EACH item, and
one of four questions over that same pair: the price after the discount, the bill for several,
how many items fit into a sum at the FULL price, and how many at the DISCOUNTED price. This is
the second gate of the silence atlas by measure — 72–76 turns of the grove stop here.

The court reads each line back through the house's frames. A page is true when the discount is
actually subtracted, when a bill for several multiplies the DISCOUNTED price and not the full
one, when a sum divides by the price the question names (full for one form, discounted for the
other), when the money written with its sign carries the same number as the ledger written
without it, and when the count form of the goods is the form of ITS number. A line of a frame
that breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import discountroad as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"discountroad"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): скидка не вычтена; счёт взят по полной цене; сумма делена
    # не на ту цену; счётная форма чужого числа.
    подсадки = (
        "each pack costs $76. the discount is $25 on each pack. how much is paid for one pack? $76: 76 − 25 = 76.",
        "each pack costs $76. the discount is $25 on each pack. how much is paid for 5 packs? $380: 5 × 76 = 380.",
        "each pack costs $76. the discount is $25 on each pack. how many packs can be bought for $380? 5 packs: 380 ÷ 51 = 5.",
        "each pack costs $76. the discount is $25 on each pack. how many packs can be bought for $255? 5 packs: 255 ÷ 76 = 5.",
        "каждая пачка стоит 76 ₽. скидка 25 ₽ на каждую пачку. сколько платить за одну пачку? 76 ₽: 76 − 25 = 76.",
        "каждая пачка стоит 76 ₽. скидка 25 ₽ на каждую пачку. сколько платить за 5 пачек? 256 ₽: 5 × 51 = 256.",
        "każdy bilet kosztuje 48 zł. rabat wynosi 17 zł na każdy bilet. ile biletów można kupić za 192 zł? 5 biletów: 192 ÷ 48 = 5.",
        "jede Karte kostet 48 €. der Rabatt beträgt 17 € auf jede Karte. wie viele Karten kann man für 124 € kaufen? 4 Karten: 124 ÷ 48 = 4.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"СКИДКА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_discountroad.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_discountroad.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_discountroad.txt по имени")
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
    print(f"СКИДКА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
