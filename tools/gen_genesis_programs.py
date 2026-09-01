#!/usr/bin/env python3
"""GENESIS layer: THE SEMANTICS OF A PROGRAM.

    let a = 7; let b = 3; let c = a * b; c = 21.
    if 3 < 5 then y = 1 else y = 2; y = 1.
    sum for i from 1 to 4 is 10.
    function f(n) = n * 2; f(5) = 10.
    factorial(5) = 120.

A programmer is not raised on the NAMES of constructs but on what they
DO. So every show here is a small program together with its result, and
`courts/program_court.py` does not parse the claim — it RUNS the
program and compares. A construct the court cannot execute is a
construct this layer does not show.

SIX CONSTRUCTS, each the smallest thing that cannot be reduced to the
previous one:
  · BINDING — a name holds a value, and later names see it;
  · ARITHMETIC over bound names, with precedence;
  · CONDITIONAL — the branch not taken must not be shown as taken;
  · BOUNDED LOOP — a sum and a product over a range, so that iteration
    is met as an accumulation and not as a word;
  · FUNCTION — a name for a computation, applied to an argument;
  · RECURSION — a function whose definition names itself, shown with
    its base case, because a recursion without a base is not a program
    but a hang.

Descriptions come in English and Russian on separate lines; the program
text itself is the same in both, because a program is not written in a
natural language and pretending otherwise would teach a falsehood.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit  # noqa: E402

СВЯЗКИ = [(7, 3, "*"), (9, 4, "+"), (12, 5, "-"), (6, 6, "*"),
          (15, 3, "-"), (8, 7, "+"), (20, 4, "*"), (11, 2, "-")]
УСЛОВИЯ = [(3, 5, "<"), (7, 5, "<"), (4, 4, "<"), (9, 2, ">"),
           (1, 8, ">"), (6, 6, ">"), (2, 9, "<"), (10, 3, ">")]
ДИАПАЗОНЫ = [(1, 4), (1, 5), (2, 5), (1, 6), (3, 6), (1, 3), (2, 4), (1, 7)]
ФУНКЦИИ = [("f", "n * 2", 5), ("g", "n + 7", 4), ("h", "n * n", 6),
           ("p", "n - 3", 9), ("q", "n * 3", 7), ("r", "n + n", 8),
           ("s", "n * 5", 3), ("t", "n - 1", 12)]
ФАКТОРИАЛ = [3, 4, 5, 6, 3, 4, 5, 6]


def pass_shows(pass_i):
    out = []
    for i in range(8):
        a, b, op = СВЯЗКИ[(pass_i + i) % len(СВЯЗКИ)]
        x, y, знак = УСЛОВИЯ[(pass_i * 3 + i) % len(УСЛОВИЯ)]
        lo, hi = ДИАПАЗОНЫ[(pass_i * 5 + i) % len(ДИАПАЗОНЫ)]
        имя, тело, арг = ФУНКЦИИ[(pass_i + i * 3) % len(ФУНКЦИИ)]
        n = ФАКТОРИАЛ[(pass_i * 2 + i) % len(ФАКТОРИАЛ)]
        значение = {"*": a * b, "+": a + b, "-": a - b}[op]
        # --- связывание и арифметика над именами
        out.append(f"let a = {a}; let b = {b}; let c = a {op} b; "
                   f"c = {значение}.")
        out.append(f"a binding gives a name to a value; here c is "
                   f"{значение}.")
        out.append(f"связывание даёт имя значению; здесь c равно "
                   f"{значение}.")
        # --- ветвление: невзятая ветвь не должна выглядеть взятой
        верно = (x < y) if знак == "<" else (x > y)
        out.append(f"if {x} {знак} {y} then y = 1 else y = 2; "
                   f"y = {1 if верно else 2}.")
        out.append(f"the branch not taken changes nothing; y = "
                   f"{1 if верно else 2}.")
        # --- ограниченный цикл как накопление
        сумма = sum(range(lo, hi + 1))
        произв = 1
        for k in range(lo, hi + 1):
            произв *= k
        out.append(f"sum for i from {lo} to {hi} is {сумма}.")
        out.append(f"сумма для i от {lo} до {hi} равна {сумма}.")
        out.append(f"product for i from {lo} to {hi} is {произв}.")
        out.append(f"произведение для i от {lo} до {hi} равно {произв}.")
        # --- функция как имя вычисления
        итог = {"n * 2": арг * 2, "n + 7": арг + 7, "n * n": арг * арг,
                "n - 3": арг - 3, "n * 3": арг * 3, "n + n": арг + арг,
                "n * 5": арг * 5, "n - 1": арг - 1}[тело]
        out.append(f"function {имя}(n) = {тело}; {имя}({арг}) = {итог}.")
        out.append(f"функция {имя}(n) = {тело}; {имя}({арг}) = {итог}.")
        # --- рекурсия, всегда со своим основанием
        факт = 1
        for k in range(2, n + 1):
            факт *= k
        out.append(f"factorial(0) = 1; factorial(n) = n * factorial(n - 1); "
                   f"factorial({n}) = {факт}.")
        out.append(f"рекурсия без основания есть зависание, а не "
                   f"программа; factorial(0) = 1.")
    return out


def main():
    emit("datasets/genesis_programs.txt", pass_shows)


if __name__ == "__main__":
    main()
