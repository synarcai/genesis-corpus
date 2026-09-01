#!/usr/bin/env python3
"""[СЕМАНТИКА ПРОГРАММЫ] — суд ВЫПОЛНЯЕТ показанное, а не разбирает его.

Программиста растят не имена конструкций, а то, что они ДЕЛАЮТ. Оттого
здесь ни одно утверждение не принимается по виду: связывание
исполняется, ветвление вычисляется, цикл прокручивается, функция
применяется, рекурсия разворачивается до основания. Конструкция,
которую прибор выполнить не может, есть конструкция, которой слою
показывать нельзя.

СУДЯТСЯ ДВА СЛОЯ СРАЗУ: новый слой семантики и давний `l3_prog`, чьи
трассы циклов, ветвления со входом и массивы не судил до сих пор никто
— они лежали в корпусе как утверждения на веру.

ТРАССА ЦИКЛА ПРОВЕРЯЕТСЯ ШАГ ЗА ШАГОМ: «трасса: i=1 s=1; i=2 s=3» есть
последовательность состояний, и прибор прокручивает её сам. Показ, где
итог верен, а трасса лжёт, учит неверному ходу при верном ответе — и
это хуже неверного ответа, ибо ход есть то, чему учатся.
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

ДЕЙСТВИЕ = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
            "*": lambda a, b: a * b}
СРАВНЕНИЕ = {"<": lambda a, b: a < b, ">": lambda a, b: a > b,
             "=": lambda a, b: a == b}

СВЯЗКА = re.compile(
    r"^(?:let|пусть) a = (\d+); (?:let|пусть) b = (\d+); "
    r"(?:let|пусть) c = a ([+\-*]) b; c = (\d+)$")
ВЕТВЬ = re.compile(
    r"^if (\d+) ([<>]) (\d+) then y = (\d+) else y = (\d+); y = (\d+)$")
ВЕТВЬ_ВХОД = re.compile(
    r"^(?:if|если) x ([<>]) (\d+) (?:then|то) y = (\d+) (?:else|иначе) "
    r"y = (\d+)\. (?:input|вход) x = (\d+)\. (?:output|выход) y = (\d+)$")
СУММА = re.compile(
    r"^(?:sum for i from|сумма для i от) (\d+) (?:to|до) (\d+) "
    r"(?:is|равна) (\d+)$")
ПРОИЗВ = re.compile(
    r"^(?:product for i from|произведение для i от) (\d+) (?:to|до) (\d+) "
    r"(?:is|равно) (\d+)$")
ФУНКЦИЯ = re.compile(
    r"^(?:function|функция) (\w+)\(n\) = n ([+\-*]) (\d+|n); \1\((\d+)\) "
    r"= (-?\d+)$")
ФАКТОРИАЛ = re.compile(
    r"^factorial\(0\) = 1; factorial\(n\) = n \* factorial\(n - 1\); "
    r"factorial\((\d+)\) = (\d+)$")
ТРАССА = re.compile(
    r"^s = 0; для i от (\d+) до (\d+): s = s \+ i\. трасса: (.+?)\. "
    r"итог s = (\d+)$")
ШАГ = re.compile(r"i=(\d+) s=(\d+)")
МАССИВ = re.compile(
    r"^массив \[([\d ]+)\]\. длина = (\d+)\. первый = (\d+)\. "
    r"последний = (\d+)$")
СОРТИРОВКА = re.compile(r"^сортировка \[([\d ]+)\] → \[([\d ]+)\]$")


def судить(строка):
    с = строка.strip().rstrip(".")
    m = СВЯЗКА.match(с)
    if m:
        a, b, оп, c = int(m.group(1)), int(m.group(2)), m.group(3), int(m.group(4))
        return True, ДЕЙСТВИЕ[оп](a, b) == c
    m = ВЕТВЬ.match(с)
    if m:
        x, зн, y, да, нет, итог = (m.group(1), m.group(2), m.group(3),
                                   m.group(4), m.group(5), m.group(6))
        ждём = int(да) if СРАВНЕНИЕ[зн](int(x), int(y)) else int(нет)
        return True, ждём == int(итог)
    m = ВЕТВЬ_ВХОД.match(с)
    if m:
        зн, порог, да, нет, вход, итог = m.groups()
        ждём = int(да) if СРАВНЕНИЕ[зн](int(вход), int(порог)) else int(нет)
        return True, ждём == int(итог)
    m = СУММА.match(с)
    if m:
        lo, hi, итог = (int(x) for x in m.groups())
        return True, sum(range(lo, hi + 1)) == итог
    m = ПРОИЗВ.match(с)
    if m:
        lo, hi, итог = (int(x) for x in m.groups())
        p = 1
        for k in range(lo, hi + 1):
            p *= k
        return True, p == итог
    m = ФУНКЦИЯ.match(с)
    if m:
        _, оп, правое, арг, итог = m.groups()
        arg = int(арг)
        b = arg if правое == "n" else int(правое)
        return True, ДЕЙСТВИЕ[оп](arg, b) == int(итог)
    m = ФАКТОРИАЛ.match(с)
    if m:
        n, итог = (int(x) for x in m.groups())
        f = 1
        for k in range(2, n + 1):
            f *= k
        return True, f == итог
    m = ТРАССА.match(с)
    if m:
        lo, hi, трасса, итог = m.groups()
        # ТРАССА ПРОКРУЧИВАЕТСЯ ШАГ ЗА ШАГОМ, а не сверяется по итогу
        шаги = [(int(a), int(b)) for a, b in ШАГ.findall(трасса)]
        s = 0
        ждали = []
        for i in range(int(lo), int(hi) + 1):
            s += i
            ждали.append((i, s))
        return True, шаги == ждали and s == int(итог)
    m = МАССИВ.match(с)
    if m:
        числа = [int(x) for x in m.group(1).split()]
        длина, первый, последний = (int(x) for x in m.groups()[1:])
        return True, (len(числа) == длина and числа[0] == первый
                      and числа[-1] == последний)
    m = СОРТИРОВКА.match(с)
    if m:
        было = [int(x) for x in m.group(1).split()]
        стало = [int(x) for x in m.group(2).split()]
        return True, sorted(было) == стало
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ПРОГРАММЫ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ПРОГРАММЫ ОТКАЗ: обход пуст, судить нечего")
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
                        примеры.append(f"{путь.name}: {строка.strip()[:90]}")
        if свои:
            print(f"  {путь.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ПРОГРАММЫ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
