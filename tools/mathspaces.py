#!/usr/bin/env python3
"""МАТЕМАТИЧЕСКИЕ ПРОСТРАНСТВА — носитель, нотация, исполнители одним домом.

Мандат 02.09 §L3: «представлять все известные пространства, включая
математические» = каждое пространство есть (носитель, нотация, группа
преобразований, исполнители, показы). Нотации согласованы с holon
(02.09): ОДИН СПАН на пространство, читаемый по письменной форме, без
точки внутри:
  · точка евклидовой плоскости «(3, 4)» — целые координаты, знак «−»;
  · граф «graph 1-2, 2-3, 3-1» — список рёбер, вершины числами;
  · плоскость Фано — семь линий тройками «124, 235, 346, 457, 561, 672,
    713» (циклический сдвиг разностного множества {1, 2, 4} по модулю 7),
    линия «124»;
  · матрица «[1 2 / 3 4]» — строки через «/», элементы пробелами.
Исполнители ниже — закон и генератора, и суда: суд исполняет заново.
Границы: только целые итоги (расстояние — лишь пифагоровы тройки,
середина — лишь целая), дробное не произносится вовсе.
"""
import collections
import re

МИНУС = "−"


# ---------- ТОЧКИ ----------
ТОЧКА = re.compile(r"\((−?\d+), (−?\d+)\)")


def точка(текст):
    м = ТОЧКА.fullmatch(текст)
    return (int(м.group(1).replace(МИНУС, "-")), int(м.group(2).replace(МИНУС, "-"))) if м else None


def число(n):
    return str(n).replace("-", МИНУС)


def запись_точки(p):
    return f"({число(p[0])}, {число(p[1])})"


def расстояние(a, b):
    """Целое расстояние или None — не целое (не произносится)."""
    d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
    d = int(round(d2 ** 0.5))
    return d if d * d == d2 else None


def середина(a, b):
    sx, sy = a[0] + b[0], a[1] + b[1]
    return (sx // 2, sy // 2) if sx % 2 == 0 and sy % 2 == 0 else None


def сдвиг(a, v):
    return (a[0] + v[0], a[1] + v[1])


def отражение(a, ось):
    return (a[0], -a[1]) if ось == "x" else (-a[0], a[1])


def поворот(a, градусов):
    """Против часовой стрелки вокруг начала координат."""
    x, y = a
    return {90: (-y, x), 180: (-x, -y), 270: (y, -x)}[градусов]


# ---------- ГРАФЫ ----------
ГРАФ = re.compile(r"graph (\d+-\d+(?:, \d+-\d+)*)")
РЕБРО = re.compile(r"(\d+)-(\d+)")


def граф(текст):
    """{вершина: множество соседей} по списку рёбер; None — не граф."""
    м = re.fullmatch(r"(?:graph |граф )?(\d+-\d+(?:, \d+-\d+)*)", текст)
    if not м:
        return None
    смеж = collections.defaultdict(set)
    for a, b in РЕБРО.findall(м.group(1)):
        смеж[int(a)].add(int(b))
        смеж[int(b)].add(int(a))
    return dict(смеж)


def рёбра(г):
    return sorted({tuple(sorted((a, b))) for a in г for b in г[a]})


def степень(г, v):
    return len(г.get(v, ()))


def путь(г, a, b):
    """Кратчайший путь списком вершин или None."""
    if a not in г or b not in г:
        return None
    пред = {a: None}
    очередь = collections.deque([a])
    while очередь:
        v = очередь.popleft()
        if v == b:
            вон = []
            while v is not None:
                вон.append(v)
                v = пред[v]
            return вон[::-1]
        for w in sorted(г[v]):
            if w not in пред:
                пред[w] = v
                очередь.append(w)
    return None


def связен(г):
    if not г:
        return True
    старт = min(г)
    return all(путь(г, старт, v) is not None for v in г)


def цикл_есть(г, вершины):
    """Замкнутый обход по рёбрам графа: все рёбра цикла присутствуют."""
    if len(вершины) < 4 or вершины[0] != вершины[-1]:
        return False
    return all(b in г.get(a, ()) for a, b in zip(вершины, вершины[1:]))


# ---------- ФАНО ----------
ФАНО = ("124", "235", "346", "457", "561", "672", "713")


def линия_через(p, q):
    return next(л for л in ФАНО if str(p) in л and str(q) in л)


def пересечение(л1, л2):
    return int(next(с for с in л1 if с in л2))


def линии_через(p):
    return [л for л in ФАНО if str(p) in л]


# ---------- МАТРИЦЫ ----------
МАТРИЦА = re.compile(r"\[((?:−?\d+ )*−?\d+(?: / (?:−?\d+ )*−?\d+)*)\]")


def матрица(текст):
    """Матрица по записи «[1 2 / 3 4]» или по её содержимому «1 2 / 3 4»."""
    м = (re.fullmatch(r"(?:matrix |матрица )?" + МАТРИЦА.pattern, текст)
         or re.fullmatch(r"(?:−?\d+ )*−?\d+(?: / (?:−?\d+ )*−?\d+)*", текст) and
         re.fullmatch(r"(.*)", текст))
    if not м:
        return None
    строки = [[int(x.replace(МИНУС, "-")) for x in р.split()] for р in м.group(1).split(" / ")]
    return строки if len({len(р) for р in строки}) == 1 else None


def запись_матрицы(m):
    return "[" + " / ".join(" ".join(число(x) for x in р) for р in m) + "]"


def транспонированная(m):
    return [list(к) for к in zip(*m)]


def сумма(a, b):
    return [[x + y for x, y in zip(ра, рб)] for ра, рб in zip(a, b)]


def на_вектор(m, v):
    return tuple(sum(x * y for x, y in zip(р, v)) for р in m)


def след(m):
    return sum(m[i][i] for i in range(len(m)))


def определитель(m):
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return sum((-1) ** j * m[0][j] * определитель(
        [р[:j] + р[j + 1:] for р in m[1:]]) for j in range(n))
