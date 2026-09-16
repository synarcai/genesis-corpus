#!/usr/bin/env python3
"""[СЧЁТ ВКЛЮЧИТЕЛЬНО] — потерянная единица, пересчитанная судом.

Суд не пишет закона заново: он берёт его у дома (`fenceforms`), где пары дней и длины рядов
объявлены двумя таблицами. Всякая разность и всякая сумма пересчитываются порознь.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

САМОПРОВЕРКА ДОМА СТЕРЕЖЁТ ТО, ЧЕГО СУДУ НЕ ВИДНО: обе стороны потери обязаны быть
показаны. Дом, дающий лишь «дней на один больше», научил бы прибавлять единицу везде — а в
столбах и распилах её надо ОТНИМАТЬ.

    python3 courts/dist_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import fenceforms  # noqa: E402 — дом, объявивший законы расстояния

ИМЯ_СУДА = "fence"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"fence"})


def _судить(строка):
    return fenceforms.судить(строка)


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
    print(f"СЧЁТ ВКЛЮЧИТЕЛЬНО {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(fenceforms.РОДЫ)}, страниц {len(fenceforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
