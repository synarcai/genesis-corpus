#!/usr/bin/env python3
"""[ВЫБОР ДЕЙСТВИЯ] — знак леджера обязан быть тем, какого требует решающее слово страницы.

Суд не пишет закона заново: он берёт его у дома (`opchoiceforms.РЕШАЮЩИЕ`), где оборот и знак
объявлены ОДНОЙ таблицей. Подмена «потеря убавляет: 11 + 9 = 20» ловится машинально, и так же
ловится подмена самого оборота при верном счёте.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

ГРАНИЦА: строка без объявленного оборота суду не подсудна — он о выборе действия, а не о счёте
вообще; счёт таких строк читает арифметика.

    python3 courts/opchoice_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import opchoiceforms  # noqa: E402 — дом, объявивший решающее слово и его знак

ИМЯ_СУДА = "opchoice"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"opchoice"})


def _судить(строка):
    return opchoiceforms.судить(строка)


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
    print(f"ВЫБОР ДЕЙСТВИЯ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"оборотов объявлено {sum(len(т) for т in opchoiceforms.РЕШАЮЩИЕ.values())}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
