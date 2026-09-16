#!/usr/bin/env python3
"""[ВЬЕТНАМСКОЕ СЧЁТНОЕ] — согласие страницы с объявленной таблицей счётных.

Суд не знает вьетнамского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона:
сходится ли счётное при имени с объявленным (пустое место счётным не считается — его нет ни в
одной таблице), и стои́т ли ЗВЁЗДОЧКА ровно при нарушении.

    РАЗРЯД ВЕЩИ НЕ ЧИТАЕТСЯ ПО ЕЁ СМЫСЛУ: «con» стои́т и при кошке, и при ноже. Суд, который
    попытался бы вывести разряд из значения, повторил бы ровно ту ошибку, ради которой дом
    поставлен.

    python3 courts/viclass_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import viclassforms  # noqa: E402 — дом, показывающий закон вьетнамского счётного

ИМЯ_СУДА = "viclass"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"viclass"})


def _судить(строка):
    return viclassforms.судить(строка)


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
    print(f"ВЬЕТНАМСКОЕ СЧЁТНОЕ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(viclassforms.РОДЫ)}, "
          f"страниц {len(viclassforms.ПОКАЗЫ)}, имён {len(viclassforms.ИМЕНА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
