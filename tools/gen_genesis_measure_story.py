#!/usr/bin/env python3
"""GENESIS layer: MEASURED STORIES — a distance compared, and a pair priced.

Two of holon's orders from the last lines of the attack (03.09): two measured acts and their
difference, and a pair priced one by the other, asked at both ends.

  «the horse ran 23 metres. the fox ran 6 metres. how many more metres did the horse run than
   the fox? 23 − 6 = 17.»
  «a tent and a lantern cost 56 dollars together. the tent costs three times as much as the
   lantern. how much does the lantern cost? 3 + 1 = 4, 56 ÷ 4 = 14.»

SCENES REWRITTEN 23.09 (the owner's word, the lead's order): the orders had been written by
reading the bands — the SVAMP jumping contest of the grasshopper, the frog and the mouse, and
GSM8K g1.26 «a house and a lot» word for word. The constructions stay, the scenes go, and every
verb now takes its own actors (tools/measurestory.py, `КТО`): «the kangaroo flew 73 metres» was a
page of this world.

The first buys the VERB as a place of the frame, not as a word: six verbs walk (jumped, ran,
walked, swam, flew, crawled — прыгнул, пробежал, прошёл, проплыл, пролетел, прополз), each with its
bare form for the question and, in Russian, with its own preposition and its past tense agreeing
with the actor. The second buys «as MUCH as» beside «times» on a price, and asks both ends of the
pair.

MASS BY THE RULE (М-148, LAW² = 9): every verb carries at least twelve shows in each language,
every multiplier twenty-four; the house declares every form it uses.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import measurestory as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_measure_story.txt"


# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ.
def язык_группа(шаг, язык):
    return [с for с, _род in F.перебор(шаг, язык)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
