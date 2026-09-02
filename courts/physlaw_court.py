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
    r"^(?:(\w+) сохраняется: было (\d+) и (\d+), стало (\d+), "
    r"сумма не изменилась"
    r"|(\w+) is conserved: (\d+) and (\d+) before, (\d+) after, "
    r"the sum did not change)\.$")
ИМЕНА_ИМПУЛЬСА = {"импульс", "momentum"}
ЭНЕРГИЯ = re.compile(
    r"^(?:(\w+) сохраняется: (\d+) \S+ разделились на (\d+) и (\d+) \S+"
    r"|(\w+) is conserved: (\d+) joules split into (\d+) and "
    r"(\d+) joules)\.$")
ИМЕНА_ЭНЕРГИИ = {"энергия", "energy"}
# ИМЯ ЗАКОНА ЧИТАЕТСЯ ГРУППОЙ И СВЕРЯЕТСЯ, А НЕ ЗАШИВАЕТСЯ В ОБРАЗЕЦ.
# Подсадка словом: «давлениЕ = сила ÷ площадь; 42 ньютона ÷ 6 квадратных
# метров = 7 паскалей» → «давлени = …» — образец с зашитым именем не
# совпадал, суд МОЛЧАЛ, а суд согласования, читающий счётные формы, звал
# строку истиной. Строка с объявленным отношением «сила ÷ площадь» под
# искажённым именем лжёт об имени — и лжёт СУДИМО. Имя берётся группой,
# и всё, что не «давление»/«pressure» при этом отношении, есть ложь.
ДАВЛЕНИЕ = re.compile(
    r"^(?:(\w+) = сила ÷ площадь; (\d+) \S+ ÷ (\d+) [^=]+= (\d+) \S+"
    r"|(\w+) = force ÷ area; (\d+) newtons ÷ (\d+) square metres "
    r"= (\d+) pascals)\.$")
ИМЕНА_ДАВЛЕНИЯ = {"давление", "pressure"}
# ЦЕЛОСТЬ — ВЕРДИКТ С ОСНОВАНИЕМ: «да» несёт частное, «нет» — остаток;
# суд считает деление, а не верит слову.
ЦЕЛОСТЬ_ДАВЛЕНИЯ = re.compile(
    r"^(?:да: (\d+) ньютон\S* на (\d+) квадратн\S+ метр\S* да[её]?т?ю?т? "
    r"(\d+) ÷ (\d+) = (\d+) паскал\S*"
    r"|нет: (\d+) ньютон\S* на (\d+) квадратн\S+ метр\S* не да[её]?т?ю?т? "
    r"целого давления, (\d+) не делится на (\d+) нацело"
    r"|yes: (\d+) newtons over (\d+) square metres give (\d+) ÷ (\d+) = (\d+) pascals"
    r"|no: (\d+) newtons over (\d+) square metres do not give a whole pressure, "
    r"(\d+) is not divisible by (\d+))\.$")
ВОЛНА = re.compile(
    r"^(?:период — (\d+) \S+; частота — (\d+) [^;]+; (\d+) × (\d+) = 60"
    r"|the period is (\d+) \S+; the frequency is (\d+) per minute; "
    r"(\d+) × (\d+) = 60)\.$")
СКОРОСТЬ_ВОЛНЫ = re.compile(
    r"^(?:(\w+) волны = длина ÷ период; (\d+) \S+ ÷ (\d+) \S+ = "
    r"(\d+) \S+ в секунду"
    r"|wave speed = length ÷ period; (\d+) metres ÷ (\d+) \S+ = "
    r"(\d+) metres per second)\.$")


import discourse  # noqa: E402
import laws  # noqa: E402
ЗАКОНЫ = laws.свод("physlaws")
ЗАКОН_ДАВЛЕНИЯ = {"en": laws.ЗАКОНЫ["physlaws"][0][2], "ru": laws.ЗАКОНЫ["physlaws"][0][3]}
ВОПРОС_ДАВЛЕНИЯ = re.compile(
    r"^(?:what is the pressure of (\d+) newtons on (\d+) square metres"
    r"|каково давление силы (\d+) \S+ на (\d+) квадратн\S+ метр\S*"
    r"|why is the pressure of (\d+) newtons on (\d+) square metres equal to (\d+) pascals"
    r"|почему давление силы (\d+) \S+ на (\d+) квадратн\S+ метр\S* равно (\d+) \S+)$")
