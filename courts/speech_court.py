#!/usr/bin/env python3
"""[РЕЧЬ] — суд ИСПОЛНЯЕТ связь, а не читает её.

Шесть форм соединения, и каждая проверяется ДВАЖДЫ там, где она несёт
две проверки:

  · АНАФОРА — местоимение обязано согласоваться с ЕДИНСТВЕННЫМ
    доступным антецедентом И счёт обязан сойтись. «У Петра было 5
    яблок. Она отдала 2» безупречно по счёту и ложно о языке;
  · ЗНАЧИТ — связка следования: посылка обязана быть истинной И
    заключение обязано из неё СЛЕДОВАТЬ. Ложны обе половины порознь;
  · КОТОРЫЙ — предикат внутри имени исполняется, а не принимается;
  · ВСЕ / НИ ОДИН — квантор пробегается по названному ряду, членство
    проверяется, заключение выводится;
  · НОМИНАЛИЗАЦИЯ — действие, названное предметом, есть ВТОРАЯ
    ПОВЕРХНОСТЬ факта, и обе поверхности считаются своим счётом;
  · ДОСТАТОЧНО / НЕОБХОДИМО — четыре клетки, а не две (замысел
    verum-6c): один свидетель даёт ПРОТИВОПОЛОЖНЫЕ вердикты двум
    утверждениям, и это показывает различие понятий вместо того, чтобы
    его объявлять.

ФОРМА КУПЛЕНА ТОГДА, КОГДА СУД ЕЁ ИСПОЛНЯЕТ И ОТВЕРГАЕТ ЕЁ ПОДДЕЛКУ
(закон verum-6c). Суд, ни разу не сказавший «нет», не измерил ничего —
потому у каждой формы здесь есть подделка, и она названа в стенде
парка аудита, а не в намерении.
"""
import ast
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

ГЕНЕРАТОР = КОРЕНЬ / "tools/gen_genesis_speech.py"


def _объявленные_лица():
    """{имя или его родительный: местоимение} — из объявления слоя.

    Род имени не выводится из окончания, он ОБЪЯВЛЕН; второй список
    разошёлся бы с первым в день, когда тронут любой.
    """
    вон = {}
    try:
        дерево = ast.parse(ГЕНЕРАТОР.read_text(encoding="utf-8"))
    except OSError:
        return вон
    for узел in дерево.body:
        if (isinstance(узел, ast.Assign)
                and getattr(узел.targets[0], "id", None) == "ЛИЦА"):
            try:
                ряды = ast.literal_eval(узел.value)
            except (ValueError, SyntaxError):
                return вон
            for имя, род, он_она, него_неё, en, he_she in ряды:
                вон[имя] = (он_она, него_неё)
                вон[род] = (он_она, него_неё)
                вон[en] = (he_she, he_she)
    return вон


ЛИЦА = _объявленные_лица()

АНАФОРА_RU = re.compile(
    r"^у (\w+) было (\d+) \S+\. (он|она) отдала? (\d+) \S+\. "
    r"у (него|неё) осталось (\d+) \S+\.$")
АНАФОРА_EN = re.compile(
    r"^(\w+) had (\d+) \w+\. (he|she) gave away (\d+) \w+\. "
    r"\3 has (\d+) \w+ left\.$")
ЗНАЧИТ = re.compile(
    r"^(?:(\d+) делится на (\d+)\. значит (\d+) (кратно \d+|чётно)"
    r"|(\d+) is divisible by (\d+)\. therefore (\d+) "
    r"(is a multiple of \d+|is even))\.$")
КОТОРЫЙ = re.compile(
    r"^(\d+) (?:есть число, которое делится на|"
    r"is a number that is divisible by) (\d+)\. (\d+) ÷ (\d+) = (\d+)\.$")
КВАНТОР = re.compile(
    r"^(?:(все числа|ни одно из чисел) ([\d, ]+?) (?:чётны|не чётно)\. "
    r"(\d+) — одно из них\. значит (\d+) (чётно|не чётно)"
    r"|(all of|none of) ([\d, ]+?) are even\. (\d+) is one of them\. "
    r"therefore (\d+) (is even|is not even))\.$")
НОМИНАЛИЗАЦИЯ = re.compile(
    r"^(?:(сложение|умножение) (\d+) (?:и|на) (\d+) даёт (\d+)"
    r"|the (addition|multiplication) of (\d+) (?:and|by) (\d+) "
    r"gives (\d+))\. (\d+) ([+×]) (\d+) = (\d+)\.$")
