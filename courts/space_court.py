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
import spacegrid as S  # noqa: E402

Г = S.СЕТКА.pattern
Ч = r"(\d+)"
КЛ = r"\((\d), ?(\d)\)"
УГОЛ_RU = {"90": 90, "180": 180, "270": 270}
ОСЬ_RU = {"слева направо": "left-right", "сверху вниз": "top-bottom"}
КУДА_RU = {"вправо": "right", "влево": "left", "вниз": "down", "вверх": "up"}


def _г(т):
    return S.разобрать(т)


def _поворот(м):
    а, угол, не, б = м.group(1), int(м.group(2)), м.group(3), м.group(4)
    if угол not in (90, 180, 270) or _г(а) is None or _г(б) is None:
        return False
    return (S.записать(S.поворот(_г(а), угол)) == б) == (не is None)


def _отражение(м):
    а, ось, не, б = м.groups()
    ось = ОСЬ_RU.get(ось, ось)
    if _г(а) is None or _г(б) is None:
        return False
    return (S.записать(S.отражение(_г(а), ось)) == б) == (не is None)


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


def _путь(м):
    r1, c1, r2, c2, а = int(м.group(1)), int(м.group(2)), int(м.group(3)), int(м.group(4)), м.group(5)
    L = int(м.group(6))
    г = _г(а)
    if г is None:
        return False
    return S.путь(г, (r1, c1), (r2, c2)) == L


def _пути_нет(м):
    r1, c1, r2, c2, а = int(м.group(1)), int(м.group(2)), int(м.group(3)), int(м.group(4)), м.group(5)
    г = _г(а)
    return г is not None and S.путь(г, (r1, c1), (r2, c2)) is None


def _счёт(м):
    а, k = м.group(1), int(м.group(2))
    г = _г(а)
    return г is not None and S.закрашено(г) == k


ОБРАЗЦЫ = (
    (rf"^grid ({Г}) rotated {Ч}° clockwise is (not )?({Г})\.$", _поворот),
    (rf"^сетка ({Г}) после поворота на {Ч}° по часовой стрелке — (не )?({Г})\.$", _поворот),
    (rf"^what is grid ({Г}) rotated {Ч}° clockwise\? it is ()({Г})\.$", _поворот),
    (rf"^какой станет сетка ({Г}) после поворота на {Ч}° по часовой стрелке\? она станет ()({Г})\.$", _поворот),
    (rf"^grid ({Г}) reflected (left-right|top-bottom) is (not )?({Г})\.$", _отражение),
    (rf"^сетка ({Г}) после отражения (слева направо|сверху вниз) — (не )?({Г})\.$", _отражение),
    (rf"^what is grid ({Г}) reflected (left-right|top-bottom)\? it is ()({Г})\.$", _отражение),
    (rf"^какой станет сетка ({Г}) после отражения (слева направо|сверху вниз)\? она станет ()({Г})\.$", _отражение),
    (rf"^grid ({Г}) shifted (right|left|down|up) by {Ч} is (not )?({Г})\.$", _сдвиг),
    (rf"^сетка ({Г}) после сдвига (вправо|влево|вниз|вверх) на {Ч} — (не )?({Г})\.$", _сдвиг),
    (rf"^what is grid ({Г}) shifted (right|left|down|up) by {Ч}\? it is ()({Г})\.$", _сдвиг),
    (rf"^какой станет сетка ({Г}) после сдвига (вправо|влево|вниз|вверх) на {Ч}\? она станет ()({Г})\.$", _сдвиг),
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
)
ПРАВИЛА = tuple((re.compile(о), п) for о, п in ОБРАЗЦЫ)


class _М:
    def __init__(self, группы):
        self._г = группы

    def group(self, i):
        return self._г[i - 1]

    def groups(self):
        return self._г


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if "/" not in с or ("#" not in с and "." not in с):
        return False, False
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            группы = tuple(None if г == "" else г for г in м.groups())
            return True, bool(проверить(_М(группы)))
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
