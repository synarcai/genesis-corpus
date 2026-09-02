#!/usr/bin/env python3
"""[ПОСЛЕДОВАТЕЛЬНОСТИ] — суд РАЗВОРАЧИВАЕТ прогрессию заново.

    the arithmetic progression from 3 with step 4 gives 3 7 11 15.
    the derivative of t^2 at 5 is 10.
    the sequence 1/2 1/4 1/8 1/16 has limit 0.

ПРЕДЕЛ ПРОВЕРЯЕТСЯ НЕ ВЕРОЙ, А УБЫВАНИЕМ И ЗНАМЕНАТЕЛЕМ: члены обязаны
строго убывать по модулю и быть степенями одного знаменателя — тогда
нуль есть предел по построению, а не по объявлению. Сумма всего ряда
считается точной дробью, и приближение, названное равенством, было бы
ложью того же рода, что «5 ÷ 2 = 2».

ПРОИЗВОДНАЯ ПРОВЕРЯЕТСЯ ЗАКОНОМ СТЕПЕНИ, А РАЗНОСТНОЕ ОТНОШЕНИЕ —
ВЫЧИСЛЕНИЕМ. Это две поверхности одного знания, и суд считает обе
своим счётом: показ, где они разошлись бы, есть противоречие, которого
не увидит счёт по отдельности.
"""
import pathlib
import re
import sys
from fractions import Fraction

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

АРИФМЕТИЧЕСКАЯ = re.compile(
    r"^(?:the arithmetic progression from (\d+) with step (\d+) gives"
    r"|арифметическая прогрессия от (\d+) с шагом (\d+) даёт) "
    r"([\d ]+)\.$")
ГЕОМЕТРИЧЕСКАЯ = re.compile(
    r"^(?:the geometric progression from (\d+) with ratio (\d+) gives"
    r"|геометрическая прогрессия от (\d+) со знаменателем (\d+) даёт) "
    r"([\d ]+)\.$")
ЧЛЕН = re.compile(
    r"^(?:term number (\d+) of the progression from (\d+) with step (\d+) is"
    r"|член номер (\d+) прогрессии от (\d+) с шагом (\d+) равен) (\d+): "
    r"(\d+) − 1 = (\d+), (\d+) × (\d+) = (\d+), (\d+) \+ (\d+) = (\d+)\.$")
СУММА = re.compile(
    r"^(?:the sum of ([\d ]+) is|сумма ([\d ]+) равна) (\d+)"
    r"(?:: (\d+) \+ (\d+) = (\d+), (\d+) × (\d+) = (\d+), (\d+) ÷ 2 = (\d+))?\.$")
ПРЕДЕЛ = re.compile(
    r"^(?:the sequence ([\d/ ]+) has limit"
    r"|последовательность ([\d/ ]+) имеет предел) (\d+)\.$")
РЯД = re.compile(
    r"^(?:the sum of the whole series ([\d/ ]+) \.\.\. is"
    r"|сумма всего ряда ([\d/ ]+) \.\.\. равна) (\d+)/(\d+)\.$")
ИЗМЕНЕНИЕ = re.compile(
    r"^(?:for f\(t\) = t\^2 the change from (\d+) to (\d+) is"
    r"|для f\(t\) = t\^2 изменение от (\d+) до (\d+) равно) (\d+)\.$")
ПРОИЗВОДНАЯ = re.compile(
    r"^(?:the derivative of t\^(\d) at (\d+) is"
    r"|производная t\^(\d) в точке (\d+) равна) (\d+)\.$")
# ОТКАЗ ЕСТЬ ТАКОЕ ЖЕ УТВЕРЖДЕНИЕ: «предела нет» истинно ровно тогда,
# когда члены и вправду растут, и суд это пересчитывает.
ОТКАЗ_ПРЕДЕЛА = re.compile(
    r"^(?:no limit for ([\d ]+): the terms grow, they do not shrink"
    r"|предела нет у ([\d ]+): члены растут, а не убывают)\.$")


def _пара(m, a, b):
    """Две первые группы образца, названного двумя языками."""
    return (int(m.group(a) or m.group(a + 2)),
            int(m.group(b) or m.group(b + 2)))


def дроби(текст):
    """Члены как точные дроби; целый член — дробь со знаменателем 1."""
    try:
        return [Fraction(int(к.split("/")[0]), int(к.split("/")[1]) if "/" in к else 1)
                for к in текст.split()]
    except (ValueError, ZeroDivisionError):
        return None


import laws  # noqa: E402
ЗАКОНЫ = laws.свод("sequences")
ЗАКОНЫ_ЯЗЫКА = laws.по_языкам("sequences")
import discourse  # noqa: E402


