#!/usr/bin/env python3
"""[ИЗМЕРЕНИЕ И ТОЧНОСТЬ] — границы измерения, пересчитанные судом.

Суд не пишет закона заново: он берёт его у дома (`measureprecforms`), где измерения и
цены деления объявлены одной таблицей. Границы пересчитываются: низ обязан быть меньше
верха, а сумма двух одинаковых длин — вдвое больше одной.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

ЧИСЛО ЧИТАЕТСЯ С ЗАПЯТОЙ ИЛИ С ТОЧКОЙ — по языку страницы: русская пишет «4,5», английская
«4.5», и суд, знающий одну запись, объявил бы половину мира немой.

    python3 courts/dist_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import measureprecforms  # noqa: E402 — дом, объявивший законы расстояния

ИМЯ_СУДА = "measureprec"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"measureprec"})


def _судить(строка):
    return measureprecforms.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import genesis
    судимо = ложных = 0
    примеры = []
    for путь in genesis.worlds(kind="shows"):
        for строка in путь.read_text(encoding="utf-8", errors="replace").split("\n"):
            если, верно = судить(строка)[:2]
            if not если:
                continue
            судимо += 1
            if not верно:
                ложных += 1
                if len(примеры) < 5:
                    примеры.append(f"{путь.stem}: {строка.strip()[:90]}")
    for п in примеры:
        print(f"  {п}")
    поза = "PASS" if ложных == 0 else "FAIL"
    print(f"ИЗМЕРЕНИЕ И ТОЧНОСТЬ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(measureprecforms.РОДЫ)}, страниц {len(measureprecforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
