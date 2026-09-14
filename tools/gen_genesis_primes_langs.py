#!/usr/bin/env python3
"""GENESIS layer: PRIME AND COMPOSITE IN EIGHT LANGUAGES.

The owner's word: every language in surplus. The numbers world says «17 is
prime; its divisors are 1 and 17.», «15 is not prime; 15 = 3 × 5.» and asks
«is 17 prime? yes: …» in en/ru; this world says it in de/fr/es/it/pt/nl/pl/
tr — the verdict word opens the answer (М-147), the witness follows. The
house of prime phrases (tools/primeforms.py) holds the phrases; the court
reads the same table and finds the least divisor itself.

MASS FROM THE RULE (М-148): the numbers walk 2..99 with a stride coprime
with the range, so every pass shows other numbers; primes and composites
come as the walk brings them.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import primeforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_primes_langs.txt"


def pass_groups(шаг):
    return F.группы(шаг)


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
