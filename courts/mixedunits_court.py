#!/usr/bin/env python3
"""[MIXED-MEASURE COURT] — the carry has a base, or the page lies; CLOSED WORLD.

A show of the mixed-measure world (tools/mixedunits.py) writes one measure in TWO units at once
and lets the smaller overflow into the greater: grams into kilograms (a thousand) and
centimetres into metres (a hundred). Before this house the свод carried no such line at all,
and every carry it showed was a carry by ten.

The court reads each line back through the house's frames. A page is true when the sum or the
difference holds in the SMALL unit, when the small part of every measure is UNDER its base
(«4 kg 1100 g» is not a measure but a carry left unfinished — the very lie the house is
written against), when the page actually crosses the unit (a sum whose grams stay under a
thousand teaches nothing plain addition did not), and when each count form is the form its
number takes by the pack's rule. A line of a frame that breaks any of these is a lie; a line of
no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import mixedunits as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"mixedunits"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): перенос не сделан («3 кг 1100 г» вместо «4 кг 100 г»);
    # сумма не сходится; заём не сделан (вычитание по большой единице отдельно от малой);
    # перенос через сто у длины.
    подсадки = (
        "the bag weighs 2 kilograms 300 grams. 1 kilogram 800 grams was added to it. how much does the bag weigh? 3 kilograms 1100 grams: 2 kilograms 300 grams + 1 kilogram 800 grams = 3 kilograms 1100 grams.",
        "the bag weighs 2 kilograms 300 grams. 1 kilogram 800 grams was added to it. how much does the bag weigh? 4 kilograms 200 grams: 2 kilograms 300 grams + 1 kilogram 800 grams = 4 kilograms 200 grams.",
        "the bag weighed 4 kilograms 100 grams. 1 kilogram 800 grams was taken out of it. how much does the bag weigh now? 3 kilograms 300 grams: 4 kilograms 100 grams − 1 kilogram 800 grams = 3 kilograms 300 grams.",
        "the rope is 2 metres 30 centimetres long. 1 metre 85 centimetres was tied to it. how long is it now? 3 metres 115 centimetres: 2 metres 30 centimetres + 1 metre 85 centimetres = 3 metres 115 centimetres.",
        "мешок весит 2 килограмма 300 граммов. в него добавили 1 килограмм 800 граммов. сколько весит мешок? 3 килограмма 1100 граммов: 2 килограмма 300 граммов + 1 килограмм 800 граммов = 3 килограмма 1100 граммов.",
        "мешок весит 2 килограмма 300 граммов. в него добавили 1 килограмм 800 граммов. сколько весит мешок? 4 килограмма 200 граммов: 2 килограмма 300 граммов + 1 килограмм 800 граммов = 4 килограмма 200 граммов.",
        "lina ma długość 2 metry 30 centymetrów. doczepiono do niej 1 metr 85 centymetrów. ile jest teraz? 3 metry 115 centymetrów: 2 metry 30 centymetrów + 1 metr 85 centymetrów = 3 metry 115 centymetrów.",
        "der Sack wog 4 Kilogramm 100 Gramm. 1 Kilogramm 800 Gramm wurden herausgenommen. wie viel wiegt der Sack jetzt? 3 Kilogramm 300 Gramm: 4 Kilogramm 100 Gramm − 1 Kilogramm 800 Gramm = 3 Kilogramm 300 Gramm.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"МЕРА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_mixedunits.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_mixedunits.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_mixedunits.txt по имени")
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
    print(f"МЕРА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
