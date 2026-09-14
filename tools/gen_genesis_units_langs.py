#!/usr/bin/env python3
"""GENESIS layer: UNIT CONVERSIONS IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The conversion worlds say
«2 hours are 120 minutes: 2 × 60 = 120» in English and Russian; this world
says eight conversions (hour→minute, day→hour, week→day, year→month,
kilometre→metre, metre→centimetre, kilogram→gram, minute→second) in
de/fr/es/it/pt/nl/pl/tr, as a statement and as the question of the small
amount answered by the statement (М-153). The house of unit names
(tools/unitforms.py) holds the names with their count forms and genders;
the ratio comes from the house of units; the court reads the same tables.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import unitforms as U  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_units_langs.txt"
def pass_groups(шаг):
    return U.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
