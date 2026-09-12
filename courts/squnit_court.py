#!/usr/bin/env python3
"""[КВАДРАТНЫЕ ЕДИНИЦЫ] — множитель размерности, пересчитанный судом.

Суд не пишет закона заново: он берёт его у дома (`squnitforms`), где пары единиц объявлены
таблицей вместе со своим множителем — а не выведены из имён. Всякая запись страницы
считается разбором свода (`arithread`).

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

САМОПРОВЕРКА ДОМА СТЕРЕЖЁТ ТО, ЧЕГО СУДУ НЕ ВИДНО: обе стороны ловушки обязаны быть
показаны, множитель обязан быть не меньше десяти (иначе ошибка не видна глазом), и знаки
трёх степеней обязаны РАЗЛИЧАТЬСЯ — иначе площадь неотличима от длины, и весь дом говорит
ни о чём.

    python3 courts/squnit_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import squnitforms  # noqa: E402 — дом, объявивший множитель размерности

ИМЯ_СУДА = "squnit"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"squnit"})


def _судить(строка):
    return squnitforms.судить(строка)


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
    print(f"КВАДРАТНЫЕ ЕДИНИЦЫ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(squnitforms.РОДЫ)}, страниц {len(squnitforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
