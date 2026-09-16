#!/usr/bin/env python3
"""[НЕМЕЦКИЙ ВИНИТЕЛЬНЫЙ] — согласие страницы с объявленной таблицей родов и падежей.

Суд не знает немецкого. Он берёт цитаты в «ёлочках», спрашивает у САМОЙ СТРАНИЦЫ, о каком
падеже она говорит («именительный», «винительный», «ich sehe»), и сверяет артикль с таблицей
дома.

    ВИНИТЕЛЬНЫЙ МЕНЯЕТ ЛИШЬ МУЖСКОЙ АРТИКЛЬ: «der» → «den». Женский и средний стоя́т
    неизменно — и оттого падеж КАЖЕТСЯ НЕВИДИМЫМ, покуда не встретится мужское имя.

    python3 courts/deacc_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import deaccforms  # noqa: E402 — дом, показывающий закон винительного

ИМЯ_СУДА = "deacc"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"deacc"})


def _судить(строка):
    return deaccforms.судить(строка)


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
    print(f"НЕМЕЦКИЙ ВИНИТЕЛЬНЫЙ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(deaccforms.РОДЫ)}, страниц {len(deaccforms.ПОКАЗЫ)}, "
          f"имён {len(deaccforms.ИМЕНА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
