#!/usr/bin/env python3
"""[ИНДОНЕЗИЙСКОЕ УДВОЕНИЕ] — согласие страницы с законом повтора.

Суд не знает индонезийского. Он берёт цитаты в «ёлочках» и спрашивает у дома три вещи:
имеет ли удвоение вид «слово-ТО ЖЕ слово»; не стои́т ли повтор при числительном; и стои́т ли
ЗВЁЗДОЧКА ровно при нарушении.

    СВОД ОТВЕРГАЛ «dua buku-buku» И НЕ ГОВОРИЛ ПОЧЕМУ. Показ отказа учит, что так нельзя, и
    не учит, почему; дом даёт причину: число уже сказало о множестве, и повтор становится
    лишним ровно там, где число названо словом.

    python3 courts/idredup_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import idredupforms  # noqa: E402 — дом, показывающий закон удвоения

ИМЯ_СУДА = "idredup"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"idredup"})


def _судить(строка):
    return idredupforms.судить(строка)


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
    print(f"ИНДОНЕЗИЙСКОЕ УДВОЕНИЕ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(idredupforms.РОДЫ)}, "
          f"страниц {len(idredupforms.ПОКАЗЫ)}, слов {len(idredupforms.СЛОВА)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
