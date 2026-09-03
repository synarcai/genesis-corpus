#!/usr/bin/env python3
"""ПРОСТРАНСТВЕННЫЙ МИР v0 — сетки 3×3..5×5 и исполнения над ними.

Мандат 02.09 §L3 (владелец: «наделить архитектуру пространственным
мышлением — представлять все известные пространства»): пространственный
образ есть ПОКАЗ со своей нотацией и своими исполнителями. Первый
носитель — квадратная сетка от 3×3 до 5×5 с фигурой из закрашенных
клеток; исполнители — поворот (90°, 180°, 270° по часовой), отражение
(слева направо, сверху вниз), перенос (на 1–2 клетки, без потери
фигуры), соседство по стороне, кратчайший путь по пустым клеткам (и
отказ, когда фигура его перекрывает), счёт клеток. Дом исполнителей
(tools/spacegrid.py) один у генератора и суда — суд исполняет заново.

ФИГУРА ВЫВЕДЕНА, НЕ НАРИСОВАНА: клетки закрашиваются по остаткам
линейного правила от номера прохода и номера показа — ни одна сетка не
вписана рукой. Отрицание берёт итог ДРУГОГО исполнителя того же рода
(поворот на 180° против 90°), и потому ложно ровно по счёту.
"""
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import spacegrid as S  # noqa: E402
from layer import emit  # noqa: E402

ЦЕЛЬ = "datasets/genesis_space.txt"
УГЛЫ = (90, 180, 270)
ОСИ = (("left-right", "слева направо"), ("top-bottom", "сверху вниз"))
СТОРОНЫ = (("right", "вправо"), ("left", "влево"), ("down", "вниз"), ("up", "вверх"))


def симметрична(строки):
    """Инвариантна ли фигура хоть под одним поворотом или отражением."""
    return any(S.поворот(строки, у) == строки for у in (90, 180, 270)) or any(
        S.отражение(строки, о) == строки for о in ("left-right", "top-bottom"))


def сетка(шаг, i):
    """Сетка n×n с фигурой по остаткам — выведенная, не нарисованная.

    ФИГУРА АСИММЕТРИЧНА ПО ЗАКОНУ, А НЕ ПО УДАЧЕ (holon, 02.09: на
    симметричной сетке поворот и отражение неотличимы по показам —
    #_#/_#_/#_# инвариантна под всеми поворотами, и рынок, видя двух
    свидетелей, отказывает). Линейное правило остатков давало
    правильные узоры; квадратичное — нет, а остаток симметрии снимается
    переворотом одной клетки в углу, чтобы фигура не стала ни пустой,
    ни полной. Каждая четвёртая сетка оставляется как вышла — поворот
    симметричной фигуры в саму себя есть тоже верный факт.
    """
    n = 3 + (шаг + i) % 3
    плотность = 2 + (шаг * 3 + i) % 3
    строки = []
    for r in range(n):
        строки.append("".join(
            "#" if (r * r * 3 + c * 7 + r * c * 5 + шаг * 11 + i * 13) % плотность == 0
            else S.ПУСТО for c in range(n)))
    # TWO DERIVED FLIPS MAKE THE POOL WIDE (holon 04.09: the remainder rule
    # alone gave 24 distinct grids in 300 shows, and the EN shift question
    # saw 2 — below LAW; the market of surfaces honestly stayed mute). The
    # cells flipped are remainders of the show's own number s = 60·pass + i
    # — derived, not drawn; the asymmetry law below still holds.
    s_ = шаг * 60 + i
    for клетка in ((s_ * 5 + 3) % (n * n), (s_ * 7 + 1) % (n * n)):
        r, c = divmod(клетка, n)
        ряд = list(строки[r])
        ряд[c] = "#" if ряд[c] == S.ПУСТО else S.ПУСТО
        строки[r] = "".join(ряд)
    if S.закрашено(строки) in (0, n * n):
        строки[0] = строки[0][:-1] + ("#" if строки[0][-1] == S.ПУСТО else S.ПУСТО)
    if (шаг + i) % 4 != 3:
        угол = 0
        while симметрична(строки) and угол < 4:
            r, c = ((0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1))[угол]
            ряд = list(строки[r])
            ряд[c] = "#" if ряд[c] == S.ПУСТО else S.ПУСТО
            строки[r] = "".join(ряд)
            угол += 1
    return строки


