#!/usr/bin/env python3
"""THE HOUSE OF GEOMETRY PHRASES — area and perimeter in eight languages.

The geometry world says «a rectangle 7 by 8 has area 7 × 8 = 56.» and «what
is the area of a rectangle 7 by 8? …» in English and Russian. This house
declares the same four facts — the area and the perimeter of a rectangle,
the perimeter and the area of a square — as PHRASES of eight more languages,
statement and question, with the ledger the geometry world writes
(«7 × 8 = 56», «7 + 8 = 15, 2 × 15 = 30», «4 × 4 = 16»). Generator and court
read one table: the generator fills the holes {a} {b} {s} and the ledger,
the court turns the same phrases into patterns and recomputes.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# per language: the rectangle phrase, the square phrase, the two predicates
# («{ф} has area {л}.»), and the four questions
ЯЗЫКИ = {
    "de": dict(прям="ein Rechteck {a} mal {b}", квад="ein Quadrat mit Seite {s}",
               пл="{ф} hat die Fläche {л}.", пер="{ф} hat den Umfang {л}.",
               в_пл="wie groß ist die Fläche eines Rechtecks {a} mal {b}?", в_пер="wie groß ist der Umfang eines Rechtecks {a} mal {b}?",
               кв_пл="wie groß ist die Fläche eines Quadrats mit Seite {s}?", кв_пер="wie groß ist der Umfang eines Quadrats mit Seite {s}?"),
    "fr": dict(прям="un rectangle {a} sur {b}", квад="un carré de côté {s}",
               пл="{ф} a une aire de {л}.", пер="{ф} a un périmètre de {л}.",
               в_пл="quelle est l'aire d'un rectangle {a} sur {b} ?", в_пер="quel est le périmètre d'un rectangle {a} sur {b} ?",
               кв_пл="quelle est l'aire d'un carré de côté {s} ?", кв_пер="quel est le périmètre d'un carré de côté {s} ?"),
    "es": dict(прям="un rectángulo de {a} por {b}", квад="un cuadrado de lado {s}",
               пл="{ф} tiene área {л}.", пер="{ф} tiene perímetro {л}.",
               в_пл="¿cuál es el área de un rectángulo de {a} por {b}?", в_пер="¿cuál es el perímetro de un rectángulo de {a} por {b}?",
               кв_пл="¿cuál es el área de un cuadrado de lado {s}?", кв_пер="¿cuál es el perímetro de un cuadrado de lado {s}?"),
    "it": dict(прям="un rettangolo {a} per {b}", квад="un quadrato di lato {s}",
               пл="{ф} ha area {л}.", пер="{ф} ha perimetro {л}.",
               в_пл="qual è l'area di un rettangolo {a} per {b}?", в_пер="qual è il perimetro di un rettangolo {a} per {b}?",
               кв_пл="qual è l'area di un quadrato di lato {s}?", кв_пер="qual è il perimetro di un quadrato di lato {s}?"),
    "pt": dict(прям="um retângulo {a} por {b}", квад="um quadrado de lado {s}",
               пл="{ф} tem área {л}.", пер="{ф} tem perímetro {л}.",
               в_пл="qual é a área de um retângulo {a} por {b}?", в_пер="qual é o perímetro de um retângulo {a} por {b}?",
               кв_пл="qual é a área de um quadrado de lado {s}?", кв_пер="qual é o perímetro de um quadrado de lado {s}?"),
    "nl": dict(прям="een rechthoek {a} bij {b}", квад="een vierkant met zijde {s}",
               пл="{ф} heeft oppervlakte {л}.", пер="{ф} heeft omtrek {л}.",
               в_пл="wat is de oppervlakte van een rechthoek {a} bij {b}?", в_пер="wat is de omtrek van een rechthoek {a} bij {b}?",
               кв_пл="wat is de oppervlakte van een vierkant met zijde {s}?", кв_пер="wat is de omtrek van een vierkant met zijde {s}?"),
    "pl": dict(прям="prostokąt {a} na {b}", квад="kwadrat o boku {s}",
               пл="{ф} ma pole {л}.", пер="{ф} ma obwód {л}.",
               в_пл="jakie jest pole prostokąta {a} na {b}?", в_пер="jaki jest obwód prostokąta {a} na {b}?",
               кв_пл="jakie jest pole kwadratu o boku {s}?", кв_пер="jaki jest obwód kwadratu o boku {s}?"),
    "tr": dict(прям="kenarları {a} ve {b} olan dikdörtgenin", квад="kenarı {s} olan karenin",
               пл="{ф} alanı: {л}.", пер="{ф} çevresi: {л}.",
               в_пл="kenarları {a} ve {b} olan dikdörtgenin alanı kaçtır?", в_пер="kenarları {a} ve {b} olan dikdörtgenin çevresi kaçtır?",
               кв_пл="kenarı {s} olan karenin alanı kaçtır?", кв_пер="kenarı {s} olan karenin çevresi kaçtır?"),
}
# the four facts: (figure key, predicate key, question key, ledger maker, checker)
ФАКТЫ = (
    ("прям", "пл", "в_пл", lambda a, b: f"{a} × {b} = {a * b}"),
    ("прям", "пер", "в_пер", lambda a, b: f"{a} + {b} = {a + b}, 2 × {a + b} = {2 * (a + b)}"),
    ("квад", "пер", "кв_пер", lambda s, _: f"4 × {s} = {4 * s}"),
    ("квад", "пл", "кв_пл", lambda s, _: f"{s} × {s} = {s * s}"),
)
ЛЕДЖЕРЫ = {
    ("прям", "пл"): (r"(\d+) × (\d+) = (\d+)", lambda a, b, г: г == (a, b, a * b)),
    ("прям", "пер"): (r"(\d+) \+ (\d+) = (\d+), 2 × (\d+) = (\d+)", lambda a, b, г: г == (a, b, a + b, a + b, 2 * (a + b))),
    ("квад", "пер"): (r"4 × (\d+) = (\d+)", lambda s, _, г: г == (s, 4 * s)),
    ("квад", "пл"): (r"(\d+) × (\d+) = (\d+)", lambda s, _, г: г == (s, s, s * s)),
}


def утверждение(язык, k, a, b):
    """Fact k of the language over the rectangle a × b or the square a."""
    я = ЯЗЫКИ[язык]
    фигура, предикат, _, леджер = ФАКТЫ[k]
    ф = я[фигура].format(a=a, b=b, s=a)
    return я[предикат].format(ф=ф, л=леджер(a, b))


def вопрос(язык, k, a, b):
    """The question of fact k, answered by the statement itself (М-153)."""
    я = ЯЗЫКИ[язык]
    return f"{я[ФАКТЫ[k][2]].format(a=a, b=b, s=a)} {утверждение(язык, k, a, b)}"


def _образец(шаблон, дыры):
    """The template as a regex: literal parts escaped, holes as groups."""
    return phrases.образец(шаблон, дыры)


def образцы(язык):
    """[(regex, k, asked)] — every statement and question of the language;
    groups: the figure's numbers, then the ledger's (and, when asked, the
    question's numbers before them)."""
    я = ЯЗЫКИ[язык]
    вон = []
    for k, (фигура, предикат, вопр, _) in enumerate(ФАКТЫ):
        ф = _образец(я[фигура], {"a": r"(\d+)", "b": r"(\d+)", "s": r"(\d+)"})
        леджер = ЛЕДЖЕРЫ[(фигура, предикат)][0]
        утв = _образец(я[предикат], {"ф": ф, "л": леджер})
        воп = _образец(я[вопр], {"a": r"(\d+)", "b": r"(\d+)", "s": r"(\d+)"})
        вон.append((re.compile("^" + утв + "$"), k, False))
        вон.append((re.compile("^" + воп + " " + утв + "$"), k, True))
    return вон


def судить_группы(k, спрошено, группы):
    """True iff the numbers of the line are one fact of the house."""
    фигура, предикат, _, _ = ФАКТЫ[k]
    n = 2 if фигура == "прям" else 1
    г = [int(x) for x in группы]
    if спрошено:
        if г[:n] != г[n:2 * n]:
            return False
        г = г[n:]
    a, b = (г[0], г[1]) if n == 2 else (г[0], None)
    return ЛЕДЖЕРЫ[(фигура, предикат)][1](a, b, tuple(г[n:]))
