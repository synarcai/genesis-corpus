#!/usr/bin/env python3
"""[КОРЕЙСКАЯ ЧАСТИЦА] — согласие страницы с объявленной таблицей слов и частиц.

Суд не знает корейского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона: сходится
ли частица при слове с рядом, объявленным для его последнего звука, и стои́т ли ЗВЁЗДОЧКА
ровно при нарушении.

    ФОРМА СЛУЖЕБНОГО СЛОВА, ЗАВИСЯЩАЯ ОТ ЗВУЧАНИЯ ПРЕДЫДУЩЕГО, ЕСТЬ ОДНО СЛОВО В ДВУХ
    ОБЛИЧЬЯХ, А НЕ ДВА СЛОВА — и суд, знающий лишь таблицу, доказывает это, не умея слышать.

    python3 courts/koparticle_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import koparticleforms  # noqa: E402 — дом, показывающий закон корейской частицы

ИМЯ_СУДА = "koparticle"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"koparticle"})


def _судить(строка):
    return koparticleforms.судить(строка)


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
    print(f"КОРЕЙСКАЯ ЧАСТИЦА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(koparticleforms.РОДЫ)}, "
          f"страниц {len(koparticleforms.ПОКАЗЫ)}, слов {len(koparticleforms.СЛОВА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
