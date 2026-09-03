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
КАНДИДАТЫ = tuple(n for n in range(8, 113) if F.следующее_простое(n) - n <= 8)


def язык_группа(шаг, язык):
    вон = []
    for i in range(16):
        j = шаг * 16 + i
        род = F.РОДЫ[i % 4]
        спросить = (i // 4) % 2 == 1
        if род in ("прост1", "прост2"):
            з = dict(n=КАНДИДАТЫ[(шаг * 53 + i * 17 + (род == "прост2") * 29) % len(КАНДИДАТЫ)])
        elif род == "множ":
            a = 3 + (j * 7 + шаг) % 10
            k = 1 + (j * 3 + шаг * 2) % 7
            з = dict(a=a, b=a * k + j % a)
        else:
            з = dict(k=2 + (j * 5 + шаг) % 9, v=2 + (j * 11 + шаг * 3) % 20)
        вон.append(F.вопрос(язык, род, **з) if спросить else F.утверждение(язык, род, **з))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
