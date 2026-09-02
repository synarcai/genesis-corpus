"""COPRIMALITY AS A VERDICT FRAME IN EIGHT LANGUAGES (holon 04.09: the market
of universals needs the predicate «teilerfremd / premiers entre eux / …» for
the executor of coprimality; the copula «sind/zijn» is bought from it).

«sind 4 und 9 teilerfremd? ja: der ggT von 4 und 9 ist 1.» — the verdict
word opens the answer (М-147), the witness is the greatest common divisor,
which the court recomputes. One table per language: the question form (two
holes), the two words, the witness form (three holes: a, b, gcd).
"""
import re
from math import gcd

ФОРМЫ = {
    "de": ("sind {} und {} teilerfremd?", "ja", "nein", "der ggT von {} und {} ist {}"),
    "fr": ("est-ce que {} et {} sont premiers entre eux ?", "oui", "non", "le pgcd de {} et {} est {}"),
    "es": ("¿son {} y {} primos entre sí?", "sí", "no", "el mcd de {} y {} es {}"),
    "it": ("sono {} e {} coprimi?", "sì", "no", "il mcd di {} e {} è {}"),
    "pl": ("czy {} i {} są względnie pierwsze?", "tak", "nie", "nwd {} i {} to {}"),
    "tr": ("{} ve {} aralarında asal mıdır?", "evet", "hayır", "{} ve {} sayılarının ebob'u {}"),
    "pt": ("são {} e {} primos entre si?", "sim", "não", "o mdc de {} e {} é {}"),
    "nl": ("zijn {} en {} onderling ondeelbaar?", "ja", "nee", "de ggd van {} en {} is {}"),
}
# the French colon carries a space before it (the writing of the language)
ДВОЕТОЧИЕ = {"fr": " : "}
# pairs alternate coprime / not coprime from the first show (М-148)
ПАРЫ = [(4, 9), (6, 9), (8, 15), (6, 8), (7, 12), (10, 15), (9, 16), (12, 18), (5, 14), (14, 21),
        (11, 20), (15, 25), (13, 21), (16, 24), (17, 30), (18, 27), (19, 22), (20, 35), (21, 32), (22, 33)]


def показ(язык, a, b):
    вопрос, да, нет, свидетель = ФОРМЫ[язык]
    d = gcd(a, b)
    return f"{вопрос.format(a, b)} {да if d == 1 else нет}{ДВОЕТОЧИЕ.get(язык, ': ')}{свидетель.format(a, b, d)}."


def показы(языки, шаг, сколько=12):
    вон = []
    for i in range(сколько):
        a, b = ПАРЫ[(шаг * 7 + i) % len(ПАРЫ)]
        for язык in языки:
            if язык in ФОРМЫ:
                вон.append(показ(язык, a, b))
    return вон


def _чисто(текст):
    return re.escape(текст).replace("\\ ", " ").replace("\\-", "-").replace("\\'", "'")


def _судья(да):
    def судить(м):
        # groups: the question's a, b; the word; the witness's a, b, gcd
        a, b, слово, a2, b2, d = int(м.group(1)), int(м.group(2)), м.group(3), int(м.group(4)), int(м.group(5)), int(м.group(6))
        return (a2, b2) == (a, b) and d == gcd(a, b) and (слово == да) == (d == 1)
    судить.__name__ = "_взаимно_просты"
    return судить


def образцы(языки):
    """[(pattern, judge)] — the coprimality frame per language."""
    вон = []
    for язык in языки:
        if язык not in ФОРМЫ:
            continue
        вопрос, да, нет, свидетель = ФОРМЫ[язык]
        воп = r"(\d+)".join(_чисто(ч) for ч in вопрос.split("{}"))
        свид = r"(\d+)".join(_чисто(ч) for ч in свидетель.split("{}"))
        двоеточие = _чисто(ДВОЕТОЧИЕ.get(язык, ": "))
        вон.append((rf"^{воп} ({да}|{нет}){двоеточие}{свид}\.$", _судья(да)))
    return вон
