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

MASS FROM THE RULE (М-148): nineteen chains per language per pass — six of
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
    # chains of THREE and FOUR steps: the ledger of the market of reasoning, and
    # the food of the library of chains (holon 03.09: a bought chain becomes a
    # step of another, so depth is what the library eats)
    for i in range(6):
        цепочка = _вглубь(язык, шаг, i + 3, шагов=3)
        if цепочка:
            вон.append(F.цепь(язык, цепочка))
    for i in range(4):
        цепочка = _вглубь(язык, шаг, i + 9, шагов=4)
        if цепочка:
            вон.append(F.цепь(язык, цепочка))
    return вон


def _вглубь(язык, шаг, i, шагов):
    """A chain of `шагов` steps: every intermediate number is one the language
    declares, and every step spends the previous result."""
    т = sorted(v for v in F.ЧИСЛА[язык] if v >= 1)
    п = _пара(язык, шаг, i)
    if п is None:
        return None
    a, b = п
    s = a + b
    цепочка = [("+", a, b, s)]
    текущее = s
    # the operations walk in turn: −, ×, −, ÷ … — each taking the running number
    порядок = ("−", "×", "−", "+")
    for k in range(шагов - 1):
        оп = порядок[(k + шаг) % len(порядок)]
        нашли = False
        if оп == "−":
            for c in sorted(v for v in т if 1 <= v < текущее):
                if (текущее - c) in F.ЧИСЛА[язык] and (текущее - c) >= 2:
                    цепочка.append(("−", текущее, c, текущее - c)); текущее -= c; нашли = True
                    break
        elif оп == "×" and F.умеет(язык, "×"):
            for d in sorted(v for v in т if v >= 2):
                if (текущее * d) in F.ЧИСЛА[язык]:
                    цепочка.append(("×", текущее, d, текущее * d)); текущее *= d; нашли = True
                    break
        else:
            for c in sorted(v for v in т if v >= 1):
                if (текущее + c) in F.ЧИСЛА[язык]:
                    цепочка.append(("+", текущее, c, текущее + c)); текущее += c; нашли = True
                    break
        if not нашли:
            # the language cannot say the next number — the chain stops honestly
            return цепочка if len(цепочка) >= шагов - 1 and len(цепочка) >= 2 else None
    return цепочка


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
