#!/usr/bin/env python3
"""GENESIS layer: LINEAR ALGEBRA — vector and matrix as ONE object.

The syllabus court named vector and matrix absent. They are not an
advanced topic bolted on: a vector is the first object that is a
NUMBER-WITH-DIRECTION, and a matrix the first object that ACTS on
another object. Every engineer meets them as the language of state and
transformation; a corpus without them cannot say what a system does.

EXACT LENGTHS ONLY. The length of (3, 4) is 5 and the length of (1, 1)
is not writable here — the corpus states what it can check, and the
Pythagorean triples that make lengths whole are named, not searched.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import linalgforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет
# МИР ДОМА по этой самой строке и по ввозу кузницы. Путь, отданный литералом
# внутрь `emit_grouped`, оставляет дом БЕЗ МИРА, и указатель честно пишет None.
#
#     ВВОЗ ЕСТЬ СВЯЗЬ, НО НАЙТИ ЕЁ УКАЗАТЕЛЬ МОЖЕТ ЛИШЬ ТАМ, ГДЕ ОБЪЯВЛЕНА ЦЕЛЬ.
ЦЕЛЬ = "datasets/genesis_linalg.txt"

# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). Ряды, помощники и все пять строителей переехали в
# `tools/linalgforms.py`; ступень законов, стоявшая ПОДЛЕ кортежа, объявлена там шестым
# родом, а не потеряна.
#
#     ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ НА ПЕРВОЙ ЖЕ ПРАВКЕ.


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
