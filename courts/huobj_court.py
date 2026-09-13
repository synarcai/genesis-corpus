#!/usr/bin/env python3
"""[ВЕНГЕРСКОЕ ОБЪЕКТНОЕ СПРЯЖЕНИЕ] — согласие страницы с объявленной таблицей двух рядов.

Суд не знает венгерского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона: всякий
ли кусок венгерской цитаты объявлен таблицей и стои́т ли ЗВЁЗДОЧКА ровно там, где ряд глагола
разошёлся с предметом действия.

    ГЛАГОЛ СОГЛАСУЕТСЯ НЕ ТОЛЬКО С ЛИЦОМ ГОВОРЯЩЕГО, НО И С ОПРЕДЕЛЁННОСТЬЮ ПРЕДМЕТА
    ДЕЙСТВИЯ, — И ТОГДА ОДНО ЛИЦО ИМЕЕТ ДВА ОКОНЧАНИЯ, А НЕ ОДНО.

    python3 courts/huobj_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import huobjforms  # noqa: E402 — дом, показывающий закон объектного спряжения

ИМЯ_СУДА = "huobj"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"huobj"})


def _судить(строка):
    return huobjforms.судить(строка)


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
    print(f"ВЕНГЕРСКОЕ ОБЪЕКТНОЕ СПРЯЖЕНИЕ {поза}: {ложных} ложных из {судимо} судимых "
          f"(рубеж 0); родов объявлено {len(huobjforms.РОДЫ)}, "
          f"страниц {len(huobjforms.ПОКАЗЫ)}, глаголов {len(huobjforms.ГЛАГОЛЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
