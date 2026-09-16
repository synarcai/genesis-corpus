#!/usr/bin/env python3
"""[РАЗЛИЧЕНИЕ ЛИЦА] — согласие страницы с объявленными рядами двенадцати пластов.

Суд не знает двенадцати языков. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона:
объявлена ли пара «местоимение + форма» хоть одним пластом и стои́т ли ЗВЁЗДОЧКА ровно там,
где пара не объявлена.

    РАЗЛИЧЕНИЕ ЛИЦА ЕСТЬ НЕ «ДА ИЛИ НЕТ», А ЛЕСТНИЦА ОТ ШЕСТИ ДО ОДНОГО.

    python3 courts/persondist_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import persondistforms  # noqa: E402 — дом, показывающий лестницу различения

ИМЯ_СУДА = "persondist"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"persondist"})


def _судить(строка):
    return persondistforms.судить(строка)


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
    print(f"РАЗЛИЧЕНИЕ ЛИЦА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(persondistforms.РОДЫ)}, "
          f"страниц {len(persondistforms.ПОКАЗЫ)}, пластов {len(persondistforms.ПЛАСТЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
