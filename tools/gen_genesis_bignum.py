#!/usr/bin/env python3
"""GENESIS layer: LARGE NUMBERS (RUNG-1 gap: GSM8K
lives in hundreds and thousands; the positional column
is bought, the shows beyond twenty are scarce).

Kinds (glyph-first — GSM8K asks in digits):
  R  place rulers      "100 + 10 = 110."
  C  hundred chains    "340 + 10 = 350."
  A  column adds       "234 + 152 = 386."
  S  column subs       "574 − 231 = 343."
  M  tens multiplication "30 × 4 = 120."
  D  clean division    "480 ÷ 4 = 120."

Instances vary by pass (32's trail number: repeats buy
weight, not coverage); bare shows; form-feed seams.
"""

import inverting
from layer import emit


def kinds_for_pass(pi):
    base = pi * 17
    shows = []
    # R: place rulers around the pass anchor
    for k in range(12):
        h = ((base + k * 7) % 9 + 1) * 100
        t = ((base + k * 5) % 9) * 10
        shows.append(f"{h} + {t} = {h + t}.")
        shows.append(
            f"{h + t} + 10 = {h + t + 10}."
        )
        shows.append(
            f"{h + t + 100} − 100 = {h + t}."
        )
    # A/S: column pairs without/with borrow mix
    for k in range(14):
        a = 111 + ((base + k * 37) % 800)
        b = 101 + ((base + k * 23) % (a - 100))
        shows.append(f"{a} + {b} = {a + b}.")
        shows.append(f"{a + b} − {b} = {a}.")
    # M/D: tens
    for k in range(10):
        m = ((base + k * 3) % 9 + 1) * 10
        f = (base + k) % 8 + 2
        shows.append(f"{m} × {f} = {m * f}.")
        shows.append(f"{m * f} ÷ {f} = {m}.")
    return shows


def with_asks(pi):
    """Every glyph equality gets its question beside it.

    KNOWLEDGE WITHOUT A QUESTION SURFACE DOES NOT ANSWER — IT ONLY
    TELLS. The layer had 424 lines and zero questions; the owner made
    zero silent worlds a law. The question is the same line with the
    predicate lifted out («what is 950 − 100? 950 − 100 = 850.»), so
    the answer is judged by the same court as the statement; a
    corrupted answer is caught — checked before writing.
    """
    out = []
    for i, show in enumerate(kinds_for_pass(pi)):
        out.append(show)
        ask = inverting.обратить(show, ("глиф",), i)
        if ask:
            out.append(ask)
    return out


def main():
    emit("datasets/genesis_bignum.txt", with_asks)


if __name__ == "__main__":
    main()