СВИД_ДАВЛЕНИЯ = re.compile(r"^(\d+) (?:newtons|\S+) ÷ (\d+) (?:square metres|квадратн\S+ метр\S*) = (\d+) (?:pascals|\S+)$")
ВЫВОД_ДАВЛЕНИЯ = re.compile(r"^(?:the pressure is (\d+) pascals|давление — (\d+) \S+)$")


def _рассуждение(с):
    """Рассуждение о давлении судится частями (дом речи)."""
    язык = "ru" if re.search(r"[а-яё]", с) else "en"
    ч_ = discourse.части(с, язык)
    if ч_ is None:
        return None
    м = ВОПРОС_ДАВЛЕНИЯ.match(ч_["вопрос"])
    if not м:
        return None
    if ч_["связка"] is None or ч_["вердикт"] is not None:
        return True, False
    г = [int(x) for x in м.groups() if x is not None]
    сила, площадь = г[0], г[1]
    if площадь == 0 or сила % площадь:
        return True, False
    p = сила // площадь
    if len(г) > 2 and г[2] != p:
        return True, False
    св = СВИД_ДАВЛЕНИЯ.match(ч_["свидетель"])
    выв = ВЫВОД_ДАВЛЕНИЯ.match(ч_["вывод"])
    return True, (bool(св) and [int(x) for x in св.groups()] == [сила, площадь, p]
                  and bool(выв) and int(next(x for x in выв.groups() if x)) == p
                  and ч_["закон"] == ЗАКОН_ДАВЛЕНИЯ[язык])


def _числа(m):
    return [int(x) for x in m.groups() if x is not None and x.isdigit()]


def судить(строка):
    """(судимо, истинно) для одной строки."""
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ, А РОД ОПРЕДЕЛЯЕТСЯ ОТВЕТОМ.
    # Связь половин держит общий дом `tools/asking.py`: величины
    # вопроса суть начальный отрезок величин ответа, и порча любой из
    # них рвёт пару. Без этого суд читал бы вторую половину строки и
    # звал истиной вопрос, спрашивающий о другом.
    if строка.strip() in ЗАКОНЫ:
        return True, True
    р = _рассуждение(строка.strip())
    if р is not None:
        return р
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
        имя = next((g for g in m.groups() if g is not None and not g.isdigit()), None)
        if имя is not None and имя not in ИМЕНА_ИМПУЛЬСА:
            return True, False
        a, b, итог = _числа(m)
        return True, a + b == итог
    m = ЭНЕРГИЯ.match(с)
    if m:
        имя = next((g for g in m.groups() if g is not None and not g.isdigit()), None)
        if имя is not None and имя not in ИМЕНА_ЭНЕРГИИ:
            return True, False
        целое, часть, остаток = _числа(m)
        return True, часть + остаток == целое
    m = ДАВЛЕНИЕ.match(с)
    if m:
        имя = m.group(1) or m.group(5)
        if имя not in ИМЕНА_ДАВЛЕНИЯ:
            return True, False
        сила, площадь, p = _числа(m)
        return True, площадь > 0 and сила == p * площадь
    m = ЦЕЛОСТЬ_ДАВЛЕНИЯ.match(с)
    if m:
        г = [int(x) for x in m.groups() if x is not None]
        if len(г) == 5:
            сила, площадь, сила2, площадь2, частное = г
            return True, ((сила, площадь) == (сила2, площадь2) and площадь != 0
                          and сила == частное * площадь)
        сила, площадь, сила2, площадь2 = г
        return True, ((сила, площадь) == (сила2, площадь2)
                      and площадь != 0 and сила % площадь != 0)
    m = ВОЛНА.match(с)
    if m:
        период, частота, п2, ч2 = _числа(m)
        return True, (период == п2 and частота == ч2
                      and период * частота == 60)
    m = СКОРОСТЬ_ВОЛНЫ.match(с)
    if m:
        имя = m.group(1)
        if имя is not None and имя != "скорость":
            return True, False
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
