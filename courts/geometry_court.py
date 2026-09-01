#!/usr/bin/env python3
"""[ГЕОМЕТРИЯ] — суд ВЫВОДИТ меру фигуры заново.

    a rectangle 3 by 4 has area 12 and perimeter 14.
    a right triangle with legs 3 and 4 has hypotenuse 5.
    a box 2 by 3 by 4 has volume 24 and surface 52.

МЕРА ФИГУРЫ НЕ ИЗМЕРЯЕТСЯ, А ВЫВОДИТСЯ, и потому проверяема нацело:
площадь есть произведение, периметр — сумма, объём — три множителя.
Показ, назвавший площадь верно, а периметр неверно, есть ложь, которую
не поймает суд, проверяющий одно из двух: здесь считаются ОБА.

ГИПОТЕНУЗА ПРОВЕРЯЕТСЯ КВАДРАТАМИ, А НЕ КОРНЕМ: целое, чей квадрат
равен сумме квадратов, есть точный ответ; всё прочее — приближение, и
корпус его не пишет.
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

ПРЯМОУГОЛЬНИК = re.compile(
    r"^(?:a rectangle (\d+) by (\d+) has area (\d+) and perimeter (\d+)"
    r"|прямоугольник (\d+) на (\d+) имеет площадь (\d+) и периметр (\d+))\.$")
КВАДРАТ = re.compile(
    r"^(?:a square with side (\d+) has area (\d+) and perimeter (\d+)"
    r"|квадрат со стороной (\d+) имеет площадь (\d+) и периметр (\d+))\.$")
ТРЕУГОЛЬНИК = re.compile(
    r"^(?:a triangle with base (\d+) and height (\d+) has area (\d+)"
    r"|треугольник с основанием (\d+) и высотой (\d+) "
    r"имеет площадь (\d+))\.$")
ГИПОТЕНУЗА = re.compile(
    r"^(?:a right triangle with legs (\d+) and (\d+) has hypotenuse (\d+)"
    r"|прямоугольный треугольник с катетами (\d+) и (\d+) "
    r"имеет гипотенузу (\d+))\.$")
КВАДРАТЫ = re.compile(r"^(\d+)\^2 \+ (\d+)\^2 = (\d+)\^2\.$")
КОРОБКА = re.compile(
    r"^(?:a box (\d+) by (\d+) by (\d+) has volume (\d+) and surface (\d+)"
    r"|коробка (\d+) на (\d+) на (\d+) имеет объём (\d+) "
    r"и поверхность (\d+))\.$")
КУБ = re.compile(
    r"^(?:a cube with edge (\d+) has volume (\d+)"
    r"|куб с ребром (\d+) имеет объём (\d+))\.$")


def числа(m, сколько):
    """Группы образца, названного двумя языками, — одним рядом."""
    все = [г for г in m.groups() if г is not None]
    return [int(x) for x in все[:сколько]]


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    m = ПРЯМОУГОЛЬНИК.match(с)
    if m:
        a, b, площадь, периметр = числа(m, 4)
        return True, площадь == a * b and периметр == 2 * (a + b)
    m = КВАДРАТ.match(с)
    if m:
        a, площадь, периметр = числа(m, 3)
        return True, площадь == a * a and периметр == 4 * a
    m = ТРЕУГОЛЬНИК.match(с)
    if m:
        b, h, площадь = числа(m, 3)
        return True, b * h == 2 * площадь
    m = ГИПОТЕНУЗА.match(с)
    if m:
        a, b, c = числа(m, 3)
        return True, a * a + b * b == c * c
    m = КВАДРАТЫ.match(с)
    if m:
        a, b, c = числа(m, 3)
        return True, a * a + b * b == c * c
    m = КОРОБКА.match(с)
    if m:
        a, b, c, объём, поверхность = числа(m, 5)
        return True, (объём == a * b * c
                      and поверхность == 2 * (a * b + b * c + a * c))
    m = КУБ.match(с)
    if m:
        a, объём = числа(m, 2)
        return True, объём == a ** 3
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ГЕОМЕТРИЯ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ГЕОМЕТРИЯ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ГЕОМЕТРИЯ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
