#!/usr/bin/env python3
"""GENESIS layer: AREA AND PERIMETER IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The geometry world says the
area and the perimeter of a rectangle and of a square in English and
Russian; this world says the same four facts in de/fr/es/it/pt/nl/pl/tr,
as a statement and as a question answered by the statement (М-153), with
the geometry world's ledger («7 × 8 = 56», «7 + 8 = 15, 2 × 15 = 30»,
«4 × 4 = 16»). The house of geometry phrases (tools/geoforms.py) holds the
phrases; the court reads the same phrases and recomputes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import geoforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_geometry_langs.txt"
ШИРИНА = 3


def язык_группа(шаг, язык):
    вон = []
    for i in range(ШИРИНА):
        for k in range(len(F.ФАКТЫ)):
            a = 2 + (шаг * 5 + i * 3 + k) % 11
            # SIDE 4 IS NEVER SHOWN (М-148 (1); holon's TSV 04.09): at side 4 the
            # perimeter «4 × 4 = 16» and the area «4 × 4 = 16» are one telling,
            # and the constant of the perimeter law is indistinguishable from
            # the side — the executors are tied by that one show.
            if a == 4:
                a = 13
            b = 2 + (шаг * 3 + i * 7 + k * 2) % 9
            if b == a:
                b += 1
            вон.append(F.утверждение(язык, k, a, b))
            вон.append(F.вопрос(язык, k, a, b))
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
