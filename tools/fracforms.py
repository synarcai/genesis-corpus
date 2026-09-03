#!/usr/bin/env python3
"""THE HOUSE OF SHARE AND PERCENT PHRASES — a part of a quantity, in three languages.

holon's word for genus 2 of g1 (03.09, G1-ATTACK «shares and percents over
quantities»): five forms, every ledger a chain of primitives (÷, ×, −)
that stays WHOLE on the axis, ≥ 10 shows per form and language, en/ru/de:

  1. «what is two thirds of 24? two thirds of 24 is 16: 24 ÷ 3 = 8, 8 × 2 = 16.»
     — the denominators 2..10 in words (half, third, quarter, fifth …), the
     numerator in words; ONE frame for every word of the fraction, so that
     the answer never differs between thirds and quarters;
  2. «what is 40 percent of 220? 40 percent of 220 is 88: 220 × 40 = 8800,
     8800 ÷ 100 = 88.» — whole on the axis, the hundred divided last;
  3. «three quarters of the pupils have a pen; 20 do not. how many pupils are
     there? 20 is one quarter of 80: 4 − 3 = 1, 20 ÷ 1 = 20, 20 × 4 = 80.» —
     the share of those without is denominator − numerator; one share is
     found, the whole is shares × denominator (one frame, three steps);
  4. «a third of a number is 12. what is the number? 12 is a third of 36:
     12 × 3 = 36.» (and «two thirds of a number is 16 … 16 ÷ 2 = 8, 8 × 3 = 24»);
  5. «12 is 40 percent of what number? 12 is 40 percent of 30: 12 × 100 =
     1200, 1200 ÷ 40 = 30.»

Generator and court read one table through tools/phrases.py (М-159); the
court reads the fraction words back to their numbers and recomputes.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# per language: the numerator words (1..9), the denominator words (den →
# (one share, several shares)), the phrase of a share, the templates
ЯЗЫКИ = {
    "en": dict(
        числ={1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"},
        знам={2: ("half", "halves"), 3: ("third", "thirds"), 4: ("quarter", "quarters"), 5: ("fifth", "fifths"), 6: ("sixth", "sixths"),
              7: ("seventh", "sevenths"), 8: ("eighth", "eighths"), 9: ("ninth", "ninths"), 10: ("tenth", "tenths")},
        доля_утв="{Ч} of {N} is {r}: {л}.", доля_воп="what is {Ч} of {N}?",
        проц_утв="{p} percent of {N} is {r}: {л}.", проц_воп="what is {p} percent of {N}?",
        дополн="{Ч} of the {В} have a pen; {m} do not. how many {В} are there? {m} is {Ч2} of {N}: {л}.",
        вещи=("pupils", "students", "children", "workers", "players"),
        число_утв="{Ч} of a number is {r}. what is the number? {r} is {Ч} of {N}: {л}.",
        проц_обр="{r} is {p} percent of what number? {r} is {p} percent of {N}: {л}.",
        связка=("is", "is"),
    ),
    "ru": dict(
        числ={1: "одна", 2: "две", 3: "три", 4: "четыре", 5: "пять", 6: "шесть", 7: "семь", 8: "восемь", 9: "девять"},
        знам={2: ("половина", "вторых"), 3: ("треть", "трети"), 4: ("четверть", "четверти"), 5: ("пятая часть", "пятых"), 6: ("шестая часть", "шестых"),
              7: ("седьмая часть", "седьмых"), 8: ("восьмая часть", "восьмых"), 9: ("девятая часть", "девятых"), 10: ("десятая часть", "десятых")},
        доля_утв="{Ч} от {N} — это {r}: {л}.", доля_воп="сколько будет {Ч} от {N}?",
        проц_утв="{p} процентов от {N} — это {r}: {л}.", проц_воп="сколько будет {p} процентов от {N}?",
        дополн="{Ч} {В} имеют ручку; {m} не имеют. сколько всего {В}? {m} — это {Ч2} от {N}: {л}.",
        вещи=("учеников", "студентов", "детей", "рабочих", "игроков"),
        число_утв="{Ч} числа {С} {r}. какое это число? {r} — это {Ч} от {N}: {л}.",
        проц_обр="{r} — это {p} процентов какого числа? {r} — это {p} процентов от {N}: {л}.",
        # THE RUSSIAN COPULA AGREES WITH THE NUMERATOR: «треть числа равна 12»,
        # «две трети числа равны 16»
        связка=("равна", "равны"),
    ),
    "de": dict(
        числ={1: "ein", 2: "zwei", 3: "drei", 4: "vier", 5: "fünf", 6: "sechs", 7: "sieben", 8: "acht", 9: "neun"},
        # THE GERMAN SHARE TAKES ITS ARTICLE («ein Drittel», «die Hälfte»); the
        # plural share drops it («zwei Drittel»)
        знам={2: ("die Hälfte", "Hälften"), 3: ("ein Drittel", "Drittel"), 4: ("ein Viertel", "Viertel"), 5: ("ein Fünftel", "Fünftel"), 6: ("ein Sechstel", "Sechstel"),
              7: ("ein Siebtel", "Siebtel"), 8: ("ein Achtel", "Achtel"), 9: ("ein Neuntel", "Neuntel"), 10: ("ein Zehntel", "Zehntel")},
        доля_утв="{Ч} von {N} {С} {r}: {л}.", доля_воп="was {С} {Ч} von {N}?",
        проц_утв="{p} Prozent von {N} sind {r}: {л}.", проц_воп="was sind {p} Prozent von {N}?",
        дополн="{Ч} der {В} haben einen Stift; {m} haben keinen. wie viele {В} gibt es? {m} {С2} {Ч2} von {N}: {л}.",
        вещи=("Schüler", "Studenten", "Kinder", "Arbeiter", "Spieler"),
        число_утв="{Ч} einer Zahl {С} {r}. welche Zahl ist es? {r} {С} {Ч} von {N}: {л}.",
        проц_обр="{r} sind {p} Prozent welcher Zahl? {r} sind {p} Prozent von {N}: {л}.",
        связка=("ist", "sind"),
    ),
}
ФОРМЫ = ("доля", "проц", "дополн", "число", "проц_обр")
ПРОЦЕНТЫ = (10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90)


def доля_слово(язык, n, d):
    """«two thirds», «one quarter», «half»; «две трети», «пятая часть»; «zwei Drittel», «die Hälfte»."""
    я = ЯЗЫКИ[язык]
    один, много = я["знам"][d]
    if n == 1:
        return один if (язык != "en" or d == 2) else f"one {один}"
    return f"{я['числ'][n]} {много}"


def _связка(язык, n):
    я = ЯЗЫКИ[язык]
    return я["связка"][0] if n == 1 else я["связка"][1]


def _все_доли():
    вон = []
    for d in range(2, 11):
        for n in range(1, d):
            if d == 2 and n > 1:
                continue
            вон.append((n, d))
    return вон


ДОЛИ = _все_доли()


def страница(язык, форма, **п):
    я = ЯЗЫКИ[язык]
    if форма == "доля":
        n, d, q = п["n"], п["d"], п["q"]           # N = q·d, r = q·n
        N, r = q * d, q * n
        л = f"{N} ÷ {d} = {q}" + (f", {q} × {n} = {r}" if n > 1 else "")
        утв = я["доля_утв"].format(Ч=доля_слово(язык, n, d), N=N, r=r, л=л, С=_связка(язык, n))
        return f"{я['доля_воп'].format(Ч=доля_слово(язык, n, d), N=N, С=_связка(язык, n))} {утв}" if п.get("вопрос") else утв
    if форма == "проц":
        p, N = п["p"], п["N"]                      # N·p divisible by 100
        r = N * p // 100
        л = f"{N} × {p} = {N * p}, {N * p} ÷ 100 = {r}"
        утв = я["проц_утв"].format(p=p, N=N, r=r, л=л)
        return f"{я['проц_воп'].format(p=p, N=N)} {утв}" if п.get("вопрос") else утв
    if форма == "дополн":
        n, d, q = п["n"], п["d"], п["q"]           # q per share; without = q·(d − n); total = q·d
        m, N = q * (d - n), q * d
        л = f"{d} − {n} = {d - n}, {m} ÷ {d - n} = {q}, {q} × {d} = {N}"
        return я["дополн"].format(Ч=доля_слово(язык, n, d), В=я["вещи"][п["вещь"]], m=m, Ч2=доля_слово(язык, d - n, d), N=N, л=л, С2=_связка(язык, d - n))
    if форма == "число":
        n, d, q = п["n"], п["d"], п["q"]           # r = q·n is the share, N = q·d the number
        r, N = q * n, q * d
        л = (f"{r} × {d} = {N}" if n == 1 else f"{r} ÷ {n} = {q}, {q} × {d} = {N}")
        return я["число_утв"].format(Ч=доля_слово(язык, n, d), r=r, N=N, л=л, С=_связка(язык, n))
    p, N = п["p"], п["N"]                          # проц_обр: r = N·p/100 given, N asked
    r = N * p // 100
    л = f"{r} × 100 = {r * 100}, {r * 100} ÷ {p} = {N}"
    return я["проц_обр"].format(r=r, p=p, N=N, л=л)


# --- the court's side ---
def _альт(слова):
    return "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    доли = [доля_слово(язык, n, d) for n, d in ДОЛИ]
    return {"Ч": _альт(доли), "Ч2": _альт(доли), "N": r"(\d+)", "r": r"(\d+)", "m": r"(\d+)", "p": r"(\d+)",
            "В": _альт(я["вещи"]), "С": _альт(я["связка"]), "С2": _альт(я["связка"]),
            "л": r"((?:\d+ [÷×−] \d+ = \d+(?:, )?)+)"}


def _шаблоны(язык):
    я = ЯЗЫКИ[язык]
    return [("доля", False, я["доля_утв"]), ("доля", True, f"{я['доля_воп']} {я['доля_утв']}"),
            ("проц", False, я["проц_утв"]), ("проц", True, f"{я['проц_воп']} {я['проц_утв']}"),
            ("дополн", False, я["дополн"]), ("число", False, я["число_утв"]), ("проц_обр", False, я["проц_обр"])]


def образцы(язык):
    дыры = _дыры(язык)
    return [(re.compile("^" + phrases.образец(ш, дыры) + "$"), phrases.порядок(ш), форма, вопрос) for форма, вопрос, ш in _шаблоны(язык)]


ОБРАЗЦЫ = {язык: образцы(язык) for язык in ЯЗЫКИ}
_ОБРАТНО = {язык: {доля_слово(язык, n, d): (n, d) for n, d in ДОЛИ} for язык in ЯЗЫКИ}


def разобрать(язык, строка):
    я = ЯЗЫКИ[язык]
    for образец, имена, форма, вопрос in ОБРАЗЦЫ[язык]:
        м = образец.match(строка)
        if not м:
            continue
        з = {}
        for имя, г in zip(имена, м.groups()):
            if имя in з and з[имя] != г:
                з = None
                break
            з[имя] = г
        if з is None:
            continue
        try:
            if форма in ("доля", "число"):
                n, d = _ОБРАТНО[язык][з["Ч"]]
                N = int(з["N"])
                if N % d:
                    return None
                return dict(форма=форма, n=n, d=d, q=N // d, вопрос=вопрос)
            if форма == "дополн":
                n, d = _ОБРАТНО[язык][з["Ч"]]
                N = int(з["N"])
                if N % d:
                    return None
                return dict(форма=форма, n=n, d=d, q=N // d, вещь=я["вещи"].index(з["В"]))
            p, N = int(з["p"]), int(з["N"])
            if p < 1 or (N * p) % 100:
                return None
            return dict(форма=форма, p=p, N=N, вопрос=вопрос)
        except (KeyError, ValueError):
            return None
    return None


def судить(строка):
    с = строка.strip()
    for язык in ЯЗЫКИ:
        п = разобрать(язык, с)
        if п is not None:
            форма = п.pop("форма")
            try:
                return True, страница(язык, форма, **п) == с
            except (KeyError, ValueError, ZeroDivisionError):
                return True, False
    return False, False
