#!/usr/bin/env python3
"""[ИМЯ ПОСЛЕ ЧИСЛИТЕЛЬНОГО] — согласие страницы с отказами, объявленными пакетами языков.

Суд не знает ни одного из семнадцати языков. Он берёт цитаты в «ёлочках» и спрашивает у дома
один закон: стои́т ли ЗВЁЗДОЧКА ровно при той строке, которую пакет её языка ОТВЕРГ, — и
отсутствует ли она при той, которую пакет назвал заменой.

    ЧИСЛИТЕЛЬНОЕ УЖЕ СКАЗАЛО «МНОГО». ЯЗЫКИ РАСХОДЯТСЯ В ТОМ, ГОВОРИТЬ ЛИ ЭТО ВТОРОЙ РАЗ, —
    И ВСЯКИЙ ОТКАЗ ЗДЕСЬ ЕСТЬ ОТВЕТ ОДНОГО ЛАГЕРЯ, ПРИНЕСЁННЫЙ В ДРУГОЙ.

    python3 courts/numnoun_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import numnounforms  # noqa: E402 — дом, показывающий водораздел лагерей

ИМЯ_СУДА = "numnoun"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"numnoun"})


def _судить(строка):
    return numnounforms.судить(строка)


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
    лагерями = " ".join(f"{л}:{len(кк)}" for л, кк in sorted(numnounforms.ЛАГЕРИ.items()))
    поза = "PASS" if ложных == 0 else "FAIL"
    print(f"ИМЯ ПОСЛЕ ЧИСЛИТЕЛЬНОГО {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(numnounforms.РОДЫ)}, страниц {len(numnounforms.ПОКАЗЫ)}, "
          f"пластов {len(numnounforms.ПЛАСТЫ)} ({лагерями}), цитат отвергнутого "
          f"{len(numnounforms.ЛОЖЬ)}, цитат замены {len(numnounforms.ПРАВДА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
