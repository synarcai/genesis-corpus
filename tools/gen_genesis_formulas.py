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
import rugram
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


# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 880 строк, вопросов ноль — он сообщал, чему равна площадь,
# и ни разу не спрашивал.
СПРОСИТЬ = {
    "value": "what is {предмет}?",
    "area": "what is the area of {предмет}?",
    "leg": "{предмет} — what is c?",
    "значение": "чему равно {предмет}?",
    "площадь": "чему равна площадь {предмет}?",
    "катет": "{предмет} — чему равно c?",
}


def спросить(искомое, предмет, ответ):
    """Вопрос о предмете и ответ о нём же — одной строкой."""
    return f"{СПРОСИТЬ[искомое].format(предмет=предмет)} {ответ}"


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
        пиф_en = f"a^2 + b^2 = c^2 with a = {a} and b = {b}"
        пиф_ru = f"формула a^2 + b^2 = c^2 при a = {a} и b = {b}"
        утв_п_en = f"{пиф_en} gives c = {c}."
        утв_п_ru = f"{пиф_ru} даёт c = {c}."
        out.append(утв_п_en)
        out.append(утв_п_ru)
        out.append(спросить("leg", пиф_en, утв_п_en))
        out.append(спросить("катет", пиф_ru, утв_п_ru))
        out.append(f"die formel a^2 + b^2 = c^2 mit a = {a} und b = {b} "
                   f"ergibt c = {c}.")
        # --- rectangle and triangle areas
        пр_en, пр_ru = f"a rectangle {w} by {h}", f"прямоугольника {w} на {h}"
        утв_пр_en = f"the area of {пр_en} is {w * h}."
        утв_пр_ru = f"площадь {пр_ru} равна {w * h}."
        out.append(утв_пр_en)
        out.append(утв_пр_ru)
        out.append(спросить("area", пр_en, утв_пр_en))
        out.append(спросить("площадь", пр_ru, утв_пр_ru))
        тр_en = f"a triangle with base {base} and height {height}"
        тр_ru = f"треугольника с основанием {base} и высотой {height}"
        утв_тр_en = f"the area of {тр_en} is {base * height // 2}."
        утв_тр_ru = f"площадь {тр_ru} равна {base * height // 2}."
        out.append(утв_тр_en)
        out.append(утв_тр_ru)
        out.append(спросить("area", тр_en, утв_тр_en))
        out.append(спросить("площадь", тр_ru, утв_тр_ru))
        # ОТКАЗ С ОСНОВАНИЕМ: площадь треугольника есть половина
        # произведения, и при нечётном произведении целой её нет. Мир
        # пишет площадь только при чётном — таков его закон, — и отказ
        # называет основание числом: само произведение и его нечётность.
        нч = height + 1 if (base * height) % 2 == 0 else height
        if (base * нч) % 2:
            out.append(f"what is the area of a triangle with base "
                       f"{base} and height {нч}? no whole answer for "
                       f"base {base} and height {нч}: {base} × {нч} = "
                       f"{base * нч} is odd.")
            out.append(f"чему равна площадь треугольника с основанием "
                       f"{base} и высотой {нч}? целого ответа нет при "
                       f"основании {base} и высоте {нч}: {base} × {нч} "
                       f"= {base * нч} нечётно.")
        # --- binomial identities, instantiated
        out.append(f"( {p} + {q} )^2 = {p}^2 + 2 × {p} × {q} + {q}^2 = "
                   f"{(p + q) ** 2}.")
        квадрат = f"( {p} + {q} )^2"
        out.append(f"{квадрат} = {(p + q) ** 2}.")
        out.append(спросить("значение", квадрат,
                            f"{квадрат} = {(p + q) ** 2}."))
        out.append(f"{p}^2 − {q}^2 = ( {p} − {q} ) × ( {p} + {q} ) = "
                   f"{p * p - q * q}.")
        # --- the sum of the first n
        сум_en = f"the sum of the first {n} numbers"
        сум_ru = f"сумма первых {n} чисел"
        утв_с_en = f"{сум_en} is {n * (n + 1) // 2}."
        утв_с_ru = f"{сум_ru} равна {n * (n + 1) // 2}."
        out.append(утв_с_en)
        out.append(утв_с_ru)
        out.append(спросить("value", сум_en, утв_с_en))
        out.append(спросить("значение", сум_ru, утв_с_ru))
        # --- geometric growth
        ст_en, ст_ru = f"{g} to the power {k}", f"{g} в степени {k}"
        утв_ст_en, утв_ст_ru = f"{ст_en} is {g ** k}.", f"{ст_ru} равно {g ** k}."
        out.append(утв_ст_en)
        out.append(утв_ст_ru)
        out.append(спросить("value", ст_en, утв_ст_en))
        out.append(спросить("значение", ст_ru, утв_ст_ru))
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
        # ОДНО УСЛОВИЕ ПРАВИЛО ДВУМЯ НЕЗАВИСИМЫМИ СЧЁТАМИ: ветвь
        # выбиралась по числу УЗЛОВ и применялась к РЁБРАМ тоже,
        # и «5 узлов и 4 рёбер» стояло в корпусе непойманным.
        # Форма каждого счёта берётся из дома отдельно.
        out.append(f"{текст} этот граф имеет "
                   f"{узлов} {rugram.форма('узел', узлов)} и "
                   f"{рёбер} {rugram.форма('ребро', рёбер)}.")
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
