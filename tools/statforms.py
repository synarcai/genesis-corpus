#!/usr/bin/env python3
"""THE HOUSE OF SUMMARY PHRASES — the mean and the percent in eight languages.

The average world says «the average of 10, 14, 15 is 13: 10 + 14 + 15 = 39,
39 ÷ 3 = 13» and the percent world «2% of 50 is 1» in English and Russian.
This house says the two facts in de/fr/es/it/pt/nl/pl/tr — statement and
question answered by the statement (М-153) — with a ledger the court
recomputes: the mean as the sum and the division, the percent as the
product and the division by 100. Generator and court read one table.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# {р} — the list «10, 14, 15»; {с} — the mean; {л} — the ledger;
# {p} — the percent, {n} — the number, {в} — the value
ЯЗЫКИ = {
    "de": dict(ср="der Durchschnitt von {р} ist {с}: {л}.", в_ср="was ist der Durchschnitt von {р}?",
               пр="{p} % von {n} sind {в}: {л}.", в_пр="was sind {p} % von {n}?"),
    "fr": dict(ср="la moyenne de {р} est {с} : {л}.", в_ср="quelle est la moyenne de {р} ?",
               пр="{p} % de {n} font {в} : {л}.", в_пр="combien font {p} % de {n} ?"),
    "es": dict(ср="el promedio de {р} es {с}: {л}.", в_ср="¿cuál es el promedio de {р}?",
               пр="el {p} % de {n} es {в}: {л}.", в_пр="¿cuánto es el {p} % de {n}?"),
    "it": dict(ср="la media di {р} è {с}: {л}.", в_ср="qual è la media di {р}?",
               пр="il {p} % di {n} è {в}: {л}.", в_пр="quanto fa il {p} % di {n}?"),
    "pt": dict(ср="a média de {р} é {с}: {л}.", в_ср="qual é a média de {р}?",
               пр="{p} % de {n} é {в}: {л}.", в_пр="quanto é {p} % de {n}?"),
    "nl": dict(ср="het gemiddelde van {р} is {с}: {л}.", в_ср="wat is het gemiddelde van {р}?",
               пр="{p} % van {n} is {в}: {л}.", в_пр="hoeveel is {p} % van {n}?"),
    "pl": dict(ср="średnia z {р} to {с}: {л}.", в_ср="ile wynosi średnia z {р}?",
               пр="{p} % z {n} to {в}: {л}.", в_пр="ile to {p} % z {n}?"),
    "tr": dict(ср="{р} sayılarının ortalaması: {л}.", в_ср="{р} sayılarının ortalaması kaçtır?",
               пр="{n} sayısının yüzde {p} kısmı: {л}.", в_пр="{n} sayısının yüzde {p} kısmı kaçtır?"),
}


def леджер_среднего(ряд):
    s = sum(ряд)
    return f"{' + '.join(map(str, ряд))} = {s}, {s} ÷ {len(ряд)} = {s // len(ряд)}"


def леджер_процента(p, n):
    return f"{n} × {p} = {n * p}, {n * p} ÷ 100 = {n * p // 100}"


def среднее(язык, ряд):
    assert sum(ряд) % len(ряд) == 0
    я = ЯЗЫКИ[язык]
    return я["ср"].format(р=", ".join(map(str, ряд)), с=sum(ряд) // len(ряд), л=леджер_среднего(ряд))


def вопрос_среднего(язык, ряд):
    return f"{ЯЗЫКИ[язык]['в_ср'].format(р=', '.join(map(str, ряд)))} {среднее(язык, ряд)}"


def процент(язык, p, n):
    assert (n * p) % 100 == 0
    я = ЯЗЫКИ[язык]
    return я["пр"].format(p=p, n=n, в=n * p // 100, л=леджер_процента(p, n))


def вопрос_процента(язык, p, n):
    return f"{ЯЗЫКИ[язык]['в_пр'].format(p=p, n=n)} {процент(язык, p, n)}"


_РЯД = r"(\d+(?:, \d+)+)"
_ЛЕДЖЕР_СР = r"((?:\d+ \+ )+\d+ = \d+, \d+ ÷ \d+ = \d+)"
_ЛЕДЖЕР_ПР = r"(\d+ × \d+ = \d+, \d+ ÷ 100 = \d+)"


def _образец(шаблон, л):
    дыры = {"р": _РЯД, "с": r"(\d+)", "л": л, "p": r"(\d+)", "n": r"(\d+)", "в": r"(\d+)"}
    return phrases.образец(шаблон, дыры)


def образцы(язык):
    """[(regex, kind, asked)] — kinds «ср» and «пр»."""
    я = ЯЗЫКИ[язык]
    ср, пр = _образец(я["ср"], _ЛЕДЖЕР_СР), _образец(я["пр"], _ЛЕДЖЕР_ПР)
    return [(re.compile("^" + ср + "$"), "ср", False),
            (re.compile("^" + _образец(я["в_ср"], "") + " " + ср + "$"), "ср", True),
            (re.compile("^" + пр + "$"), "пр", False),
            (re.compile("^" + _образец(я["в_пр"], "") + " " + пр + "$"), "пр", True)]


def судить_группы(язык, вид, спрошено, группы):
    """Groups follow the template's hole order; the tr statement has no {с}/{в}."""
    я = ЯЗЫКИ[язык]
    шаблон = я[вид]
    порядок = phrases.порядок(шаблон)
    г = list(группы)
    if спрошено:
        в_порядок = phrases.порядок(я["в_" + вид])
        спрош = dict(zip(в_порядок, г[:len(в_порядок)])); г = г[len(в_порядок):]
    else:
        спрош = {}
    з = dict(zip(порядок, г))
    if вид == "ср":
        ряд = [int(x) for x in з["р"].split(", ")]
        if sum(ряд) % len(ряд):
            return False
        if з["л"] != леджер_среднего(ряд):
            return False
        if "с" in з and int(з["с"]) != sum(ряд) // len(ряд):
            return False
        return not спрош or спрош.get("р") == з["р"]
    p, n = int(з["p"]), int(з["n"])
    if (n * p) % 100 or з["л"] != леджер_процента(p, n):
        return False
    if "в" in з and int(з["в"]) != n * p // 100:
        return False
    return not спрош or (int(спрош.get("p", p)) == p and int(спрош.get("n", n)) == n)