def судить(строка):
    """(судимо, истинно) для одной строки."""
    if строка.strip() in ЗАКОНЫ:
        return True, True
    с = строка.strip()
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ: род определяется ответом, а связь
    # половин — общим домом `tools/asking.py`.
    р = discourse.судить_рассуждение_мира(строка, судить, ЗАКОНЫ_ЯЗЫКА)
    if р is not None:
        return р
    если = asking.судить_парой(с, судить)
    if если is not None:
        return если
    m = АРИФМЕТИЧЕСКАЯ.match(с)
    if m:
        a, d = _пара(m, 1, 2)
        названо = [int(x) for x in m.group(5).split()]
        return True, названо == [a + k * d for k in range(len(названо))]
    m = ГЕОМЕТРИЧЕСКАЯ.match(с)
    if m:
        a, q = _пара(m, 1, 2)
        названо = [int(x) for x in m.group(5).split()]
        return True, названо == [a * q ** k for k in range(len(названо))]
    m = СУММА.match(с)
    if m:
        члены = [int(x) for x in (m.group(1) or m.group(2)).split()]
        итог = int(m.group(3))
        if m.group(4) is None:
            return True, sum(члены) == итог
        # ЗВЕНЬЯ: первый + последний, k × сумма, ÷ 2 — арифметическая прогрессия.
        a1, an, s1, k, s2, ks, ks2, r = (int(m.group(i)) for i in range(4, 12))
        шаг = члены[1] - члены[0] if len(члены) > 1 else 0
        прогрессия = all(b - a == шаг for a, b in zip(члены, члены[1:]))
        return True, (прогрессия and (a1, an) == (члены[0], члены[-1]) and s1 == a1 + an
                      and k == len(члены) and s2 == s1 and ks == k * s1 and ks2 == ks
                      and 2 * r == ks and r == итог == sum(члены))
    m = ПРЕДЕЛ.match(с)
    if m:
        члены = дроби(m.group(1) or m.group(2))
        if not члены or len(члены) < 2:
            return False, True
        убывают = all(б < а for а, б in zip(члены, члены[1:]))
        # ЗНАМЕНАТЕЛЬ ОДИН НА ВСЮ ЦЕПЬ: 1/q, 1/q², … — тогда нуль есть
        # предел по построению, а не по слову «имеет».
        q = члены[0].denominator
        степени = all(ч == Fraction(1, q ** (k + 1))
                      for k, ч in enumerate(члены))
        # ЦЕЛАЯ ЦЕПЬ С ПОСТОЯННЫМ ЦЕЛЫМ ДЕЛИТЕЛЕМ ≥ 2 убывает к нулю по
        # построению так же, как 1/q, 1/q², …
        целые = all(ч.denominator == 1 for ч in члены)
        делитель = (члены[0] / члены[1]) if члены[1] else None
        цепь = (целые and делитель is not None and делитель.denominator == 1
                and делитель >= 2
                and all(а == б * делитель for а, б in zip(члены, члены[1:])))
        return True, убывают and (степени or цепь) and int(m.group(3)) == 0
    m = РЯД.match(с)
    if m:
        члены = дроби(m.group(1) or m.group(2))
        if not члены:
            return False, True
        q = члены[0].denominator
        if q < 2:
            return True, False
        ждём = Fraction(1, q - 1)
        назван = Fraction(int(m.group(3)), int(m.group(4)))
        return True, ждём == назван
    m = ИЗМЕНЕНИЕ.match(с)
    if m:
        было, стало = _пара(m, 1, 2)
        return True, стало * стало - было * было == int(m.group(5))
    m = ПРОИЗВОДНАЯ.match(с)
    if m:
        степень = int(m.group(1) or m.group(3))
        x = int(m.group(2) or m.group(4))
        return True, степень * x ** (степень - 1) == int(m.group(5))
    m = ОТКАЗ_ПРЕДЕЛА.match(с)
    if m:
        члены = [int(x) for x in (m.group(1) or m.group(2)).split()]
        if len(члены) < 2:
            return False, True
        return True, all(б > а for а, б in zip(члены, члены[1:]))
    m = ЧЛЕН.match(с)
    if m:
        n = int(m.group(1) or m.group(4))
        a = int(m.group(2) or m.group(5))
        d = int(m.group(3) or m.group(6))
        итог, n1, n2, n3, d1, p, a1, p2, r = (int(m.group(i)) for i in range(7, 16))
        return True, (n1 == n and n2 == n - 1 == n3 and d1 == d and p == (n - 1) * d
                      and a1 == a and p2 == p and r == a + p and итог == r)
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ПОСЛЕДОВАТЕЛЬНОСТИ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ПОСЛЕДОВАТЕЛЬНОСТИ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ПОСЛЕДОВАТЕЛЬНОСТИ {поза}: {ложных} ложных из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
