#!/usr/bin/env python3
"""[ЯПОНСКОЕ СЧЁТНОЕ] — согласие страницы с объявленной таблицей счётных.

Суд не знает японского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона: сходится
ли счётное при имени с объявленным для него — в ЯПОНСКОМ порядке («имяが числосчётное») и в
КИТАЙСКОМ («числосчётноеの имя»), — и стои́т ли ЗВЁЗДОЧКА ровно при нарушении.

    ЗНАК, СЛУЖАЩИЙ И ИМЕНЕМ, И СЧЁТНЫМ, ЧИТАЕТСЯ ПО МЕСТУ, А НЕ ПО СЕБЕ: «本» перед частицей
    есть книга, «本» после числа есть мера длинных вещей. Суд читает место, а не знак.

    python3 courts/jaclass_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import jaclassforms  # noqa: E402 — дом, показывающий закон японского счётного

ИМЯ_СУДА = "jaclass"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"jaclass"})


def _судить(строка):
    return jaclassforms.судить(строка)


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
    print(f"ЯПОНСКОЕ СЧЁТНОЕ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(jaclassforms.РОДЫ)}, "
          f"страниц {len(jaclassforms.ПОКАЗЫ)}, имён {len(jaclassforms.ИМЕНА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
