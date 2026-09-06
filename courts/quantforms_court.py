#!/usr/bin/env python3
"""[QUANTIFIER COURT] — every claim carries its counted witness; CLOSED WORLD.

A show of the quantifier world (tools/quantforms.py) is a counted basket and one of five
claims over it: all are red (refuted by a counted witness, or true and witnessed by the whole
count), some are green (witnessed by their number), none are blue (refused with its ground —
the colour the basket never carried), and the complement counted («how many are not red? 9 − 5
= 4»). The census found four lines of «every one of» in the whole свод.

The court reads each line back through the house's frames. A page is true when the count of the
basket is the count of its parts, when the witness names the number that makes the claim true
or false, and when the complement is the difference. A page whose witness counts wrong is a
lie, however right its yes or no. A line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import quantforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"quantforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): свидетель опровержения посчитан неверно; дополнение
    # сложено вместо вычитания; свидетель существования чужого числа — на пяти языках.
    подсадки = (
        "there are 5 apples in the basket: 3 red and 2 green. are all the apples red? no: 3 are green.",
        "there are 9 apples in the basket: 5 red and 4 green. how many apples are not red? 14: 9 − 5 = 14.",
        "there are 5 apples in the basket: 3 red and 2 green. are there any green ones? yes: 4 are green.",
        "в корзине 5 яблок: 3 красных и 2 зелёных. все ли яблоки красные? нет: 3 зелёных.",
        "в корзине 9 яблок: 5 красных и 4 зелёных. сколько яблок не красных? 5: 9 − 5 = 5.",
        "w koszyku jest 9 jabłek: 5 czerwonych i 4 zielone. ile jabłek nie jest czerwonych? 5: 9 − 5 = 5.",
        "im Korb sind 5 Äpfel: 3 rote und 2 grüne. sind alle Äpfel rot? nein: 4 sind grün.",
        "il y a 7 pommes dans le panier : 4 rouges et 3 vertes. y a-t-il des vertes ? oui : 5 sont vertes.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"КВАНТОР FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_quantforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_quantforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_quantforms.txt по имени")
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
    print(f"КВАНТОР {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
