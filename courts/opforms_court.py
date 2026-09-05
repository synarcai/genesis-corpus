#!/usr/bin/env python3
"""[OPERATOR-WORD COURT] — the order recomputes by its preposition, or the page lies; CLOSED WORLD.

A show of the operator-word world (tools/opforms.py) is one page of an ORDER: a verb standing
before both numbers, the operands separated by the preposition its language uses, an echo
question that carries no operation of its own («what do you get?»), and the answer — bare, or
with the ledger of signs.

The court reads each line back through the house's frames. A page is true when the answer is
the result of THAT operation on THAT order of operands (the preposition's order, not the
reading order: «subtract 2 from 9» is 9 − 2), when the ledger, where the page carries one,
holds the same numbers and the same result, and when an order that names one number is
answered by the pair house's own word of not-knowing. The court also carries a frame the
world never writes: the one-number order answered by a NUMBER — a lie by construction, and
the trap for a reader that guesses. A line of a frame that breaks any of these is a lie; a
line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import opforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"opforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): деление, прочитанное умножением (ровно замеренный дефект
    # удержанного ключа: «divide 14 em 2 partes iguais. o que dá?» → 28); вычитание,
    # прочитанное сложением; порядок операндов слева направо; леджер против ответа; приказ
    # одного числа, отвеченный числом.
    подсадки = (
        "divide 14 em 2 partes iguais. o que dá? 28.",
        "divide 14 by 2. what do you get? 28.",
        "subtract 2 from 9. what do you get? 11.",
        "вычти 2 из 9. что получится? 11.",
        "teile 18 durch 3. wie viel kommt heraus? 6: 18 ÷ 3 = 5.",
        "podziel 18 przez 3. ile wychodzi? 5.",
        "divide 14. o que dá? 7.",
        "раздели 14. что получится? 7.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:160]}")
        print(f"ОПЕРАЦИЯ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_opforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_opforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_opforms.txt по имени")
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
    print(f"ОПЕРАЦИЯ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
