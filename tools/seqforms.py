#!/usr/bin/env python3
"""THE HOUSE OF PROGRESSION PHRASES — the k-th term in eight languages.

The sequences world says «term number 5 of the progression from 9 with
step 4 is 25: 5 − 1 = 4, 4 × 4 = 16, 9 + 16 = 25» in en/ru; this house says
the same in de/fr/es/it/pt/nl/pl/tr, statement and question answered by
the statement (М-153), the ledger unchanged. Generator and court read one
table through tools/phrases.py.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

ЯЗЫКИ = {
    "de": dict(утв="das Glied Nummer {k} der Folge ab {a} mit Schritt {d} ist {v}: {л}.", воп="was ist das Glied Nummer {k} der Folge ab {a} mit Schritt {d}?"),
    "fr": dict(утв="le terme numéro {k} de la progression partant de {a} avec le pas {d} est {v} : {л}.", воп="quel est le terme numéro {k} de la progression partant de {a} avec le pas {d} ?"),
    "es": dict(утв="el término número {k} de la progresión desde {a} con paso {d} es {v}: {л}.", воп="¿cuál es el término número {k} de la progresión desde {a} con paso {d}?"),
    "it": dict(утв="il termine numero {k} della progressione da {a} con passo {d} è {v}: {л}.", воп="qual è il termine numero {k} della progressione da {a} con passo {d}?"),
    "pt": dict(утв="o termo número {k} da progressão desde {a} com passo {d} é {v}: {л}.", воп="qual é o termo número {k} da progressão desde {a} com passo {d}?"),
    "nl": dict(утв="term nummer {k} van de rij vanaf {a} met stap {d} is {v}: {л}.", воп="wat is term nummer {k} van de rij vanaf {a} met stap {d}?"),
    "pl": dict(утв="wyraz numer {k} ciągu od {a} o kroku {d} to {v}: {л}.", воп="ile wynosi wyraz numer {k} ciągu od {a} o kroku {d}?"),
    "tr": dict(утв="{a} ile başlayan ve adımı {d} olan dizinin {k} numaralı terimi: {л}.", воп="{a} ile başlayan ve adımı {d} olan dizinin {k} numaralı terimi kaçtır?"),
}
ДЫРЫ = {"k": r"(\d+)", "a": r"(\d+)", "d": r"(\d+)", "v": r"(\d+)", "л": r"(\d+ − 1 = \d+, \d+ × \d+ = \d+, \d+ \+ \d+ = \d+)"}


def леджер(k, a, d):
    return f"{k} − 1 = {k - 1}, {k - 1} × {d} = {(k - 1) * d}, {a} + {(k - 1) * d} = {a + (k - 1) * d}"


def утверждение(язык, k, a, d):
    return ЯЗЫКИ[язык]["утв"].format(k=k, a=a, d=d, v=a + (k - 1) * d, л=леджер(k, a, d))


def вопрос(язык, k, a, d):
    return f"{ЯЗЫКИ[язык]['воп'].format(k=k, a=a, d=d)} {утверждение(язык, k, a, d)}"


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
    k, a, d = int(з["k"]), int(з["a"]), int(з["d"])
    if k < 2 or з["л"] != леджер(k, a, d):
        return False
    if "v" in з and int(з["v"]) != a + (k - 1) * d:
        return False
    return all(int(спрош[имя]) == int(з[имя]) for имя in спрош)
