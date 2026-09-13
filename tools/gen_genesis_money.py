#!/usr/bin/env python3
"""GENESIS layer: MONEY IN CENTS, AND THE BRIDGE TO THE DECIMAL WRITING.

e9's order (04.09, the g1 band: 15 of 65 problems carry «$16.50», and the
organism is honestly mute on decimals): money is counted in CENTS — whole
numbers on the one axis the organism owns — and the decimal writing of a
price is shown as a BRIDGE with its ledger beside it: «16.50 dollars is 1650
cents: 16 × 100 = 1600, 1600 + 50 = 1650.» A sum in dollars carries the
same sum in cents as its witness («16.50 + 2.50 = 19.00 dollars: 1650 + 250
= 1900 cents»), so the decimal never stands without the whole number that
the court recomputes. Prices, sums, multiples and change in cents (EN) and
kopecks (RU); the answer opens with the question's first quantity (М-145).
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import coinforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_money.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
