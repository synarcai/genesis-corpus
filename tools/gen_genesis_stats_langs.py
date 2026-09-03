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
ПРОЦЕНТЫ = ((20, 50), (10, 40), (25, 80), (50, 30), (5, 60), (30, 90), (75, 40), (20, 35), (40, 25), (15, 60), (60, 45), (8, 75))


def ряд(шаг, i):
    """A list with an integer mean: a base, a step and a length from the seams."""
    длина = 2 + (шаг + i) % 4
    старт = 3 + (шаг * 5 + i * 7) % 20
    шаг_ = 1 + (шаг * 3 + i) % 6
    р = [старт + k * шаг_ for k in range(длина)]
    while sum(р) % длина:
        р[-1] += 1
    return р


def язык_группа(шаг, язык):
    вон = []
    for i in range(6):
        р = ряд(шаг, i)
        вон.append(F.среднее(язык, р) if i % 2 == 0 else F.вопрос_среднего(язык, р))
        p, n = ПРОЦЕНТЫ[(шаг * 5 + i * 2) % len(ПРОЦЕНТЫ)]
        вон.append(F.вопрос_процента(язык, p, n) if i % 2 == 0 else F.процент(язык, p, n))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
