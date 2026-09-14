#!/usr/bin/env python3
"""GENESIS layer: «MORE THAN» AND «TIMES AS MANY» IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The comparison worlds say the
difference and the ratio of two holdings in en/ru; this world says them in
de/fr/es/it/pt/nl/pl/tr — the two facts, then the comparison with its
ledger, as a statement and as the question answered by it (М-153); actors
from the packs, things with their count forms, the multiplier by the
language's own word. The house of comparison phrases (tools/cmpforms.py)
holds the phrases; the court recomputes the difference and the ratio.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import cmpforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_compare_langs.txt"


def pass_groups(шаг):
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
