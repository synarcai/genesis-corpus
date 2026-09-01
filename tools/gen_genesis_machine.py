#!/usr/bin/env python3
"""GENESIS layer: HOW A MACHINE HOLDS A NUMBER.

    13 in binary is 1101.        13 in hex is d.
    13 and 6 is 4.               13 or 6 is 15.
    13 xor 6 is 11.              13 shifted left by 2 is 52.
    1101 in binary is 13 in decimal.
    a byte holds 8 bits and 256 values.

A programmer meets the same number in several dresses and must know
they are one number. Bases and bit operations are the most exactly
checkable knowledge there is — and the corpus had NOT ONE show of
either: no hex, no bitwise and/or/xor, no shifts.

WHAT IS SHOWN AND WHY EACH:
  · BASES two, eight and sixteen, in both directions — writing a
    number in a base and reading it back — because a base is a
    translation, and a translation shown one way teaches a table;
  · AND, OR, XOR as operations on the SAME pair, so their difference
    is met rather than described: the same 13 and 6 give 4, 15 and 11;
  · SHIFTS, with their arithmetic meaning stated beside them («shifted
    left by 2 is 52» beside «13 × 4 = 52»), because a shift that is
    not tied to multiplication is a trick instead of a fact;
  · WIDTH — what a byte holds — since every bound a programmer meets
    later stands on it.

NEGATIVE NUMBERS ARE ABSENT DELIBERATELY. Two's complement needs a
declared width, and the same bits mean different numbers at different
widths: shown without the width, it is not a fact but a coincidence.
It waits for a layer that declares width in every show.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import json  # noqa: E402

from langpack import count_form_index  # noqa: E402
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

RU_PACK = json.loads(
    (pathlib.Path(__file__).resolve().parent
     / "langpacks/ru.json").read_text(encoding="utf-8"))
RU_RULE = {"forms": ["one", "few", "many"],
           "count_agreement": RU_PACK["count_agreement"]}
# ПРАВИЛО ЧИСЛА ЧИТАЕТСЯ ИЗ ПАКЕТА, а не переписывается: «4 бит» ложно,
# «4 бита» верно, и знает это описание русского языка.
ФОРМЫ = {"бит": ("бит", "бита", "бит"),
         "значение": ("значение", "значения", "значений")}


def ру(слово, k):
    return ФОРМЫ[слово][count_form_index(RU_PACK, RU_RULE, k)]

ЧИСЛА = [13, 6, 25, 40, 7, 100, 31, 64, 18, 255, 12, 9, 200, 33, 17, 48]
ПАРЫ = [(13, 6), (12, 10), (7, 3), (25, 9), (60, 15), (14, 7),
        (31, 16), (100, 36), (9, 5), (21, 12), (63, 21), (40, 24)]
СДВИГИ = [(13, 2), (5, 3), (7, 1), (3, 4), (9, 2), (11, 3),
          (6, 2), (25, 1), (2, 5), (17, 2)]
ШИРИНЫ = [(4, "nibble"), (8, "byte"), (16, "halfword"), (32, "word")]


def pass_shows(pass_i):
    out = []
    for i in range(12):
        n = ЧИСЛА[(pass_i * 3 + i) % len(ЧИСЛА)]
        a, b = ПАРЫ[(pass_i + i) % len(ПАРЫ)]
        s, k = СДВИГИ[(pass_i * 5 + i) % len(СДВИГИ)]
        бит, имя = ШИРИНЫ[(pass_i + i) % len(ШИРИНЫ)]
        # --- основания, в обе стороны
        out.append(f"{n} in binary is {n:b}.")
        out.append(f"{n:b} in binary is {n} in decimal.")
        out.append(f"{n} in octal is {n:o}.")
        out.append(f"{n:o} in octal is {n} in decimal.")
        out.append(f"{n} in hex is {n:x}.")
        out.append(f"{n:x} in hex is {n} in decimal.")
        out.append(f"{n} в двоичной записи это {n:b}.")
        out.append(f"{n} в шестнадцатеричной записи это {n:x}.")
        # --- три операции на ОДНОЙ паре, чтобы различие встретилось
        out.append(f"{a} and {b} is {a & b}.")
        out.append(f"{a} or {b} is {a | b}.")
        out.append(f"{a} xor {b} is {a ^ b}.")
        out.append(f"{a} и {b} побитово это {a & b}.")
        out.append(f"{a} или {b} побитово это {a | b}.")
        # --- сдвиг, всегда рядом со своим умножением
        out.append(f"{s} shifted left by {k} is {s << k}.")
        out.append(f"{s} × {2 ** k} = {s << k}.")
        out.append(f"{s << k} shifted right by {k} is {s}.")
        out.append(f"{s} сдвинутое влево на {k} это {s << k}.")
        # --- ширина
        out.append(f"a {имя} holds {бит} {by_count(бит, 'bits')} and "
                   f"{2 ** бит} values.")
        out.append(f"with {бит} bits you can write {2 ** бит} "
                   f"{by_count(2 ** бит, 'numbers')}.")
        out.append(f"{имя} держит {бит} {ру('бит', бит)} и "
                   f"{2 ** бит} {ру('значение', 2 ** бит)}.")
    return out


def main():
    emit("datasets/genesis_machine.txt", pass_shows)


if __name__ == "__main__":
    main()
