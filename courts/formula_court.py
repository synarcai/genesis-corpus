#!/usr/bin/env python3
"""[ФОРМУЛА И ДИАГРАММА] — записи проверяются подстановкой и обходом.

Формула и схема суть ЗНАКИ, а не украшение, и корпус, который их
показывает, обязан быть проверяем на них так же полно, как на числах.
Формула здесь подставляется своими же числами и вычисляется; диаграмма
разбирается, её узлы и рёбра пересчитываются, достижимость ОБХОДИТСЯ —
прибор не верит описанию, он идёт по графу.

СЕМЬ РОДОВ: теорема Пифагора на целых тройках; площадь прямоугольника
и треугольника; квадрат суммы и разность квадратов, поставленные
своими числами; сумма первых n; степень; и диаграмма — счётом узлов и
рёбер, длиной кратчайшего пути и числом рёбер, названным СЛОВОМ на
четырёх языках.

ЧЕГО ЗДЕСЬ НЕТ НАМЕРЕННО: приближений. Ни π, ни нецелых корней, ни
десятичных — корпус, объявляющий «3.14» значением окружности, учит
округление как истину. Приближение есть отдельный род, и ему нужен
свой суд прежде своих показов.
"""
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from genesis import Unreadable, worlds  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-corpus-file

# число, названное словом, на четырёх языках — ровно те, что слой пишет
СЛОВОМ = {"two": 2, "два": 2, "zwei": 2, "二": 2,
          "three": 3, "три": 3, "drei": 3, "三": 3,
          "four": 4, "четыре": 4, "vier": 4, "四": 4,
          "five": 5, "пять": 5, "fünf": 5, "五": 5}
РЕБРО = re.compile(r"([A-Za-z]\w*)\s*-->\s*(?:\|[^|]*\|\s*)?([A-Za-z]\w*)")
ГРАФ = re.compile(r"^graph\s+(?:TD|LR|TB|RL|BT)\s*;")


def разбор_графа(строка):
    """(узлы, рёбра) диаграммы mermaid, или None."""
    if not ГРАФ.match(строка.strip()):
        return None
    рёбра = РЕБРО.findall(строка)
    if not рёбра:
        return None
    узлы = {у for пара in рёбра for у in пара}
    return узлы, рёбра


def путь(рёбра, откуда, куда):
    """Длина кратчайшего пути ОБХОДОМ, или None."""
    смежность = collections.defaultdict(list)
    for a, b in рёбра:
        смежность[a].append(b)
    очередь, видано = collections.deque([(откуда, 0)]), {откуда}
    while очередь:
        узел, шагов = очередь.popleft()
        if узел == куда:
            return шагов
        for сосед in смежность[узел]:
            if сосед not in видано:
                видано.add(сосед)
                очередь.append((сосед, шагов + 1))
    return None


