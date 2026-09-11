#!/usr/bin/env python3
"""[ДЕЛЕНИЕ НА ДОЛЮ] — рост при делении и обратный ход проверки, пересчитанные судом.

Суд не пишет закона заново: он берёт его у дома (`divshareforms`), где рамки и числа объявлены
одной таблицей. Подмена произведения, частного и самого НАПРАВЛЕНИЯ роста ловятся машинально:
рост сверяется числами, а не принимается на слово.

    СУД, ПИШУЩИЙ ЗАКОН ВТОРОЙ РАЗ, РАСХОДИТСЯ С ДОМОМ НА ПЕРВОЙ ЖЕ ПРАВКЕ.

ГРАНИЦА: строка, которой рамка дома не порождает и которая не расходится с нею одним словом,
суду не подсудна — ложь о СВОЁМ мире говорит замыкание, а не начало строки.

    python3 courts/divshare_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
import divshareforms  # noqa: E402 — дом, объявивший деление на долю

ИМЯ_СУДА = "divshare"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"divshare"})


def _судить(строка):
    return divshareforms.судить(строка)


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
    print(f"ДЕЛЕНИЕ НА ДОЛЮ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(divshareforms.РОДЫ)}, страниц {len(divshareforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
