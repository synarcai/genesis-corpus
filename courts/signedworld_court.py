#!/usr/bin/env python3
"""[SIGNED-WORLD COURT] — the sum crosses zero and recomputes, or the page lies; CLOSED WORLD.

A show of the signed world (tools/signedworld.py) is one movement across zero in a frame where
a language writes the minus sign without apology: a morning below zero that warms above it, a
morning above zero that cools below it, the difference through zero («by how much is 3 warmer
than −5? by 8: 3 − (−5) = 8»), and a lift rising from an underground floor.

The court reads each line back through the house's frames. A page is true when the signed sum
recomputes, when the movement ACTUALLY CROSSES ZERO (a page that stays on one side is not
about the sign and the house does not write it), when the difference through zero is positive
and its lower side really is negative, and when each count form is the form of the ABSOLUTE
value of its number («−5 градусов», «−1 градус», «−2 stopnie»). A line of a frame that breaks
any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import signedworld as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"signedworld"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): сумма через ноль не сходится; охлаждение считано без знака;
    # вычитание отрицательного прочитано как «минус делает меньше»; лифт приехал не туда;
    # счётная форма градуса взята не по модулю.
    подсадки = (
        "in the morning it was −5 degrees. it became 8 degrees warmer. how many degrees is it now? 3 degrees: (−5) + 8 = 4.",
        "in the morning it was 3 degrees. it became 8 degrees colder. how many degrees is it now? 5 degrees: 3 − 8 = 5.",
        "by how much is 3 warmer than −5? by 2: 3 − (−5) = 2.",
        "the lift is on floor −2. the lift goes up 5 floors. on which floor is the lift? on floor 7. (−2) + 5 = 7.",
        "утром было −5 градусов. стало на 8 градусов теплее. сколько градусов стало? 3 градуса: (−5) + 8 = 4.",
        "утром было 3 градуса. стало на 8 градусов холоднее. сколько градусов стало? −5 градуса: 3 − 8 = −5.",
        "rano było −5 stopni. zrobiło się cieplej o 8 stopni. ile stopni jest teraz? 3 stopni: (−5) + 8 = 3.",
        "am Morgen waren es −5 Grad. es wurde um 8 Grad wärmer. wie viel Grad sind es jetzt? −3 Grad: (−5) + 8 = −3.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ЗНАК FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_signedworld.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_signedworld.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_signedworld.txt по имени")
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
    print(f"ЗНАК {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
