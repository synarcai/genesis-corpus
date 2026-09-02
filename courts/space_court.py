#!/usr/bin/env python3
"""[ПРОСТРАНСТВО v0] — исполнитель воспроизводит каждую строку показа.

Мир сеток (tools/gen_genesis_space.py) показывает исполнения над сеткой
3×3..5×5: поворот, отражение, перенос, соседство, путь, счёт — и вопросы
к ним. Суд не сверяет с записанным: он ИСПОЛНЯЕТ названное над показанной
сеткой тем же домом исполнителей (tools/spacegrid.py) и сравнивает итог;
отрицание истинно, когда итог не совпал; отказ «пути нет» судится
работой — поиском, который ничего не нашёл.
"""
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import families  # noqa: E402
import spacegrid as S  # noqa: E402

Г = S.СЕТКА.pattern
Ч = r"(\d+)"
КЛ = r"\((\d), ?(\d)\)"
УГОЛ_RU = {"90": 90, "180": 180, "270": 270}
ОСЬ_RU = {"слева направо": "left-right", "сверху вниз": "top-bottom"}
КУДА_RU = {"вправо": "right", "влево": "left", "вниз": "down", "вверх": "up"}


def _г(т):
    return S.разобрать(т)


ОСНОВАНИЕ = re.compile(r"no cell differs|(\d+) cells? differs?|ни одна клетка не отличается|отлича(?:ется|ются) (\d+) клет(?:ка|ки|ок)")


def _полярность(истинная, б, не, основание):
    """Полярность судится числом расходящихся клеток; названное основание —
    тем же числом, пересчитанным."""
    k = S.разница(истинная, б.split("/"))
    if k is None:
        return False
    if основание is not None:
        мм = ОСНОВАНИЕ.fullmatch(основание)
        if not мм or int(мм.group(1) or мм.group(2) or 0) != k:
            return False
    return (k == 0) == (не is None)


def _поворот(м):
    г = м.groups()
    а, угол, не, б = г[0], int(г[1]), г[2], г[3]
    основание = г[4] if len(г) > 4 else None
    if угол not in (90, 180, 270) or _г(а) is None or _г(б) is None:
        return False
    return _полярность(S.поворот(_г(а), угол), б, не, основание)


def _отражение(м):
    г = м.groups()
    а, ось, не, б = г[0], г[1], г[2], г[3]
    основание = г[4] if len(г) > 4 else None
    ось = ОСЬ_RU.get(ось, ось)
    if _г(а) is None or _г(б) is None:
        return False
    return _полярность(S.отражение(_г(а), ось), б, не, основание)


def _сдвиг(м):
    а, куда, k, не, б = м.groups()
    куда = КУДА_RU.get(куда, куда)
    if _г(а) is None or _г(б) is None:
        return False
    return (S.записать(S.сдвиг(_г(а), куда, int(k))) == б) == (не is None)


def _соседи(м):
    r, c, а, k = int(м.group(1)), int(м.group(2)), м.group(3), int(м.group(4))
    г = _г(а)
    if г is None or not (1 <= r <= len(г) and 1 <= c <= len(г[0])):
        return False
    return S.соседи(г, r, c) == k


def _в_сетке(г, r, c):
    return 1 <= r <= len(г) and 1 <= c <= len(г[0])


def _путь(м):
    r1, c1, r2, c2, а = int(м.group(1)), int(м.group(2)), int(м.group(3)), int(м.group(4)), м.group(5)
    L = int(м.group(6))
    г = _г(а)
    if г is None or not _в_сетке(г, r1, c1) or not _в_сетке(г, r2, c2):
        return False
    return S.путь(г, (r1, c1), (r2, c2)) == L


def _пути_нет(м):
    r1, c1, r2, c2, а = int(м.group(1)), int(м.group(2)), int(м.group(3)), int(м.group(4)), м.group(5)
    г = _г(а)
    # КЛЕТКА ВНЕ СЕТКИ — ЛОЖЬ, А НЕ ОТСУТСТВИЕ ПУТИ: основание «закрашенные
    # клетки перекрывают» о ней неверно (порча координаты, 03.09).
    if г is None or not _в_сетке(г, r1, c1) or not _в_сетке(г, r2, c2):
        return False
    return S.путь(г, (r1, c1), (r2, c2)) is None


