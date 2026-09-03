#!/usr/bin/env python3
"""GENESIS layer: TWO KINDS AND A SUM OF WEIGHTS — the system of two unknowns.

e9's order (03.09, the profile of muteness of the g1 band, genus 5): «there
are 20 animals … 70 legs, how many cows?» was mute not for the arithmetic
but because no page ever said how many legs a cow has. This world says it —
and answers with a chain of primitives, not a guess:

  «there are 20 animals in a farm, chickens and cows. a chicken has 2 legs
   and a cow has 4 legs. there are 70 legs in all. how many cows are there?
   2 × 20 = 40, 70 − 40 = 30, 4 − 2 = 2, 30 ÷ 2 = 15. so the answer is 15.»

The chain is the substitution written out: all of the lesser kind would give
2 × 20 legs; the surplus is bought by swaps, each swap adding 4 − 2. Both
questions are asked — the greater kind and the lesser (which adds one step,
20 − 15 = 5). Three pairs per language (chickens and cows, bicycles and
cars, beetles and spiders), en/ru/de; the house of two kinds
(tools/twokinds.py) declares every count form it uses.

MASS FROM THE RULE (М-148, and the measured price of mass): twenty-four pages per
language per pass — twelve per question — so every (pair, question, language)
cell holds twenty pages and more.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import twokinds as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_two_kinds.txt"


def язык_группа(шаг, язык):
    вон = []
    пар = len(F.ЯЗЫКИ[язык]["пары"])
    j = шаг * 13
    for i in range(24):
        пара = (шаг + i) % пар
        n = 8 + (шаг * 5 + i * 7 + j) % 40
        бол = 1 + (шаг * 3 + i * 5 + j) % (n - 1)
        спрос = "бол" if i % 2 == 0 else "мал"
        try:
            вон.append(F.страница(язык, пара, n, бол, спрос))
        except ValueError:
            pass
        j += 1
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
