#!/usr/bin/env python3
"""[КАЛЕНДАРЬ] — суд ПРОХОДИТ круг недели заново.

    4 days after wednesday comes sunday.   → суд считает по модулю 7
    march is month number 3 and has 31 days.
    the first 3 months of a common year have 90 days in all.

НЕДЕЛЯ ЕСТЬ СРАВНЕНИЕ ПО МОДУЛЮ СЕМЬ В ОДЕЖДЕ, и потому проверяется
тем же счётом, каким суд чисел проверяет остаток. Имена дней и длины
месяцев объявлены фактом — их нельзя вывести, их знают, — но всякий
ОТВЕТ выводится из них счётом, а не берётся из второго списка.

ПОРЯДОК ИМЁН ЕСТЬ ЕДИНСТВЕННОЕ ОБЪЯВЛЕНИЕ, И ОН ЧИТАЕТСЯ ИЗ ГЕНЕРАТОРА
СЛОЯ — не потому, что суду лень, а потому, что второй список имён
разошёлся бы с первым в день, когда тронут любой. Отсутствие
объявления есть ОТКАЗ, а не чистота (М-88).
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

ГЕНЕРАТОР = КОРЕНЬ / "tools/gen_genesis_calendar.py"


def объявленное():
    """Имена и длины из генератора слоя; пусто — отказ, а не чистота."""
    вон = {}
    try:
        дерево = ast.parse(ГЕНЕРАТОР.read_text(encoding="utf-8"))
    except OSError:
        return вон
    for узел in дерево.body:
        if not (isinstance(узел, ast.Assign)
                and isinstance(узел.targets[0], ast.Name)):
            continue
        try:
            вон[узел.targets[0].id] = ast.literal_eval(узел.value)
        except (ValueError, SyntaxError):
            continue
    return вон


ОБЪЯВЛЕНО = объявленное()
НУЖНО = ("ДНИ_RU", "ДНИ_EN", "ДНИ_RU_РОД", "ДНИ_RU_ТВОР", "ДНИ_RU_БЫЛ",
         "МЕСЯЦЫ_RU", "МЕСЯЦЫ_EN", "МЕСЯЦЫ_RU_РОД",
         "МЕСЯЦЫ_RU_ТВОР", "ДЛИНЫ")

# THE LEDGER OF THE CYCLE after the colon (03.09): «2 + 3 = 5, day 5 is
# friday», over the edge «6 + 3 = 9, 9 − 7 = 2, день 2 — вторник»
ЛЕДЖЕР_КРУГА = (r"(?:: (\d+) \+ (\d+) = (\d+)(?:, (\d+) − 7 = (\d+))?, "
                r"(?:day (\d+) is|день (\d+) —) (\w+))?")
ЧЕРЕЗ = re.compile(
    r"^(?:(\d+) days? after (\w+) comes (\w+)"
    r"|через (\d+) \S+ после (\w+) наступает (\w+))" + ЛЕДЖЕР_КРУГА + r"\.$")
СОСЕД = re.compile(
    r"^(?:the day (after|before) (\w+) is (\w+)"
    r"|день (после|перед) (\w+) — это (\w+))\.$")
НОМЕР_ДНЯ = re.compile(
    r"^(?:(\w+) is day number (\d+) of the week"
    r"|(\w+) — день номер (\d+) недели)\.$")
МЕСЯЦ = re.compile(
    r"^(?:(\w+) is month number (\d+) and has (\d+) days"
    r"|(\w+) — месяц номер (\d+), в нём (\d+) \S+)\.$")
МЕСЯЦ_ПОСЛЕ = re.compile(
    r"^(?:the month after (\w+) is (\w+)"
    r"|месяц после (\w+) — это (\w+))\.$")
# СЧЁТ ПРАВИТ ФОРМОЙ И ГЛАГОЛА: «the first month … has», «the first 2
# months … have» — единица без числительного читается единицей.
ПЕРВЫЕ_МЕСЯЦЫ = re.compile(
    r"^(?:the first (?:(\d+) months|(month)) of a common year (?:have|has) (\d+) days in all"
    r"|\S+ (\d+) \S+ обычного года дают (\d+) \S+ всего)\.$")
# КОЛЕСО ПАРОЙ: связь живёт ВНУТРИ показа, и суд проходит круг для
# обеих половин — названной и выведенной.
ПАРА_ПОСЛЕ = re.compile(
    r"^(?:сегодня (\w+)\. после (\w+) — (\w+)"
    r"|today is (\w+)\. after (\w+) comes (\w+))\.$")
ПАРА_ПЕРЕД = re.compile(
    r"^(?:сегодня (\w+)\. перед (\w+) был\w? (\w+)"
    r"|today is (\w+)\. before (\w+) was (\w+))\.$")
# ВОПРОСНАЯ ПОВЕРХНОСТЬ ТОГО ЖЕ КРУГА. Порядок скобок нарочно один и
# тот же в обоих языках — (сторона, откуда, откуда, куда), — чтобы суд
# не гадал, где ответ: разошедшийся порядок и есть та щель, в которую
# уходит вердикт о чужом дне.
ВОПРОС_СОСЕД = re.compile(
    r"^(?:what (?:day|month) comes (after|before) (\w+)\? "
    r"(?:after|before) (\w+) comes (\w+)"
    r"|какой (?:день|месяц) (?:идёт )?(после|перед) (\w+)\? "
    r"(?:после|перед) (\w+) — (\w+))\.$")
# ВЧЕРА И ЗАВТРА ОТ НАЗВАННОГО СЕГОДНЯ (06.09): круг проходится на шаг назад или вперёд
ВОПРОС_ВЧЕРА = re.compile(
    r"^(?:today is (\w+)\. what day (was yesterday|will it be tomorrow)\? (\w+)"
    r"|сегодня (\w+)\. какой день (был вчера|будет завтра)\? (\w+))\.$")
ВОПРОС_ЧЕРЕЗ = re.compile(
    r"^(?:what day is (\d+) days after (\w+)\? "
    r"(\d+) days after (\w+) comes (\w+)"
    r"|какой день через (\d+) \S+ после (\w+)\? "
    r"через (\d+) \S+ после (\w+) — (\w+))" + ЛЕДЖЕР_КРУГА + r"\.$")
ГОД = re.compile(
    r"^(?:a common year has (\d+) days and (\d+) full weeks"
    r"|обычный год имеет (\d+) дней и (\d+) полных недели)\.$")


def круг(имя):
    """(индекс, длина круга) по любому объявленному имени, или None."""
    для = (("ДНИ_EN", "ДНИ_RU", "ДНИ_RU_РОД", "ДНИ_RU_ТВОР"),
           ("МЕСЯЦЫ_EN", "МЕСЯЦЫ_RU", "МЕСЯЦЫ_RU_РОД",
            "МЕСЯЦЫ_RU_ТВОР"))
    for семья in для:
        for ключ in семья:
            ряд = ОБЪЯВЛЕНО.get(ключ)
            if ряд and имя in ряд:
                return ряд.index(имя), len(ряд)
    return None


def _леджер_круга(хвост, откуда, k, куда):
    """The chain after the colon, when written: «i + k = s[, s − 7 = j], day
    j is Y» — i and j the declared day numbers (index + 1), Y the day named."""
    if not хвост:
        return True
    ч = [int(x) for x in хвост[:-1]]
    имя = хвост[-1]
    i, j = откуда[0] + 1, куда[0] + 1
    s = i + k
    ожидание = [i, k, s] + ([s, s - 7] if s > 7 else []) + [j]
    return ч == ожидание and (s - 7 if s > 7 else s) == j and круг(имя) == куда and имя in (ОБЪЯВЛЕНО.get("ДНИ_EN", ()) + ОБЪЯВЛЕНО.get("ДНИ_RU", ()))


def судить(строка):
    """(судимо, истинно) для одной строки."""
    if not all(к in ОБЪЯВЛЕНО for к in НУЖНО):
        return False, True
    с = строка.strip()
    m = ЧЕРЕЗ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        k, откуда, куда = int(г[0]), круг(г[1]), круг(г[2])
        if откуда is None or куда is None:
            return False, True
        return True, (откуда[0] + k) % откуда[1] == куда[0] and _леджер_круга(г[3:], откуда, k, куда)
    m = ВОПРОС_ВЧЕРА.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        сегодня, куда, ответ = г
        откуда, к = круг(сегодня), круг(ответ)
        if откуда is None or к is None:
            return False, True
        шаг = -1 if куда in ("was yesterday", "был вчера") else 1
        return True, (откуда[0] + шаг) % откуда[1] == к[0]
    m = ВОПРОС_СОСЕД.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        сторона, спрошен, повтор, ответ = г[0], г[1], г[2], г[3]
        откуда, куда = круг(спрошен), круг(ответ)
        if откуда is None or куда is None or спрошен != повтор:
            return False, True
        шаг = 1 if сторона in ("after", "после") else -1
        return True, (откуда[0] + шаг) % откуда[1] == куда[0]
    m = ВОПРОС_ЧЕРЕЗ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        k, спрошен, k2, повтор, ответ = (int(г[0]), г[1], int(г[2]),
                                         г[3], г[4])
        откуда, куда = круг(спрошен), круг(ответ)
        if (откуда is None or куда is None or спрошен != повтор
                or k != k2):
            return False, True
        return True, (откуда[0] + k) % откуда[1] == куда[0] and _леджер_круга(г[5:], откуда, k, куда)
    m = СОСЕД.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        сторона, откуда, куда = г[0], круг(г[1]), круг(г[2])
        if откуда is None or куда is None:
            return False, True
        шаг = 1 if сторона in ("after", "после") else -1
        return True, (откуда[0] + шаг) % откуда[1] == куда[0]
    m = НОМЕР_ДНЯ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        где = круг(г[0])
        if где is None:
            return False, True
        return True, где[0] + 1 == int(г[1])
    m = МЕСЯЦ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        где = круг(г[0])
        if где is None:
            return False, True
        i = где[0]
        return True, (i + 1 == int(г[1])
                      and ОБЪЯВЛЕНО["ДЛИНЫ"][i] == int(г[2]))
    m = МЕСЯЦ_ПОСЛЕ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        откуда, куда = круг(г[0]), круг(г[1])
        if откуда is None or куда is None:
            return False, True
        return True, (откуда[0] + 1) % откуда[1] == куда[0]
    m = ПЕРВЫЕ_МЕСЯЦЫ.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        сколько, всего = (1 if г[0] == "month" else int(г[0])), int(г[1])
        if not 1 <= сколько <= len(ОБЪЯВЛЕНО["ДЛИНЫ"]):
            return True, False
        return True, sum(ОБЪЯВЛЕНО["ДЛИНЫ"][:сколько]) == всего
    for образец, шаг in ((ПАРА_ПОСЛЕ, 1), (ПАРА_ПЕРЕД, -1)):
        m = образец.match(с)
        if not m:
            continue
        г = [x for x in m.groups() if x is not None]
        сегодня, назван, сосед = (круг(x) for x in г)
        if None in (сегодня, назван, сосед):
            return False, True
        # НАЗВАННЫЙ ВТОРЫМ ОБЯЗАН БЫТЬ ТЕМ ЖЕ ДНЁМ: падежная форма и
        # именительная суть одно слово, и суд их сводит через круг.
        return True, (сегодня[0] == назван[0]
                      and (сегодня[0] + шаг) % сегодня[1] == сосед[0])
    m = ГОД.match(с)
    if m:
        г = [x for x in m.groups() if x is not None]
        дней, недель = int(г[0]), int(г[1])
        return True, (дней == sum(ОБЪЯВЛЕНО["ДЛИНЫ"])
                      and недель == дней // 7)
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"КАЛЕНДАРЬ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    if not all(к in ОБЪЯВЛЕНО for к in НУЖНО):
        нет = [к for к in НУЖНО if к not in ОБЪЯВЛЕНО]
        print(f"КАЛЕНДАРЬ ОТКАЗ: не объявлено {нет} — судить нечем")
        return 2
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("КАЛЕНДАРЬ ОТКАЗ: обход пуст, судить нечего")
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
    print(f"КАЛЕНДАРЬ {поза}: {ложных} ложных из {судимых} судимых "
          f"({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
