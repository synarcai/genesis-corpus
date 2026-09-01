#!/usr/bin/env python3
"""GENESIS layer: THE FOUNDATIONS OF ALGORITHMS.

    sorting 3 1 2 gives 1 2 3.
    сортировка 3 1 2 даёт 1 2 3.
    the gcd of 12 and 18 is 6.
    binary search on 8 items takes at most 3 steps.

EVERY SHOW IS EXACTLY CHECKABLE, AND ITS CHECKER IS IN THE REPOSITORY
(`scripts/algo_court.py`). A corpus meant to raise an engineer cannot
contain a claim nobody can verify: an unverifiable show teaches the
form of knowledge without its substance, and the organism owns the
form.

SEVEN GENERA, chosen because each is a foundation something else
stands on:
  · list operations — order, extremum, aggregate, size;
  · number theory — gcd, lcm, primality, factorial, power;
  · recursion — fibonacci by its index;
  · COMPLEXITY — linear search costs n, binary search costs
    ceil(log2 n): the first fact of engineering, and the one that
    makes an algorithm a choice rather than a habit;
  · data structures — stack takes the last, queue takes the first;
  · positional notation — the same number in base two;
  · division with quotient and remainder, in the algorithmic surface.

TWO SURFACES (en, ru) on separate lines, never one: a line carrying
two scripts is a splice, and the language census counts it as such.
Numbers stay figures — this layer teaches operations, not numerals.
"""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

LISTS = [
    [3, 1, 2], [5, 4], [7, 2, 9, 1], [6, 6, 2], [8, 3, 5, 1, 9],
    [4, 10, 7], [2, 8], [9, 5, 3, 7], [1, 4, 2, 6], [10, 3, 8],
]
PAIRS = [(12, 18), (8, 12), (9, 6), (14, 21), (10, 15),
         (16, 24), (5, 15), (18, 27), (7, 14), (20, 30)]
SMALL = [5, 6, 7, 8, 9, 10, 11, 12, 13, 15]
POWERS = [(2, 5), (3, 3), (2, 8), (5, 2), (4, 3),
          (2, 6), (3, 4), (10, 2), (2, 10), (6, 2)]
SIZES = [2, 4, 8, 16, 32, 64, 3, 5, 10, 20]


def spaced(xs):
    return " ".join(str(x) for x in xs)


def pass_shows(pass_i):
    out = []
    k = len(LISTS)
    for i in range(k):
        xs = LISTS[(pass_i + i) % k]
        a, b = PAIRS[(pass_i * 3 + i) % len(PAIRS)]
        n = SMALL[(pass_i * 2 + i) % len(SMALL)]
        base, exp = POWERS[(pass_i + i * 3) % len(POWERS)]
        size = SIZES[(pass_i * 5 + i) % len(SIZES)]
        # --- list operations
        out.append(f"sorting {spaced(xs)} gives {spaced(sorted(xs))}.")
        out.append(f"сортировка {spaced(xs)} даёт {spaced(sorted(xs))}.")
        out.append(f"reversing {spaced(xs)} gives {spaced(xs[::-1])}.")
        out.append(f"разворот {spaced(xs)} даёт {spaced(xs[::-1])}.")
        out.append(f"the maximum of {spaced(xs)} is {max(xs)}.")
        out.append(f"максимум {spaced(xs)} равен {max(xs)}.")
        out.append(f"the minimum of {spaced(xs)} is {min(xs)}.")
        out.append(f"минимум {spaced(xs)} равен {min(xs)}.")
        out.append(f"the sum of {spaced(xs)} is {sum(xs)}.")
        out.append(f"сумма {spaced(xs)} равна {sum(xs)}.")
        out.append(f"the length of {spaced(xs)} is {len(xs)}.")
        out.append(f"длина {spaced(xs)} равна {len(xs)}.")
        # --- number theory
        out.append(f"the gcd of {a} and {b} is {math.gcd(a, b)}.")
        out.append(f"нод {a} и {b} равен {math.gcd(a, b)}.")
        out.append(f"the lcm of {a} and {b} is {a * b // math.gcd(a, b)}.")
        out.append(f"нок {a} и {b} равен {a * b // math.gcd(a, b)}.")
        простое = n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
        out.append(f"{n} is prime." if простое else f"{n} is not prime.")
        out.append(f"{n} простое." if простое else f"{n} не простое.")
        out.append(f"the factorial of {min(n, 8)} is {math.factorial(min(n, 8))}.")
        out.append(f"факториал {min(n, 8)} равен {math.factorial(min(n, 8))}.")
        out.append(f"{base} to the power {exp} is {base ** exp}.")
        out.append(f"{base} в степени {exp} равно {base ** exp}.")
        # --- recursion by index
        фиб = [0, 1]
        while len(фиб) <= n:
            фиб.append(фиб[-1] + фиб[-2])
        out.append(f"fibonacci number {n} is {фиб[n]}.")
        out.append(f"число фибоначчи номер {n} равно {фиб[n]}.")
        # --- complexity, the first fact of engineering
        шагов = math.ceil(math.log2(size)) if size > 1 else 1
        out.append(
            f"linear search on {size} {by_count(size, 'items')} takes at "
            f"most {size} {by_count(size, 'steps')}.")
        out.append(
            f"линейный поиск по {size} элементам требует не более "
            f"{size} шагов.")
        out.append(
            f"binary search on {size} {by_count(size, 'items')} takes at "
            f"most {шагов} {by_count(шагов, 'steps')}.")
        out.append(
            f"двоичный поиск по {size} элементам требует не более "
            f"{шагов} шагов.")
        # --- data structures: what comes back first
        out.append(
            f"pushing {spaced(xs)} on a stack and popping gives {xs[-1]}.")
        out.append(
            f"положив {spaced(xs)} в стек и сняв, получаем {xs[-1]}.")
        out.append(
            f"adding {spaced(xs)} to a queue and taking gives {xs[0]}.")
        out.append(
            f"добавив {spaced(xs)} в очередь и взяв, получаем {xs[0]}.")
        # --- positional notation
        out.append(f"{n} in binary is {n:b}.")
        out.append(f"{n} в двоичной записи это {n:b}.")
        # --- quotient and remainder, the algorithmic surface
        q, r = divmod(a, b) if a >= b else divmod(b, a)
        hi, lo = (a, b) if a >= b else (b, a)
        out.append(
            f"dividing {hi} by {lo} gives quotient {q} and remainder {r}.")
        out.append(
            f"деление {hi} на {lo} даёт частное {q} и остаток {r}.")
    return out


def main():
    emit("datasets/genesis_algorithms.txt", pass_shows)


if __name__ == "__main__":
    main()
