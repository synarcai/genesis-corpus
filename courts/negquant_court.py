#!/usr/bin/env python3
"""[ОТРИЦАНИЕ КВАНТОРА] — равносильности отрицания, пересчитанные судом.

Суд не пишет закона заново: он берёт его у дома (`negquantforms`), где мешки объявлены
одной таблицей. Счёт мешка пересчитывается — красных и синих вместе обязано быть всего, —
а ИСТИННОСТЬ каждого высказывания выводится домом из того же счёта.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

САМОПРОВЕРКА ДОМА СТЕРЕЖЁТ ТО, ЧЕГО СУД НЕ ВИДИТ: все три вида мешка обязаны быть в
таблице. Без смешанного различие «не все» и «все не» не показано вовсе; без крайних не
показано, что оно бывает НЕЗАМЕТНЫМ, — а именно незаметность и делает ловушку ловушкой.

    python3 courts/dist_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import negquantforms  # noqa: E402 — дом, объявивший законы расстояния

ИМЯ_СУДА = "negquant"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"negquant"})


def _судить(строка):
    return negquantforms.судить(строка)


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
    print(f"ОТРИЦАНИЕ КВАНТОРА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(negquantforms.РОДЫ)}, страниц {len(negquantforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
