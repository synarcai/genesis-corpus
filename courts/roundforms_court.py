#!/usr/bin/env python3
"""[ROUNDING COURT] — the rule of the half is declared, and the ledger compares; CLOSED WORLD.

A show of the rounding world (tools/roundforms.py) rounds one number to a base and names BOTH
distances in its ledger, because rounding is a COMPARISON and not the dropping of a digit: a
page that merely truncated would answer forty for forty-seven as well. Where the distances are
equal the answer is not forced by the numbers at all — the corpus declares «the half goes up»,
and declares it ON THE PAGE in every language.

The court reads each line back through the house's frames. A page is true when the two edges
are the edges of THAT base, when the distances are their differences, when the answer is the
nearer edge — and, in the form of the half, when the distances are equal and the answer is the
upper edge. A page of equal distances judged by the nearer-edge form is a lie, and so is a half
sent down. A line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import roundforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"roundforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): отброшена цифра вместо сравнения; расстояние посчитано
    # неверно; половина ушла вниз вопреки объявленному правилу; у сотен взят не тот край.
    подсадки = (
        "what is 47 rounded to the nearest ten? 40: 47 − 40 = 7, 50 − 47 = 3.",
        "what is 47 rounded to the nearest ten? 50: 47 − 40 = 7, 50 − 47 = 4.",
        "what is 45 rounded to the nearest ten? 40: 45 − 40 = 5, 50 − 45 = 5, the half goes up.",
        "what is 437 rounded to the nearest hundred? 500: 437 − 400 = 37, 500 − 437 = 63.",
        "сколько будет 47, если округлить до десятков? 40: 47 − 40 = 7, 50 − 47 = 3.",
        "сколько будет 45, если округлить до десятков? 40: 45 − 40 = 5, 50 − 45 = 5, половина идёт вверх.",
        "ile wynosi 437 zaokrąglone do setek? 500: 437 − 400 = 37, 500 − 437 = 63.",
        "wie lautet 47 gerundet auf Zehner? 40: 47 − 40 = 7, 50 − 47 = 3.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ОКРУГЛЕНИЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_roundforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_roundforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_roundforms.txt по имени")
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
    print(f"ОКРУГЛЕНИЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
