#!/usr/bin/env python3
"""[ЛОВУШКИ СЛУЧАЯ] — пять ловушек среднего и случая, пересчитанные судом.

Суд не пишет закона заново: он берёт его у дома (`chancetrapforms`), где наборы, броски и
третья причина объявлены тремя таблицами. Всякая сумма, всякое деление, всякое
произведение и всякий размах пересчитываются порознь.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

САМОПРОВЕРКА ДОМА СТЕРЕЖЁТ БОЛЬШЕЕ, ЧЕМ СЧЁТ: среднее обязано быть целым и НЕ РАВНЫМ ни
одному члену набора (иначе ловушка спрячется в тот же миг, как покажется), частота обязана
отличаться от половины, а третья причина — расти вместе с обоими числами.

    python3 courts/dist_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import chancetrapforms  # noqa: E402 — дом, объявивший законы расстояния

ИМЯ_СУДА = "chancetrap"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"chancetrap"})


def _судить(строка):
    return chancetrapforms.судить(строка)


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
    print(f"ЛОВУШКИ СЛУЧАЯ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(chancetrapforms.РОДЫ)}, страниц {len(chancetrapforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
