#!/usr/bin/env python3
"""[ГРАНИЦА ВЕЛИЧИНЫ] — возможно ли действие, и это проверено сравнением.

Суд не пишет закона заново: он берёт его у дома (`boundforms`), где рамки, вещи и числа
объявлены одной таблицей. Подмена разности, вывернутое сравнение и подмена одного слова ловятся
машинально.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

ГРАНИЦА: строка, которой рамка дома не порождает и которая не расходится с нею одним словом,
суду не подсудна — ложь о СВОЁМ мире говорит замыкание, а не начало строки.

    python3 courts/bound_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import boundforms  # noqa: E402 — дом, объявивший рамки границы величины
import closedworld  # noqa: E402

ИМЯ_СУДА = "bound"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"bound"})


def _судить(строка):
    return boundforms.судить(строка)


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
    print(f"ГРАНИЦА ВЕЛИЧИНЫ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(boundforms.РОДЫ)}, страниц {len(boundforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
