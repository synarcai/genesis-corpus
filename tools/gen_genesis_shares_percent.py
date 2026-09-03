#!/usr/bin/env python3
"""GENESIS layer: SHARES AND PERCENTS OVER QUANTITIES — genus 2 of the g1 band.

holon's word (03.09, G1-ATTACK): five forms, every ledger a chain of
primitives that stays WHOLE on the axis, ≥ 10 shows per form and language,
en/ru/de — «what is two thirds of 24? two thirds of 24 is 16: 24 ÷ 3 = 8,
8 × 2 = 16.», «what is 40 percent of 220? 40 percent of 220 is 88: 220 × 40
= 8800, 8800 ÷ 100 = 88.», «three quarters of the pupils have a pen; 20 do
not. how many pupils are there? 20 is one quarter of 80: 4 − 3 = 1, 20 ÷ 1
= 20, 20 × 4 = 80.», «two thirds of a number is 16. what is the number? 16
is two thirds of 24: 16 ÷ 2 = 8, 8 × 3 = 24.», «12 is 40 percent of what
number? 12 is 40 percent of 30: 12 × 100 = 1200, 1200 ÷ 40 = 30.» The house
of share and percent phrases (tools/fracforms.py) holds the templates; the
court reads the fraction words back to their numbers and recomputes.

MASS FROM THE RULE (М-148): 24 shows per language per pass — the share
walks the 45 declared (numerator, denominator) pairs with a stride coprime
with the table, the percents the eleven declared ones, and every quantity
is chosen so that the answer is whole.
"""
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fracforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_shares_percent.txt"


def _доля(j):
    return F.ДОЛИ[(j * 7) % len(F.ДОЛИ)]


def _процент(j):
    """(p, N) with N·p divisible by 100 — the answer whole: N is a multiple of
    100 ÷ gcd(p, 100)."""
    p = F.ПРОЦЕНТЫ[j % len(F.ПРОЦЕНТЫ)]
    шаг = 100 // math.gcd(p, 100)
    return p, шаг * (2 + (j * 3) % 12)


def язык_группа(шаг, язык):
    вон = []
    j = шаг * 29
    # the share of a quantity: eight per pass, statement and question in turn
    for i in range(8):
        n, d = _доля(j + i)
        вон.append(F.страница(язык, "доля", n=n, d=d, q=2 + (шаг * 5 + i * 7 + j) % 25, вопрос=(i + шаг) % 2 == 1))
    j += 8
    # the percent of a quantity: six per pass
    for i in range(6):
        p, N = _процент(j + i)
        вон.append(F.страница(язык, "проц", p=p, N=N, вопрос=(i + шаг) % 2 == 0))
    j += 6
    # the complement («three quarters have; 20 do not»): four per pass
    for i in range(4):
        n, d = _доля(j + i * 3)
        if d - n < 1:
            n, d = 1, d
        вон.append(F.страница(язык, "дополн", n=n, d=d, q=2 + (шаг * 7 + i * 5 + j) % 18, вещь=(шаг + i) % 5))
    j += 4
    # the number from its share: three per pass
    for i in range(3):
        n, d = _доля(j + i * 5)
        вон.append(F.страница(язык, "число", n=n, d=d, q=2 + (шаг * 3 + i * 11 + j) % 20))
    j += 3
    # the number from its percent: three per pass
    for i in range(3):
        p, N = _процент(j + i * 4)
        вон.append(F.страница(язык, "проц_обр", p=p, N=N))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