# ВОПРОС ПОВТОРЯЕТ ПРЕДМЕТ, ОТВЕТ — УТВЕРЖДЕНИЕ: половины сверяются, утверждение судится своим судьёй.
def _поворот_вопрос(м):
    а, угол, а2, угол2, б = м.groups()
    return а == а2 and угол == угол2 and _поворот(_М((а, угол, None, б)))


def _отражение_вопрос(м):
    а, ось, а2, ось2, б = м.groups()
    return а == а2 and ось == ось2 and _отражение(_М((а, ось, None, б)))


def _сдвиг_вопрос(м):
    а, куда, k, а2, куда2, k2, б = м.groups()
    return (а, куда, k) == (а2, куда2, k2) and _сдвиг(_М((а, куда, k, None, б)))


def _счёт_вопрос(м):
    а, а2, k = м.groups()
    return а == а2 and _счёт(_М((а2, k)))


def _счёт(м):
    а, k = м.group(1), int(м.group(2))
    г = _г(а)
    return г is not None and S.закрашено(г) == k


ОБРАЗЦЫ = (
    (rf"^grid ({Г}) rotated {Ч}° clockwise is (not )?({Г}): ([^.]+)\.$", _поворот),
    (rf"^сетка ({Г}) после поворота на {Ч}° по часовой стрелке — (не )?({Г}): ([^.]+)\.$", _поворот),
    (rf"^grid ({Г}) reflected (left-right|top-bottom) is (not )?({Г}): ([^.]+)\.$", _отражение),
    (rf"^сетка ({Г}) после отражения (слева направо|сверху вниз) — (не )?({Г}): ([^.]+)\.$", _отражение),
    (rf"^grid ({Г}) rotated {Ч}° clockwise is (not )?({Г})\.$", _поворот),
    (rf"^сетка ({Г}) после поворота на {Ч}° по часовой стрелке — (не )?({Г})\.$", _поворот),
    (rf"^what is grid ({Г}) rotated {Ч}° clockwise\? grid ({Г}) rotated {Ч}° clockwise is ({Г})\.$", _поворот_вопрос),
    (rf"^какой станет сетка ({Г}) после поворота на {Ч}° по часовой стрелке\? сетка ({Г}) после поворота на {Ч}° по часовой стрелке — ({Г})\.$", _поворот_вопрос),
    (rf"^grid ({Г}) reflected (left-right|top-bottom) is (not )?({Г})\.$", _отражение),
    (rf"^сетка ({Г}) после отражения (слева направо|сверху вниз) — (не )?({Г})\.$", _отражение),
    (rf"^what is grid ({Г}) reflected (left-right|top-bottom)\? grid ({Г}) reflected (left-right|top-bottom) is ({Г})\.$", _отражение_вопрос),
    (rf"^какой станет сетка ({Г}) после отражения (слева направо|сверху вниз)\? сетка ({Г}) после отражения (слева направо|сверху вниз) — ({Г})\.$", _отражение_вопрос),
    (rf"^grid ({Г}) shifted (right|left|down|up) by {Ч} is (not )?({Г})\.$", _сдвиг),
    (rf"^сетка ({Г}) после сдвига (вправо|влево|вниз|вверх) на {Ч} — (не )?({Г})\.$", _сдвиг),
    (rf"^what is grid ({Г}) shifted (right|left|down|up) by {Ч}\? grid ({Г}) shifted (right|left|down|up) by {Ч} is ({Г})\.$", _сдвиг_вопрос),
    (rf"^какой станет сетка ({Г}) после сдвига (вправо|влево|вниз|вверх) на {Ч}\? сетка ({Г}) после сдвига (вправо|влево|вниз|вверх) на {Ч} — ({Г})\.$", _сдвиг_вопрос),
    (rf"^the number of filled side-neighbours of cell {КЛ} in grid ({Г}) is {Ч}\.$", _соседи),
    (rf"^число закрашенных соседей по стороне у клетки {КЛ} в сетке ({Г}) — {Ч}\.$", _соседи),
    (rf"^how many filled side-neighbours does cell {КЛ} in grid ({Г}) have\? it has {Ч}\.$", _соседи),
    (rf"^сколько закрашенных соседей по стороне у клетки {КЛ} в сетке ({Г})\? {Ч}\.$", _соседи),
    (rf"^the length of the shortest path from {КЛ} to {КЛ} through empty cells by side in grid ({Г}) is {Ч}\.$", _путь),
    (rf"^длина кратчайшего пути от {КЛ} до {КЛ} по пустым клеткам по стороне в сетке ({Г}) — {Ч}\.$", _путь),
    (rf"^how long is the shortest path from {КЛ} to {КЛ} through empty cells by side in grid ({Г})\? {Ч}\.$", _путь),
    (rf"^какова длина кратчайшего пути от {КЛ} до {КЛ} по пустым клеткам по стороне в сетке ({Г})\? {Ч}\.$", _путь),
    (rf"^there is no path from {КЛ} to {КЛ} through empty cells by side in grid ({Г}): the filled cells cut it off\.$", _пути_нет),
    (rf"^пути от {КЛ} до {КЛ} по пустым клеткам по стороне в сетке ({Г}) нет: закрашенные клетки его перекрывают\.$", _пути_нет),
    (rf"^the number of filled cells in grid ({Г}) is {Ч}\.$", _счёт),
    (rf"^число закрашенных клеток в сетке ({Г}) — {Ч}\.$", _счёт),
    (rf"^how many filled cells does grid ({Г}) have\? the number of filled cells in grid ({Г}) is {Ч}\.$", _счёт_вопрос),
    (rf"^сколько закрашенных клеток в сетке ({Г})\? число закрашенных клеток в сетке ({Г}) — {Ч}\.$", _счёт_вопрос),
)
# СЕМЕЙСТВО ЕСТЬ РОД (М-146): формы одной рамки — утверждение с основанием,
# утверждение, вопрос, отказ — один род на язык.
СЕМЕЙСТВА_СУДА = (
    ("поворот", [ОБРАЗЦЫ[i] for i in (0, 1, 4, 5, 6, 7)]),
    ("отражение", [ОБРАЗЦЫ[i] for i in (2, 3, 8, 9, 10, 11)]),
    ("сдвиг", [ОБРАЗЦЫ[i] for i in (12, 13, 14, 15)]),
    ("соседи", [ОБРАЗЦЫ[i] for i in (16, 17, 18, 19)]),
    ("путь", [ОБРАЗЦЫ[i] for i in (20, 21, 22, 23, 24, 25)]),
    ("счёт", [ОБРАЗЦЫ[i] for i in (26, 27, 28, 29)]),
)
assert sum(len(ф) for _, ф in СЕМЕЙСТВА_СУДА) == len(ОБРАЗЦЫ) == 30, len(ОБРАЗЦЫ)