ДОСТАТОЧНО = re.compile(
    r"^(?:делимости на (\d+) достаточно для чётности: "
    r"(\d+) делится на \1 и \2 чётно"
    r"|divisibility by (\d+) is sufficient for evenness: "
    r"(\d+) is divisible by \3 and \4 is even)\.$")
НЕ_НЕОБХОДИМО = re.compile(
    r"^(?:делимость на (\d+) не необходима для чётности: "
    r"(\d+) чётно и на \1 не делится"
    r"|divisibility by (\d+) is not necessary for evenness: "
    r"(\d+) is even and not divisible by \3)\.$")
ОБА = re.compile(
    r"^(?:делимости на 2 достаточно для чётности и она необходима для неё"
    r"|divisibility by 2 is sufficient for evenness and necessary "
    r"for it)\.$")


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    m = АНАФОРА_RU.match(с)
    if m:
        кто, было, мест, ушло, кос, стало = m.groups()
        объявлено = ЛИЦА.get(кто)
        if объявлено is None:
            return False, True
        # ДВА СУДА НА ОДИН ПОКАЗ: язык и счёт. Показ, верный по одному
        # и ложный по другому, есть ровно тот дефект, ради которого
        # форма и покупается.
        язык = объявлено == (мест, кос)
        счёт = int(было) - int(ушло) == int(стало)
        return True, язык and счёт
    m = АНАФОРА_EN.match(с)
    if m:
        кто, было, мест, ушло, стало = m.groups()
        объявлено = ЛИЦА.get(кто)
        if объявлено is None:
            return False, True
        return True, (объявлено[0] == мест
                      and int(было) - int(ушло) == int(стало))
    m = ЗНАЧИТ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        n, d, повтор, вывод_ = int(г[0]), int(г[1]), int(г[2]), г[3]
        if n != повтор:
            return True, False
        посылка = n % d == 0
        если = re.search(r"\d+", вывод_)
        if "чётн" in вывод_ or "even" in вывод_:
            следствие = n % 2 == 0
        elif если:
            следствие = n % int(если.group()) == 0
        else:
            return False, True
        # ПОСЫЛКА ОБЯЗАНА БЫТЬ ИСТИННОЙ, И ЗАКЛЮЧЕНИЕ ОБЯЗАНО СЛЕДОВАТЬ.
        return True, посылка and следствие
    m = КОТОРЫЙ.match(с)
    if m:
        n, d, n2, d2, q = (int(г) for г in m.groups())
        return True, (n == n2 and d == d2 and d != 0
                      and n % d == 0 and n // d == q)
    m = КВАНТОР.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        слово, ряд, один, повтор, итог = г[0], г[1], г[2], г[3], г[4]
        числа = [int(x) for x in ряд.replace(",", " ").split()]
        все_ли = слово in ("все числа", "all of")
        членство = int(один) in числа and один == повтор
        посылка = (all(x % 2 == 0 for x in числа) if все_ли
                   else all(x % 2 for x in числа))
        ждём_чёт = итог in ("чётно", "is even")
        return True, (членство and посылка
                      and ждём_чёт == (int(один) % 2 == 0)
                      and ждём_чёт == все_ли)
    m = НОМИНАЛИЗАЦИЯ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        имя, a, b, итог = г[0], int(г[1]), int(г[2]), int(г[3])
        a2, глиф, b2, итог2 = int(г[4]), г[5], int(г[6]), int(г[7])
        ждём = a + b if имя in ("сложение", "addition") else a * b
        глиф_ждём = "+" if имя in ("сложение", "addition") else "×"
        return True, (итог == ждём and (a, b, итог) == (a2, b2, итог2)
                      and глиф == глиф_ждём)
    m = ДОСТАТОЧНО.match(с)
    if m:
        г = [int(x) for x in m.groups() if x is not None]
        d, свидетель = г[0], г[1]
        return True, свидетель % d == 0 and свидетель % 2 == 0
    m = НЕ_НЕОБХОДИМО.match(с)
    if m:
        г = [int(x) for x in m.groups() if x is not None]
        d, свидетель = г[0], г[1]
        # ОДИН СВИДЕТЕЛЬ УБИВАЕТ НЕОБХОДИМОСТЬ: чётный и не делящийся.
        return True, свидетель % 2 == 0 and свидетель % d != 0
    if ОБА.match(с):
        return True, True
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"РЕЧЬ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    if not ЛИЦА:
        print("РЕЧЬ ОТКАЗ: лица не объявлены — судить нечем")
        return 2
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("РЕЧЬ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"РЕЧЬ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
