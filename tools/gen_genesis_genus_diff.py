#!/usr/bin/env python3
"""GENESIS layer: DEFINITIONS BY GENUS AND DIFFERENCE — and four questions of one fact.

The measure of the shelf (03.09) counted «связка без числа» — a copula without
a number — as fourteen per cent of the sentences of books, the largest kind of
prose no house of the corpus had ever written. The world «definitions» QUOTES a
dictionary of the shelf; this world WRITES the form itself, and holon named the
shape: ONE LINE holding «утверждение. вопрос? ответ.», as in the
world of inquiry, so that the market of the copula buys the FACT from the
statement and the form of the ANSWER only from the question→answer pair
standing beside it:

  «a pen is a tool that writes. what is a pen? a tool that writes.»
  «a pen is a tool that writes. is a pen a tool or an animal? a tool.»
  «a pen is a tool that writes. what does a pen do? a pen writes.»
  «a pen is a tool that writes. which tool writes? a pen.»

Four questions of one fact, and their answers cover every role of it: the whole
predicate, the genus alone, the difference alone, and the NAME alone — the last
is the inversion, where the difference asks and the thing answers.

Twenty-three things over nine genera in each of en/ru/de; the house
(tools/defforms.py) declares every word and every agreement it uses. The world
writes each distinct line ONCE — the lexicon is finite, and repeating it would
be weight, not knowledge (the measured price of mass, 03.09); the mass law
(М-148) is met by the count of things: every «language × question» cell holds
twenty-three shows and more.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import defforms as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_genus_diff.txt"
# the choice question of a thing is asked against three declared genera, not
# all nine: three suffice to say that the answer is the thing's own genus
ЧУЖИХ_РОДОВ = 3


def строки(язык):
    """Every distinct line of the world, in the order of the table."""
    вон = []
    for i in range(len(F.ЯЗЫКИ[язык]["определения"])):
        for форма in F.ФОРМЫ:
            сдвиги = range(ЧУЖИХ_РОДОВ) if форма == "род" else (0,)
            вон += [F.показ(язык, форма, i, с) for с in сдвиги]
    return вон


ВСЕ = {язык: строки(язык) for язык in F.ЯЗЫКИ}


def pass_groups(шаг):
    return [[с for j, с in enumerate(ВСЕ[язык]) if j % len(PASSES) == шаг]
            for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
