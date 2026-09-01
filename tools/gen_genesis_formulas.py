#!/usr/bin/env python3
"""GENESIS layer: FORMULAS AND DIAGRAMS, described in four languages.

    a^2 + b^2 = c^2 with a = 3 and b = 4 gives c = 5.
    формула a^2 + b^2 = c^2 при a = 3 и b = 4 даёт c = 5.
    graph TD; A-->B; B-->C;
    this graph has 3 nodes and 2 edges.
    этот граф имеет 3 узла и 2 ребра.

TWO NOTATIONS THE ORGANISM MUST READ AS SIGNS, NOT AS DECORATION: a
formula and a diagram. Both are checkable, and both are checked
(`scripts/formula_court.py`): the formula is instantiated with its own
numbers and evaluated; the diagram is parsed, its nodes and edges are
counted, its reachability is walked.

DESCRIPTIONS COME IN FOUR LANGUAGES ON SEPARATE LINES — English,
Russian, German, Chinese — because the owner asked for the notation to
live among descriptive texts in different languages, and because a
sign explained in one language only is learnt as that language.

WHAT IS DELIBERATELY ABSENT: anything approximate. No π, no square
roots that are not whole, no decimals — a corpus that states «3.14» as
the value of a circle teaches a rounding as a truth. Approximation is
a genus of its own and needs its own court before it needs shows.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit  # noqa: E402

# (a, b, c) with a² + b² = c² — whole triples only
TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
           (20, 21, 29), (9, 40, 41), (12, 35, 37), (28, 45, 53)]
RECTS = [(3, 4), (5, 6), (7, 2), (8, 9), (4, 11), (6, 6), (10, 3), (12, 5)]
# triangles with an even product, so half of it is whole
TRIS = [(6, 4), (8, 5), (10, 3), (12, 7), (4, 9), (14, 5), (6, 11), (16, 3)]
BINOMS = [(2, 3), (4, 1), (5, 2), (3, 7), (6, 4), (9, 2), (7, 5), (10, 3)]
SUMS = [4, 5, 6, 7, 8, 9, 10, 12]
GEOM = [(2, 3), (3, 2), (2, 4), (5, 2), (2, 5), (4, 2), (3, 3), (2, 6)]
GRAPHS = [
    ("graph TD; A-->B; B-->C;", 3, 2, "A", "C", 2),
    ("graph TD; A-->B; A-->C;", 3, 2, "A", "C", 1),
    ("graph TD; A-->B; B-->C; C-->D;", 4, 3, "A", "D", 3),
    ("graph TD; A-->B; B-->C; A-->C;", 3, 3, "A", "C", 1),
    ("graph TD; A-->B; B-->C; C-->D; D-->E;", 5, 4, "A", "E", 4),
    ("graph TD; A-->B; B-->D; A-->C; C-->D;", 4, 4, "A", "D", 2),
]
СЛОВОМ = {
    2: ("two", "два", "zwei", "二"), 3: ("three", "три", "drei", "三"),
    4: ("four", "четыре", "vier", "四"), 5: ("five", "пять", "fünf", "五"),
}


def pass_shows(pass_i):
    out = []
    for i in range(8):
        a, b, c = TRIPLES[(pass_i + i) % len(TRIPLES)]
        w, h = RECTS[(pass_i * 3 + i) % len(RECTS)]
        base, height = TRIS[(pass_i * 5 + i) % len(TRIS)]
        p, q = BINOMS[(pass_i + i * 3) % len(BINOMS)]
        n = SUMS[(pass_i * 2 + i) % len(SUMS)]
        g, k = GEOM[(pass_i * 7 + i) % len(GEOM)]
        # --- Pythagoras
        out.append(f"a^2 + b^2 = c^2 with a = {a} and b = {b} gives c = {c}.")
        out.append(f"формула a^2 + b^2 = c^2 при a = {a} и b = {b} "
                   f"даёт c = {c}.")
        out.append(f"die formel a^2 + b^2 = c^2 mit a = {a} und b = {b} "
                   f"ergibt c = {c}.")
        # --- rectangle and triangle areas
        out.append(f"the area of a rectangle {w} by {h} is {w * h}.")
        out.append(f"площадь прямоугольника {w} на {h} равна {w * h}.")
        out.append(f"the area of a triangle with base {base} and height "
                   f"{height} is {base * height // 2}.")
        out.append(f"площадь треугольника с основанием {base} и высотой "
                   f"{height} равна {base * height // 2}.")
        # --- binomial identities, instantiated
        out.append(f"( {p} + {q} )^2 = {p}^2 + 2 × {p} × {q} + {q}^2 = "
                   f"{(p + q) ** 2}.")
        out.append(f"( {p} + {q} )^2 = {(p + q) ** 2}.")
        out.append(f"{p}^2 − {q}^2 = ( {p} − {q} ) × ( {p} + {q} ) = "
                   f"{p * p - q * q}.")
        # --- the sum of the first n
        out.append(f"the sum of the first {n} numbers is {n * (n + 1) // 2}.")
        out.append(f"сумма первых {n} чисел равна {n * (n + 1) // 2}.")
        # --- geometric growth
        out.append(f"{g} to the power {k} is {g ** k}.")
        out.append(f"{g} в степени {k} равно {g ** k}.")
        # --- diagrams
        текст, узлов, рёбер, откуда, куда, шагов = GRAPHS[
            (pass_i * 3 + i) % len(GRAPHS)]
        # ПОКАЗ НЕСЁТ И ЗНАК, И ЕГО ОПИСАНИЕ. Перестановка проходов
        # отрывает соседние строки друг от друга, а «этот граф имеет
        # 3 узла» без своего графа не значит ничего и не судится ничем.
        # Диаграмма и её описание — один показ, одна строка.
        out.append(текст)
        out.append(f"{текст} this graph has {узлов} nodes and "
                   f"{рёбер} edges.")
        out.append(f"{текст} этот граф имеет {узлов} узла и "
                   f"{рёбер} ребра." if узлов < 5 else
                   f"{текст} этот граф имеет {узлов} узлов и "
                   f"{рёбер} рёбер.")
        out.append(f"{текст} in this graph {откуда} reaches {куда} in "
                   f"{шагов} steps." if шагов > 1 else
                   f"{текст} in this graph {откуда} reaches {куда} in "
                   f"1 step.")
        en, ru, de, zh = СЛОВОМ.get(рёбер, (str(рёбер),) * 4)
        out.append(f"{текст} the diagram has {en} edges.")
        out.append(f"{текст} диаграмма имеет {ru} ребра." if рёбер < 5
                   else f"{текст} диаграмма имеет {ru} рёбер.")
        out.append(f"{текст} das diagramm hat {de} kanten.")
        out.append(f"{текст} 这个图有{zh}条边。")
    return out


def main():
    emit("datasets/genesis_formulas.txt", pass_shows)


if __name__ == "__main__":
    main()
