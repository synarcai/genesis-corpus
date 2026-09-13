#!/usr/bin/env python3
"""GENESIS layer: FOUNDATIONS OF MATHEMATICS — and the named case.

Five subjects of mathematics and one of language stood absent or thin.

  · A FUNCTION is a correspondence taken as ONE OBJECT — the first time
    a rule becomes a thing that can itself be argued about;
  · INJECTION and BIJECTION are the two questions one asks of any
    correspondence, and their difference is shown by a WITNESS, not by
    a definition: one pair of inputs with the same output kills
    injectivity and kills nothing else;
  · CARDINALITY is the discovery that infinities are comparable: the
    even numbers are as many as the naturals because n ↔ 2n pairs them
    off, and that pairing is exhibited, not asserted;
  · PROOF BY CONTRADICTION is the shape of argument that assumes what
    it denies. It is shown with every step computable;
  · THE NAMED CASE closes a gap the corpus carried from the start: it
    showed case forms IN USE («после понедельника», «в часе») and NEVER
    NAMED THEM. To show a form without its name is to leave the reader
    without the word by which the knowledge is found anywhere else.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mathfoundforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ: указатель родов ищет МИР ДОМА по ней и по ввозу кузницы.
ЦЕЛЬ = "datasets/genesis_mathfound.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
