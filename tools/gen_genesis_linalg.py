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

ТРОЙКИ = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17),
          (9, 12, 15), (7, 24, 25))
assert all(a * a + b * b == c * c for a, b, c in ТРОЙКИ)


def сложение(шаг):
    вон = []
    for i in range(24):
        a, b = 1 + (i % 7) + шаг, 2 + (i % 5)
        c, d = 3 + (i % 4), 1 + (i % 6)
        вон.append(f"({a}, {b}) + ({c}, {d}) = ({a + c}, {b + d}).")
        вон.append(f"({a}, {b}) − ({c}, {d}) = ({a - c}, {b - d}).")
        k = 2 + (i % 4)
        вон.append(f"{k} × ({a}, {b}) = ({k * a}, {k * b}).")
        вон.append(f"{k} умножить на ({a}, {b}) даёт ({k * a}, {k * b}).")
    return вон


def длины(шаг):
    вон = []
    for a, b, c in ТРОЙКИ:
        вон.append(f"the vector ({a}, {b}) has length {c}.")
        вон.append(f"вектор ({a}, {b}) имеет длину {c}.")
        вон.append(f"the vector ({b}, {a}) has length {c}.")
        вон.append(f"вектор ({b}, {a}) имеет длину {c}.")
    return вон


def произведения(шаг):
    вон = []
    for i in range(24):
        a, b = 1 + (i % 6) + шаг, 2 + (i % 5)
        c, d = 3 + (i % 4), 1 + (i % 7)
        вон.append(f"the dot product of ({a}, {b}) and ({c}, {d}) "
                   f"is {a * c + b * d}.")
        вон.append(f"скалярное произведение ({a}, {b}) и ({c}, {d}) "
                   f"равно {a * c + b * d}.")
    return вон


def матрицы(шаг):
    вон = []
    for i in range(24):
        a, b = 1 + (i % 5) + шаг, 2 + (i % 4)
        c, d = 3 + (i % 3), 1 + (i % 6)
        вон.append(f"the matrix [{a} {b}; {c} {d}] has determinant "
                   f"{a * d - b * c}.")
        вон.append(f"матрица [{a} {b}; {c} {d}] имеет определитель "
                   f"{a * d - b * c}.")
        x, y = 1 + (i % 4), 2 + (i % 3)
        вон.append(f"[{a} {b}; {c} {d}] × ({x}, {y}) = "
                   f"({a * x + b * y}, {c * x + d * y}).")
        вон.append(f"[{a} {b}; {c} {d}] умножить на ({x}, {y}) даёт "
                   f"({a * x + b * y}, {c * x + d * y}).")
    return вон


ГРУППЫ = (сложение, длины, произведения, матрицы)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_linalg.txt", pass_groups)


if __name__ == "__main__":
    main()
