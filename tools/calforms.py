#!/usr/bin/env python3
"""THE HOUSE OF WEEKDAY PHRASES — «k days after X comes Y» in eight languages.

The calendar world says «3 days after tuesday comes friday» and «через 3
дня после понедельника наступает четверг» in en/ru — the shows from which
the organism buys the weekly cycle without names and without the seven.
This house names the days in de/fr/es/it/pt/nl/pl/tr with the oblique form
the phrase needs (Polish locative after «po», Turkish ablative «-dan»,
Spanish «del» + the article) and the count form of «day», and the two
phrases — the statement and the question answered by it (М-153). Generator
and court read one table; the court counts the cycle itself.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# per language: days (nominative), oblique days where the phrase bends them,
# the count forms of «day» (one, many), the statement and the question
ЯЗЫКИ = {
    "de": dict(дни=("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"),
               день=("Tag", "Tage"), утв="{n} {д} nach {X} kommt {Y}.", воп="welcher Tag kommt {n} {д} nach {X}?"),
    "fr": dict(дни=("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"),
               день=("jour", "jours"), утв="{n} {д} après {X} vient {Y}.", воп="quel jour vient {n} {д} après {X} ?"),
    "es": dict(дни=("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"),
               день=("día", "días"), утв="{n} {д} después del {X} viene el {Y}.", воп="¿qué día viene {n} {д} después del {X}?"),
    "it": dict(дни=("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"),
               день=("giorno", "giorni"), утв="{n} {д} dopo {X} viene {Y}.", воп="che giorno viene {n} {д} dopo {X}?"),
    "pt": dict(дни=("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"),
               день=("dia", "dias"), утв="{n} {д} depois de {X} vem {Y}.", воп="que dia vem {n} {д} depois de {X}?"),
    "nl": dict(дни=("maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"),
               день=("dag", "dagen"), утв="{n} {д} na {X} komt {Y}.", воп="welke dag komt {n} {д} na {X}?"),
    "pl": dict(дни=("poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"),
               косв=("poniedziałku", "wtorku", "środzie", "czwartku", "piątku", "sobocie", "niedzieli"),
               день=("dzień", "dni"), утв="{n} {д} po {X} przypada {Y}.", воп="jaki dzień przypada {n} {д} po {X}?"),
    "tr": dict(дни=("pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"),
               косв=("pazartesiden", "salıdan", "çarşambadan", "perşembeden", "cumadan", "cumartesinden", "pazardan"),
               день=("gün", "gün"), утв="{X} {n} {д} sonra {Y} gelir.", воп="{X} {n} {д} sonra hangi gün gelir?"),
}


def _косв(язык, i):
    я = ЯЗЫКИ[язык]
    return я.get("косв", я["дни"])[i]


def _день(язык, n):
    ф = ЯЗЫКИ[язык]["день"]
    return ф[0] if n == 1 else ф[1]


def утверждение(язык, i, n):
    я = ЯЗЫКИ[язык]
    return я["утв"].format(n=n, д=_день(язык, n), X=_косв(язык, i), Y=я["дни"][(i + n) % 7])


def вопрос(язык, i, n):
    я = ЯЗЫКИ[язык]
    return f"{я['воп'].format(n=n, д=_день(язык, n), X=_косв(язык, i))} {утверждение(язык, i, n)}"


def _образец(язык, шаблон):
    я = ЯЗЫКИ[язык]
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    дыры = {"n": r"(\d+)", "д": alt(я["день"]), "X": alt(я.get("косв", я["дни"])), "Y": alt(я["дни"])}
    return phrases.образец(шаблон, дыры)


def образцы(язык):
    я = ЯЗЫКИ[язык]
    утв = _образец(язык, я["утв"])
    return [(re.compile("^" + утв + "$"), False),
            (re.compile("^" + _образец(язык, я["воп"]) + " " + утв + "$"), True)]


def судить_группы(язык, спрошено, группы):
    я = ЯЗЫКИ[язык]
    порядок = phrases.порядок(я["утв"])
    г = list(группы)
    if спрошено:
        в_порядок = phrases.порядок(я["воп"])
        спрош = dict(zip(в_порядок, г[:len(в_порядок)])); г = г[len(в_порядок):]
    else:
        спрош = {}
    з = dict(zip(порядок, г))
    n = int(з["n"])
    if not 1 <= n <= 6 or з["д"] != _день(язык, n):
        return False
    косв = я.get("косв", я["дни"])
    i = косв.index(з["X"])
    if я["дни"][(i + n) % 7] != з["Y"]:
        return False
    if спрош and (int(спрош["n"]) != n or спрош["X"] != з["X"] or спрош["д"] != з["д"]):
        return False
    return True
