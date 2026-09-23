#!/usr/bin/env python3
"""GENESIS layer: THE RATE PER UNIT — see tools/perunitforms.py for the law.

ONE TRIPLE, ONE PASS: the three questions of a triple (the total, the number of units, the rate)
stand in the same pass, in every form of the rate, so that a pass never shows the relation asked
from one end only. The set of triples (and of the sums of two counts) is cut across the passes,
not repeated by them.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import perunitforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_perunit.txt"


def pass_groups(шаг):
    тройки = F.тройки()[шаг::len(PASSES)]
    суммы = F.суммы()[шаг::len(PASSES)]
    вон = []
    for язык in F.ЯЗЫКИ:
        свои = []
        for i in range(len(F.ВМЕСТИЛИЩА[язык])):
            свои += [F.страница(язык, i, род, a, b, c)
                     for a, b, c in тройки for род in F.РОДЫ if род != F.СУММА]
            if i in F.ВЕЗУТ:
                свои += [F.страница(язык, i, F.СУММА, a, b, c, b1=b1, b2=b2) for a, b1, b2, b, c in суммы]
        вон.append(свои)
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