ФОРМЫ = [
    (r"^a\^2 \+ b\^2 = c\^2 with a = (\d+) and b = (\d+) gives c = (\d+)$",
     lambda a, b, c: int(a) ** 2 + int(b) ** 2 == int(c) ** 2),
    (r"^формула a\^2 \+ b\^2 = c\^2 при a = (\d+) и b = (\d+) "
     r"даёт c = (\d+)$",
     lambda a, b, c: int(a) ** 2 + int(b) ** 2 == int(c) ** 2),
    (r"^die formel a\^2 \+ b\^2 = c\^2 mit a = (\d+) und b = (\d+) "
     r"ergibt c = (\d+)$",
     lambda a, b, c: int(a) ** 2 + int(b) ** 2 == int(c) ** 2),
    (r"^the area of a rectangle (\d+) by (\d+) is (\d+)$",
     lambda a, b, c: int(a) * int(b) == int(c)),
    (r"^площадь прямоугольника (\d+) на (\d+) равна (\d+)$",
     lambda a, b, c: int(a) * int(b) == int(c)),
    (r"^the area of a triangle with base (\d+) and height (\d+) is (\d+)$",
     lambda a, b, c: int(a) * int(b) == 2 * int(c)),
    (r"^площадь треугольника с основанием (\d+) и высотой (\d+) "
     r"равна (\d+)$",
     lambda a, b, c: int(a) * int(b) == 2 * int(c)),
    (r"^\( (\d+) \+ (\d+) \)\^2 = (\d+)\^2 \+ 2 × \3 × (\d+) \+ \4\^2 = "
     r"(\d+)$",
     lambda a, b, c, d, e: (int(a) + int(b)) ** 2 == int(e)),
    (r"^\( (\d+) \+ (\d+) \)\^2 = (\d+)$",
     lambda a, b, c: (int(a) + int(b)) ** 2 == int(c)),
    (r"^(\d+)\^2 − (\d+)\^2 = \( \1 − \2 \) × \( \1 \+ \2 \) = (\d+)$",
     lambda a, b, c: int(a) ** 2 - int(b) ** 2 == int(c)),
    (r"^the sum of the first (\d+) numbers is (\d+)$",
     lambda a, b: int(a) * (int(a) + 1) // 2 == int(b)),
    (r"^сумма первых (\d+) чисел равна (\d+)$",
     lambda a, b: int(a) * (int(a) + 1) // 2 == int(b)),
]
ФОРМЫ += [
    # законы степеней, поставленные числами
    (r"^(\d+)\^(\d+) × \1\^(\d+) = \1\^(\d+)$",
     lambda a, m, n, k: int(m) + int(n) == int(k)),
    (r"^\( (\d+)\^(\d+) \)\^(\d+) = \1\^(\d+)$",
     lambda a, m, n, k: int(m) * int(n) == int(k)),
    # приведение подобных: правило и его оправдание
    (r"^(\d+) x \+ (\d+) x = (\d+) x$",
     lambda p_, q, r: int(p_) + int(q) == int(r)),
    (r"^при x = (\d+) это (\d+) \+ (\d+) = (\d+)$",
     lambda x, a, b, c: int(a) + int(b) == int(c)),
    (r"^with x = (\d+) this is (\d+) \+ (\d+) = (\d+)$",
     lambda x, a, b, c: int(a) + int(b) == int(c)),
    # распределительный закон, поставленный числами
    (r"^(\d+) × \( (\d+) \+ (\d+) \) = (\d+) \+ (\d+)$",
     lambda a, b, c, d, e: int(a) * int(b) == int(d)
     and int(a) * int(c) == int(e)),
    # индексы
    (r"^x_1 = (\d+) and x_2 = (\d+), so x_1 \+ x_2 = (\d+)$",
     lambda a, b, c: int(a) + int(b) == int(c)),
    (r"^x_1 = (\d+) и x_2 = (\d+), значит x_1 \+ x_2 = (\d+)$",
     lambda a, b, c: int(a) + int(b) == int(c)),
    # отношения
    (r"^(\d+) ≥ (\d+)$", lambda a, b: int(a) >= int(b)),
    (r"^(\d+) ≤ (\d+)$", lambda a, b: int(a) <= int(b)),
    (r"^(\d+) ≠ (\d+)$", lambda a, b: int(a) != int(b)),
    (r"^(\d+) = (\d+), поэтому × перестановочно$",
     lambda a, b: int(a) == int(b)),
]
СОБРАНО = [(re.compile(о), ф) for о, ф in ФОРМЫ]

# ИМЯ ЗНАКА — ФАКТ ЯЗЫКА, и читается из пакета, а не пишется тут.
ПАКЕТЫ = КОРЕНЬ / "tools/langpacks"
НАЗВАН = re.compile(
    r"^(\S+) (?:is called|называется|heisst) (.+?)$")


def имена_знаков():
    вон = {}
    if not ПАКЕТЫ.is_dir():
        return вон
    for ф in sorted(ПАКЕТЫ.glob("*.json")):
        try:
            import json as _json
            п = _json.loads(ф.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for знак, имя in (п.get("sign_names") or {}).items():
            имена = [имя] if isinstance(имя, str) else list(имя)
            вон.setdefault(знак, set()).update(
                str(x).lower() for x in имена)
    return вон


ИМЕНА = имена_знаков()

# ТОЖДЕСТВО, СКАЗАННОЕ БУКВАМИ, ПРОВЕРЯЕТСЯ ПОДСТАНОВКОЙ ПО ДИАПАЗОНУ.
# Правило «a^m × a^n = a^( m + n )» не содержит чисел, и прибор,
# принимающий его на веру, оставляет самое важное непроверенным: именно
# правило организм и должен купить. Каждое объявленное тождество
# ставится всеми значениями малого диапазона; одно расхождение — ложь.
ТОЖДЕСТВА = {
    "a^m × a^n = a^( m + n )":
        lambda a, m, n: a ** m * a ** n == a ** (m + n),
    "( a^m )^n = a^( m × n )":
        lambda a, m, n: (a ** m) ** n == a ** (m * n),
    "a × ( b + c ) = a × b + a × c":
        lambda a, b, c: a * (b + c) == a * b + a * c,
}
ДИАПАЗОН = range(2, 6)


def тождество_держится(правило):
    проверка = ТОЖДЕСТВА[правило]
    return all(проверка(x, y, z)
               for x in ДИАПАЗОН for y in ДИАПАЗОН for z in ДИАПАЗОН)
УЗЛЫ_EN = re.compile(r"^this graph has (\d+) nodes and (\d+) edges$")
УЗЛЫ_RU = re.compile(r"^этот граф имеет (\d+) узл\w+ и (\d+) р[её]б\w+$")
ПУТЬ_EN = re.compile(
    r"^in this graph (\w+) reaches (\w+) in (\d+) steps?$")
РЁБЕР_СЛОВОМ = re.compile(
    r"^(?:the diagram has|диаграмма имеет|das diagramm hat)\s+(\S+)\s+"
    r"(?:edges|ребра|рёбер|kanten)\.?$")
РЁБЕР_ZH = re.compile(r"^这个图有(\S)条边$")


ХВОСТ = re.compile(r"^graph\s+(?:TD|LR|TB|RL|BT)\s*;(?:[^;]*;)*\s*")


def судить(строка, граф=None):
    """(судимо, истинно) — показ САМОДОСТАТОЧЕН.

    Описание диаграммы несёт свою диаграмму: перестановка проходов
    разводит соседние строки, и «этот граф имеет 3 узла» без своего
    графа не значит ничего. Прибор поэтому читает граф ИЗ ТОЙ ЖЕ
    строки, а не помнит предыдущую.
    """
    с = строка.strip().rstrip(".。")
    граф = разбор_графа(строка)
    if граф:
        хвост = ХВОСТ.sub("", строка).strip().rstrip(".。")
        if not хвост:
            return False, True
        с = хвост
    for образец, проверка in СОБРАНО:
        m = образец.match(с)
        if m:
            return True, bool(проверка(*m.groups()))
    if с in ТОЖДЕСТВА:
        return True, тождество_держится(с)
    m = НАЗВАН.match(с)
    if m and m.group(1) in ИМЕНА:
        return True, m.group(2).strip().lower() in ИМЕНА[m.group(1)]
    if граф:
        узлы, рёбра = граф
        m = УЗЛЫ_EN.match(с) or УЗЛЫ_RU.match(с)
        if m:
            return True, (len(узлы) == int(m.group(1))
                          and len(рёбра) == int(m.group(2)))
        m = ПУТЬ_EN.match(с)
        if m:
            д = путь(рёбра, m.group(1), m.group(2))
            return True, д == int(m.group(3))
        m = РЁБЕР_СЛОВОМ.match(с) or РЁБЕР_ZH.match(с)
        if m:
            сколько = СЛОВОМ.get(m.group(1))
            if сколько is not None:
                return True, сколько == len(рёбра)
    return False, True


def обход(явные):
    if явные:
        return [pathlib.Path(п) for п in явные]
    try:
        return worlds(kind="shows")
    except Unreadable as беда:
        print(f"ФОРМУЛЫ ОТКАЗ: {беда}")
        sys.exit(2)


def main():
    явные = [а for а in sys.argv[1:] if not а.startswith("-")]
    пути = [п for п in обход(явные) if п.is_file()]
    if not пути:
        print("ФОРМУЛЫ ОТКАЗ: обход пуст, судить нечего")
        return 2
    ложных = судимых = 0
    примеры = []
    for путь_ in пути:
        свои = 0
        with путь_.open(encoding="utf-8", errors="replace") as поток:
            for строка in поток:
                судимо, истинно = судить(строка)
                if not судимо:
                    continue
                судимых += 1
                if not истинно:
                    ложных += 1
                    свои += 1
                    if len(примеры) < 4:
                        примеры.append(f"{путь_.name}: {строка.strip()[:70]}")
        if свои:
            print(f"  {путь_.name:<30} ложных {свои}")
    for п in примеры:
        print(f"    {п}")
    поза = "ЛЕНТА" if явные else (
        "PASS" if ложных <= ЛОЖНЫХ_РУБЕЖ else "FAIL")
    print(f"ФОРМУЛЫ {поза}: {ложных} ложных записей из {судимых} "
          f"судимых ({len(пути)} файлов)")
    if явные:
        return 0
    return 0 if ложных <= ЛОЖНЫХ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
