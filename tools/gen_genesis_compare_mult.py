#!/usr/bin/env python3
"""GENESIS layer: THE MULTIPLE — «as many» and «as much» on one number.

The band dies on thirteen questions of one genus, «how many times as
much», and the root is named exactly: the corpus bought the frame «as
MANY as» and never bought «as MUCH as», because the two never stood
SIDE BY SIDE ON THE SAME NUMBERS. English chooses the word by what is
being compared — a countable thing takes «many», a measured amount
takes «much» — and that choice is a fact of the language, not of the
arithmetic. Shown apart, the two frames look like two unrelated
phrases; shown together on one multiplier, they are one relation said
twice, and the difference between them is the lesson.

SIX ACTS OF ONE MULTIPLICATION:

    РАМКА       — «tom has 12 apples … three times as many apples as
                  ann» beside «the house cost 90000 dollars … three
                  times as much as the lot»: countable and measured,
                  one multiplier, one show
    МНОЖИТЕЛЬ   — «three times 5 is 15» AND «thrice 5 is 15»: the
                  multiplier as a WORD, which is where the band's
                  questions live — «twice», «double», «вдвое»
    ОСНОВАНИЕ   — «12 is three times more than 4: 12 = 3 × 4»: the
                  ground stands beside the claim, never behind it
    ОБРАТНОЕ    — «how many times more is 12 than 4?»: the same fact
                  asked from the other end, and its ground is a
                  DIVISION, for that is what the question performs
    РАЗНОСТНОЕ  — «8 more apples, and three times as many» in ONE
                  show: difference and multiple on the same two
                  numbers, because a reader who never saw them
                  together has no way to learn that they differ
    ЦЕНА        — the money frame of the band: «the lot cost 30000
                  dollars, so the house cost 90000 dollars»

EVERY FORM OF BOTH LANGUAGES IS TAKEN, NOT WRITTEN. The Russian count
form comes from `tools/rugram.py` («12 яблок», «4 яблока», «1
яблоко»), the gender of the past tense from the same house's rule of
gender («том собрал», «аня собрала», «кольцо стоило»), the numeral
word and its genitive from the language pack («вдвое больше семи —
четырнадцать»), the English plural from the `plural` organ («1 apple»,
«3 apples»). A generator that takes its forms cannot write a wrong
one; a generator that writes them will write a wrong one as often as
it writes.

THE ARTICLE IS CHOSEN BY SOUND, NOT BY LETTER: «an apple» and «an
hour», «a book» and «a university». The rule looks at the letter and a
NAMED class of exceptions says where the letter lies about the sound —
the same shape rugram uses for «-мя», and for the same reason: a rule
that knows why it retreats is a rule, and a list of words is not.

A CORE OF VERBATIM REPEATS. The first three cases of every genus are
the SAME in every pass, twice per pass — ten identical shows in the
layer — while the rest walk their numbers. A form is bought by
REPETITION: the neighbour's measurement, not an opinion. Numbers that
never repeat teach arithmetic and buy no frame at all.
"""

import collections
import json
import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import layer  # noqa: E402
import numerals  # noqa: E402
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402
from plural import by_count, singular  # noqa: E402

# ДОМ ОТДЕЛЁН ОТ КУЗНИЦЫ (13.09): таблицы, показы, роды и словарь показов живут в
# `tools/cmpmultforms.py`, а кузница берёт у него готовые группы. Мир был третьим по величине
# бездомным миром свода — 2 759 строк без объявленного рода.
#
#     МИР, ЧЬИ СТРАНИЦЫ НЕ НАЗВАНЫ РОДОМ, ЧИТАЕТСЯ ТОЛЬКО ТЕМ, КТО ЧИТАЕТ КУЗНИЦУ.
import cmpmultforms as F  # noqa: E402

ЦЕЛЬ = "datasets/genesis_compare_mult.txt"


def pass_groups(шаг):
    """Одна группа на РОД — сборка живёт в доме, кузница её лишь зовёт."""
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
