#!/usr/bin/env python3
"""THE HOUSE OF SHARE NAMES — «two thirds of 12» in eight languages.

The share world says «two thirds of 12 is 8: 12 divided by 3 is 4, and 4
times 2 is 8» and «две трети от 12 — это 8» in en/ru. This house names the
shares (the half, a third, two thirds, a quarter, three quarters, a fifth,
two fifths) in de/fr/es/it/pt/nl/pl/tr, with the copula the numerator
demands («ein Drittel … ist», «zwei Drittel … sind»; «est/font»,
«es/son», «è/sono», «é/são»), and the two phrases — the statement with its
ledger and the question answered by it (М-153). The share is read back from
its name, never from the line; the ledger writes the division and, at a
numerator above one, the multiplication — no action that changes nothing.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

ДОЛИ = ((1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5))
ИМЕНА = {
    "de": ("die Hälfte", "ein Drittel", "zwei Drittel", "ein Viertel", "drei Viertel", "ein Fünftel", "zwei Fünftel"),
    "fr": ("la moitié", "un tiers", "deux tiers", "un quart", "trois quarts", "un cinquième", "deux cinquièmes"),
    "es": ("la mitad", "un tercio", "dos tercios", "un cuarto", "tres cuartos", "un quinto", "dos quintos"),
    "it": ("la metà", "un terzo", "due terzi", "un quarto", "tre quarti", "un quinto", "due quinti"),
    "pt": ("a metade", "um terço", "dois terços", "um quarto", "três quartos", "um quinto", "dois quintos"),
    "nl": ("de helft", "een derde", "twee derde", "een kwart", "driekwart", "een vijfde", "twee vijfde"),
    "pl": ("połowa", "jedna trzecia", "dwie trzecie", "jedna czwarta", "trzy czwarte", "jedna piąta", "dwie piąte"),
    "tr": ("yarısı", "üçte biri", "üçte ikisi", "dörtte biri", "dörtte üçü", "beşte biri", "beşte ikisi"),
}
# the phrases: {и} the share name, {n} the number, {в} the value, {л} the
# ledger, {с} the copula by the numerator (one, many), {в_с} the question's
ЯЗЫКИ = {
    "de": dict(с=("ist", "sind"), вс=("was ist", "was sind"), утв="{и} von {n} {с} {в}: {л}.", воп="{вс} {и} von {n}?"),
    "fr": dict(с=("est", "font"), вс=("combien vaut", "combien valent"), утв="{и} de {n} {с} {в} : {л}.", воп="{вс} {и} de {n} ?"),
    "es": dict(с=("es", "son"), вс=("¿cuánto es", "¿cuánto son"), утв="{и} de {n} {с} {в}: {л}.", воп="{вс} {и} de {n}?"),
    "it": dict(с=("è", "sono"), вс=("quanto fa", "quanto fanno"), утв="{и} di {n} {с} {в}: {л}.", воп="{вс} {и} di {n}?"),
    "pt": dict(с=("é", "são"), вс=("quanto é", "quanto são"), утв="{и} de {n} {с} {в}: {л}.", воп="{вс} {и} de {n}?"),
    "nl": dict(с=("is", "is"), вс=("wat is", "wat is"), утв="{и} van {n} {с} {в}: {л}.", воп="{вс} {и} van {n}?"),
    "pl": dict(с=("to", "to"), вс=("ile to", "ile to"), утв="{и} z {n} {с} {в}: {л}.", воп="{вс} {и} z {n}?"),
    "tr": dict(с=("", ""), вс=("", ""), утв="{n} sayısının {и}: {л}.", воп="{n} sayısının {и} kaçtır?"),
}


def доля(язык, имя):
    return ДОЛИ[ИМЕНА[язык].index(имя)]


def леджер(ч, з, n):
    q = n // з
    return f"{n} ÷ {з} = {q}" if ч == 1 else f"{n} ÷ {з} = {q}, {q} × {ч} = {q * ч}"


def утверждение(язык, k, n):
    ч, з = ДОЛИ[k]
    assert n % з == 0
    я = ЯЗЫКИ[язык]
    return я["утв"].format(и=ИМЕНА[язык][k], n=n, с=я["с"][0 if ч == 1 else 1], в=n // з * ч, л=леджер(ч, з, n))


def вопрос(язык, k, n):
    ч, _ = ДОЛИ[k]
    я = ЯЗЫКИ[язык]
    return f"{я['воп'].format(вс=я['вс'][0 if ч == 1 else 1], и=ИМЕНА[язык][k], n=n)} {утверждение(язык, k, n)}"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    return {"и": alt(ИМЕНА[язык]), "n": r"(\d+)", "в": r"(\d+)", "с": alt(я["с"]), "вс": alt(я["вс"]),
            "л": r"(\d+ ÷ \d+ = \d+(?:, \d+ × \d+ = \d+)?)"}


def образцы(язык):
    я = ЯЗЫКИ[язык]
    д = _дыры(язык)
    утв = phrases.образец(я["утв"], д)
    return [(re.compile("^" + утв + "$"), False),
            (re.compile("^" + phrases.образец(я["воп"], д) + " " + утв + "$"), True)]


def судить_группы(язык, спрошено, группы):
    я = ЯЗЫКИ[язык]
    г = list(группы)
    спрош = {}
    if спрошено:
        имена = phrases.порядок(я["воп"])
        спрош = dict(zip(имена, г[:len(имена)])); г = г[len(имена):]
    з = dict(zip(phrases.порядок(я["утв"]), г))
    ч, зн = доля(язык, з["и"])
    n = int(з["n"])
    if n % зн or з["л"] != леджер(ч, зн, n):
        return False
    if "в" in з and int(з["в"]) != n // зн * ч:
        return False
    if "с" in з and з["с"] != я["с"][0 if ч == 1 else 1]:
        return False
    if спрош and (спрош.get("и") != з["и"] or int(спрош.get("n", n)) != n or спрош.get("вс", "") != (я["вс"][0 if ч == 1 else 1] if "вс" in спрош else "")):
        return False
    return True
