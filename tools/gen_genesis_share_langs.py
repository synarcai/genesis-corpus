#!/usr/bin/env python3
"""GENESIS layer: SHARES IN EIGHT LANGUAGES — «two thirds of 12».

The owner's word: every language in surplus. The share world says «two
thirds of 12 is 8» with its ledger in en/ru; this world says seven shares
(the half, a third, two thirds, a quarter, three quarters, a fifth, two
fifths) of a number in de/fr/es/it/pt/nl/pl/tr, statement and question
answered by the statement (М-153), the ledger the division and — at a
numerator above one — the multiplication. The house of share names
(tools/shareforms.py) holds the names and copulas; the court reads the
share back from its name and recomputes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import shareforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_share_langs.txt"


def язык_группа(шаг, язык):
    вон = []
    for i, (ч, з) in enumerate(F.ДОЛИ):
        n = з * (2 + (шаг * 5 + i * 3) % 12)
        вон.append(F.утверждение(язык, i, n) if (шаг + i) % 2 == 0 else F.вопрос(язык, i, n))
        n2 = з * (2 + (шаг * 7 + i * 5 + 1) % 12)
        вон.append(F.вопрос(язык, i, n2) if (шаг + i) % 2 == 0 else F.утверждение(язык, i, n2))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
