#!/usr/bin/env python3
"""GENESIS layer: SEARCH WITH ITS LEDGER IN TEN LANGUAGES.

holon's order for the market of reasoning (03.09): the answer that is FOUND
by a bounded walk shows the walk — «the smallest prime greater than 90 is
97: 91 = 7 × 13, 92 = 2 × 46, …, 97 is prime.», «the smallest whole number n
with n × 7 > 30 is 5: 1 × 7 = 7 ≤ 30, …, 5 × 7 = 35 > 30.», «какое число,
если его пятая часть равна 6? пятая часть числа равна 6; число — 30:
6 × 5 = 30.» — three operations, four surfaces (the next prime is asked two
ways: one operation, two questions), statement and question answered by the
statement (М-153), in en/ru/de/fr/es/it/pt/nl/pl/tr. The house of search
phrases (tools/searchforms.py) holds the phrases; the court reads the same
table and walks the same walk.

MASS FROM THE RULE (М-148): every template gets ten shows over the five
passes on ten different numbers; the indices of number and template are
decoupled (the walk of the number is a stride coprime with the table).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import searchforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_search_langs.txt"
# the numbers whose walk to the next prime is at most eight steps (the walk
# 113 → 127 would be a line of fourteen witnesses)
# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ.
КАНДИДАТЫ = F.КАНДИДАТЫ


def язык_группа(шаг, язык):
    return [с for с, _род in F.перебор(шаг, язык)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
