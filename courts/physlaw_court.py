#!/usr/bin/env python3
"""[ЗАКОНЫ ФИЗИКИ] — размерность, сохранение, давление, волна.

    размерность величины сила есть M L / T^2; измеряется в ньютонах.
    давление = сила ÷ площадь; 6 ньютонов ÷ 2 квадратных метра = 3 паскаля.
    период — 3 секунды; частота — 20 колебаний в минуту; 3 × 20 = 60.

РАЗМЕРНОСТЬ ЕСТЬ ПРОВЕРКА, КОТОРАЯ НИЧЕГО НЕ СТОИТ И ЛОВИТ ВСЁ: закон,
чьи стороны расходятся размерностью, неверен ДО всякого числа. Формула
размерности объявлена в генераторе слоя (её нельзя вывести из имени
величины), и суд сверяет с объявлением — как имя знака.

СОХРАНЕНИЕ ПРОВЕРЯЕТСЯ РАВЕНСТВОМ СУММ, давление — делением нацело,
волна — произведением периода на частоту. Всё исполнимо, и потому
ничего не принимается на веру.
"""
import ast
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

ГЕНЕРАТОР = КОРЕНЬ / "tools/gen_genesis_physlaws.py"


def объявленные_размерности():
    """{имя величины: (формула, единица)} — из генератора слоя."""
    вон = {}
    try:
        дерево = ast.parse(ГЕНЕРАТОР.read_text(encoding="utf-8"))
    except OSError:
        return вон
    for узел in дерево.body:
        if (isinstance(узел, ast.Assign)
                and getattr(узел.targets[0], "id", None) == "РАЗМЕРНОСТИ"):
            try:
                ряды = ast.literal_eval(узел.value)
            except (ValueError, SyntaxError):
                return вон
            for ру, en, форм, ру_ед, en_ед in ряды:
                вон[ру] = (форм, ру_ед)
                вон[en] = (форм, en_ед)
    return вон


РАЗМЕРНОСТИ = объявленные_размерности()

РАЗМЕРНОСТЬ = re.compile(
    r"^(?:размерность величины (\S+) есть (.+?); измеряется в (.+?)"
    r"|the dimension of (\S+) is (.+?); it is measured in (.+?))\.$")
ИМПУЛЬС = re.compile(
    r"^(?:импульс сохраняется: было (\d+) и (\d+), стало (\d+), "
    r"сумма не изменилась"
    r"|momentum is conserved: (\d+) and (\d+) before, (\d+) after, "
    r"the sum did not change)\.$")
ЭНЕРГИЯ = re.compile(
    r"^(?:энергия сохраняется: (\d+) \S+ разделились на (\d+) и (\d+) \S+"
    r"|energy is conserved: (\d+) joules split into (\d+) and "
    r"(\d+) joules)\.$")
ДАВЛЕНИЕ = re.compile(
    r"^(?:давление = сила ÷ площадь; (\d+) \S+ ÷ (\d+) [^=]+= (\d+) \S+"
    r"|pressure = force ÷ area; (\d+) newtons ÷ (\d+) square metres "
    r"= (\d+) pascals)\.$")
# ОТКАЗ ЕСТЬ ТАКОЕ ЖЕ УТВЕРЖДЕНИЕ: «целого нет» истинно ровно тогда,
# когда сила и вправду не делится на площадь нацело. Суд считает
# остаток, а не верит слову «нет».
ОТКАЗ_ДАВЛЕНИЯ = re.compile(
    r"^(?:целого ответа нет: (\d+) ньютон\S* на (\d+) квадратн\S+ "
    r"метр\S* не да[её]?т?ю?т? целого давления, (\d+) не делится на "
    r"(\d+) нацело"
    r"|no whole answer: (\d+) newtons over (\d+) square metres do not "
    r"give a whole pressure, (\d+) is not divisible by (\d+))\.$")
ВОЛНА = re.compile(
    r"^(?:период — (\d+) \S+; частота — (\d+) [^;]+; (\d+) × (\d+) = 60"
    r"|the period is (\d+) \S+; the frequency is (\d+) per minute; "
    r"(\d+) × (\d+) = 60)\.$")
СКОРОСТЬ_ВОЛНЫ = re.compile(
    r"^(?:скорость волны = длина ÷ период; (\d+) \S+ ÷ (\d+) \S+ = "
    r"(\d+) \S+ в секунду"
    r"|wave speed = length ÷ period; (\d+) metres ÷ (\d+) \S+ = "
    r"(\d+) metres per second)\.$")


def _числа(m):
    return [int(x) for x in m.groups() if x is not None and x.isdigit()]


def судить(строка):
    """(судимо, истинно) для одной строки."""
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ, А РОД ОПРЕДЕЛЯЕТСЯ ОТВЕТОМ.
    # Связь половин держит общий дом `tools/asking.py`: величины
    # вопроса суть начальный отрезок величин ответа, и порча любой из
    # них рвёт пару. Без этого суд читал бы вторую половину строки и
    # звал истиной вопрос, спрашивающий о другом.
    если = asking.судить_парой(строка, судить)
    if если is not None:
        return если
    с = строка.strip()
    m = РАЗМЕРНОСТЬ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        имя, форм, ед = г[0], г[1], г[2]
        объявлено = РАЗМЕРНОСТИ.get(имя)
        if объявлено is None:
            return False, True
        return True, объявлено == (форм, ед)
    m = ИМПУЛЬС.match(с)
    if m:
        a, b, итог = _числа(m)
        return True, a + b == итог
    m = ЭНЕРГИЯ.match(с)
    if m:
        целое, часть, остаток = _числа(m)
        return True, часть + остаток == целое
    m = ДАВЛЕНИЕ.match(с)
    if m:
        сила, площадь, p = _числа(m)
        return True, площадь > 0 and сила == p * площадь
    m = ОТКАЗ_ДАВЛЕНИЯ.match(с)
    if m:
        г = [int(x) for x in m.groups() if x is not None]
        сила, площадь, сила2, площадь2 = г
        return True, (сила == сила2 and площадь == площадь2
                      and площадь != 0 and сила % площадь != 0)
    m = ВОЛНА.match(с)
    if m:
        период, частота, п2, ч2 = _числа(m)
        return True, (период == п2 and частота == ч2
                      and период * частота == 60)
    m = СКОРОСТЬ_ВОЛНЫ.match(с)
    if m:
        длина, период, скорость = _числа(m)
        return True, период > 0 and длина == скорость * период
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ЗАКОНЫ ФИЗИКИ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    if not РАЗМЕРНОСТИ:
        print("ЗАКОНЫ ФИЗИКИ ОТКАЗ: размерности не объявлены")
        return 2
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ЗАКОНЫ ФИЗИКИ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"ЗАКОНЫ ФИЗИКИ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
