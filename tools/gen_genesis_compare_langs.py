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


def язык_группа(шаг, язык):
    вон = []
    имена = F.ИМЕНА[язык]
    for i in range(6):
        A = имена[(шаг * 3 + i * 2) % len(имена)]
        B = имена[(шаг * 3 + i * 2 + 1) % len(имена)]
        в = F.ВЕЩИ[язык][(шаг + i) % 4]
        y = 2 + (шаг * 5 + i * 3) % 9
        d = 1 + (шаг * 2 + i * 5) % 8
        x = y + d
        вон.append(F.больше(язык, A, B, x, y, в) if i % 2 == 0 else F.вопрос_больше(язык, A, B, x, y, в))
        k = 2 + (шаг + i) % 4
        y2 = 2 + (шаг * 7 + i) % 6
        вон.append(F.вопрос_кратно(язык, A, B, y2 * k, y2, в) if i % 2 == 0 else F.кратно(язык, A, B, y2 * k, y2, в))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ФРАЗЫ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
