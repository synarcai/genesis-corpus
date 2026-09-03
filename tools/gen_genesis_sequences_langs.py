#!/usr/bin/env python3
"""GENESIS layer: THE k-TH TERM OF A PROGRESSION IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The sequences world says
«term number 5 of the progression from 9 with step 4 is 25: 5 − 1 = 4,
4 × 4 = 16, 9 + 16 = 25» in en/ru; this world says it in
de/fr/es/it/pt/nl/pl/tr, statement and question answered by the statement
(М-153), the ledger unchanged. The house of progression phrases
(tools/seqforms.py) holds the phrases; the court reads the same table.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import seqforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_sequences_langs.txt"


def язык_группа(шаг, язык):
    вон = []
    for i in range(8):
        k = 2 + (шаг * 3 + i) % 7
        a = 2 + (шаг * 5 + i * 3) % 20
        d = 1 + (шаг * 2 + i * 5) % 9
        вон.append(F.утверждение(язык, k, a, d) if i % 2 == 0 else F.вопрос(язык, k, a, d))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
