#!/usr/bin/env python3
"""GENESIS layer: SPEED AND PRESSURE IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The physics worlds say speed =
distance ÷ time and pressure = force ÷ area in en/ru; this world says both
in de/fr/es/it/pt/nl/pl/tr, statement and question answered by the
statement (М-153), with the unit names in their count forms and the ledger
«72 ÷ 8 = 9». The house of physics phrases (tools/physforms.py) holds the
phrases and the units; the court divides itself.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import physforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_physics_langs.txt"


def pass_groups(шаг):
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
