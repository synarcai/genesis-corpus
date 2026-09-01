#!/usr/bin/env python3
"""[ПАДЕЖ И СООТВЕТСТВИЕ] — форма имени и свойства функции.

    слово час в родительном падеже — часа.
    функция f(x) = 2x на {1 2 3} инъективна: разные входы дают разные выходы.
    допустим, 7 чётно. тогда 7 = 2k. но 7 = 2 × 3 + 1. противоречие.

ПАДЕЖ СВЕРЯЕТСЯ С ОБЪЯВЛЕННОЙ ПАРАДИГМОЙ, а не выводится окончанием:
русскую форму нельзя получить отсечением, её называют. Корпус показывал
падежи В РАБОТЕ с самого начала и НИ РАЗУ НЕ НАЗЫВАЛ — свод оснований
честно числил парадигму имени непокрытой.

ИНЪЕКТИВНОСТЬ ИСПОЛНЯЕТСЯ, А НЕ ПРИНИМАЕТСЯ: суд применяет правило ко
всей названной области и смотрит, не совпали ли выходы. Свидетель
опровержения проверяется отдельно — он обязан быть НАСТОЯЩИМ
свидетелем, то есть двумя разными входами с одним выходом.

ДОКАЗАТЕЛЬСТВО ОТ ПРОТИВНОГО ПРОВЕРЯЕТСЯ ЦЕЛИКОМ: допущение обязано
быть ложным, вычисление в шаге — верным, и вывод обязан быть отрицанием
допущения. Цепь, верная по шагам и заключившая не то, есть та же
болезнь «предмет вышел из множества» (довод verum-6c).
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import units  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402
from rugram import ПАДЕЖИ, ПАДЕЖИ_В, ПАРАДИГМЫ  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

ПАДЕЖОМ = re.compile(
    r"^слово (\S+) в (\S+) падеже — (\S+)\.$")
СКОЛЬКО_ПАДЕЖЕЙ = re.compile(r"^падежей шесть: (.+)\.$")
ФУНКЦИЯ = re.compile(
    r"^(?:функция f на множестве \{([\d ]+)\} задана правилом "
    r"f\(x\) = (\d+)x; f\((\d+)\) = (\d+)"
    r"|the function f on the set \{([\d ]+)\} is given by "
    r"f\(x\) = (\d+)x; f\((\d+)\) = (\d+))\.$")
ИНЪЕКТИВНА = re.compile(
    r"^(?:функция f\(x\) = (\d+)x на множестве \{([\d ]+)\} инъективна"
    r"|the function f\(x\) = (\d+)x on \{([\d ]+)\} is injective)"
    r": [^.]+\.$")
НЕ_ИНЪЕКТИВНА = re.compile(
    r"^(?:функция f\(x\) = x mod 2 на множестве \{([\d ]+)\} "
    r"не инъективна: f\((\d+)\) = f\((\d+)\)"
    r"|the function f\(x\) = x mod 2 on \{([\d ]+)\} is not injective: "
    r"f\((\d+)\) = f\((\d+)\))\.$")
МОЩНОСТЬ = re.compile(
    r"^(?:мощность множества \{([a-z ]+)\} равна (\d+)"
    r"|the cardinality of the set \{([a-z ]+)\} is (\d+))\.$")
СЧЁТНОСТЬ = re.compile(
    r"^(?:чётные числа счётны: (\d+) отвечает (\d+), и это биекция "
    r"с натуральными"
    r"|the even numbers are countable: (\d+) maps to (\d+), and this "
    r"is a bijection with the naturals)\.$")
ПРОТИВНОЕ = re.compile(
    r"^(?:допустим, (\d+) чётно\. тогда (\d+) = 2k для целого k\. но "
    r"(\d+) = 2 × (\d+) \+ (\d+)\. противоречие: (\d+) нечётно"
    r"|suppose (\d+) is even\. then (\d+) = 2k for a whole k\. but "
    r"(\d+) = 2 × (\d+) \+ (\d+)\. contradiction: (\d+) is odd)\.$")
ИНДУКЦИЯ = re.compile(
    r"^(?:индукция: основание n = 1 верно, шаг от n к n\+1 верен, "
    r"значит верно до n = (\d+); сумма первых (\d+) чисел равна (\d+)"
    r"|induction: the base n = 1 holds, the step from n to n\+1 holds, "
    r"hence it holds up to n = (\d+); the sum of the first (\d+) "
    r"numbers is (\d+))\.$")


def _г(m):
    return [x for x in m.groups() if x is not None]


# ЧИСЛОВАЯ РАМКА СУДИТСЯ ПРАВИЛОМ ПИСЬМА, А НЕ ТАБЛИЦЕЙ. Суд выводит
# множественное САМ и сверяет с названным: это вторая рука к паре,
# объявленной в доме единиц, и она ловит ложь ДОМА, а не только порчу
# строки. Исключение объявлено там же и названо в показе вслух.
МНОЖЕСТВЕННОЕ = re.compile(
    r"^the plural of (\w+) is (\w+)\.$")
ЕДИНСТВЕННОЕ = re.compile(
    r"^the singular of (\w+) is (\w+)\.$")
ИСКЛЮЧЕНИЕ = re.compile(
    r"^the plural of (\w+) is (\w+), not (\w+): it does not follow "
    r"the rule\.$")
_ОБЪЯВЛЕННЫЕ = frozenset(
    units.англ(и, м) for и in units.ФОРМЫ_ВСЕХ for м in (False, True)
    if units.ФОРМЫ_ВСЕХ[и][0])
ВОПРОС_ЧИСЛА = re.compile(
    r"^what is the (plural|singular) of (\w+)\? (.+)$")


def _объявлено(слово):
    """Есть ли такое английское слово в доме единиц."""
    return слово in _ОБЪЯВЛЕННЫЕ


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    m = ВОПРОС_ЧИСЛА.match(с)
    if m:
        какое, спрошено, ответ = m.groups()
        образец = (МНОЖЕСТВЕННОЕ if какое == "plural"
                   else ЕДИНСТВЕННОЕ)
        свой = образец.match(ответ)
        if свой is None:
            return False, True
        судимо, истинно = судить(ответ)
        назван = свой.group(1)
        return судимо, bool(истинно and назван == спрошено)
    m = ИСКЛЮЧЕНИЕ.match(с)
    if m:
        один, много, наивное = m.groups()
        return True, (units.МН_ИСКЛЮЧЕНИЯ.get(один) == много
                      and наивное == один + "s" and наивное != много)
    m = МНОЖЕСТВЕННОЕ.match(с)
    if m:
        один, много = m.groups()
        return True, (_объявлено(один)
                      and units.мн_правилом(один) == много)
    m = ЕДИНСТВЕННОЕ.match(с)
    if m:
        много, один = m.groups()
        # ЕДИНСТВЕННОЕ ОБЯЗАНО БЫТЬ ОБЪЯВЛЕННЫМ СЛОВОМ, А НЕ ЛЮБОЙ
        # СТРОКОЙ, ЧЬЁ ПРАВИЛО ДАЁТ НАЗВАННОЕ МНОЖЕСТВЕННОЕ. «the
        # singular of inches is inche» проходило правило («inche» + s
        # = «inches») и было ложью: правило проверяет ПЕРЕХОД, а не
        # СУЩЕСТВОВАНИЕ. Слова корпуса объявлены домом единиц.
        return True, (_объявлено(один)
                      and units.мн_правилом(один) == много)
    m = ПАДЕЖОМ.match(с)
    if m:
        слово, падеж_в, форма = m.groups()
        парадигма = ПАРАДИГМЫ.get(слово)
        if парадигма is None or падеж_в not in ПАДЕЖИ_В:
            return False, True
        return True, парадигма[ПАДЕЖИ_В.index(падеж_в)] == форма
    m = СКОЛЬКО_ПАДЕЖЕЙ.match(с)
    if m:
        названы = [x.strip() for x in m.group(1).split(",")]
        return True, названы == list(ПАДЕЖИ)
    m = ФУНКЦИЯ.match(с)
    if m:
        г = _г(m)
        область = [int(x) for x in г[0].split()]
        k, точка, итог = int(г[1]), int(г[2]), int(г[3])
        return True, точка in область and k * точка == итог
    m = ИНЪЕКТИВНА.match(с)
    if m:
        г = _г(m)
        k, область = int(г[0]), [int(x) for x in г[1].split()]
        выходы = [k * x for x in область]
        return True, k != 0 and len(set(выходы)) == len(выходы)
    m = НЕ_ИНЪЕКТИВНА.match(с)
    if m:
        г = _г(m)
        область = [int(x) for x in г[0].split()]
        a, b = int(г[1]), int(г[2])
        # СВИДЕТЕЛЬ ОБЯЗАН БЫТЬ НАСТОЯЩИМ: два РАЗНЫХ входа области с
        # ОДНИМ выходом. Иначе опровержение опровергает пустоту.
        return True, (a in область and b in область and a != b
                      and a % 2 == b % 2)
    m = МОЩНОСТЬ.match(с)
    if m:
        г = _г(m)
        буквы = г[0].split()
        return True, len(set(буквы)) == len(буквы) == int(г[1])
    m = СЧЁТНОСТЬ.match(с)
    if m:
        n, m2 = (int(x) for x in _г(m))
        return True, m2 == 2 * n
    m = ПРОТИВНОЕ.match(с)
    if m:
        г = [int(x) for x in _г(m)]
        n, n2, n3, k, r, n4 = г
        return True, (n == n2 == n3 == n4 and n % 2 == 1
                      and n == 2 * k + r and r == 1)
    m = ИНДУКЦИЯ.match(с)
    if m:
        верх, верх2, сумма = (int(x) for x in _г(m))
        return True, верх == верх2 and сумма == верх * (верх + 1) // 2
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ПАДЕЖ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    if not ПАРАДИГМЫ:
        print("ПАДЕЖ ОТКАЗ: парадигмы не объявлены")
        return 2
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ПАДЕЖ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ПАДЕЖ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
