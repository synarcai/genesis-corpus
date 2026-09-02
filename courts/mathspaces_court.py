#!/usr/bin/env python3
"""[МАТЕМАТИЧЕСКИЕ ПРОСТРАНСТВА] — исполнитель воспроизводит каждую строку.

Мир mathspaces показывает евклидовы точки, графы, плоскость Фано и
матрицы (нотации согласованы с holon 02.09). Суд не сверяет с записанным
— он исполняет названное тем же домом (tools/mathspaces.py) и сравнивает;
полярность судится итогом, основание после двоеточия — пересчитывается
(число, ребро, путь, линия), отказ судится работой поиска.
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
import mathspaces as M  # noqa: E402
import rugram  # noqa: E402

Т = M.ТОЧКА.pattern
Ч = r"(−?\d+)"
ГР = r"(\d+-\d+(?:, \d+-\d+)*)"
МТ = M.МАТРИЦА.pattern
ФП = ", ".join(M.ФАНО)


def _n(т):
    return int(т.replace(M.МИНУС, "-"))


def _p(м, i):
    return (_n(м.group(i)), _n(м.group(i + 1)))


def _полярность(истина, названо, не, основание=None, верное_основание=None):
    """Истина полярности; основание, если названо, обязано равняться
    верному (строкой после нормализации пробелов)."""
    if основание is not None and верное_основание is not None:
        if " ".join(основание.split()) != " ".join(верное_основание.split()):
            return False
    return (истина == названо) == (не is None)


# ----- точки -----
def _расстояние(м):
    a, b, не, d, осн = _p(м, 1), _p(м, 3), м.group(5), _n(м.group(6)), м.group(7)
    ист = M.расстояние(a, b)
    if ист is None:
        return False
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    верное = f"{dx}² + {dy}² = {ист}²" if не is None else f"it is {ист}" if "it is" in (осн or "") else f"оно {ист}"
    return _полярность(ист, d, не, осн, верное)


def _середина(м):
    a, b, не, c, осн = _p(м, 1), _p(м, 3), м.group(5), _p(м, 6), м.group(8)
    ист = M.середина(a, b)
    if ист is None:
        return False
    if не is None:
        верное = (f"({M.число(a[0])} + {M.число(b[0])}) ÷ 2 = {M.число(ист[0])} and "
                  f"({M.число(a[1])} + {M.число(b[1])}) ÷ 2 = {M.число(ист[1])}")
        if осн and " и " in осн:
            верное = верное.replace(" and ", " и ")
    else:
        верное = f"it is {M.запись_точки(ист)}" if "it is" in (осн or "") else f"это {M.запись_точки(ист)}"
    return _полярность(ист, c, не, осн, верное)


def _сдвиг(м):
    a, v, не, c, осн = _p(м, 1), _p(м, 3), м.group(5), _p(м, 6), м.group(8)
    ист = M.сдвиг(a, v)
    if не is None:
        верное = f"({M.число(a[0])} + {M.число(v[0])}, {M.число(a[1])} + {M.число(v[1])})"
    else:
        верное = f"it is {M.запись_точки(ист)}" if "it is" in (осн or "") else f"это {M.запись_точки(ист)}"
    return _полярность(ист, c, не, осн, верное)


def _отражение(м):
    a, ось, не, c, осн = _p(м, 1), м.group(3), м.group(4), _p(м, 5), м.group(7)
    ист = M.отражение(a, ось)
    if не is None:
        верное = ("x stays, y changes sign" if ось == "x" else "y stays, x changes sign") if "stays" in (осн or "") else \
                 ("x остаётся, y меняет знак" if ось == "x" else "y остаётся, x меняет знак")
    else:
        верное = f"it is {M.запись_точки(ист)}" if "it is" in (осн or "") else f"это {M.запись_точки(ист)}"
    return _полярность(ист, c, не, осн, верное)


def _поворот(м):
    a, угол, не, c, осн = _p(м, 1), int(м.group(3)), м.group(4), _p(м, 5), м.group(7)
    if угол not in (90, 180, 270):
        return False
    ист = M.поворот(a, угол)
    if не is None:
        верное = {90: "(x, y) goes to (−y, x)", 180: "(x, y) goes to (−x, −y)", 270: "(x, y) goes to (y, −x)"}[угол] \
            if "goes" in (осн or "") else {90: "(x, y) переходит в (−y, x)", 180: "(x, y) переходит в (−x, −y)", 270: "(x, y) переходит в (y, −x)"}[угол]
    else:
        верное = f"it is {M.запись_точки(ист)}" if "it is" in (осн or "") else f"это {M.запись_точки(ист)}"
    return _полярность(ист, c, не, осн, верное)


# ----- графы -----
def _степень(м):
    v, г, не, d, осн = int(м.group(1)), M.граф(м.group(2)), м.group(3), int(м.group(4)), м.group(5)
    if г is None or v not in г:
        return False
    ист = M.степень(г, v)
    if не is None:
        # Основание — рёбра вершины; порядок перечисления не есть закон.
        свои = {f"{min(v, w)}-{max(v, w)}" for w in г[v]}
        мм = re.fullmatch(r"(?:its edges are|его рёбра) (.+)", осн or "")
        return bool(мм) and set(мм.group(1).split(", ")) == свои and ист == d
    верное = f"it is {ист}" if "it is" in (осн or "") else f"она {ист}"
    return _полярность(ист, d, не, осн, верное)


def _счёт_графа(м):
    г, что, k = M.граф(м.group(1)), м.group(2), int(м.group(3))
    if г is None:
        return False
    # СЛОВО ЧИТАЕТСЯ ФОРМАМИ ДОМА РУССКОГО СЧЁТА, И ФОРМА ПРИ ЧИСЛЕ
    # СВЕРЯЕТСЯ ТЕМ ЖЕ ДОМОМ (суд родов 03.09: рамку графа суд счёта не
    # читает, и согласование здесь судит суд пространств сам — он
    # хозяин рода по делу, а не по имени).
    if что == "vertices":
        ист = len(г)
    elif что == "edges":
        ист = len(M.рёбра(г))
    elif что in rugram.СЧЁТНЫЕ["вершина"]:
        ист = len(г)
        if что != rugram.форма("вершина", k):
            return False
    else:
        ист = len(M.рёбра(г))
        if что != rugram.форма("ребро", k):
            return False
    return ист == k


def _путь(м):
    г, a, b, L, осн = M.граф(м.group(1)), int(м.group(2)), int(м.group(3)), int(м.group(4)), м.group(5)
    if г is None:
        return False
    п = M.путь(г, a, b)
    if п is None or len(п) - 1 != L:
        return False
    вершины = [int(x) for x in осн.split("-")]
    return (len(вершины) == L + 1 and вершины[0] == a and вершины[-1] == b
            and all(y in г.get(x, ()) for x, y in zip(вершины, вершины[1:])))


def _пути_нет(м):
    г, a, b = M.граф(м.group(1)), int(м.group(2)), int(м.group(3))
    return г is not None and a in г and b in г and M.путь(г, a, b) is None


def _связность(м):
    г, не, осн = M.граф(м.group(1)), м.group(2), м.group(3)
    if г is None:
        return False
    ист = M.связен(г)
    if не is None:
        return ист
    мм = re.fullmatch(r"(?:no path from|нет пути от) (\d+) (?:to|до) (\d+)", осн)
    return (not ист) and bool(мм) and M.путь(г, int(мм.group(1)), int(мм.group(2))) is None


def _цикл(м):
    г, не, цикл, осн = M.граф(м.group(1)), м.group(2), м.group(3), м.group(4)
    if г is None:
        return False
    вершины = [int(x) for x in цикл.split("-")]
    ист = M.цикл_есть(г, вершины)
    if не is None:
        return ист
    мм = re.fullmatch(r"(\d+)-(\d+) (?:is not an edge|не ребро)", осн)
    if not мм:
        return False
    x, y = int(мм.group(1)), int(мм.group(2))
    пара = (x, y) in zip(вершины, вершины[1:]) or (y, x) in zip(вершины, вершины[1:])
    return (not ист) and пара and y not in г.get(x, ())


# ----- Фано -----
def _фано_линия(м):
    p, q, л = int(м.group(1)), int(м.group(2)), м.group(3)
    return 1 <= p <= 7 and 1 <= q <= 7 and p != q and M.линия_через(p, q) == л


def _фано_точка(м):
    л1, л2, p = м.group(1), м.group(2), int(м.group(3))
    return л1 in M.ФАНО and л2 in M.ФАНО and л1 != л2 and M.пересечение(л1, л2) == p


def _фано_пучок(м):
    p, k, линии = int(м.group(1)), int(м.group(2)), м.group(3).split(", ")
    return 1 <= p <= 7 and k == 3 and линии == M.линии_через(p)


def _фано_не_на_линии(м):
    p, q, л, несёт = int(м.group(1)), int(м.group(2)), м.group(3), м.group(4)
    return (л in M.ФАНО and not (str(p) in л and str(q) in л)
            and несёт == ", ".join(л))


# ----- матрицы -----
def _транспонирование(м):
    a, не, b, осн = M.матрица(м.group(1)), м.group(2), M.матрица(м.group(3)), м.group(4)
    if a is None or b is None:
        return False
    ист = M.транспонированная(a)
    if не is None:
        return ист == b
    return ист != b and осн in (f"it is {M.запись_матрицы(ист)}", f"это {M.запись_матрицы(ист)}")


def _сумма(м):
    a, b, c = M.матрица(м.group(1)), M.матрица(м.group(2)), M.матрица(м.group(3))
    return None not in (a, b, c) and len(a) == len(b) and M.сумма(a, b) == c


def _на_вектор(м):
    a, v, w, осн = M.матрица(м.group(1)), _p(м, 2), _p(м, 4), м.group(6)
    if a is None or len(a[0]) != 2 or len(a) != 2:
        return False
    ист = M.на_вектор(a, v)
    if ист != w:
        return False
    союз = " and " if " and " in осн else " и "
    верное = союз.join(
        f"{M.число(a[i][0])} × {M.число(v[0])} + {M.число(a[i][1])} × {M.число(v[1])} = {M.число(ист[i])}"
        for i in range(2))
    return " ".join(осн.split()) == верное


def _след(м):
    a, не, t, осн = M.матрица(м.group(1)), м.group(2), _n(м.group(3)), м.group(4)
    if a is None or len(a) != len(a[0]):
        return False
    ист = M.след(a)
    if не is None:
        верное = " + ".join(M.число(a[i][i]) for i in range(len(a))) + f" = {M.число(ист)}"
    else:
        верное = f"it is {M.число(ист)}" if "it is" in осн else f"он {M.число(ист)}"
    return _полярность(ист, t, не, осн, верное)


def _определитель(м):
    a, не, d, осн = M.матрица(м.group(1)), м.group(2), _n(м.group(3)), м.group(4)
    if a is None or len(a) != 2 or len(a[0]) != 2:
        return False
    ист = M.определитель(a)
    if не is None:
        верное = (f"{M.число(a[0][0])} × {M.число(a[1][1])} − {M.число(a[0][1])} × "
                  f"{M.число(a[1][0])} = {M.число(ист)}")
    else:
        верное = f"it is {M.число(ист)}" if "it is" in осн else f"он {M.число(ист)}"
    return _полярность(ист, d, не, осн, верное)


def _строка_столбец(м):
    что, k, a, v = м.group(1), int(м.group(2)), M.матрица(м.group(3)), _p(м, 4)
    if a is None or len(a) != 2 or len(a[0]) != 2:
        return False
    ист = tuple(a[k - 1]) if что in ("row", "строка") else tuple(р[k - 1] for р in a)
    return 1 <= k <= 2 and ист == v


ОБРАЗЦЫ = (
    (rf"^the distance between {Т} and {Т} is (not )?{Ч}: (.+)\.$", _расстояние),
    (rf"^расстояние между {Т} и {Т} — (не )?{Ч}: (.+)\.$", _расстояние),
    (rf"^the midpoint of {Т} and {Т} is (not )?{Т}: (.+)\.$", _середина),
    (rf"^середина отрезка {Т} и {Т} — (не )?{Т}: (.+)\.$", _середина),
    (rf"^{Т} shifted by {Т} is (not )?{Т}: (.+)\.$", _сдвиг),
    (rf"^{Т} после сдвига на {Т} — (не )?{Т}: (.+)\.$", _сдвиг),
    (rf"^{Т} reflected in the (x|y)-axis is (not )?{Т}: (.+)\.$", _отражение),
    (rf"^{Т} после отражения относительно оси (x|y) — (не )?{Т}: (.+)\.$", _отражение),
    (rf"^{Т} rotated (\d+)° counterclockwise about the origin is (not )?{Т}: (.+)\.$", _поворот),
    (rf"^{Т} после поворота на (\d+)° против часовой стрелки вокруг начала координат — (не )?{Т}: (.+)\.$", _поворот),
    (rf"^the degree of (\d+) in graph {ГР} is (not )?(\d+): (.+)\.$", _степень),
    (rf"^степень вершины (\d+) в графе {ГР} — (не )?(\d+): (.+)\.$", _степень),
    (rf"^graph {ГР} has (\d+) (vertices|edges)\.$", lambda м: _счёт_графа(type("М", (), {"group": lambda self, i: (м.group(1), м.group(3), м.group(2))[i - 1]})())),
    (rf"^в графе {ГР} (\d+) (вершин[аы]?|р[её]б(?:ро|ра|ер))\.$", lambda м: _счёт_графа(type("М", (), {"group": lambda self, i: (м.group(1), м.group(3), м.group(2))[i - 1]})())),
    (rf"^graph {ГР} has a path from (\d+) to (\d+) of length (\d+): ([\d-]+)\.$", _путь),
    (rf"^в графе {ГР} есть путь от (\d+) до (\d+) длины (\d+): ([\d-]+)\.$", _путь),
    (rf"^there is no path from (\d+) to (\d+) in graph {ГР}: the edges do not join them\.$",
     lambda м: _пути_нет(type("М", (), {"group": lambda self, i: (м.group(3), м.group(1), м.group(2))[i - 1]})())),
    (rf"^пути от (\d+) до (\d+) в графе {ГР} нет: рёбра их не соединяют\.$",
     lambda м: _пути_нет(type("М", (), {"group": lambda self, i: (м.group(3), м.group(1), м.group(2))[i - 1]})())),
    (rf"^graph {ГР} is (not )?connected: (.+)\.$", _связность),
    (rf"^граф {ГР} (не )?связен: (.+)\.$", _связность),
    (rf"^graph {ГР} (?:has|does (not )?have) the cycle ([\d-]+): (.+)\.$", _цикл),
    (rf"^в графе {ГР} (нет |есть )цикл[а]? ([\d-]+): (.+)\.$", lambda м: _цикл(type("М", (), {"group": lambda self, i: (м.group(1), None if м.group(2) == "есть " else "не", м.group(3), м.group(4))[i - 1]})())),
    (rf"^Fano plane {re.escape(ФП)}: points (\d) and (\d) lie on exactly one line, (\d\d\d)\.$", _фано_линия),
    (rf"^плоскость Фано {re.escape(ФП)}: точки (\d) и (\d) лежат ровно на одной линии, (\d\d\d)\.$", _фано_линия),
    (rf"^Fano plane {re.escape(ФП)}: lines (\d\d\d) and (\d\d\d) meet at exactly one point, (\d)\.$", _фано_точка),
    (rf"^плоскость Фано {re.escape(ФП)}: линии (\d\d\d) и (\d\d\d) пересекаются ровно в одной точке, (\d)\.$", _фано_точка),
    (rf"^Fano plane {re.escape(ФП)}: point (\d) lies on exactly (\d) lines: (\d\d\d, \d\d\d, \d\d\d)\.$", _фано_пучок),
    (rf"^плоскость Фано {re.escape(ФП)}: точка (\d) лежит ровно на (\d) линиях: (\d\d\d, \d\d\d, \d\d\d)\.$", _фано_пучок),
    (rf"^Fano plane {re.escape(ФП)}: points (\d) and (\d) do not lie on line (\d\d\d): it carries (\d, \d, \d)\.$", _фано_не_на_линии),
    (rf"^плоскость Фано {re.escape(ФП)}: точки (\d) и (\d) не лежат на линии (\d\d\d): она несёт (\d, \d, \d)\.$", _фано_не_на_линии),
    (rf"^matrix {МТ} transposed is (not )?{МТ}(?:: (.+))?\.$", _транспонирование),
    (rf"^матрица {МТ} транспонированная — (не )?{МТ}(?:: (.+))?\.$", _транспонирование),
    (rf"^{МТ} \+ {МТ} = {МТ}\.$", _сумма),
    (rf"^{МТ} · {Т} = {Т}: (.+)\.$", _на_вектор),
    (rf"^the trace of {МТ} is (not )?{Ч}: (.+)\.$", _след),
    (rf"^след матрицы {МТ} — (не )?{Ч}: (.+)\.$", _след),
    (rf"^the determinant of {МТ} is (not )?{Ч}: (.+)\.$", _определитель),
    (rf"^определитель матрицы {МТ} — (не )?{Ч}: (.+)\.$", _определитель),
    (rf"^(row|column) (\d) of {МТ} is {Т}\.$", _строка_столбец),
    (rf"^(строка|столбец) (\d) матрицы {МТ} — {Т}\.$", _строка_столбец),
)
ПРАВИЛА = tuple((re.compile(о), п) for о, п in ОБРАЗЦЫ)


def судить(строка):
    """(судимо, истинно) для одной строки."""
    # ВОПРОС СУДИТСЯ СВОИМ ОТВЕТОМ (дом пары): «what is the distance
    # between (1, 2) and (4, 6)? the distance between … is 5: …» — ответ
    # есть то же утверждение, и его судит тот же образец.
    если = asking.судить_парой(строка, судить)
    if если is not None:
        return если
    с = строка.strip()
    if not any(з in с for з in ("(", "graph ", "граф", "Fano", "Фано", "[")):
        return False, False
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            try:
                return True, bool(проверить(м))
            except (ValueError, IndexError, KeyError, StopIteration):
                return True, False
    return False, False


def main():
    import collections
    итог = collections.Counter()
    for путь in [pathlib.Path(п) for п in sys.argv[1:]] or [КОРЕНЬ / "datasets" / "genesis_mathspaces.txt"]:
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip():
                continue
            судимо, истинно = судить(с)
            итог["несудимо" if not судимо else ("истина" if истинно else "ЛОЖЬ")] += 1
            if судимо and not истинно:
                print("  ЛОЖЬ:", с[:120])
    ложь = итог["ЛОЖЬ"]
    print(f"ПРОСТРАНСТВА {'PASS' if not ложь else 'FAIL'}: {ложь} ложных, "
          f"{итог['истина']} истинных, {итог['несудимо']} несудимых")
    return 0 if not ложь else 1


if __name__ == "__main__":
    sys.exit(main())
