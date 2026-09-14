#!/usr/bin/env python3
"""GENESIS layer: THE MEAN AND THE PERCENT IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The average and percent
worlds say «the average of 10, 14, 15 is 13» and «2% of 50 is 1» in en/ru;
this world says both in de/fr/es/it/pt/nl/pl/tr, statement and question
answered by the statement (М-153), with a ledger the court recomputes
(«10 + 14 + 15 = 39, 39 ÷ 3 = 13», «50 × 20 = 1000, 1000 ÷ 100 = 10»). The
house of summary phrases (tools/statforms.py) holds the phrases.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import statforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_stats_langs.txt"
def pass_groups(шаг):
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
