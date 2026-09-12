#!/usr/bin/env python3
"""[КЛАСС В СУАХИЛИ] — согласие страницы с объявленной таблицей классов и числительных.

Суд не знает суахили. Он берёт цитаты в «ёлочках» и спрашивает у дома три вещи, объявленные
там таблицей: сходится ли числительное при имени с законным для его класса; берёт ли
множественное имя своё числительное; и стои́т ли ЗВЁЗДОЧКА ровно при нарушении.

    СВОД ОТВЕРГАЛ «kitabu mmoja» ПЯТНАДЦАТЬЮ СТРОКАМИ И НЕ ГОВОРИЛ ПОЧЕМУ. Показ отказа учит,
    что так нельзя, и не учит, почему; ученик запоминает список запретов вместо одного
    правила — и первый же случай вне списка берёт наугад.

    python3 courts/swclass_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import swclassforms  # noqa: E402 — дом, показывающий закон класса

ИМЯ_СУДА = "swclass"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"swclass"})


def _судить(строка):
    return swclassforms.судить(строка)


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
    print(f"КЛАСС В СУАХИЛИ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(swclassforms.РОДЫ)}, "
          f"страниц {len(swclassforms.ПОКАЗЫ)}, имён {len(swclassforms.ИМЕНА)}, "
          f"классов {len(swclassforms.ПРИСТАВКИ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