class _М:
    def __init__(self, группы):
        self._г = группы

    def group(self, i):
        return self._г[i - 1]

    def groups(self):
        return self._г


# ПУСТАЯ ГРУППА ЧИТАЕТСЯ КАК ОТСУТСТВУЮЩАЯ: образцы вопроса держат «()» на
# месте «(not )?», чтобы группы стояли одинаково у всех форм рамки.
ПРАВИЛА = families.правила(
    СЕМЕЙСТВА_СУДА,
    обёртка=lambda мм: _М(tuple(None if г == "" else г for г in мм.groups())))


import laws  # noqa: E402
ЗАКОНЫ = laws.свод("space")


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if с in ЗАКОНЫ:
        return True, True
    if "/" not in с or ("#" not in с and "_" not in с):
        return False, False
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            return True, bool(проверить(м))
    return False, False


def main():
    import collections
    итог = collections.Counter()
    for путь in [pathlib.Path(п) for п in sys.argv[1:]] or [КОРЕНЬ / "datasets" / "genesis_space.txt"]:
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip():
                continue
            судимо, истинно = судить(с)
            итог["несудимо" if not судимо else ("истина" if истинно else "ЛОЖЬ")] += 1
            if судимо and not истинно:
                print("  ЛОЖЬ:", с[:120])
    ложь = итог["ЛОЖЬ"]
    print(f"ПРОСТРАНСТВО {'PASS' if not ложь else 'FAIL'}: {ложь} ложных, "
          f"{итог['истина']} истинных, {итог['несудимо']} несудимых")
    return 0 if not ложь else 1


if __name__ == "__main__":
    sys.exit(main())
