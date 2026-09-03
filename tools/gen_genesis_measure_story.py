#!/usr/bin/env python3
"""GENESIS layer: MEASURED STORIES — a distance compared, and a pair priced.

Two of holon's orders from the last lines of the attack (03.09):

  «the frog jumped 31 inches. the grasshopper jumped 25 inches. how many more
   inches did the frog jump than the grasshopper? 31 − 25 = 6.»
  «a house and a lot cost 120 dollars together. the house costs three times as
   much as the lot. how much does the lot cost? 3 + 1 = 4, 120 ÷ 4 = 30.»

The first buys the VERB as a place of the frame, not as a word: six verbs walk
(jumped, ran, walked, swam, flew, crawled — прыгнул, пробежал, прошёл, проплыл,
пролетел, прополз), each with its bare form for the question and, in Russian,
with its own preposition and its past tense agreeing with the actor. The second
buys «as MUCH as» beside «times» on a price, and asks both ends of the pair.

MASS BY THE RULE (М-148, LAW² = 9): every verb carries twelve shows in each
language, every multiplier twenty-four; the house (tools/measurestory.py)
declares every form it uses.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import measurestory as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_measure_story.txt"


def язык_группа(шаг, язык):
    я = F.ЯЗЫКИ[язык]
    вон = []
    деятелей, мер = len(я["деятели"]), len(я["меры"])
    for г in range(len(я["глаголы"])):
        for i in range(6):
            д = (шаг * 3 + г * 2 + i) % деятелей
            второй = (д + 1 + i % (деятелей - 1)) % деятелей
            a, b = F.ПАРЫ_МЕРЫ[(шаг * 5 + г * 3 + i) % len(F.ПАРЫ_МЕРЫ)]
            for форма in ("мера_больше", "мера_меньше"):
                try:
                    вон.append(F.мера(язык, форма, a, b, м=(шаг + г + i) % мер,
                                      г=г, деятель=д, второй=второй))
                except ValueError:
                    pass
    for k in F.МНОЖИТЕЛИ:
        for i in range(6):
            товар = (шаг + k + i) % len(я["товары"])
            основание = F.ОСНОВАНИЯ_ЦЕНЫ[(шаг * 3 + k * 2 + i) % len(F.ОСНОВАНИЯ_ЦЕНЫ)]
            for форма in ("пара_мал", "пара_бол"):
                вон.append(F.пара(язык, форма, товар=товар, k=k, основание=основание))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
