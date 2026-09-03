#!/usr/bin/env python3
"""GENESIS layer: DIVISION WITH A REMAINDER IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The remainders world says «17
divided by 5 is 3 remainder 2: 5 × 3 = 15, 17 − 15 = 2» in en/ru; this
world says it in de/fr/es/it/pt/nl/pl/tr, statement and question answered
by the statement (М-153), the ledger unchanged. The house of remainder
phrases (tools/remforms.py) holds the phrases; the court reads the same
table and divides again.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import remforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_remainders_langs.txt"


def язык_группа(шаг, язык):
    вон = []
    for i in range(8):
        b = 2 + (шаг * 3 + i * 5) % 8                 # 2..9
        q = 2 + (шаг * 5 + i * 3) % 9                 # 2..10
        r = 1 + (шаг * 7 + i * 11) % (b - 1)          # 1..b−1 — never zero
        a = b * q + r
        вон.append(F.утверждение(язык, a, b) if i % 2 == 0 else F.вопрос(язык, a, b))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
