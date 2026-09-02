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

# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт те же
# величины, из которых собран ответ. Замер вопросной поверхности назвал
# этот мир немым: 1560 строк, вопросов ноль — он сообщал, что 7 простое,
# и ни разу не спрашивал, простое ли 7.
СПРОСИТЬ = {
    "prime": "is {n} prime?",
    "factorise": "what does {n} factorise into?",
    "divisors": "what are the divisors of {n}?",
    "mod": "what is {a} mod {m}?",
    "congruent": "are {a} and {b} congruent modulo {m}?",
    "coprime": "are {a} and {b} coprime?",
    "простое": "простое ли {n}?",
    "разложение": "во что раскладывается {n}?",
    "делители": "каковы делители {n}?",
    "остаток": "чему равно {a} по модулю {m}?",
    "сравнимы": "сравнимы ли {a} и {b} по модулю {m}?",
    "взаимно": "взаимно ли просты {a} и {b}?",
}


def спросить(искомое, ответ, **части):
    """Вопрос и ответ одной строкой; величины у них одни и те же."""
    return f"{СПРОСИТЬ[искомое].format(**части)} {ответ}"


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
            утв_en = f"{n} is prime; its divisors are 1 and {n}."
            утв_ru = f"{n} простое; его делители — 1 и {n}."
        else:
            м = разложение(n)
            утв_en = f"{n} is not prime; {n} = {м[0]} × {n // м[0]}."
            утв_ru = f"{n} составное; {n} = {м[0]} × {n // м[0]}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("prime", утв_en, n=n))
        вон.append(спросить("простое", утв_ru, n=n))
    return вон


def ни_то_ни_другое(шаг):
    """Отказ с основанием: единица не проста и не составна.

    ВОПРОС, НА КОТОРЫЙ ЧЕСТНЫЙ ОТВЕТ — «НИ ТО НИ ДРУГОЕ». Простое имеет
    ровно два делителя, составное — больше двух; у единицы делитель
    ОДИН, и она не попадает ни в один род. Основание названо числом, и
    суд пересчитывает его тем же перебором делителей, каким судит
    простоту.
    """
    n = 1
    return [
        f"{СПРОСИТЬ['prime'].format(n=n)} {n} is neither prime nor "
        f"composite: its only divisor is {n}.",
        f"{СПРОСИТЬ['простое'].format(n=n)} {n} ни простое, ни "
        f"составное: его единственный делитель — {n}.",
    ]


def разложения(шаг):
    """Всякое число есть произведение простых — и произведение сходится."""
    вон = []
    for n in range(4, 40):
        м = разложение(n)
        если = " × ".join(str(x) for x in м)
        утв_en = f"{n} factorises into {если}."
        утв_ru = f"{n} раскладывается в {если}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("factorise", утв_en, n=n))
        вон.append(спросить("разложение", утв_ru, n=n))
    return вон


def делители_числа(шаг):
    """Список делителей назван целиком и проверяем целиком."""
    вон = []
    for n in range(6, 30):
        если = " ".join(str(d) for d in делители(n))
        утв_en = f"the divisors of {n} are {если}."
        утв_ru = f"делители {n} — это {если}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("divisors", утв_en, n=n))
        вон.append(спросить("делители", утв_ru, n=n))
    return вон


def сравнения(шаг):
    """Остаток есть отношение, а не только действие."""
    вон = []
    for i in range(24):
        a, m = 7 + i * 3 + шаг, 2 + (i % 7)
        r = a % m
        утв_о_en, утв_о_ru = (f"{a} mod {m} = {r}.",
                              f"{a} по модулю {m} равно {r}.")
        утв_с_en = f"{a} and {r} are congruent modulo {m}."
        утв_с_ru = f"{a} и {r} сравнимы по модулю {m}."
        вон.append(утв_о_en)
        вон.append(утв_о_ru)
        вон.append(утв_с_en)
        вон.append(утв_с_ru)
        вон.append(спросить("mod", утв_о_en, a=a, m=m))
        вон.append(спросить("остаток", утв_о_ru, a=a, m=m))
        вон.append(спросить("congruent", утв_с_en, a=a, b=r, m=m))
        вон.append(спросить("сравнимы", утв_с_ru, a=a, b=r, m=m))
        # ВТОРАЯ ПОЛЯРНОСТЬ ТОЙ ЖЕ РАМКОЙ (аудит покупок holon 03.09):
        # 120 показов «сравнимы» без единого «нет» — форма без
        # фальсификатора. Несравнимое число — соседний остаток.
        b2 = r + 1 if r + 1 < m else r - 1
        нет_en = (f"{a} and {b2} are not congruent modulo {m}: "
                  f"{a} mod {m} = {r}, {b2} mod {m} = {b2 % m}.")
        нет_ru = (f"{a} и {b2} не сравнимы по модулю {m}: "
                  f"{a} по модулю {m} равно {r}, {b2} по модулю {m} равно {b2 % m}.")
        вон.append(нет_en)
        вон.append(нет_ru)
        вон.append(спросить("congruent", нет_en, a=a, b=b2, m=m))
        вон.append(спросить("сравнимы", нет_ru, a=a, b=b2, m=m))
    return вон


def взаимно_простые(шаг):
    """Взаимная простота есть НОД, равный единице."""
    from math import gcd
    вон = []
    for i in range(20):
        a, b = 4 + i + шаг, 9 + i * 2
        если = "coprime" if gcd(a, b) == 1 else "not coprime"
        ру = "взаимно просты" if gcd(a, b) == 1 else "не взаимно просты"
        утв_en = f"{a} and {b} are {если}; their gcd is {gcd(a, b)}."
        утв_ru = f"{a} и {b} {ру}; их нод равен {gcd(a, b)}."
        вон.append(утв_en)
        вон.append(утв_ru)
        вон.append(спросить("coprime", утв_en, a=a, b=b))
        вон.append(спросить("взаимно", утв_ru, a=a, b=b))
    return вон


import laws  # noqa: E402


def законы(pass_i):
    """Ступень определений фразами рода (дом законов, 03.09)."""
    return laws.ступень("numbers")


ГРУППЫ = (простые, ни_то_ни_другое, разложения, делители_числа,
          сравнения, взаимно_простые, законы)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_numbers.txt", pass_groups)


if __name__ == "__main__":
    main()
