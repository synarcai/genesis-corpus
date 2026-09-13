#!/usr/bin/env python3
"""GENESIS layer: THE LADDER OF INQUIRY — how a question is answered.

A dialogue probe on the trained organism came back with twelve mute
mouths, and every one of them was a QUESTION: «is 91 a prime number?»,
«give a counterexample: all odd numbers are prime», «what is the sum of
the first 5 odd numbers?». The corpus already held the facts — primes,
factorisations, counterexamples — and held them as STATEMENTS. Nowhere
did it hold the ACT of deciding a case that had been ASKED.

THE LADDER. A researcher does not know a subject by its facts; a
researcher knows it by four rungs, and each rung is a different act:

    ОПРЕДЕЛЕНИЕ  — what the notion IS, said in words and not shown
    ИСПОЛНЕНИЕ   — a particular case DECIDED, with the ground beside
                   the verdict («no: 91 = 7 × 13»)
    КОНТРПРИМЕР  — a universal claim KILLED by one witness; the cheapest
                   proof there is, and the one a confirming corpus never
                   teaches
    ОБОБЩЕНИЕ    — the law that the cases were instances of

A corpus that shows only the second rung teaches arithmetic. A corpus
that shows all four teaches INQUIRY, and inquiry is what the owner asked
for: «выращиваем универсала-исследователя-математика».

ONE MECHANISM, SIX GENERA. The ladder is not written six times. It is a
form, and each genus DECLARES its four rungs as functions over the pass
number; the layer walks the same ladder for primality, divisibility, the
sum of odd numbers, the conditional, injectivity and the square. Adding
a genus costs a declaration and no machinery — which is the test that
the form is a form and not a template.

EVERY GROUND IS COMPUTED HERE AND RE-COMPUTED BY THE COURT. The verdict
«no: 91 = 7 × 13» is not written; it is factorised, and
`courts/inquiry_court.py` factorises again rather than believing the
line. A counterexample is not trusted either: the court checks that the
witness REALLY refutes the claim, because a counterexample that does not
refute is the most convincing lie a corpus can carry.

BOTH TONGUES, ONE FACT. English and Russian say the same thing and are
judged by the same computation, so a defect in one surface cannot hide
behind the other.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import inquiryforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_inquiry.txt"


def main():
    emit_grouped(ЦЕЛЬ, F.группы)


if __name__ == "__main__":
    main()
