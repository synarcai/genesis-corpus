#!/usr/bin/env python3
"""[МЕСТО ЧИСЛА В ИМЕНИ] — согласие страницы с формами, объявленными пакетами языков.

Суд не знает ни одного из двадцати семи языков. Он берёт цитаты в «ёлочках» и спрашивает у
дома один закон: всякая цитата обязана быть ОБЪЯВЛЕННОЙ ФОРМОЙ пакета, а ЗВЁЗДОЧКА обязана
стоять ровно при той строке, которую пакет ОТВЕРГ.

    ЧИСЛО ЖИВЁТ В ИМЕНИ — В ХВОСТЕ, В ГОЛОВЕ, ВНУТРИ, В СЛУЖЕБНОМ СЛОВЕ, В ОТДЕЛЬНОМ СЛОВЕ
    ПОДЛЕ — ИЛИ НЕ ЖИВЁТ ВОВСЕ. Место вычислено сравнением двух объявленных форм.

    python3 courts/numplace_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import numplaceforms  # noqa: E402 — дом, показывающий водораздел лагерей

ИМЯ_СУДА = "numplace"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"numplace"})


def _судить(строка):
    return numplaceforms.судить(строка)


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
    местами = " ".join(f"{м.split()[-1]}:{sum(по.values())}"
                       for м, по in sorted(numplaceforms.МЕСТА.items()))
    поза = "PASS" if ложных == 0 else "FAIL"
    print(f"МЕСТО ЧИСЛА В ИМЕНИ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(numplaceforms.РОДЫ)}, страниц {len(numplaceforms.ПОКАЗЫ)}, "
          f"пластов {len(numplaceforms.ПЛАСТЫ)}, мест {len(numplaceforms.МЕСТА)} ({местами}), "
          f"цитат отвергнутого {len(numplaceforms.ЛОЖЬ)}, объявленных форм "
          f"{len(numplaceforms.ПРАВДА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
