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


def pass_groups(шаг):
    """Одна группа на ЯЗЫК — сборка живёт в доме, кузница её лишь зовёт."""
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
