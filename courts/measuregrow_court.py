#!/usr/bin/env python3
"""[РОСТ МЕРЫ] — четыре закона роста, пересчитанные судом.

Суд не пишет закона заново: он берёт его у дома (`measuregrowforms`), где квадраты, кубы и
пары прямоугольников объявлены четырьмя таблицами. Всякое произведение — двух множителей и
трёх — и всякая сумма пересчитываются порознь.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

ТРОЙНОЕ ПРОИЗВЕДЕНИЕ ЧИТАЕТСЯ ПРЕЖДЕ ДВОЙНОГО И ВЫРЕЗАЕТСЯ ИЗ СТРОКИ: «2 × 2 × 2 = 8»
содержит внутри себя «2 × 2», и признак двойного, прочитав его, объявил бы 2 × 2 = 8.

САМОПРОВЕРКА ДОМА СТЕРЕЖЁТ СВОЙСТВО ЛОВУШКИ, которого суду не видно: у пары с одним
периметром площади обязаны РАЗЛИЧАТЬСЯ, у пары с одной площадью — периметры.

    python3 courts/dist_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import measuregrowforms  # noqa: E402 — дом, объявивший законы расстояния

ИМЯ_СУДА = "measuregrow"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"measuregrow"})


def _судить(строка):
    return measuregrowforms.судить(строка)


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
    print(f"РОСТ МЕРЫ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(measuregrowforms.РОДЫ)}, страниц {len(measuregrowforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