def показ_поворота(г, шаг, i):
    угол = УГЛЫ[(шаг + i) % 3]
    а, б = S.записать(г), S.записать(S.поворот(г, угол))
    чужой = S.записать(S.поворот(г, УГЛЫ[(шаг + i + 1) % 3]))
    форма = (шаг + i) % 4
    if форма == 0:
        return f"grid {а} rotated {угол}° clockwise is {б}: {S.основание_en(0)}."
    if форма == 1:
        return f"сетка {а} после поворота на {угол}° по часовой стрелке — {б}: {S.основание_ru(0)}."
    if форма == 2:
        if чужой == б:
            return f"what is grid {а} rotated {угол}° clockwise? grid {а} rotated {угол}° clockwise is {б}."
        k = S.разница(S.поворот(г, угол), чужой.split("/"))
        return (f"grid {а} rotated {угол}° clockwise is not {чужой}: {S.основание_en(k)}." if i % 2 else
                f"сетка {а} после поворота на {угол}° по часовой стрелке — не {чужой}: {S.основание_ru(k)}.")
    return (f"what is grid {а} rotated {угол}° clockwise? grid {а} rotated {угол}° clockwise is {б}." if i % 2 else
            f"какой станет сетка {а} после поворота на {угол}° по часовой стрелке? сетка {а} после поворота на {угол}° по часовой стрелке — {б}.")


