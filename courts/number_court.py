#!/usr/bin/env python3
"""[ЧИСЛА] — суд РАСКЛАДЫВАЕТ заново, а не читает разложение.

    12 factorises into 2 × 2 × 3.      → суд раскладывает 12 сам
    the divisors of 12 are 1 2 3 4 6 12. → суд перебирает делители сам
    17 and 2 are congruent modulo 5.   → суд берёт оба остатка сам

ПРОСТОТА ЕСТЬ УТВЕРЖДЕНИЕ О ВСЕХ ДЕЛИТЕЛЯХ, а не о названных двух:
«9 is prime; its divisors are 1 and 9» безупречно по форме и ложно —
тройка не названа, и потому список делителей ПЕРЕСЧИТЫВАЕТСЯ целиком,
а не сверяется с тем, что показ о себе говорит.

СВИДЕТЕЛЬСТВО СОСТАВНОГО ПРОВЕРЯЕТСЯ ПРОИЗВЕДЕНИЕМ: «18 составное;
18 = 2 × 9» истинно лишь тогда, когда произведение сходится И оба
множителя больше единицы — иначе всякое число «составное» через 1 × n.
"""
import pathlib
import re
import sys
from math import gcd

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

# СЕМЕЙСТВО ЕСТЬ РОД (М-146): ответ на «простое ли?» — то же утверждение
# со словом вердикта впереди (М-147); слово согласно образцу по построению
# («да» стоит лишь перед простым, «нет» — перед составным), суд считает
# делители, а не верит слову.
ПРОСТОЕ = re.compile(
    r"^(?:(?:yes|да): )?(\d+) (?:is prime; its divisors are|простое; его делители —) "
    r"1 (?:and|и) (\d+)\.$")
СОСТАВНОЕ = re.compile(
    r"^(?:(?:no|нет): )?(\d+) (?:is not prime|составное); \1 = (\d+) × (\d+)\.$")
РАЗЛОЖЕНИЕ = re.compile(
    r"^(\d+) (?:factorises into|раскладывается в) ([\d ×]+)\.$")
ДЕЛИТЕЛИ = re.compile(
    r"^(?:the divisors of (\d+) are|делители (\d+) — это) ([\d ]+)\.$")
ОСТАТОК = re.compile(
    r"^(\d+) (?:mod (\d+) =|по модулю (\d+) равно) (\d+)\.$")
СРАВНИМЫ = re.compile(
    r"^(\d+) (?:and (\d+) are congruent modulo|и (\d+) сравнимы по модулю) "
    r"(\d+)\.$")
# ВТОРАЯ ПОЛЯРНОСТЬ: «не сравнимы» истинно ровно тогда, когда остатки
# разные, и оба остатка суд считает сам.
НЕ_СРАВНИМЫ = re.compile(
    r"^(\d+) (?:and (\d+) are not congruent modulo (\d+): (\d+) mod (\d+) = (\d+), (\d+) mod (\d+) = (\d+)"
    r"|и (\d+) не сравнимы по модулю (\d+): (\d+) по модулю (\d+) равно (\d+), (\d+) по модулю (\d+) равно (\d+))\.$")
# НИ ТО НИ ДРУГОЕ: у единицы делитель один, и она не проста и не
# составна. Отказ истинен ровно тогда, когда делитель и вправду один.
НИ_ТО_НИ_ДРУГОЕ = re.compile(
    r"^(\d+) (?:is neither prime nor composite: its only divisor is"
    r"|ни простое, ни составное: его единственный делитель —) (\d+)\.$")
ВЗАИМНО = re.compile(
    r"^(\d+) (?:and|и) (\d+) (?:are (coprime|not coprime); their gcd is"
    r"|(взаимно просты|не взаимно просты); их нод равен) (\d+)\.$")


def делители_числа(n):
    """Все делители, перебором — суд считает, а не верит."""
    return [d for d in range(1, n + 1) if n % d == 0]


def разложить(n):
    вон, d = [], 2
    while d * d <= n:
        while n % d == 0:
            вон.append(d)
            n //= d
        d += 1
    if n > 1:
        вон.append(n)
    return вон


import laws  # noqa: E402
ЗАКОНЫ = laws.свод("numbers")


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if с in ЗАКОНЫ:
        return True, True
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ, а связь половин — общим домом
    # `tools/asking.py`: величины вопроса суть начальный отрезок
    # величин ответа, и порча любой из них рвёт пару.
    если = asking.судить_парой(с, судить)
    if если is not None:
        return если
    m = ПРОСТОЕ.match(с)
    if m:
        n, названный = int(m.group(1)), int(m.group(2))
        return True, делители_числа(n) == [1, n] and названный == n
    m = СОСТАВНОЕ.match(с)
    if m:
        n, a, b = (int(г) for г in m.groups())
        return True, (a * b == n and a > 1 and b > 1
                      and делители_числа(n) != [1, n])
    m = РАЗЛОЖЕНИЕ.match(с)
    if m:
        n = int(m.group(1))
        названо = [int(x) for x in m.group(2).split("×")]
        return True, названо == разложить(n)
    m = ДЕЛИТЕЛИ.match(с)
    if m:
        n = int(m.group(1) or m.group(2))
        названо = [int(x) for x in m.group(3).split()]
        return True, названо == делители_числа(n)
    m = ОСТАТОК.match(с)
    if m:
        a = int(m.group(1))
        мод = int(m.group(2) or m.group(3))
        r = int(m.group(4))
        return True, мод > 0 and a % мод == r
    m = СРАВНИМЫ.match(с)
    if m:
        a = int(m.group(1))
        b = int(m.group(2) or m.group(3))
        мод = int(m.group(4))
        return True, мод > 0 and a % мод == b % мод
    m = НЕ_СРАВНИМЫ.match(с)
    if m:
        г = [int(x) for x in m.groups() if x is not None]
        a, b, мод, a2, м2, r1, b2, м3, r2 = г
        return True, (мод > 0 and (a2, м2, b2, м3) == (a, мод, b, мод)
                      and r1 == a % мод and r2 == b % мод and r1 != r2)
    m = НИ_ТО_НИ_ДРУГОЕ.match(с)
    if m:
        n, единственный = int(m.group(1)), int(m.group(2))
        return True, (делители_числа(n) == [n] and единственный == n)
    m = ВЗАИМНО.match(с)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        сказано = m.group(3) or m.group(4)
        нод = int(m.group(5))
        взаимно = сказано in ("coprime", "взаимно просты")
        return True, нод == gcd(a, b) and взаимно == (gcd(a, b) == 1)
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ЧИСЛА ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ЧИСЛА ОТКАЗ: обход пуст, судить нечего")
        return 2
    ложных = судимых = 0
    примеры = []
    for путь in пути:
        свои = 0
        with путь.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                судимо, истинно = судить(строка)
                if not судимо:
                    continue
                судимых += 1
                if not истинно:
                    ложных += 1
                    свои += 1
                    if len(примеры) < 4:
                        примеры.append(f"{путь.name}: {строка.strip()[:80]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ЧИСЛА {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
