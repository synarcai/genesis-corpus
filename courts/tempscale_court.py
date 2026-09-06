#!/usr/bin/env python3
"""[TEMPERATURE SCALE COURT] — a factor AND an offset, and the road back in reverse order; CLOSED WORLD.

A show of the two scales (tools/tempscale.py) is one temperature said twice. The court recomputes
both steps and judges the CONSTANTS of the law as numbers of the page, not as letters of the
pattern: nine fifths and thirty-two stand in holes, so a page that multiplies by five ninths is a
LIE and not a silence. It demands the road back in the OPPOSITE order (the offset first, then the
inverted factor), the corpus's minus sign «−» (not a hyphen), and the parenthesis around a
negative first summand — the record of the signed world, not decoration. The two anchors are the
facts the corpus already holds: water freezes at zero Celsius and boils at a hundred, and the verb
of each anchor is the house of nature's own.

The census found zero lines carrying «Celsius» or «Fahrenheit» in the whole свод before this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import tempscale as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"tempscale"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): сдвиг забыт; множитель перевёрнут; сдвиг подменён;
    # дорога назад идёт в ТОМ ЖЕ порядке; скобка при отрицательном первом слагаемом снята;
    # опора нуля названа кипением; опора сотни названа замерзанием; сумма шага неверна.
    подсадки = (
        "20 градусов по Цельсию — сколько это по Фаренгейту? 36 градусов по Фаренгейту: 20 × 9 ÷ 5 = 36. 36 + 32 = 36.",
        "20 degrees Celsius — how much is that in Fahrenheit? 68 degrees Fahrenheit: 20 × 5 ÷ 9 = 36. 36 + 32 = 68.",
        "20 Grad Celsius — wie viel ist das in Fahrenheit? 68 Grad Fahrenheit: 20 × 9 ÷ 5 = 36. 36 + 30 = 68.",
        "68 stopni Fahrenheita — ile to jest Celsjusza? 20 stopni Celsjusza: 68 × 5 ÷ 9 = 36. 36 − 32 = 20.",
        "14 градусов по Фаренгейту — сколько это по Цельсию? −10 градусов по Цельсию: 14 − 32 = −18. −18 × 5 ÷ 9 = −10.",
        "0 градусов по Цельсию — это 32 градуса по Фаренгейту: при этой температуре вода кипит.",
        "100 Grad Celsius sind 212 Grad Fahrenheit: bei dieser Temperatur gefriert Wasser.",
        "25 grados Celsius — ¿cuánto es eso en Fahrenheit? 78 grados Fahrenheit: 25 × 9 ÷ 5 = 45. 45 + 32 = 78.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"ШКАЛА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_tempscale.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_tempscale.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_tempscale.txt по имени")
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
    print(f"ШКАЛА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
