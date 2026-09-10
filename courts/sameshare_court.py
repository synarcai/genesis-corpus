#!/usr/bin/env python3
"""[ОДНА ДОЛЯ РАЗНЫМИ ЗАПИСЯМИ] — тождество долей, пересчитанное от целого.

Суд не пишет закона заново: он берёт его у дома (`sameshareforms`), где рамки, доли и целые
объявлены одной таблицей, а имена долей взяты у дома долей. Подмена частного, подмена
произведения и подмена одного слова ловятся машинально.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

ГРАНИЦА: строка, которой рамка дома не порождает и которая не расходится с нею одним словом,
суду не подсудна — ложь о СВОЁМ мире говорит замыкание, а не начало строки.

    python3 courts/sameshare_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import sameshareforms  # noqa: E402 — дом, объявивший тождество записей доли

ИМЯ_СУДА = "sameshare"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"sameshare"})


def _судить(строка):
    return sameshareforms.судить(строка)


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
    print(f"ОДНА ДОЛЯ РАЗНЫМИ ЗАПИСЯМИ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(sameshareforms.РОДЫ)}, страниц {len(sameshareforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
