#!/usr/bin/env python3
"""[ШВЕДСКИЙ РОД] — согласие страницы с объявленной таблицей артиклей.

Суд не знает шведского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона: сходится
ли артикль при имени с объявленным и стои́т ли ЗВЁЗДОЧКА ровно при нарушении — артикля или
формы прилагательного.

    ШВЕДСКИХ РОДОВ ДВА: ОБЩИЙ БЕРЁТ «en», СРЕДНИЙ — «ett». ПО САМОМУ СЛОВУ РОД НЕ ВИДЕН.

    python3 courts/svgender_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import svgenderforms  # noqa: E402 — дом, показывающий закон шведского рода

ИМЯ_СУДА = "svgender"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"svgender"})


def _судить(строка):
    return svgenderforms.судить(строка)


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
    print(f"ШВЕДСКИЙ РОД {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(svgenderforms.РОДЫ)}, страниц {len(svgenderforms.ПОКАЗЫ)}, "
          f"имён {len(svgenderforms.ИМЕНА)}, пар с прилагательным "
          f"{len(svgenderforms.ПРИЛАГАТЕЛЬНЫЕ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