def показ_отражения(г, шаг, i):
    # ОСЬ НЕ СЦЕПЛЕНА С ФОРМОЙ: прежде ось бралась чётностью (шаг + i), а
    # отрицание — остатком 3 по модулю 4 того же числа, и отражение слева
    # направо не получало отрицаний вовсе (holon: полярная пара не
    # собирается по закону, не по дефекту). Ось идёт своим шагом.
    en, ru = ОСИ[(i // 4 + шаг) % 2]
    а, б = S.записать(г), S.записать(S.отражение(г, en))
    форма = (шаг + i) % 4
    if форма == 0:
        return f"grid {а} reflected {en} is {б}: {S.основание_en(0)}."
    if форма == 1:
        return f"сетка {а} после отражения {ru} — {б}: {S.основание_ru(0)}."
    if форма == 3:
        другая = ОСИ[1 - ОСИ.index((en, ru))][0]     # ЧУЖОЙ итог — по другой оси
        чужой = S.записать(S.отражение(г, другая))
        k = S.разница(S.отражение(г, en), чужой.split("/"))
        if k:
            return (f"grid {а} reflected {en} is not {чужой}: {S.основание_en(k)}." if i % 2 else
                    f"сетка {а} после отражения {ru} — не {чужой}: {S.основание_ru(k)}.")
    return (f"what is grid {а} reflected {en}? grid {а} reflected {en} is {б}." if i % 2 else
            f"какой станет сетка {а} после отражения {ru}? сетка {а} после отражения {ru} — {б}.")


def сетка_компактная(шаг, i):
    """A 5×5 grid whose figure sits in one 2×2 block — derived, not drawn:
    the block's corner and the three filled cells of the block are
    remainders of the show's number. A shift by 2 loses no cell of such a
    figure in one horizontal and one vertical direction (holon 04.09: «by
    2» wants ≥ 8 distinct grids per direction, and the wide figures of the
    remainder rule almost never survive a shift by two)."""
    s_ = шаг * 20 + i
    n = 5
    # three independent digits of the show's number in base 4 — remainders
    # of s_, s_ ÷ 4 and s_ ÷ 16 (one remainder of s_ would fix all three)
    r0, c0 = s_ % 4, (s_ // 4) % 4
    пусто = (s_ // 16) % 4                   # the block's empty cell
    строки = []
    for r in range(n):
        ряд = []
        for c in range(n):
            в_блоке = r0 <= r <= r0 + 1 and c0 <= c <= c0 + 1
            ряд.append("#" if в_блоке and (r - r0) * 2 + (c - c0) != пусто else S.ПУСТО)
        строки.append("".join(ряд))
    return строки


def показ_сдвига(г, шаг, i, счёт=None, расстояния=(1, 2)):
    """For each distance 1 and 2 a direction that loses no cell — the one
    shown LEAST so far in the pass (ties by the side order), so that every
    direction and both distances gather their distinct grids evenly — in
    ALL FOUR forms, the statement and the question in both languages
    (holon 04.09: every EN shift form and «by 2» want ≥ 8 distinct grids;
    «first lawful direction» and round-robin both skewed the count to the
    sides that are lawful most often)."""
    вон = []
    а = S.записать(г)
    счёт = счёт if счёт is not None else {}
    for k in расстояния:
        годные = [(en, ru) for en, ru in СТОРОНЫ if not S.теряет(г, en, k)]
        if not годные:
            continue
        en, ru = min(годные, key=lambda с: (счёт.get((с[0], k), 0), СТОРОНЫ.index(с)))
        счёт[(en, k)] = счёт.get((en, k), 0) + 1
        б = S.записать(S.сдвиг(г, en, k))
        вон += [f"grid {а} shifted {en} by {k} is {б}.",
                f"сетка {а} после сдвига {ru} на {k} — {б}.",
                f"what is grid {а} shifted {en} by {k}? grid {а} shifted {en} by {k} is {б}.",
                f"какой станет сетка {а} после сдвига {ru} на {k}? сетка {а} после сдвига {ru} на {k} — {б}."]
    return вон or None


def показ_соседей(г, шаг, i):
    n = len(г)
    r, c = 1 + (шаг + i) % n, 1 + (шаг * 2 + i) % n
    k = S.соседи(г, r, c)
    а = S.записать(г)
    форма = (шаг + i) % 4
    return [f"the number of filled side-neighbours of cell ({r}, {c}) in grid {а} is {k}.",
            f"число закрашенных соседей по стороне у клетки ({r}, {c}) в сетке {а} — {k}.",
            f"how many filled side-neighbours does cell ({r}, {c}) in grid {а} have? it has {k}.",
            f"сколько закрашенных соседей по стороне у клетки ({r}, {c}) в сетке {а}? {k}."][форма]


def показ_пути(г, шаг, i):
    n = len(г)
    пустые = [(r + 1, c + 1) for r in range(n) for c in range(n) if г[r][c] == S.ПУСТО]
    if len(пустые) < 2:
        return None
    a = пустые[(шаг + i) % len(пустые)]
    b = пустые[(шаг * 3 + i * 5 + 1) % len(пустые)]
    if a == b:
        b = пустые[(пустые.index(a) + 1) % len(пустые)]
    L = S.путь(г, a, b)
    а = S.записать(г)
    (r1, c1), (r2, c2) = a, b
    if L is None:
        return (f"there is no path from ({r1}, {c1}) to ({r2}, {c2}) through empty cells by side in grid {а}: the filled cells cut it off."
                if i % 2 else
                f"пути от ({r1}, {c1}) до ({r2}, {c2}) по пустым клеткам по стороне в сетке {а} нет: закрашенные клетки его перекрывают.")
    форма = (шаг + i) % 4
    return [f"the length of the shortest path from ({r1}, {c1}) to ({r2}, {c2}) through empty cells by side in grid {а} is {L}.",
            f"длина кратчайшего пути от ({r1}, {c1}) до ({r2}, {c2}) по пустым клеткам по стороне в сетке {а} — {L}.",
            f"how long is the shortest path from ({r1}, {c1}) to ({r2}, {c2}) through empty cells by side in grid {а}? {L}.",
            f"какова длина кратчайшего пути от ({r1}, {c1}) до ({r2}, {c2}) по пустым клеткам по стороне в сетке {а}? {L}."][форма]


def показ_счёта(г, шаг, i):
    а, k = S.записать(г), S.закрашено(г)
    # ВОПРОСНАЯ ПОВЕРХНОСТЬ СЧЁТА: ответ — само утверждение.
    форма = (шаг + i) % 4
    return [f"the number of filled cells in grid {а} is {k}.",
            f"число закрашенных клеток в сетке {а} — {k}.",
            f"how many filled cells does grid {а} have? the number of filled cells in grid {а} is {k}.",
            f"сколько закрашенных клеток в сетке {а}? число закрашенных клеток в сетке {а} — {k}."][форма]


import laws  # noqa: E402


def pass_shows(шаг):
    вон = list(laws.ступень("space"))
    счёт_сдвигов = {}          # per pass: how often each (side, distance) was shown
    сдвиг_ = lambda г, шаг, i: показ_сдвига(г, шаг, i, счёт_сдвигов)
    for i in range(60):
        г = сетка(шаг, i)
        for показ in (показ_поворота, показ_отражения, сдвиг_,
                      показ_соседей, показ_пути, показ_счёта):
            с = показ(г, шаг, i)
            if isinstance(с, list):
                вон.extend(с)
            elif с:
                вон.append(с)
    # compact figures: shifts by 2 in every direction
    for i in range(20):
        вон.extend(показ_сдвига(сетка_компактная(шаг, i), шаг, i, счёт_сдвигов, расстояния=(2,)) or [])
    return вон


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
