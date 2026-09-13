#!/usr/bin/env python3
"""GENESIS layer: THE JOINT BETWEEN TWO NUMERIC PHRASES.

32's number of 04.09 named a lock, and this layer is the corpus' half of the
key. A market may read the joint word BY POSITION — «the word standing
between two numeric phrases of one clause» — before it has bought anything
(М-162: the role is known by position, the law is bought by links). But a
corpus that shows ONE word in that position teaches the word, not the
position: today the whole svod puts «and» there, with six translations.

The layer shows a FAN in one and the same place, and — the sharper half —
the place WITHOUT any word:

    ann has 5 apples and 3 pears.               ← слово
    ann has 5 apples plus 3 pears.              ← другое слово, та же роль
    ann has 5 apples, 3 pears and 2 plums.      ← запятая И слово, одна клауза
    ann has 5 apples, 3 pears, 2 plums.         ← позиция без слова вовсе

MASS BY THE RULE (М-148): every joint of every language carries six shows of
the two-member frame and six of the three-member one per pass, and the bare
list carries as many as the language has joints — so no surface thins when a
new joint is declared beside it (the law of the fan, lived in the comparative
layer: a count that depends on a list must READ that list).

Words, names and the word for «things» are NOT declared here: they are the
declared vocabulary of the action-pages house, read through the joints house
(tools/jointforms.py). Two houses, one dictionary.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jointforms as F  # noqa: E402
import actionpages as A  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_joints.txt"
# ПЕРЕБОР ЖИВЁТ В ДОМЕ, А НЕ ЗДЕСЬ (13.09): дом обязан знать свои страницы, чтобы назвать
# их род. ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ НА ПЕРВОЙ ЖЕ ПРАВКЕ.
НА_СОЧЛЕНЕНИЕ = F.НА_СОЧЛЕНЕНИЕ


def язык_группа(шаг, язык):
    return [с for с, _род in F.перебор(шаг, язык)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
