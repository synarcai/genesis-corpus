#!/usr/bin/env python3
"""GENESIS layer: NUMBER THEORY — primes, factorisation, congruence.

The syllabus court named three subjects absent from the whole corpus:
factorisation into primes, congruence modulo n, and the notion of a
prime itself. They are not decoration: unique factorisation is the
first structural theorem a mathematician meets, and congruence is the
first equivalence relation that is not equality.

EVERY LINE IS COMPUTED, NEVER WRITTEN. The divisor list, the
factorisation, the residue — all derived here and re-derived by
`courts/number_court.py`, which factorises again rather than trusting
the text. A layer that states a factorisation it did not compute
teaches the organism to trust a number nobody checked.

THREE SURFACES, TWO LANGUAGES: the glyph form («17 mod 5 = 2»), the
Russian sentence and the English sentence say ONE fact, and the court
judges all three by the same computation.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402


def делители(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def простое(n):
    return n > 1 and len(делители(n)) == 2


def разложение(n):
    вон, d = [], 2
    while d * d <= n:
        while n % d == 0:
            вон.append(d)
            n //= d
        d += 1
    if n > 1:
        вон.append(n)
    return вон


def простые(шаг):
    """Простое и составное — каждое со своим свидетельством."""
    вон = []
    for n in range(2, 30):
        if простое(n):
            вон.append(f"{n} is prime; its divisors are 1 and {n}.")
            вон.append(f"{n} простое; его делители — 1 и {n}.")
        else:
            м = разложение(n)
            вон.append(f"{n} is not prime; {n} = {м[0]} × {n // м[0]}.")
            вон.append(f"{n} составное; {n} = {м[0]} × {n // м[0]}.")
    return вон


def разложения(шаг):
    """Всякое число есть произведение простых — и произведение сходится."""
    вон = []
    for n in range(4, 40):
        м = разложение(n)
        если = " × ".join(str(x) for x in м)
        вон.append(f"{n} factorises into {если}.")
        вон.append(f"{n} раскладывается в {если}.")
    return вон


def делители_числа(шаг):
    """Список делителей назван целиком и проверяем целиком."""
    вон = []
    for n in range(6, 30):
        если = " ".join(str(d) for d in делители(n))
        вон.append(f"the divisors of {n} are {если}.")
        вон.append(f"делители {n} — это {если}.")
    return вон


def сравнения(шаг):
    """Остаток есть отношение, а не только действие."""
    вон = []
    for i in range(24):
        a, m = 7 + i * 3 + шаг, 2 + (i % 7)
        r = a % m
        вон.append(f"{a} mod {m} = {r}.")
        вон.append(f"{a} по модулю {m} равно {r}.")
        вон.append(f"{a} and {r} are congruent modulo {m}.")
        вон.append(f"{a} и {r} сравнимы по модулю {m}.")
    return вон


def взаимно_простые(шаг):
    """Взаимная простота есть НОД, равный единице."""
    from math import gcd
    вон = []
    for i in range(20):
        a, b = 4 + i + шаг, 9 + i * 2
        если = "coprime" if gcd(a, b) == 1 else "not coprime"
        ру = "взаимно просты" if gcd(a, b) == 1 else "не взаимно просты"
        вон.append(f"{a} and {b} are {если}; their gcd is {gcd(a, b)}.")
        вон.append(f"{a} и {b} {ру}; их нод равен {gcd(a, b)}.")
    return вон


ГРУППЫ = (простые, разложения, делители_числа, сравнения, взаимно_простые)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_numbers.txt", pass_groups)


if __name__ == "__main__":
    main()
