#!/usr/bin/env python3
"""GENESIS layer: LINEAR ALGEBRA — vector and matrix as ONE object.

The syllabus court named vector and matrix absent. They are not an
advanced topic bolted on: a vector is the first object that is a
NUMBER-WITH-DIRECTION, and a matrix the first object that ACTS on
another object. Every engineer meets them as the language of state and
transformation; a corpus without them cannot say what a system does.

EXACT LENGTHS ONLY. The length of (3, 4) is 5 and the length of (1, 1)
is not writable here — the corpus states what it can check, and the
Pythagorean triples that make lengths whole are named, not searched.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 1320 строк, вопросов ноль.
СПРОСИТЬ = {
    "length": "what is the length of {предмет}?",
    "dot": "what is the dot product of {предмет}?",
    "det": "what is the determinant of {предмет}?",
    "value": "what is {предмет}?",
    "длина": "чему равна длина {предмет}?",
    "скалярное": "чему равно скалярное произведение {предмет}?",
    "определитель": "чему равен определитель {предмет}?",
    "значение": "чему равно {предмет}?",
}


def спросить(искомое, предмет, ответ):
    """Вопрос о предмете и ответ о нём же — одной строкой."""
    return f"{СПРОСИТЬ[искомое].format(предмет=предмет)} {ответ}"


def полный_квадрат(n):
    """Целое ли число корень: отказ считает основание, а не верит."""
    к = int(n ** 0.5)
    while к * к < n:
        к += 1
    return к * к == n


ТРОЙКИ = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17),
          (9, 12, 15), (7, 24, 25))
assert all(a * a + b * b == c * c for a, b, c in ТРОЙКИ)


def сложение(шаг):
    вон = []
    for i in range(24):
        a, b = 1 + (i % 7) + шаг, 2 + (i % 5)
        c, d = 3 + (i % 4), 1 + (i % 6)
        for знак, x, y in (("+", a + c, b + d), ("−", a - c, b - d)):
            предмет = f"({a}, {b}) {знак} ({c}, {d})"
            утв = f"{предмет} = ({x}, {y})."
            вон.append(утв)
            вон.append(спросить("value", предмет, утв))
            вон.append(спросить("значение", предмет, утв))
        k = 2 + (i % 4)
        пред_en = f"{k} × ({a}, {b})"
        пред_ru = f"{k} умножить на ({a}, {b})"
        утв_en = f"{пред_en} = ({k * a}, {k * b})."
        утв_ru = f"{пред_ru} даёт ({k * a}, {k * b})."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("value", пред_en, утв_en))
        вон.append(спросить("значение", пред_ru, утв_ru))
    return вон


def длины(шаг):
    вон = []
    for a, b, c in ТРОЙКИ:
        for x, y in ((a, b), (b, a)):
            пред_en, пред_ru = f"the vector ({x}, {y})", f"вектор ({x}, {y})"
            утв_en = f"{пред_en} has length {c}."
            утв_ru = f"{пред_ru} имеет длину {c}."
            вон.append(утв_en)
            вон.append(утв_ru)
            вон.append(спросить("length", пред_en, утв_en))
            вон.append(спросить("длина", f"вектора ({x}, {y})", утв_ru))
    return вон


def отказ_длины(шаг):
    """Вопрос, чей честный ответ — «целого нет, и вот почему».

    ДЛИНА ВЕКТОРА ЕСТЬ КОРЕНЬ, И КОРЕНЬ РЕДКО ЦЕЛ. Мир пишет длину
    только на точных тройках — таков его объявленный закон, — и отказ
    называет ОСНОВАНИЕ числом: сумму квадратов и то, что она не полный
    квадрат. Суд пересчитывает оба.
    """
    вон = []
    for i in range(16):
        a = 2 + (шаг + i) % 9
        b = a + 1 + (шаг * 3 + i) % 7
        с = a * a + b * b
        if полный_квадрат(с):
            continue
        вон.append(f"what is the length of the vector ({a}, {b})? no "
                   f"whole answer for ({a}, {b}): {a}^2 + {b}^2 = {с}, "
                   f"and {с} is not a perfect square.")
        вон.append(f"чему равна длина вектора ({a}, {b})? целого "
                   f"ответа нет для ({a}, {b}): {a}^2 + {b}^2 = {с}, "
                   f"а {с} не полный квадрат.")
    return вон


def произведения(шаг):
    вон = []
    for i in range(24):
        a, b = 1 + (i % 6) + шаг, 2 + (i % 5)
        c, d = 3 + (i % 4), 1 + (i % 7)
        пред_en = f"({a}, {b}) and ({c}, {d})"
        пред_ru = f"({a}, {b}) и ({c}, {d})"
        утв_en = f"the dot product of {пред_en} is {a * c + b * d}."
        утв_ru = (f"скалярное произведение {пред_ru} равно "
                  f"{a * c + b * d}.")
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("dot", пред_en, утв_en))
        вон.append(спросить("скалярное", пред_ru, утв_ru))
    return вон


def матрицы(шаг):
    вон = []
    for i in range(24):
        a, b = 1 + (i % 5) + шаг, 2 + (i % 4)
        c, d = 3 + (i % 3), 1 + (i % 6)
        пред_en = f"the matrix [{a} {b}; {c} {d}]"
        пред_ru = f"матрица [{a} {b}; {c} {d}]"
        утв_en = f"{пред_en} has determinant {a * d - b * c}."
        утв_ru = f"{пред_ru} имеет определитель {a * d - b * c}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("det", пред_en, утв_en))
        вон.append(спросить("определитель", f"матрицы [{a} {b}; {c} {d}]",
                            утв_ru))
        x, y = 1 + (i % 4), 2 + (i % 3)
        пр_en = f"[{a} {b}; {c} {d}] × ({x}, {y})"
        пр_ru = f"[{a} {b}; {c} {d}] умножить на ({x}, {y})"
        утв_п_en = f"{пр_en} = ({a * x + b * y}, {c * x + d * y})."
        утв_п_ru = f"{пр_ru} даёт ({a * x + b * y}, {c * x + d * y})."
        вон.append(утв_п_en)
        вон.append(утв_п_ru)
        вон.append(спросить("value", пр_en, утв_п_en))
        вон.append(спросить("значение", пр_ru, утв_п_ru))
    return вон


ГРУППЫ = (сложение, длины, отказ_длины, произведения, матрицы)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_linalg.txt", pass_groups)


if __name__ == "__main__":
    main()
