#!/usr/bin/env python3
"""THE HOUSE OF SEARCH PHRASES — an answer found by a bounded walk, in ten languages.

holon's order for the market of reasoning (03.09, ONE-CARRIER: the ledger is
the program is the proof): a genus whose answer is FOUND, not computed in one
step, must show the search itself as a ledger of primitive steps, so that
the organism buys the walk from the shows and not from code. Three
operations, four question surfaces, every language of the front:

  · NEXT PRIME — «the smallest prime greater than 90 is 97: 91 = 7 × 13,
    92 = 2 × 46, 93 = 3 × 31, 94 = 2 × 47, 95 = 5 × 19, 96 = 2 × 48, 97 is
    prime.» and the same walk asked as «the next prime after 90» — two
    surfaces of ONE operation (the question-as-operation thesis, Д-1);
  · SMALLEST MULTIPLIER — «the smallest whole number n with n × 7 > 30 is 5:
    1 × 7 = 7 ≤ 30, 2 × 7 = 14 ≤ 30, 3 × 7 = 21 ≤ 30, 4 × 7 = 28 ≤ 30,
    5 × 7 = 35 > 30.»;
  · THE NUMBER FROM ITS PART — «какое число, если его пятая часть равна 6?
    пятая часть числа равна 6; число — 30: 6 × 5 = 30.» (the share world
    says it in English with a verbal ledger; here the ledger is symbolic and
    the surface is in ten languages).

Every step is a primitive the organism owns (factor witness, primality,
product, comparison); a composite step names its witness («92 = 2 × 46»),
the found prime names its law («97 is prime»). Statement and question
answered by the statement (М-153); generator and court read one table
through tools/phrases.py (М-159).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# The unit parts of a number, k = 2..10, as the language names them (fillers
# of the frame — holes as much as a number is, М-159).
ЧАСТИ = {
    "en": ("half", "a third", "a quarter", "a fifth", "a sixth", "a seventh", "an eighth", "a ninth", "a tenth"),
    "ru": ("половина", "треть", "четверть", "пятая часть", "шестая часть", "седьмая часть", "восьмая часть", "девятая часть", "десятая часть"),
    "de": ("die Hälfte", "ein Drittel", "ein Viertel", "ein Fünftel", "ein Sechstel", "ein Siebtel", "ein Achtel", "ein Neuntel", "ein Zehntel"),
    "fr": ("la moitié", "un tiers", "un quart", "un cinquième", "un sixième", "un septième", "un huitième", "un neuvième", "un dixième"),
    "es": ("la mitad", "un tercio", "un cuarto", "un quinto", "un sexto", "un séptimo", "un octavo", "un noveno", "un décimo"),
    "it": ("la metà", "un terzo", "un quarto", "un quinto", "un sesto", "un settimo", "un ottavo", "un nono", "un decimo"),
    "pt": ("a metade", "um terço", "um quarto", "um quinto", "um sexto", "um sétimo", "um oitavo", "um nono", "um décimo"),
    "nl": ("de helft", "een derde", "een kwart", "een vijfde", "een zesde", "een zevende", "een achtste", "een negende", "een tiende"),
    "pl": ("połowa", "jedna trzecia", "jedna czwarta", "jedna piąta", "jedna szósta", "jedna siódma", "jedna ósma", "jedna dziewiąta", "jedna dziesiąta"),
    "tr": ("yarısı", "üçte biri", "dörtte biri", "beşte biri", "altıda biri", "yedide biri", "sekizde biri", "dokuzda biri", "onda biri"),
}

# прост — the law the found prime names; the rest are the four surfaces
# (утв — statement, воп — question), each with its holes.
ЯЗЫКИ = {
    "en": dict(прост="{p} is prime",
               прост1_утв="the smallest prime greater than {n} is {p}: {л}.", прост1_воп="what is the smallest prime greater than {n}?",
               прост2_утв="the next prime after {n} is {p}: {л}.", прост2_воп="what is the next prime after {n}?",
               множ_утв="the smallest whole number n with n × {a} > {b} is {k}: {л}.", множ_воп="what is the smallest whole number n with n × {a} > {b}?",
               часть_утв="{ч} of a number is {v}; the number is {x}: {v} × {k} = {x}.", часть_воп="what is the number if {ч} of it is {v}?"),
    "ru": dict(прост="{p} простое",
               прост1_утв="наименьшее простое больше {n} — это {p}: {л}.", прост1_воп="какое наименьшее простое больше {n}?",
               прост2_утв="следующее простое после {n} — это {p}: {л}.", прост2_воп="какое следующее простое после {n}?",
               множ_утв="наименьшее целое n, при котором n × {a} > {b}, — это {k}: {л}.", множ_воп="каково наименьшее целое n, при котором n × {a} > {b}?",
               часть_утв="{ч} числа равна {v}; число — {x}: {v} × {k} = {x}.", часть_воп="какое число, если его {ч} равна {v}?"),
    "de": dict(прост="{p} ist prim",
               прост1_утв="die kleinste Primzahl größer als {n} ist {p}: {л}.", прост1_воп="was ist die kleinste Primzahl größer als {n}?",
               прост2_утв="die nächste Primzahl nach {n} ist {p}: {л}.", прост2_воп="was ist die nächste Primzahl nach {n}?",
               множ_утв="die kleinste ganze Zahl n mit n × {a} > {b} ist {k}: {л}.", множ_воп="was ist die kleinste ganze Zahl n mit n × {a} > {b}?",
               часть_утв="{ч} einer Zahl ist {v}; die Zahl ist {x}: {v} × {k} = {x}.", часть_воп="welche Zahl ist es, wenn {ч} davon {v} ist?"),
    "fr": dict(прост="{p} est premier",
               прост1_утв="le plus petit nombre premier supérieur à {n} est {p} : {л}.", прост1_воп="quel est le plus petit nombre premier supérieur à {n} ?",
               прост2_утв="le nombre premier suivant après {n} est {p} : {л}.", прост2_воп="quel est le nombre premier suivant après {n} ?",
               множ_утв="le plus petit entier n tel que n × {a} > {b} est {k} : {л}.", множ_воп="quel est le plus petit entier n tel que n × {a} > {b} ?",
               часть_утв="{ч} d'un nombre est {v} ; le nombre est {x} : {v} × {k} = {x}.", часть_воп="quel est le nombre si {ч} de celui-ci est {v} ?"),
    "es": dict(прост="{p} es primo",
               прост1_утв="el menor primo mayor que {n} es {p}: {л}.", прост1_воп="¿cuál es el menor primo mayor que {n}?",
               прост2_утв="el siguiente primo después de {n} es {p}: {л}.", прост2_воп="¿cuál es el siguiente primo después de {n}?",
               множ_утв="el menor entero n con n × {a} > {b} es {k}: {л}.", множ_воп="¿cuál es el menor entero n con n × {a} > {b}?",
               часть_утв="{ч} de un número es {v}; el número es {x}: {v} × {k} = {x}.", часть_воп="¿cuál es el número si {ч} de él es {v}?"),
    "it": dict(прост="{p} è primo",
               прост1_утв="il più piccolo primo maggiore di {n} è {p}: {л}.", прост1_воп="qual è il più piccolo primo maggiore di {n}?",
               прост2_утв="il primo successivo dopo {n} è {p}: {л}.", прост2_воп="qual è il primo successivo dopo {n}?",
               множ_утв="il più piccolo intero n con n × {a} > {b} è {k}: {л}.", множ_воп="qual è il più piccolo intero n con n × {a} > {b}?",
               часть_утв="{ч} di un numero è {v}; il numero è {x}: {v} × {k} = {x}.", часть_воп="qual è il numero se {ч} di esso è {v}?"),
    "pt": dict(прост="{p} é primo",
               прост1_утв="o menor primo maior que {n} é {p}: {л}.", прост1_воп="qual é o menor primo maior que {n}?",
               прост2_утв="o próximo primo depois de {n} é {p}: {л}.", прост2_воп="qual é o próximo primo depois de {n}?",
               множ_утв="o menor inteiro n com n × {a} > {b} é {k}: {л}.", множ_воп="qual é o menor inteiro n com n × {a} > {b}?",
               часть_утв="{ч} de um número é {v}; o número é {x}: {v} × {k} = {x}.", часть_воп="qual é o número se {ч} dele é {v}?"),
    "nl": dict(прост="{p} is priem",
               прост1_утв="het kleinste priemgetal groter dan {n} is {p}: {л}.", прост1_воп="wat is het kleinste priemgetal groter dan {n}?",
               прост2_утв="het volgende priemgetal na {n} is {p}: {л}.", прост2_воп="wat is het volgende priemgetal na {n}?",
               множ_утв="het kleinste gehele getal n met n × {a} > {b} is {k}: {л}.", множ_воп="wat is het kleinste gehele getal n met n × {a} > {b}?",
               часть_утв="{ч} van een getal is {v}; het getal is {x}: {v} × {k} = {x}.", часть_воп="wat is het getal als {ч} ervan {v} is?"),
    "pl": dict(прост="{p} jest liczbą pierwszą",
               прост1_утв="najmniejsza liczba pierwsza większa od {n} to {p}: {л}.", прост1_воп="jaka jest najmniejsza liczba pierwsza większa od {n}?",
               прост2_утв="następna liczba pierwsza po {n} to {p}: {л}.", прост2_воп="jaka jest następna liczba pierwsza po {n}?",
               множ_утв="najmniejsza liczba całkowita n, dla której n × {a} > {b}, to {k}: {л}.", множ_воп="jaka jest najmniejsza liczba całkowita n, dla której n × {a} > {b}?",
               часть_утв="{ч} liczby to {v}; liczba to {x}: {v} × {k} = {x}.", часть_воп="jaka to liczba, jeśli jej {ч} to {v}?"),
    "tr": dict(прост="{p} asaldır",
               прост1_утв="{n} sayısından büyük en küçük asal sayı {p}: {л}.", прост1_воп="{n} sayısından büyük en küçük asal sayı kaçtır?",
               прост2_утв="{n} sayısından sonraki asal sayı {p}: {л}.", прост2_воп="{n} sayısından sonraki asal sayı kaçtır?",
               множ_утв="n × {a} > {b} olan en küçük tam sayı {k}: {л}.", множ_воп="n × {a} > {b} olan en küçük tam sayı kaçtır?",
               часть_утв="bir sayının {ч} {v} ise sayı {x} olur: {v} × {k} = {x}.", часть_воп="{ч} {v} olan sayı kaçtır?"),
}
РОДЫ = ("прост1", "прост2", "множ", "часть")


def простое(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def делитель(m):
    """The least proper divisor — the witness of a composite."""
    return next(d for d in range(2, m + 1) if m % d == 0)


def следующее_простое(n):
    p = n + 1
    while not простое(p):
        p += 1
    return p


def леджер_простого(язык, n):
    """«91 = 7 × 13, …, 97 is prime» — the walk from n + 1 to the prime."""
    p = следующее_простое(n)
    шаги = [f"{m} = {делитель(m)} × {m // делитель(m)}" for m in range(n + 1, p)]
    return ", ".join(шаги + [ЯЗЫКИ[язык]["прост"].format(p=p)])


def наименьший_множитель(a, b):
    k = 1
    while k * a <= b:
        k += 1
    return k


def леджер_множителя(a, b):
    k = наименьший_множитель(a, b)
    return ", ".join([f"{j} × {a} = {j * a} ≤ {b}" for j in range(1, k)] + [f"{k} × {a} = {k * a} > {b}"])


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    прост = re.escape(я["прост"]).replace(r"\{p\}", r"\d+")
    части = "|".join(re.escape(ч) for ч in ЧАСТИ[язык])
    return {"n": r"(\d+)", "p": r"(\d+)", "a": r"(\d+)", "b": r"(\d+)", "k": r"(\d+)", "v": r"(\d+)", "x": r"(\d+)",
            "ч": f"({части})",
            "л": r"((?:\d+ = \d+ × \d+, )*" + прост + r"|(?:\d+ × \d+ = \d+ ≤ \d+, )*\d+ × \d+ = \d+ > \d+)"}


def утверждение(язык, род, **з):
    я = ЯЗЫКИ[язык]
    if род in ("прост1", "прост2"):
        з = dict(з, p=следующее_простое(з["n"]), л=леджер_простого(язык, з["n"]))
    elif род == "множ":
        з = dict(з, k=наименьший_множитель(з["a"], з["b"]), л=леджер_множителя(з["a"], з["b"]))
    else:
        з = dict(з, ч=ЧАСТИ[язык][з["k"] - 2], x=з["v"] * з["k"])
    return я[род + "_утв"].format(**з)


def вопрос(язык, род, **з):
    я = ЯЗЫКИ[язык]
    з2 = dict(з, ч=ЧАСТИ[язык][з["k"] - 2]) if род == "часть" else з
    return f"{я[род + '_воп'].format(**з2)} {утверждение(язык, род, **з)}"


def образцы(язык):
    я = ЯЗЫКИ[язык]; дыры = _дыры(язык)
    вон = []
    for род in РОДЫ:
        утв = phrases.образец(я[род + "_утв"], дыры)
        вон.append((re.compile("^" + утв + "$"), род, False))
        вон.append((re.compile("^" + phrases.образец(я[род + "_воп"], дыры) + " " + утв + "$"), род, True))
    return вон


def _собрать(имена, группы):
    """The holes by name; a REPEATED hole is filled identically or the line
    lies (М-159 — «the number is 31: 6 × 5 = 30» once passed because the last
    group won the dict)."""
    з = {}
    for имя, г in zip(имена, группы):
        if имя in з and з[имя] != г:
            return None
        з[имя] = г
    return з


def судить_группы(язык, род, спрошено, группы):
    я = ЯЗЫКИ[язык]
    г = list(группы)
    спрош = {}
    if спрошено:
        имена = phrases.порядок(я[род + "_воп"])
        спрош = _собрать(имена, г[:len(имена)]); г = г[len(имена):]
    з = _собрать(phrases.порядок(я[род + "_утв"]), г)
    if спрош is None or з is None or any(спрош[имя] != з[имя] for имя in спрош):
        return False
    if род in ("прост1", "прост2"):
        n, p = int(з["n"]), int(з["p"])
        return n >= 1 and p == следующее_простое(n) and з["л"] == леджер_простого(язык, n)
    if род == "множ":
        a, b, k = int(з["a"]), int(з["b"]), int(з["k"])
        return a >= 1 and k == наименьший_множитель(a, b) and з["л"] == леджер_множителя(a, b)
    k, v, x = int(з["k"]), int(з["v"]), int(з["x"])
    return з["ч"] == ЧАСТИ[язык][k - 2] and x == v * k
