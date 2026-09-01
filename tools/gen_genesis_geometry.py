#!/usr/bin/env python3
"""GENESIS layer: GEOMETRY — measure of a figure, derived not measured.

The syllabus court named area, volume and the Pythagorean theorem
absent. A corpus that knows units but not FIGURES knows how to say a
length and not how to earn one: the area of a rectangle is not
measured, it is DERIVED from two lengths, and that derivation is the
first place where multiplication means something other than repeated
counting.

PYTHAGORAS IS SHOWN ON EXACT TRIPLES ONLY. A hypotenuse of √2 is true
and unwritable here: the corpus states what it can check, and an
approximation named as an equality would be a lie of the same kind as
«5 ÷ 2 = 2».
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

# ТРОЙКИ НАЗВАНЫ, А НЕ НАЙДЕНЫ ПЕРЕБОРОМ: каждая проверена здесь же.
ТРОЙКИ = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15),
          (8, 15, 17), (7, 24, 25), (20, 21, 29), (12, 16, 20))
assert all(a * a + b * b == c * c for a, b, c in ТРОЙКИ)


def прямоугольники(шаг):
    вон = []
    for i in range(24):
        a, b = 2 + (i % 9) + шаг, 3 + (i % 7)
        вон.append(f"a rectangle {a} by {b} has area {a * b} "
                   f"and perimeter {2 * (a + b)}.")
        вон.append(f"прямоугольник {a} на {b} имеет площадь {a * b} "
                   f"и периметр {2 * (a + b)}.")
    return вон


def квадраты(шаг):
    вон = []
    for i in range(16):
        a = 2 + (i % 12) + шаг
        вон.append(f"a square with side {a} has area {a * a} "
                   f"and perimeter {4 * a}.")
        вон.append(f"квадрат со стороной {a} имеет площадь {a * a} "
                   f"и периметр {4 * a}.")
    return вон


def треугольники(шаг):
    """Площадь через основание и высоту — только при чётном произведении."""
    вон = []
    for i in range(20):
        b, h = 2 + (i % 10) + шаг, 4 + (i % 6)
        if (b * h) % 2:
            b += 1
        вон.append(f"a triangle with base {b} and height {h} "
                   f"has area {b * h // 2}.")
        вон.append(f"треугольник с основанием {b} и высотой {h} "
                   f"имеет площадь {b * h // 2}.")
    return вон


def пифагор(шаг):
    вон = []
    for a, b, c in ТРОЙКИ:
        вон.append(f"a right triangle with legs {a} and {b} "
                   f"has hypotenuse {c}.")
        вон.append(f"прямоугольный треугольник с катетами {a} и {b} "
                   f"имеет гипотенузу {c}.")
        вон.append(f"{a}^2 + {b}^2 = {c}^2.")
    return вон


def тела(шаг):
    вон = []
    for i in range(20):
        a, b, c = 2 + (i % 5) + шаг, 3 + (i % 4), 2 + (i % 6)
        вон.append(f"a box {a} by {b} by {c} has volume {a * b * c} "
                   f"and surface {2 * (a * b + b * c + a * c)}.")
        вон.append(f"коробка {a} на {b} на {c} имеет объём {a * b * c} "
                   f"и поверхность {2 * (a * b + b * c + a * c)}.")
        вон.append(f"a cube with edge {a} has volume {a ** 3}.")
        вон.append(f"куб с ребром {a} имеет объём {a ** 3}.")
    return вон


ГРУППЫ = (прямоугольники, квадраты, треугольники, пифагор, тела)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_geometry.txt", pass_groups)


if __name__ == "__main__":
    main()
