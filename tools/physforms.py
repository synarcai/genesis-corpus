#!/usr/bin/env python3
"""THE HOUSE OF PHYSICS PHRASES — speed and pressure in eight languages.

The physics worlds say «what is the speed of a body that covered 72 metres
in 8 seconds? … 9 metres per second» and «the pressure of 10 newtons on 2
square metres is 5 pascals: 10 newtons ÷ 2 square metres = 5 pascals» in
en/ru. This house says the two laws — speed = distance ÷ time, pressure =
force ÷ area — in de/fr/es/it/pt/nl/pl/tr, statement and question answered
by the statement (М-153), with the unit names in their count forms (Polish
few/many by the pack's count_agreement, German and Dutch invariable) and the
ledger «72 ÷ 8 = 9». Generator and court read one table through
tools/phrases.py; the court divides itself.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holes  # noqa: E402
import phrases  # noqa: E402

# unit forms beside a count ≥ 2: one string, or (few, many) for pl
ЕДИНИЦЫ = {
    "de": dict(m="Meter", s="Sekunden", v="Meter pro Sekunde", N="Newton", A="Quadratmeter", p="Pascal"),
    "fr": dict(m="mètres", s="secondes", v="mètres par seconde", N="newtons", A="mètres carrés", p="pascals"),
    "es": dict(m="metros", s="segundos", v="metros por segundo", N="newtons", A="metros cuadrados", p="pascales"),
    "it": dict(m="metri", s="secondi", v="metri al secondo", N="newton", A="metri quadrati", p="pascal"),
    "pt": dict(m="metros", s="segundos", v="metros por segundo", N="newtons", A="metros quadrados", p="pascais"),
    "nl": dict(m="meter", s="seconden", v="meter per seconde", N="newton", A="vierkante meter", p="pascal"),
    "pl": dict(m=("metry", "metrów"), s=("sekundy", "sekund"), v=("metry na sekundę", "metrów na sekundę"),
               N=("niutony", "niutonów"), A=("metry kwadratowe", "metrów kwadratowych"), p=("paskale", "paskali")),
    "tr": dict(m="metre", s="saniyede", v="metre bölü saniye", N="newton", A="metrekare", p="pascal"),
}
ЯЗЫКИ = {
    "de": dict(ск="ein Körper, der {s} {ем} in {t} {ес} zurücklegt, hat die Geschwindigkeit {v} {ев}: {л}.",
               в_ск="wie groß ist die Geschwindigkeit eines Körpers, der {s} {ем} in {t} {ес} zurücklegt?",
               да="eine Kraft von {F} {еN} auf {A} {еA} erzeugt den Druck {p} {еp}: {л}.",
               в_да="wie groß ist der Druck einer Kraft von {F} {еN} auf {A} {еA}?"),
    "fr": dict(ск="un corps qui parcourt {s} {ем} en {t} {ес} a une vitesse de {v} {ев} : {л}.",
               в_ск="quelle est la vitesse d'un corps qui parcourt {s} {ем} en {t} {ес} ?",
               да="une force de {F} {еN} sur {A} {еA} produit une pression de {p} {еp} : {л}.",
               в_да="quelle est la pression d'une force de {F} {еN} sur {A} {еA} ?"),
    "es": dict(ск="un cuerpo que recorre {s} {ем} en {t} {ес} tiene una velocidad de {v} {ев}: {л}.",
               в_ск="¿cuál es la velocidad de un cuerpo que recorre {s} {ем} en {t} {ес}?",
               да="una fuerza de {F} {еN} sobre {A} {еA} produce una presión de {p} {еp}: {л}.",
               в_да="¿cuál es la presión de una fuerza de {F} {еN} sobre {A} {еA}?"),
    "it": dict(ск="un corpo che percorre {s} {ем} in {t} {ес} ha una velocità di {v} {ев}: {л}.",
               в_ск="qual è la velocità di un corpo che percorre {s} {ем} in {t} {ес}?",
               да="una forza di {F} {еN} su {A} {еA} produce una pressione di {p} {еp}: {л}.",
               в_да="qual è la pressione di una forza di {F} {еN} su {A} {еA}?"),
    "pt": dict(ск="um corpo que percorre {s} {ем} em {t} {ес} tem uma velocidade de {v} {ев}: {л}.",
               в_ск="qual é a velocidade de um corpo que percorre {s} {ем} em {t} {ес}?",
               да="uma força de {F} {еN} sobre {A} {еA} produz uma pressão de {p} {еp}: {л}.",
               в_да="qual é a pressão de uma força de {F} {еN} sobre {A} {еA}?"),
    "nl": dict(ск="een lichaam dat {s} {ем} in {t} {ес} aflegt, heeft een snelheid van {v} {ев}: {л}.",
               в_ск="wat is de snelheid van een lichaam dat {s} {ем} in {t} {ес} aflegt?",
               да="een kracht van {F} {еN} op {A} {еA} geeft een druk van {p} {еp}: {л}.",
               в_да="wat is de druk van een kracht van {F} {еN} op {A} {еA}?"),
    "pl": dict(ск="ciało, które przebywa {s} {ем} w {t} {ес}, ma prędkość {v} {ев}: {л}.",
               в_ск="jaka jest prędkość ciała, które przebywa {s} {ем} w {t} {ес}?",
               да="siła {F} {еN} na {A} {еA} wywiera ciśnienie {p} {еp}: {л}.",
               в_да="jakie jest ciśnienie siły {F} {еN} na {A} {еA}?"),
    "tr": dict(ск="{t} {ес} {s} {ем} yol alan bir cismin hızı: {л}.",
               в_ск="{t} {ес} {s} {ем} yol alan bir cismin hızı kaçtır?",
               да="{F} {еN} kuvvetin {A} {еA} üzerindeki basıncı: {л}.",
               в_да="{F} {еN} kuvvetin {A} {еA} üzerindeki basıncı kaçtır?"),
}
ЛЕДЖЕР = r"(\d+ ÷ \d+ = \d+)"


def единица(язык, ключ, n):
    ф = ЕДИНИЦЫ[язык][ключ]
    if isinstance(ф, tuple):
        return ф[0] if holes.форма_счёта("pl", n) == "few" else ф[1]
    return ф


def _поля(язык, вид, a, b):
    """The numbers and their unit forms for law `вид` («ск» or «да»)."""
    c = a // b
    if вид == "ск":
        return dict(s=a, t=b, v=c, ем=единица(язык, "m", a), ес=единица(язык, "s", b), ев=единица(язык, "v", c), л=f"{a} ÷ {b} = {c}")
    return dict(F=a, A=b, p=c, еN=единица(язык, "N", a), еA=единица(язык, "A", b), еp=единица(язык, "p", c), л=f"{a} ÷ {b} = {c}")


def утверждение(язык, вид, a, b):
    assert a % b == 0
    return ЯЗЫКИ[язык][вид].format(**_поля(язык, вид, a, b))


def вопрос(язык, вид, a, b):
    return f"{ЯЗЫКИ[язык]['в_' + вид].format(**_поля(язык, вид, a, b))} {утверждение(язык, вид, a, b)}"


def _дыры(язык):
    alt = lambda ключ: "(" + "|".join(re.escape(ф) for ф in sorted((ЕДИНИЦЫ[язык][ключ],) if isinstance(ЕДИНИЦЫ[язык][ключ], str) else ЕДИНИЦЫ[язык][ключ], key=len, reverse=True)) + ")"
    return {"s": r"(\d+)", "t": r"(\d+)", "v": r"(\d+)", "F": r"(\d+)", "A": r"(\d+)", "p": r"(\d+)", "л": ЛЕДЖЕР,
            "ем": alt("m"), "ес": alt("s"), "ев": alt("v"), "еN": alt("N"), "еA": alt("A"), "еp": alt("p")}


def образцы(язык):
    я = ЯЗЫКИ[язык]
    д = _дыры(язык)
    вон = []
    for вид in ("ск", "да"):
        утв = phrases.образец(я[вид], д)
        вон.append((re.compile("^" + утв + "$"), вид, False))
        вон.append((re.compile("^" + phrases.образец(я["в_" + вид], д) + " " + утв + "$"), вид, True))
    return вон


def судить_группы(язык, вид, спрошено, группы):
    я = ЯЗЫКИ[язык]
    г = list(группы)
    имена = (phrases.порядок(я["в_" + вид]) if спрошено else []) + phrases.порядок(я[вид])
    з = {}
    for имя, значение in zip(имена, г):
        if имя in з and з[имя] != значение:
            return False               # a hole named twice is filled twice the same
        з[имя] = значение
    a, b = (int(з["s"]), int(з["t"])) if вид == "ск" else (int(з["F"]), int(з["A"]))
    if b < 2 or a % b or a // b < 2:
        return False
    ожид = _поля(язык, вид, a, b)
    return all(str(ожид[к]) == з[к] for к in ожид if к in з)
