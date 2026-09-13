#!/usr/bin/env python3
"""[РОМАНСКИЙ РОД] — согласие страницы с объявленной таблицей артиклей четырёх пластов.

Суд не знает четырёх языков. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона:
сходится ли артикль при имени с объявленным ХОТЬ В ОДНОМ пласте, где оба куска свои, и стои́т
ли ЗВЁЗДОЧКА ровно при нарушении.

    РОД ИМЕНИ СКАЗАН АРТИКЛЕМ, А НЕ ВЫВЕДЕН ИЗ СЛОВА; и роды четырёх родственных языков НЕ
    СОВПАДАЮТ.

    python3 courts/romgender_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import romgenderforms  # noqa: E402 — дом, показывающий закон романского рода

ИМЯ_СУДА = "romgender"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"romgender"})


def _судить(строка):
    return romgenderforms.судить(строка)


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
    print(f"РОМАНСКИЙ РОД {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(romgenderforms.РОДЫ)}, "
          f"страниц {len(romgenderforms.ПОКАЗЫ)}, пластов {len(romgenderforms.ПЛАСТЫ)}, "
          f"имён {sum(len(р) for р in romgenderforms.ИМЕНА.values())}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
