#!/usr/bin/env python3
"""[НЕМЕЦКИЙ ПРЕДЛОГ ДВУХ ПАДЕЖЕЙ] — согласие страницы с объявленной таблицей артиклей.

Суд не знает немецкого. Он берёт цитаты в «ёлочках» и спрашивает у дома три вещи, объявленные
там таблицей: стои́т ли при предлоге ДВУХ падежей один из двух законных артиклей этого имени;
берёт ли предлог ОДНОГО падежа свой и только свой; и стои́т ли ЗВЁЗДОЧКА ровно при нарушении.

    СУД НЕ РЕШАЕТ, ГДЕ МЕСТО, А ГДЕ НАПРАВЛЕНИЕ, И НЕ ДОЛЖЕН: смысл цитаты ему не подсуден.
    Он судит СОГЛАСИЕ ФОРМЫ С ТАБЛИЦЕЙ — и этого довольно, чтобы поймать чужой падеж.

    python3 courts/decase_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import decaseforms  # noqa: E402 — дом, показывающий закон двух падежей

ИМЯ_СУДА = "decase"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"decase"})


def _судить(строка):
    return decaseforms.судить(строка)


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
    print(f"ПРЕДЛОГ ДВУХ ПАДЕЖЕЙ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(decaseforms.РОДЫ)}, "
          f"страниц {len(decaseforms.ПОКАЗЫ)}, имён {len(decaseforms.ИМЕНА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
