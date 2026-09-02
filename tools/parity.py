"""PARITY AS A CHOICE QUESTION IN EVERY LANGUAGE (holon 03.09: the market of
universals needs a verdict predicate «even/odd» per language).

«is 20 even or odd? even: 20 = 2 × 10.» — the chosen alternative opens the
answer (М-147 for a choice question), the witness is the division by two.
One table names, per language, the question form (a hole for the number)
and the two words; the generators of the two-language worlds and their
courts read the same table.
"""
import re

ФОРМЫ = {
    "de": ("ist {} gerade oder ungerade?", "gerade", "ungerade"),
    "fr": ("est-ce que {} est pair ou impair ?", "pair", "impair"),
    "es": ("¿es {} par o impar?", "par", "impar"),
    "it": ("{} è pari o dispari?", "pari", "dispari"),
    "pl": ("czy {} jest parzyste, czy nieparzyste?", "parzyste", "nieparzyste"),
    "tr": ("{} çift mi tek mi?", "çift", "tek"),
    "pt": ("{} é par ou ímpar?", "par", "ímpar"),
    "nl": ("is {} even of oneven?", "even", "oneven"),
}


def показ(язык, n):
    вопрос, чёт, нечёт = ФОРМЫ[язык]
    if n % 2 == 0:
        return f"{вопрос.format(n)} {чёт}: {n} = 2 × {n // 2}."
    return f"{вопрос.format(n)} {нечёт}: {n} = 2 × {n // 2} + 1."


def показы(языки, шаг, сколько=12):
    """Both parities by mass, odd composites among the odd (М-148): 9, 15,
    21, 25 … alternate with primes and evens from the first show."""
    ряд = [9, 20, 15, 12, 21, 7, 25, 18, 27, 11, 33, 14, 35, 13, 39, 16, 45, 22, 49, 17]
    вон = []
    for i in range(сколько):
        n = ряд[(шаг * 5 + i) % len(ряд)]
        for язык in языки:
            if язык in ФОРМЫ:
                вон.append(показ(язык, n))
    return вон


def _судья(чёт, нечёт):
    def судить(м):
        слово, n, q, хвост = м.group(1), int(м.group(2)), int(м.group(3)), м.group(4)
        чётное = слово == чёт
        return (n == 2 * q + (0 if чётное else 1)) and (хвост is None) == чётное
    судить.__name__ = "_чётность"
    return судить


def образцы(языки):
    """[(pattern, judge)] — the choice frame of parity per language."""
    вон = []
    for язык in языки:
        if язык not in ФОРМЫ:
            continue
        вопрос, чёт, нечёт = ФОРМЫ[язык]
        части = вопрос.split("{}")
        # the hole of the question is matched but not captured: the judge's
        # groups are (word, n, q, tail)
        воп = r"\d+".join(re.escape(ч).replace("\\ ", " ").replace("\\-", "-").replace("\\'", "'") for ч in части)
        вон.append((rf"^{воп} ({чёт}|{нечёт}): (\d+) = 2 × (\d+)( \+ 1)?\.$", _судья(чёт, нечёт)))
    return вон
