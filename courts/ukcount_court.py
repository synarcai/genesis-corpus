#!/usr/bin/env python3
"""[УКРАИНСКАЯ СЧЁТНАЯ ЯЧЕЙКА] — согласие страницы с объявленной таблицей трёх форм.

Суд не знает украинского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона:
сходится ли форма имени с ячейкой, объявленной для ПОСЛЕДНЕЙ ЦИФРЫ числа, и стои́т ли
ЗВЁЗДОЧКА ровно при нарушении.

    ДВА БЛИЗКИХ ЯЗЫКА, РАЗОШЕДШИЕСЯ В ОДНОЙ ЯЧЕЙКЕ, ОПАСНЕЕ ДВУХ ДАЛЁКИХ: сходство зовёт
    переносить, а расхождение стои́т ровно там, куда перенос приводит.

    python3 courts/ukcount_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import ukcountforms  # noqa: E402 — дом, показывающий закон счётной ячейки

ИМЯ_СУДА = "ukcount"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"ukcount"})


def _судить(строка):
    return ukcountforms.судить(строка)


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
    print(f"УКРАИНСКАЯ ЯЧЕЙКА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(ukcountforms.РОДЫ)}, "
          f"страниц {len(ukcountforms.ПОКАЗЫ)}, слов {len(ukcountforms.СЛОВА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
