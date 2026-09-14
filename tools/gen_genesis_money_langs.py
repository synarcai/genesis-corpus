#!/usr/bin/env python3
"""GENESIS layer: MONEY WITH THE DECIMAL COMMA — nine languages.

The owner's word: every language in surplus. The money world wrote prices
the English way («16.50 dollars», «$16.50») and the Russian way in words
(«16 рублей 50 копеек»); Europe writes «16,50 Euro», «16,50 euros», «16,50
zł», Turkey «16,50 lira», Russia also «16,50 рубля» — the DECIMAL COMMA, a
writing the organism had never seen. The same four shapes as the money
world: the bridge («16,50 Euro sind 1650 Cent: 16 × 100 = 1600, 1600 + 50 =
1650.»), the question of the small unit, the way back, and a sum whose
witness is the sum in cents. The house of money writings
(tools/moneyforms.py) holds the units, their count forms, the copulas and
the questions; the court reads the same table and recomputes every link.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import moneyforms as M  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_money_langs.txt"
ШИРИНА = 8


def pass_groups(шаг):
    """Одна группа на ЯЗЫК — сборка живёт в доме, кузница её лишь зовёт."""
    return M.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
