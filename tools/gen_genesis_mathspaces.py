#!/usr/bin/env python3
"""МАТЕМАТИЧЕСКИЕ ПРОСТРАНСТВА v0 — четыре пространства, четыре спана.

Мандат 02.09 §L3 («представлять все известные пространства, включая
математические»), нотации согласованы с holon: точка «(3, 4)», граф
«graph 1-2, 2-3, 3-1», плоскость Фано «124, 235, 346, 457, 561, 672,
713», матрица «[1 2 / 3 4]». Каждое пространство — своя группа показов
в проходе (emit_grouped: роды не мешаются), исполнители — дом
tools/mathspaces.py, общий с судом. Обе полярности с основанием после
двоеточия, которое суд пересчитывает; отказ (пути в графе нет) — работой
поиска. Только целые итоги: расстояния — пифагоровы тройки, середины —
целые; дробное не произносится.
"""
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import mathspaces as M  # noqa: E402
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_mathspaces.txt"
ТРОЙКИ = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (7, 24, 25))
ФП = ", ".join(M.ФАНО)


def т(p):
    return M.запись_точки(p)


def ч(n):
    return M.число(n)


# ---------- точки ----------
def показы_точек(шаг):
    вон = []
    for i in range(14):
        a = ((шаг * 3 + i) % 9 - 4, (шаг * 5 + i * 2) % 9 - 4)
        dx, dy, d = ТРОЙКИ[(шаг + i) % len(ТРОЙКИ)]
        if (шаг + i) % 2:
            dx, dy = dy, dx
        sx, sy = (1 if (i + шаг) % 3 else -1), (1 if (i * шаг) % 2 == 0 else -1)
        b = (a[0] + sx * dx, a[1] + sy * dy)
        ru = (шаг + i) % 2 == 1
        форма = (шаг + i) % 3
        if форма == 0:
            вон.append(f"расстояние между {т(a)} и {т(b)} — {d}: {dx}² + {dy}² = {d}²." if ru else
                       f"the distance between {т(a)} and {т(b)} is {d}: {dx}² + {dy}² = {d}².")
        elif форма == 1:
            чуж = d + 1 + (i % 2)
            вон.append(f"расстояние между {т(a)} и {т(b)} — не {чуж}: оно {d}." if ru else
                       f"the distance between {т(a)} and {т(b)} is not {чуж}: it is {d}.")
        else:
            c = (a[0] + 2 * ((шаг + i) % 4 - 2), a[1] + 2 * ((шаг * i) % 4 - 1))
            m = M.середина(a, c)
            вон.append((f"середина отрезка {т(a)} и {т(c)} — {т(m)}: ({ч(a[0])} + {ч(c[0])}) ÷ 2 = {ч(m[0])} и "
                        f"({ч(a[1])} + {ч(c[1])}) ÷ 2 = {ч(m[1])}.") if ru else
                       (f"the midpoint of {т(a)} and {т(c)} is {т(m)}: ({ч(a[0])} + {ч(c[0])}) ÷ 2 = {ч(m[0])} and "
                        f"({ч(a[1])} + {ч(c[1])}) ÷ 2 = {ч(m[1])}."))
        v = ((шаг + i) % 5 - 2, (шаг * 2 + i) % 5 - 2)
        s = M.сдвиг(a, v)
        if i % 4 == 0:
            вон.append(f"{т(a)} после сдвига на {т(v)} — {т(s)}: ({ч(a[0])} + {ч(v[0])}, {ч(a[1])} + {ч(v[1])})." if ru else
                       f"{т(a)} shifted by {т(v)} is {т(s)}: ({ч(a[0])} + {ч(v[0])}, {ч(a[1])} + {ч(v[1])}).")
        elif i % 4 == 1:
            чуж = (s[0] + 1, s[1])
            вон.append(f"{т(a)} после сдвига на {т(v)} — не {т(чуж)}: это {т(s)}." if ru else
                       f"{т(a)} shifted by {т(v)} is not {т(чуж)}: it is {т(s)}.")
        elif i % 4 == 2:
            ось = "x" if (шаг + i) % 2 else "y"
            r = M.отражение(a, ось)
            осн_en = "x stays, y changes sign" if ось == "x" else "y stays, x changes sign"
            осн_ru = "x остаётся, y меняет знак" if ось == "x" else "y остаётся, x меняет знак"
            вон.append(f"{т(a)} после отражения относительно оси {ось} — {т(r)}: {осн_ru}." if ru else
                       f"{т(a)} reflected in the {ось}-axis is {т(r)}: {осн_en}.")
        else:
            угол = (90, 180, 270)[(шаг + i) % 3]
            r = M.поворот(a, угол)
            прав = {90: ("(x, y) goes to (−y, x)", "(x, y) переходит в (−y, x)"),
                    180: ("(x, y) goes to (−x, −y)", "(x, y) переходит в (−x, −y)"),
                    270: ("(x, y) goes to (y, −x)", "(x, y) переходит в (y, −x)")}[угол]
            if (шаг + i) % 2:
                чуж = M.поворот(a, (90, 180, 270)[(шаг + i + 1) % 3])
                if чуж != r:
                    вон.append(f"{т(a)} после поворота на {угол}° против часовой стрелки вокруг начала координат — не {т(чуж)}: это {т(r)}." if ru else
                               f"{т(a)} rotated {угол}° counterclockwise about the origin is not {т(чуж)}: it is {т(r)}.")
                    continue
            вон.append(f"{т(a)} после поворота на {угол}° против часовой стрелки вокруг начала координат — {т(r)}: {прав[1]}." if ru else
                       f"{т(a)} rotated {угол}° counterclockwise about the origin is {т(r)}: {прав[0]}.")
    return вон


