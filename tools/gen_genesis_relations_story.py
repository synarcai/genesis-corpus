#!/usr/bin/env python3
"""GENESIS layer: A MULTIPLE, A DIFFERENCE AND A SUM — school pages in three languages.

e9's order (03.09, G1-ATTACK, genus 1 «multiplicative relation + sum», 21
tasks of the g1 band): «there are twice as many worker bees as baby bees.
there are 750 bees in all. how many baby bees are there? 1 + 2 = 3, 750 ÷ 3
= 250. so the answer is 250.», «bobby has 5 fewer than three times as many
games as brian. brian has 20 games. how many games does bobby have? 3 × 20
= 60, 60 − 5 = 55. so the answer is 55.», the same relation backwards
(«janey has 3 more than twice the number of books sally has. janey has 21
books. how many books does sally have? 21 − 3 = 18, 18 ÷ 2 = 9.»), and the
ages («ruby is three times as old as sam …», «together they are 32 years
old …», the g1 idiom «three times older than») — in en/ru/de, whole
answers, the words of multiplicity declared (twice, three times, four
times, half as many, a third as many; вдвое/втрое/вчетверо, удвоенное/
утроенное/учетверённое; doppelt/dreimal/viermal, halb/ein Drittel). The
house of relation pages (tools/relstory.py) holds the templates; the court
reads them back and regenerates the page.

MASS FROM THE RULE (М-148): every (form, sign, multiplicity, language) cell gets ≥ 9 pages
over the five passes on different numbers; names, things and pairs walk
with strides coprime with their tables.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import relstory as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_relations_story.txt"


# ПЕРЕБОР ЖИВЁТ В ДОМЕ, А НЕ ЗДЕСЬ (13.09): дом обязан знать свои страницы, чтобы назвать
# их род. ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ НА ПЕРВОЙ ЖЕ ПРАВКЕ.
def язык_группа(шаг, язык):
    return [с for с, _род in F.перебор(шаг, язык)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
