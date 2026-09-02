#!/usr/bin/env python3
"""СРЕЗЫ МАССЫ — корпус, где у каждой рамки не больше k показов.

Слово владельца (03.09): найти, насколько минимальным должен быть корпус.
Организм покупает рамку по массе показов; колено кривой «масса → куплено»
есть минимальная масса, и минимальный корпус = рамок × колено. Срезы массы
дают точки этой кривой: тот же свод, та же полоса, но рамке оставлено k
показов (первые k в порядке свода — детерминированно, без жребия).

Рамка здесь — скелет строки первой ступени (числа → #, имена → @, нотации —
одна дыра), тот же, что в переписи форм (scripts/form_census.py).

    python3 tools/mass_slices.py --в <каталог> --массы 3,5,9,20
"""
import argparse
import collections
import hashlib
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
sys.path.insert(0, str(КОРЕНЬ / "scripts"))
from form_census import скелет  # noqa: E402

ПОЛНЫЙ = КОРЕНЬ / "datasets" / "GENESIS-FULL.txt"


# ОСЬ — НЕ РАМКА, А ОСНОВАНИЕ (e9 04.09): цепь цифр «0 + 1 = 1 … 9 + 1 = 10 …»
# есть показы ОДНОЙ рамки «# + # = #», и срез ≤ k показов рвал её — счётный
# орган на MASS3/5 оставался без базы 10, и арифметика цифр шла рефлексом
# ленты («10 − 9 = 21»). Звено оси (шаг на единицу вверх или вниз) входит в
# срез целиком, без потолка; цепи числительными словом («zero plus one …»)
# срезу не подвластны и так: у каждой такой строки свой скелет.
ОСЬ = re.compile(r"^(\d+) ([+−]) 1 = (\d+)\.$")


def звено_оси(строка):
    м = ОСЬ.match(строка.strip())
    if not м:
        return False
    a, знак, b = int(м.group(1)), м.group(2), int(м.group(3))
    return b == (a + 1 if знак == "+" else a - 1)


def срез(k):
    масса = collections.Counter()
    вон = []
    for строка in ПОЛНЫЙ.read_text(encoding="utf-8").splitlines():
        if not строка.strip() or строка.startswith("\x0c") or звено_оси(строка):
            вон.append(строка)
            continue
        ск = скелет(строка)
        if масса[ск] < k:
            масса[ск] += 1
            вон.append(строка)
    return вон


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--в", required=True)
    ap.add_argument("--массы", default="3,5,9,20")
    а = ap.parse_args()
    куда = pathlib.Path(а.в); куда.mkdir(parents=True, exist_ok=True)
    полный = [с for с in ПОЛНЫЙ.read_text(encoding="utf-8").splitlines() if с.strip() and not с.startswith("\x0c")]
    for k in (int(x) for x in а.массы.split(",")):
        строки = срез(k)
        файл = куда / f"GENESIS-FULL-MASS{k}.txt"
        текст = "\n".join(строки) + "\n"
        файл.write_text(текст, encoding="utf-8")
        ш = hashlib.sha256(текст.encode("utf-8")).hexdigest()[:16]
        n = sum(1 for с in строки if с.strip() and not с.startswith("\x0c"))
        print(f"масса {k:3}: строк {n:7} ({100 * n // len(полный):3} % полного) байт {файл.stat().st_size:9} sha {ш} → {файл}")


if __name__ == "__main__":
    main()
