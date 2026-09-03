#!/usr/bin/env python3
"""THE HOUSE OF REMAINDER PHRASES — division with a remainder in eight languages.

The remainders world says «17 divided by 5 is 3 remainder 2: 5 × 3 = 15,
17 − 15 = 2» and «17 разделить на 5 будет 3, остаток 2: …» in en/ru; this
house says the same in de/fr/es/it/pt/nl/pl/tr, statement and question
answered by the statement (М-153), the ledger of the division unchanged
(holon 03.09, ONE-CARRIER: the answer that is computed shows its steps).
Generator and court read one table through tools/phrases.py (М-159).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

ЯЗЫКИ = {
    "de": dict(утв="{a} geteilt durch {b} ist {q} Rest {r}: {л}.", воп="was ist {a} geteilt durch {b}?"),
    "fr": dict(утв="{a} divisé par {b} fait {q} reste {r} : {л}.", воп="combien font {a} divisé par {b} ?"),
    "es": dict(утв="{a} dividido entre {b} es {q} con resto {r}: {л}.", воп="¿cuánto es {a} dividido entre {b}?"),
    "it": dict(утв="{a} diviso {b} fa {q} con resto {r}: {л}.", воп="quanto fa {a} diviso {b}?"),
    "pt": dict(утв="{a} dividido por {b} é {q} com resto {r}: {л}.", воп="quanto é {a} dividido por {b}?"),
    "nl": dict(утв="{a} gedeeld door {b} is {q} rest {r}: {л}.", воп="wat is {a} gedeeld door {b}?"),
    "pl": dict(утв="{a} podzielone przez {b} to {q} reszta {r}: {л}.", воп="ile to {a} podzielone przez {b}?"),
    "tr": dict(утв="{a} bölü {b} eşittir {q} kalan {r}: {л}.", воп="{a} bölü {b} kaçtır?"),
}
ДЫРЫ = {"a": r"(\d+)", "b": r"(\d+)", "q": r"(\d+)", "r": r"(\d+)", "л": r"(\d+ × \d+ = \d+, \d+ − \d+ = \d+)"}


def леджер(a, b):
    q, r = divmod(a, b)
    return f"{b} × {q} = {b * q}, {a} − {b * q} = {r}"


def утверждение(язык, a, b):
    q, r = divmod(a, b)
    return ЯЗЫКИ[язык]["утв"].format(a=a, b=b, q=q, r=r, л=леджер(a, b))


def вопрос(язык, a, b):
    return f"{ЯЗЫКИ[язык]['воп'].format(a=a, b=b)} {утверждение(язык, a, b)}"


def образцы(язык):
    я = ЯЗЫКИ[язык]
    утв = phrases.образец(я["утв"], ДЫРЫ)
    return [(re.compile("^" + утв + "$"), False),
            (re.compile("^" + phrases.образец(я["воп"], ДЫРЫ) + " " + утв + "$"), True)]


def судить_группы(язык, спрошено, группы):
    я = ЯЗЫКИ[язык]
    г = list(группы)
    спрош = {}
    if спрошено:
        имена = phrases.порядок(я["воп"])
        спрош = dict(zip(имена, г[:len(имена)])); г = г[len(имена):]
    з = dict(zip(phrases.порядок(я["утв"]), г))
    a, b, q, r = int(з["a"]), int(з["b"]), int(з["q"]), int(з["r"])
    # THE REMAINDER IS NEVER ZERO IN THIS HOUSE (as in the remainders world:
    # a «remainder 0» show would teach that the genus and the quotient coincide)
    if b < 2 or r == 0 or divmod(a, b) != (q, r) or з["л"] != леджер(a, b):
        return False
    return all(int(спрош[имя]) == int(з[имя]) for имя in спрош)