# ---------- графы ----------
def граф_текст(шаг, i):
    """Рёбра по остаткам: 4–6 вершин, 4–7 рёбер, без петель и повторов."""
    n = 4 + (шаг + i) % 3
    рёбра = []
    k = 0
    while len(рёбра) < 3 + (шаг + i) % 4 and k < 40:
        a = 1 + (шаг * 7 + i * 3 + k * 5) % n
        b = 1 + (шаг * 11 + i * 5 + k * 7 + 1) % n
        k += 1
        if a != b and (min(a, b), max(a, b)) not in рёбра:
            рёбра.append((min(a, b), max(a, b)))
    рёбра.sort()
    return ", ".join(f"{a}-{b}" for a, b in рёбра)


def показы_графов(шаг):
    вон = []
    for i in range(14):
        текст = граф_текст(шаг, i)
        г = M.граф(текст)
        ru = (шаг + i) % 2 == 1
        верш = sorted(г)
        v = верш[(шаг + i) % len(верш)]
        d = M.степень(г, v)
        свои = ", ".join(f"{min(v, w)}-{max(v, w)}" for w in sorted(г[v]))
        if i % 3 == 0:
            вон.append(f"степень вершины {v} в графе {текст} — {d}: его рёбра {свои}." if ru else
                       f"the degree of {v} in graph {текст} is {d}: its edges are {свои}.")
        elif i % 3 == 1:
            вон.append(f"степень вершины {v} в графе {текст} — не {d + 1}: она {d}." if ru else
                       f"the degree of {v} in graph {текст} is not {d + 1}: it is {d}.")
        else:
            # СЧЁТНАЯ ФОРМА — ДОМА РУССКОГО СЧЁТА (суд родов 03.09: «3 рёбер»
            # шло мимо суда согласования, ибо форму писал генератор сам).
            вон.append(f"в графе {текст} {len(верш)} {rugram.форма('вершина', len(верш))}." if ru else f"graph {текст} has {len(верш)} vertices.")
            вон.append(f"в графе {текст} {len(M.рёбра(г))} {rugram.форма('ребро', len(M.рёбра(г)))}." if ru else f"graph {текст} has {len(M.рёбра(г))} edges.")
        a, b = верш[0], верш[-1]
        п = M.путь(г, a, b)
        if п is None:
            вон.append(f"пути от {a} до {b} в графе {текст} нет: рёбра их не соединяют." if ru else
                       f"there is no path from {a} to {b} in graph {текст}: the edges do not join them.")
            вон.append(f"граф {текст} не связен: нет пути от {a} до {b}." if ru else
                       f"graph {текст} is not connected: no path from {a} to {b}.")
        else:
            вон.append(f"в графе {текст} есть путь от {a} до {b} длины {len(п) - 1}: {'-'.join(map(str, п))}." if ru else
                       f"graph {текст} has a path from {a} to {b} of length {len(п) - 1}: {'-'.join(map(str, п))}.")
            if M.связен(г):
                вон.append(f"граф {текст} связен: из {a} достижима каждая вершина." if ru else
                           f"graph {текст} is connected: every vertex is reached from {a}.")
        # цикл: тройка вершин
        for x in верш:
            for y in sorted(г[x]):
                for z in sorted(г[y]):
                    if z != x and x in г[z] and x < y < z:
                        вон.append(f"в графе {текст} есть цикл {x}-{y}-{z}-{x}: все три ребра есть." if ru else
                                   f"graph {текст} has the cycle {x}-{y}-{z}-{x}: all three edges are present.")
                        break
                else:
                    continue
                break
            else:
                continue
            break
        # цикл, которого нет: пара несмежных вершин
        for x in верш:
            for y in верш:
                if x < y and y not in г[x]:
                    z = next((w for w in верш if w in г[x] and w != y), None)
                    if z is not None:
                        вон.append(f"в графе {текст} нет цикла {x}-{y}-{z}-{x}: {x}-{y} не ребро." if ru else
                                   f"graph {текст} does not have the cycle {x}-{y}-{z}-{x}: {x}-{y} is not an edge.")
                        break
            else:
                continue
            break
    return вон


