#!/usr/bin/env python3
"""[ВСЕ ПОЛОСЫ БЕСЕДЫ] — одна таблица по всем declarations/BESEDA-*.txt.

    python3 scripts/beseda_all.py [--свод datasets/GENESIS-FULL.txt]

Зовёт scripts/beseda_reach.py на каждую полосу и печатает строку ИТОГО каждой:
строкой / с формой / немых. Прибор долгий (минуты на полосу) — в набор леджера
не входит, зовётся рукой после точки свода или по пробному своду.
"""
import argparse
import pathlib
import re
import subprocess
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]


def main():
    ап = argparse.ArgumentParser()
    ап.add_argument("--свод", default="datasets/GENESIS-FULL.txt")
    а = ап.parse_args()
    полосы = sorted((КОРЕНЬ / "declarations").glob("BESEDA-*.txt"),
                    key=lambda п: (len(п.stem), п.stem))
    итоги = []
    for п in полосы:
        вывод = subprocess.run([sys.executable, str(КОРЕНЬ / "scripts/beseda_reach.py"), "--полоса", str(п), "--свод", а.свод],
                               capture_output=True, text=True).stdout
        м = re.search(r"ИТОГО\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+— строкой (\d+) %, с формой (\d+) %", вывод)
        if not м:
            итоги.append((п.stem, None)); continue
        итоги.append((п.stem, tuple(int(x) for x in м.groups())))
    print(f"{'полоса':<12} {'строкой':>8} {'формой':>7} {'немых':>6}   строкой %  с формой %")
    for имя, з in итоги:
        if z := з:
            print(f"{имя:<12} {z[0]:>8} {z[1]:>7} {z[3]:>6}   {z[4]:>8} %  {z[5]:>8} %")
        else:
            print(f"{имя:<12} — не измерена")
    return 0


if __name__ == "__main__":
    sys.exit(main())
