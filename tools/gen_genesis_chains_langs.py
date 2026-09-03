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

MASS FROM THE RULE (М-148): twelve chains per language per pass — six of
(+, −), three of (×, +), three of three steps — on numbers that walk with
strides coprime with the pack's table, so a language shows other numbers
every pass.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import chainforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_chains_langs.txt"


def _пара(язык, шаг, i):
    """(a, b) whose sum and difference the language can say."""
    т = sorted(v for v in F.ЧИСЛА[язык] if v >= 1)
    for сдвиг in range(len(т)):
        a = т[(шаг * 7 + i * 5 + сдвиг) % len(т)]
        b = т[(шаг * 3 + i * 11 + сдвиг * 3) % len(т)]
        if a < 1 or b < 1 or (a + b) not in F.ЧИСЛА[язык]:
            continue
        return a, b
    return None


def _тройка(язык, шаг, i, оп):
    """(a, b) whose product (or quotient) and the next step the language can say."""
    т = sorted(v for v in F.ЧИСЛА[язык] if v >= 1)
    for сдвиг in range(len(т)):
        a = т[(шаг * 5 + i * 3 + сдвиг) % len(т)]
        b = т[(шаг * 11 + i * 7 + сдвиг * 2) % len(т)]
        if a < 2 or b < 2:
            continue
        p = a * b if оп == "×" else None
        if p is None or p not in F.ЧИСЛА[язык]:
            continue
        return a, b
    return None


def язык_группа(шаг, язык):
    вон = []
    если = F.умеет
    if not (если(язык, "+") and если(язык, "−")):
        return вон
    # six chains (+, −): the sum is spent by a subtraction
    for i in range(6):
        п = _пара(язык, шаг, i)
        if п is None:
            continue
        a, b = п
        s = a + b
        for c in sorted(v for v in F.ЧИСЛА[язык] if 1 <= v < s):
            if (s - c) in F.ЧИСЛА[язык] and c != b:
                вон.append(F.цепь(язык, (("+", a, b, s), ("−", s, c, s - c))))
                break
    # three chains (×, +): the product is grown by an addition
    if если(язык, "×"):
        for i in range(3):
            п = _тройка(язык, шаг, i, "×")
            if п is None:
                continue
            a, b = п
            p = a * b
            for c in sorted(v for v in F.ЧИСЛА[язык] if v >= 1):
                if (p + c) in F.ЧИСЛА[язык] and c != a:
                    вон.append(F.цепь(язык, (("×", a, b, p), ("+", p, c, p + c))))
                    break
    # three chains of THREE steps: the ledger of the market of reasoning
    for i in range(3):
        п = _пара(язык, шаг, i + 3)
        if п is None:
            continue
        a, b = п
        s = a + b
        for c in sorted(v for v in F.ЧИСЛА[язык] if 1 <= v < s):
            r = s - c
            if r not in F.ЧИСЛА[язык] or r < 2:
                continue
            for d in sorted(v for v in F.ЧИСЛА[язык] if v >= 2):
                if если(язык, "×") and (r * d) in F.ЧИСЛА[язык]:
                    вон.append(F.цепь(язык, (("+", a, b, s), ("−", s, c, r), ("×", r, d, r * d))))
                    break
            else:
                continue
            break
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
