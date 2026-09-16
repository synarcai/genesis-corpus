#!/usr/bin/env python3
"""[ИСПАНСКОЕ HAY] — согласие страницы с домом, пересчитанное судом.

Суд не знает испанского. Он спрашивает у дома (`hayforms.судить`), своя ли это страница, и
всякую строку, разошедшуюся с показом РОВНО ОДНИМ словом, зовёт ложью.

    СУД, ЧИТАЮЩИЙ ПО ПРИЗНАКУ, А НЕ ПО ПРИНАДЛЕЖНОСТИ К СВОЕМУ НАБОРУ, ЗОВЁТ ЛОЖЬЮ ЧУЖУЮ
    РЕЧЬ, СОВПАВШУЮ С НИМ ФОРМОЙ.

Закон этот куплен той же ночью и чужой прозой: два соседних дома звали ложью сноску у
Бердяева и письмо Чаадаева, оттого что судили по образцу. Здесь идиома взята сразу верная.

    python3 courts/hay_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import hayforms  # noqa: E402 — дом, показывающий неизменность «hay»

ИМЯ_СУДА = "hay"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"hay"})


def _судить(строка):
    return hayforms.судить(строка)


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
    print(f"ИСПАНСКОЕ HAY {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(hayforms.РОДЫ)}, страниц {len(hayforms.ПОКАЗЫ)}, "
          f"вещей {len(hayforms.ВЕЩИ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
