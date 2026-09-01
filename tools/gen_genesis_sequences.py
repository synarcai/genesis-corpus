#!/usr/bin/env python3
"""GENESIS layer: SEQUENCES — progression, limit, rate of change.

Three subjects the syllabus court named absent: progression, limit, and
derivative. They are one family: a sequence with a law, what it tends
to, and how fast it changes. Without them the corpus knows numbers but
not PROCESSES, and every science is about processes.

EXACTNESS IS KEPT BY CHOICE OF EXAMPLE, NOT BY ROUNDING. The limit is
shown on sequences whose terms are exact fractions and whose limit is
an integer; the derivative on polynomials where the difference
quotient is exact. A corpus that says «approximately» teaches
approximation, and the arithmetic court would rightly call it false.
"""

import sys
import pathlib
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402

ДЛИНА = 4


def арифметические(шаг):
    """Прогрессия названа началом и шагом; члены выведены."""
    вон = []
    for i in range(24):
        a, d = 2 + i + шаг, 2 + (i % 5)
        члены = [a + k * d for k in range(ДЛИНА)]
        если = " ".join(str(x) for x in члены)
        n = ДЛИНА + 1
        вон.append(f"the arithmetic progression from {a} with step {d} "
                   f"gives {если}.")
        вон.append(f"арифметическая прогрессия от {a} с шагом {d} "
                   f"даёт {если}.")
        # ПОКАЗ САМОДОСТАТОЧЕН: «её член номер 5» без своей прогрессии
        # не значит ничего, а перестановка проходов разводит соседей.
        вон.append(f"term number {n} of the progression from {a} "
                   f"with step {d} is {a + (n - 1) * d}.")
        вон.append(f"член номер {n} прогрессии от {a} с шагом {d} "
                   f"равен {a + (n - 1) * d}.")
        вон.append(f"the sum of {если} is {sum(члены)}.")
        вон.append(f"сумма {если} равна {sum(члены)}.")
    return вон


def геометрические(шаг):
    """Отношение вместо разности — тот же закон, другое действие."""
    вон = []
    for i in range(20):
        a, q = 1 + (i % 5) + шаг, 2 + (i % 3)
        члены = [a * q ** k for k in range(ДЛИНА)]
        если = " ".join(str(x) for x in члены)
        вон.append(f"the geometric progression from {a} with ratio {q} "
                   f"gives {если}.")
        вон.append(f"геометрическая прогрессия от {a} со знаменателем {q} "
                   f"даёт {если}.")
    return вон


def пределы(шаг):
    """Бесконечный процесс с конечным итогом — на точных дробях."""
    вон = []
    for i in range(16):
        q = 2 + (i % 4)
        члены = [Fraction(1, q ** k) for k in range(1, ДЛИНА + 1)]
        если = " ".join(f"{x.numerator}/{x.denominator}" for x in члены)
        вон.append(f"the sequence {если} has limit 0.")
        вон.append(f"последовательность {если} имеет предел 0.")
        # сумма геометрического ряда: a/(1-q) при a = 1/q
        сумма = Fraction(1, q - 1)
        вон.append(f"the sum of the whole series {если} ... is "
                   f"{сумма.numerator}/{сумма.denominator}.")
        вон.append(f"сумма всего ряда {если} ... равна "
                   f"{сумма.numerator}/{сумма.denominator}.")
    return вон


def производные(шаг):
    """Скорость изменения — разностным отношением и законом степени."""
    вон = []
    for i in range(20):
        x = 1 + (i % 8) + шаг
        # f(t) = t^2: точное разностное отношение на шаге 1
        было, стало = x * x, (x + 1) * (x + 1)
        вон.append(f"for f(t) = t^2 the change from {x} to {x + 1} "
                   f"is {стало - было}.")
        вон.append(f"для f(t) = t^2 изменение от {x} до {x + 1} "
                   f"равно {стало - было}.")
        вон.append(f"the derivative of t^2 at {x} is {2 * x}.")
        вон.append(f"производная t^2 в точке {x} равна {2 * x}.")
        вон.append(f"the derivative of t^3 at {x} is {3 * x * x}.")
        вон.append(f"производная t^3 в точке {x} равна {3 * x * x}.")
    return вон


ГРУППЫ = (арифметические, геометрические, пределы, производные)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_sequences.txt", pass_groups)


if __name__ == "__main__":
    main()
