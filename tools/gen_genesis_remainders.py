#!/usr/bin/env python3
"""GENESIS layer: DIVISION WITH A REMAINDER (genus 9).

    17 = 5 × 3 + 2.
    17 divided by 5 is 3 remainder 2.
    17 apples shared among 5 kids leaves 2 left over.
    17 разделить на 5 будет 3, остаток 2.

THE GLYPH AXIS JUDGES ITSELF. A remainder has no glyph of its own, so
the weld is written as the identity it actually is — «a = b × q + r» —
and `scripts/arith_court.py` verifies every one of them without being
told anything about remainders. A surface that cannot be checked is a
surface that can lie twice.

EVERY PAIR IS INEXACT BY CONSTRUCTION: the divisor never divides the
dividend, because a «remainder 0» show would teach that the genus and
plain division are the same thing. The fractions layer says the exact
case, and says it exactly.

TWO DIFFERENT PAIRS PER SURFACE at least, as holon's market requires:
a surface shown on one pair teaches the pair, not the surface.

The sharer of the sharing surface is an ANIMATE word and the shared
thing is not — «17 apples shared among 5 kids» is true of the world,
«17 kids shared among 5 apples» is grammatical and false, and no
census can see the difference (M-103).
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from gsm_items import ANIMATE, ITEMS  # noqa: E402
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

THINGS = [w for w in ITEMS if w not in ANIMATE]
SHARERS = sorted(ANIMATE)
# (dividend, divisor) — never exact, and each divisor twice over
PAIRS = [(17, 5), (23, 5), (14, 3), (20, 3), (19, 4), (26, 4),
         (13, 2), (21, 2), (34, 7), (30, 7), (29, 6), (38, 6),
         (25, 8), (39, 8), (28, 9), (40, 9)]
BARE = [
    "a remainder is what is left over.",
    "what is a remainder?",
    "остаток — это то, что не разделилось.",
    "что такое остаток?",
]


def pass_shows(pass_i):
    out = []
    for i, (a, b) in enumerate(PAIRS):
        q, r = divmod(a, b)
        assert r and a == b * q + r, (a, b)
        thing = THINGS[(pass_i * 5 + i * 3) % len(THINGS)]
        who = SHARERS[(pass_i * 3 + i) % len(SHARERS)]
        out.append(f"{a} = {b} × {q} + {r}.")
        out.append(f"{a} divided by {b} is {q} remainder {r}.")
        out.append(
            f"{a} {by_count(a, thing)} shared among {b} "
            f"{by_count(b, who)} leaves {r} left over."
        )
        out.append(
            f"{a} разделить на {b} будет {q}, остаток {r}."
        )
    for tpl in BARE:
        out.append(tpl)
    return out


def main():
    emit("datasets/genesis_remainders.txt", pass_shows)


if __name__ == "__main__":
    main()
