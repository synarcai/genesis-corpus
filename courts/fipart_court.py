#!/usr/bin/env python3
"""[ФИНСКИЙ ПАРТИТИВ] — согласие страницы с объявленной таблицей трёх форм.

Суд не знает финского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона: стои́т ли
после числа больше единицы ПАРТИТИВ, а при «yksi» — именительный, и стои́т ли ЗВЁЗДОЧКА ровно
при нарушении.

    ПАДЕЖ И ЧИСЛО — ДВЕ РАЗНЫЕ ВЕЩИ, И ПОСЛЕ ФИНСКОГО ЧИСЛА РАБОТАЕТ ПЕРВОЕ: «kaksi taloa»
    есть ЕДИНСТВЕННОЕ в частичном падеже, а не множественное.

    python3 courts/fipart_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import fipartforms  # noqa: E402 — дом, показывающий закон партитива

ИМЯ_СУДА = "fipart"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"fipart"})


def _судить(строка):
    return fipartforms.судить(строка)


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
    print(f"ФИНСКИЙ ПАРТИТИВ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(fipartforms.РОДЫ)}, "
          f"страниц {len(fipartforms.ПОКАЗЫ)}, слов {len(fipartforms.СЛОВА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
