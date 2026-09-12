#!/usr/bin/env python3
"""[НИДЕРЛАНДСКИЙ АРТИКЛЬ] — согласие страницы с объявленной таблицей «de/het».

Суд не знает нидерландского. Он берёт цитаты в «ёлочках» и спрашивает у дома четыре вещи,
объявленные там таблицей: сходится ли артикль при слове с записанным; берёт ли уменьшительное
«het», а множественное «de»; и стои́т ли ЗВЁЗДОЧКА ровно при нарушении.

    АРТИКЛЬ, КОТОРЫЙ НЕ ВЫВОДИТСЯ ИЗ СЛОВА, ПРОВЕРЯЕТСЯ ТОЛЬКО ТАБЛИЦЕЙ — и суд, который
    попытался бы вывести его из длины, звука или смысла, повторил бы ровно ту ошибку, ради
    которой дом поставлен.

    python3 courts/nlarticle_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import nlarticleforms  # noqa: E402 — дом, показывающий закон нидерландского артикля

ИМЯ_СУДА = "nlarticle"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"nlarticle"})


def _судить(строка):
    return nlarticleforms.судить(строка)


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
    print(f"НИДЕРЛАНДСКИЙ АРТИКЛЬ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(nlarticleforms.РОДЫ)}, "
          f"страниц {len(nlarticleforms.ПОКАЗЫ)}, слов {len(nlarticleforms.СЛОВА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
