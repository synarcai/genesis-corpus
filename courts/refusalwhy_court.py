#!/usr/bin/env python3
"""[ПРИЧИНА ОТКАЗА] — согласие страницы с объявлениями пакетов о том, что отвергнуто.

Суд не знает двадцати девяти языков. Он спрашивает у дома два закона: стои́т ли ЗВЁЗДОЧКА
ровно на тех цитатах, которые пакет объявил отвергаемыми, и не приведена ли отвергнутая
строка БЕЗ звёздочки.

    ОТКАЗ, НЕ ПРОЦИТИРОВАННЫЙ НИ ОДНИМ ДОМОМ, ОБЪЯСНЁН ТОЛЬКО ЗАМЕНОЙ — а замена без
    объяснения есть второй показ, а не закон.

    python3 courts/refusalwhy_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import refusalwhyforms  # noqa: E402 — дом, называющий причину отказа

ИМЯ_СУДА = "refusalwhy"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"refusalwhy"})


def _судить(строка):
    return refusalwhyforms.судить(строка)


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
    print(f"ПРИЧИНА ОТКАЗА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(refusalwhyforms.РОДЫ)}, "
          f"страниц {len(refusalwhyforms.ПОКАЗЫ)}, "
          f"пар прочитано из объявлений {len(refusalwhyforms.ПАРЫ)}, "
          f"причин {len(refusalwhyforms.ПРИЧИНЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