# ---------- Фано ----------
def показы_фано(шаг):
    вон = []
    for i in range(10):
        ru = (шаг + i) % 2 == 1
        p = 1 + (шаг + i) % 7
        q = 1 + (шаг * 3 + i * 2 + 1) % 7
        if q == p:
            q = q % 7 + 1
        л = M.линия_через(p, q)
        вон.append(f"плоскость Фано {ФП}: точки {p} и {q} лежат ровно на одной линии, {л}." if ru else
                   f"Fano plane {ФП}: points {p} and {q} lie on exactly one line, {л}.")
        л1, л2 = M.ФАНО[(шаг + i) % 7], M.ФАНО[(шаг * 2 + i + 3) % 7]
        if л1 == л2:
            л2 = M.ФАНО[(M.ФАНО.index(л1) + 1) % 7]
        x = M.пересечение(л1, л2)
        вон.append(f"плоскость Фано {ФП}: линии {л1} и {л2} пересекаются ровно в одной точке, {x}." if ru else
                   f"Fano plane {ФП}: lines {л1} and {л2} meet at exactly one point, {x}.")
        if i % 2 == 0:
            вон.append(f"плоскость Фано {ФП}: точка {p} лежит ровно на 3 линиях: {', '.join(M.линии_через(p))}." if ru else
                       f"Fano plane {ФП}: point {p} lies on exactly 3 lines: {', '.join(M.линии_через(p))}.")
        else:
            чужая = next(лл for лл in M.ФАНО if str(p) not in лл or str(q) not in лл)
            вон.append(f"плоскость Фано {ФП}: точки {p} и {q} не лежат на линии {чужая}: она несёт {', '.join(чужая)}." if ru else
                       f"Fano plane {ФП}: points {p} and {q} do not lie on line {чужая}: it carries {', '.join(чужая)}.")
    return вон


# ---------- матрицы ----------
def показы_матриц(шаг):
    вон = []
    for i in range(14):
        a = [[(шаг + i) % 5 - 1, (шаг * 2 + i) % 4], [(шаг + i * 3) % 5 - 2, (шаг * 3 + i) % 4 + 1]]
        b = [[(i + 1) % 3, (шаг + 2) % 3], [(шаг * i) % 3, (i + шаг) % 3 - 1]]
        ru = (шаг + i) % 2 == 1
        А, Б = M.запись_матрицы(a), M.запись_матрицы(b)
        форма = i % 7
        if форма == 0:
            вон.append(f"матрица {А} транспонированная — {M.запись_матрицы(M.транспонированная(a))}: строки становятся столбцами." if ru else
                       f"matrix {А} transposed is {M.запись_матрицы(M.транспонированная(a))}: rows become columns.")
        elif форма == 1:
            т_ = M.транспонированная(a)
            if т_ != a:
                вон.append(f"матрица {А} транспонированная — не {А}: это {M.запись_матрицы(т_)}." if ru else
                           f"matrix {А} transposed is not {А}: it is {M.запись_матрицы(т_)}.")
        elif форма == 2:
            вон.append(f"{А} + {Б} = {M.запись_матрицы(M.сумма(a, b))}.")
        elif форма == 3:
            v = ((шаг + i) % 3, 1 + (i % 2))
            w = M.на_вектор(a, v)
            союз = " и " if ru else " and "
            осн = союз.join(f"{ч(a[k][0])} × {ч(v[0])} + {ч(a[k][1])} × {ч(v[1])} = {ч(w[k])}" for k in range(2))
            вон.append(f"{А} · {т(v)} = {т(w)}: {осн}.")
        elif форма == 4:
            s = M.след(a)
            if (шаг + i) % 2:
                вон.append(f"след матрицы {А} — {ч(s)}: {ч(a[0][0])} + {ч(a[1][1])} = {ч(s)}." if ru else
                           f"the trace of {А} is {ч(s)}: {ч(a[0][0])} + {ч(a[1][1])} = {ч(s)}.")
            else:
                вон.append(f"след матрицы {А} — не {ч(s + 1)}: он {ч(s)}." if ru else
                           f"the trace of {А} is not {ч(s + 1)}: it is {ч(s)}.")
        elif форма == 5:
            d = M.определитель(a)
            if (шаг + i) % 2:
                вон.append(f"определитель матрицы {А} — {ч(d)}: {ч(a[0][0])} × {ч(a[1][1])} − {ч(a[0][1])} × {ч(a[1][0])} = {ч(d)}." if ru else
                           f"the determinant of {А} is {ч(d)}: {ч(a[0][0])} × {ч(a[1][1])} − {ч(a[0][1])} × {ч(a[1][0])} = {ч(d)}.")
            else:
                вон.append(f"определитель матрицы {А} — не {ч(d - 1)}: он {ч(d)}." if ru else
                           f"the determinant of {А} is not {ч(d - 1)}: it is {ч(d)}.")
        else:
            k = 1 + i % 2
            вон.append(f"строка {k} матрицы {А} — {т(tuple(a[k - 1]))}." if ru else f"row {k} of {А} is {т(tuple(a[k - 1]))}.")
            вон.append(f"столбец {k} матрицы {А} — {т((a[0][k - 1], a[1][k - 1]))}." if ru else
                       f"column {k} of {А} is {т((a[0][k - 1], a[1][k - 1]))}.")
    return вон


def pass_groups(шаг):
    return [показы_точек(шаг), показы_графов(шаг), показы_фано(шаг), показы_матриц(шаг)]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
