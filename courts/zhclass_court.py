#!/usr/bin/env python3
"""[КИТАЙСКОЕ СЧЁТНОЕ СЛОВО] — согласие страницы с объявленной таблицей счётных.

Суд не знает китайского. Он берёт цитаты в «ёлочках» и спрашивает у дома два закона: сходится
ли счётное слово при имени с объявленным для него (пустое место счётным не считается — его
нет ни в одной таблице), и стои́т ли ЗВЁЗДОЧКА ровно при нарушении.

    СВОД ОТВЕРГАЛ «一本笔» И «三本猫» И НЕ ГОВОРИЛ ПОЧЕМУ. Дом даёт причину: счётное говорит,
    ЧТО ИМЕННО считают, и выбирает его ИМЯ, а не говорящий.

    python3 courts/zhclass_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import zhclassforms  # noqa: E402 — дом, показывающий закон счётного слова

ИМЯ_СУДА = "zhclass"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"zhclass"})


def _судить(строка):
    return zhclassforms.судить(строка)


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
    print(f"КИТАЙСКОЕ СЧЁТНОЕ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(zhclassforms.РОДЫ)}, "
          f"страниц {len(zhclassforms.ПОКАЗЫ)}, имён {len(zhclassforms.ИМЕНА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
