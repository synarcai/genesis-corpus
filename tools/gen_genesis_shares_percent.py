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

MASS FROM THE RULE (М-148, and holon's word 03.09 — LAW² different shows per WORD of a fraction): 86 shows per language per pass — the share
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


# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09) ВМЕСТЕ СО СВОИМИ ПОМОЩНИКАМИ.
def язык_группа(шаг, язык):
    return [с for с, _род in F.перебор(шаг, язык)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
