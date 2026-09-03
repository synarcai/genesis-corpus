#!/usr/bin/env python3
"""THE HOUSE OF PRIME PHRASES — prime and composite in eight languages.

The numbers world says «17 is prime; its divisors are 1 and 17.», «15 is not
prime; 15 = 3 × 5.» and asks «is 17 prime? yes: …» in en/ru; this house
says the same in de/fr/es/it/pt/nl/pl/tr: the verdict opens the answer
(М-147), the witness follows — the two divisors of a prime, the factor pair
of a composite. Generator and court read one table through tools/phrases.py
(М-159); the court finds the least divisor itself.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# per language: the prime statement, the composite statement, the question,
# the yes/no words
ЯЗЫКИ = {
    "de": dict(прост="{n} ist eine Primzahl; ihre Teiler sind 1 und {n}.", сост="{n} ist keine Primzahl: {n} = {d} × {m}.", воп="ist {n} eine Primzahl?", да="ja", нет="nein"),
    "fr": dict(прост="{n} est premier ; ses diviseurs sont 1 et {n}.", сост="{n} n'est pas premier : {n} = {d} × {m}.", воп="{n} est-il premier ?", да="oui", нет="non"),
    "es": dict(прост="{n} es primo; sus divisores son 1 y {n}.", сост="{n} no es primo: {n} = {d} × {m}.", воп="¿es {n} primo?", да="sí", нет="no"),
    "it": dict(прост="{n} è primo; i suoi divisori sono 1 e {n}.", сост="{n} non è primo: {n} = {d} × {m}.", воп="{n} è primo?", да="sì", нет="no"),
    "pt": dict(прост="{n} é primo; os seus divisores são 1 e {n}.", сост="{n} não é primo: {n} = {d} × {m}.", воп="{n} é primo?", да="sim", нет="não"),
    "nl": dict(прост="{n} is priem; zijn delers zijn 1 en {n}.", сост="{n} is niet priem: {n} = {d} × {m}.", воп="is {n} priem?", да="ja", нет="nee"),
    "pl": dict(прост="{n} jest liczbą pierwszą; jej dzielniki to 1 i {n}.", сост="{n} nie jest liczbą pierwszą: {n} = {d} × {m}.", воп="czy {n} jest liczbą pierwszą?", да="tak", нет="nie"),
    "tr": dict(прост="{n} asaldır; bölenleri 1 ve {n} sayılarıdır.", сост="{n} asal değildir: {n} = {d} × {m}.", воп="{n} asal mıdır?", да="evet", нет="hayır"),
}
ДЫРЫ = {"n": r"(\d+)", "d": r"(\d+)", "m": r"(\d+)"}


def простое(n):
    return n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))


def делитель(n):
    """The least proper divisor of a composite — its witness."""
    return next(d for d in range(2, n) if n % d == 0)


def утверждение(язык, n):
    я = ЯЗЫКИ[язык]
    if простое(n):
        return я["прост"].format(n=n)
    d = делитель(n)
    return я["сост"].format(n=n, d=d, m=n // d)


def вопрос(язык, n):
    """THE VERDICT WORD OPENS THE ANSWER (М-147): «ist 17 eine Primzahl? ja: 17
    ist eine Primzahl; …»."""
    я = ЯЗЫКИ[язык]
    return f"{я['воп'].format(n=n)} {я['да'] if простое(n) else я['нет']}: {утверждение(язык, n)}"


def образцы(язык):
    я = ЯЗЫКИ[язык]
    прост = phrases.образец(я["прост"], ДЫРЫ)
    сост = phrases.образец(я["сост"], ДЫРЫ)
    воп = phrases.образец(я["воп"], ДЫРЫ)
    return [(re.compile("^" + прост + "$"), "прост", False), (re.compile("^" + сост + "$"), "сост", False),
            (re.compile("^" + воп + " " + re.escape(я["да"]) + ": " + прост + "$"), "прост", True),
            (re.compile("^" + воп + " " + re.escape(я["нет"]) + ": " + сост + "$"), "сост", True)]


def судить_группы(язык, вид, спрошено, группы):
    г = [int(x) for x in группы]
    if спрошено:
        if г[0] != г[1]:
            return False
        г = г[1:]
    if вид == "прост":
        n, n2 = г[0], г[1]
        return n == n2 and простое(n)
    n, n2, d, m = г
    # the witness is the least divisor and its cofactor — the house's own pair
    return n == n2 and not простое(n) and n > 1 and d == делитель(n) and d * m == n
