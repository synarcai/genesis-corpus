#!/usr/bin/env python3
"""GENESIS layer: THE VALUE ASKED IN EIGHT LANGUAGES.

The owner's word (03.09): every language in surplus. The svod asked the
value of an expression in English and Russian only («what is 3 + 4?»,
«сколько будет 3 + 4?»); in de/fr/es/it/pl/pt/nl/tr the question of value
had no shows at all (34 lines, one Italian world). This world asks it with
the forms the packs declare (ask_forms.value: the question in two forms and
the task form — «was ist {}?», «wie viel ist {}?», «berechne {}.»; Turkish
puts the question word at the end: «{} kaç eder?») over the four operations,
and the answer is the one telling the corpus has for a value: the equation
«3 + 4 = 7.», recomputed by the court of arithmetic; the house of the pair
binds the question to the answer by the form of value (М-156), so a changed
number in the question is caught.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import paraphrase  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_arith_langs.txt"
ЯЗЫКИ = ("de", "fr", "es", "it", "pl", "pt", "nl", "tr")
ШИРИНА = 16


def выражение(шаг, i):
    """(expression, value) — the four operations in turn, exact division."""
    a = 3 + (шаг * 7 + i * 5) % 40
    b = 2 + (шаг * 3 + i * 11) % 12
    оп = (шаг + i) % 4
    if оп == 0:
        return f"{a} + {b}", a + b
    if оп == 1:
        a, b = max(a, b), min(a, b)
        return f"{a} − {b}", a - b
    if оп == 2:
        return f"{a} × {b}", a * b
    q = 2 + (шаг * 5 + i) % 9
    return f"{b * q} ÷ {b}", q


def язык_группа(шаг, язык):
    формы = paraphrase.формы(язык, "value")
    вон = []
    for i in range(ШИРИНА):
        в, з = выражение(шаг, i)
        форма = формы[(шаг + i) % len(формы)]
        вон.append(f"{форма.format(в)} {в} = {з}.")
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
