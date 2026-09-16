#!/usr/bin/env python3
"""[МЕСТО ЛИЦА] — согласие страницы с объявленной таблицей восьми языков.

Суд не знает восьми языков. Он берёт цитаты в «ёлочках» и спрашивает у дома три закона:
всякий ли кусок предметной цитаты объявлен таблицей; одного ли языка местоимение и форма;
стои́т ли ЗВЁЗДОЧКА ровно там, где лицо местоимения расходится с лицом формы.

    ЛИЦО ГОВОРЯЩЕГО ЖИВЁТ В ГЛАГОЛЕ — В ХВОСТЕ СЛОВА, В ГОЛОВЕ СЛОВА, НА ОБОИХ ЕГО КОНЦАХ,
    В ОТДЕЛЬНОМ СЛОВЕ ПРИ НЁМ — ИЛИ НЕ ЖИВЁТ ВОВСЕ.

    python3 courts/personplace_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import personplaceforms  # noqa: E402 — дом, показывающий закон места лица

ИМЯ_СУДА = "personplace"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"personplace"})


def _судить(строка):
    return personplaceforms.судить(строка)


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
    print(f"МЕСТО ЛИЦА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(personplaceforms.РОДЫ)}, "
          f"страниц {len(personplaceforms.ПОКАЗЫ)}, "
          f"языков {len(personplaceforms.ЯЗЫКИ_ПРЕДМЕТА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
