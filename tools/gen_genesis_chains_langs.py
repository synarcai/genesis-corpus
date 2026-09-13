#!/usr/bin/env python3
"""GENESIS layer: A CHAIN OF TWO AND THREE STEPS IN TWENTY-NINE LANGUAGES.

The owner's word: every language in surplus. Nineteen of the twenty-nine
declared languages (am, ar, el, fa, fi, he, hi, hu, id, ja, ka, ko, sv, sw,
ta, th, uk, vi, zh) carried lexicon and single equalities only, and NOT ONE
CHAIN — the form the market of reasoning buys (holon, ONE-CARRIER: the
ledger is the program is the proof). This world says «九加四等于十三。
十三减九等于四。», «девять плюс четыре равно тринадцать. тринадцать минус
девять равно четыре.», «tisa jumlisha nne ni sawa na kumi na tatu. kumi na
tatu toa tisa ni sawa na nne.» — the result of a step is an operand of the
next.

NOT ONE NEW WORD: the house of chains (tools/chainforms.py) reads the
TEMPLATES each pack already declares in `show_kinds.arithmetic`, tells the
operation by the place of the holes, and fills them with the pack's own
numerals; a number the language does not declare is never said.

MASS FROM THE RULE (М-148): twenty-three chains per language per pass (four of them searches) — six of
(+, −), three of (×, +), six of three steps and four of four steps — on numbers that walk with
strides coprime with the pack's table, so a language shows other numbers
every pass.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chainforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_chains_langs.txt"


def pass_groups(шаг):
    """Одна группа на ЯЗЫК — сборка живёт в доме, кузница её лишь зовёт."""
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
