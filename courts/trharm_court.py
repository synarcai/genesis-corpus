#!/usr/bin/env python3
"""[ТУРЕЦКАЯ ГАРМОНИЯ] — согласие страницы с объявленной таблицей основ и суффиксов.

Суд не знает турецкого. Он берёт цитаты в «ёлочках» и спрашивает у дома три вещи: сходится ли
суффикс при основе с объявленным для неё; не стои́т ли суффикс при числительном; и стои́т ли
ЗВЁЗДОЧКА ровно при нарушении.

    СУФФИКС, МЕНЯЮЩИЙ ГЛАСНУЮ ПО ОСНОВЕ, ЕСТЬ ОДИН СУФФИКС, А НЕ ДВА — и суд, знающий лишь
    таблицу, доказывает это одним сравнением, не умея читать гласных.

    python3 courts/trharm_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import trharmforms  # noqa: E402 — дом, показывающий закон гармонии

ИМЯ_СУДА = "trharm"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"trharm"})


def _судить(строка):
    return trharmforms.судить(строка)


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
    print(f"ТУРЕЦКАЯ ГАРМОНИЯ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(trharmforms.РОДЫ)}, "
          f"страниц {len(trharmforms.ПОКАЗЫ)}, основ {len(trharmforms.ОСНОВЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
