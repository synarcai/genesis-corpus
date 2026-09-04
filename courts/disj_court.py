#!/usr/bin/env python3
"""[ИСКЛЮЧЕНИЕ COURT] — the oracle is the REMAINDER, not a list of shows.

The second world of this corpus judged by computation rather than by
membership (the first is courts/infer_court.py). Each frame becomes a pattern
whose number holes are read back and recomputed:

  · the series must be exactly 0 … d−1 — exhaustive BY DIVISION, not by
    declaration, and this is the whole reason the row is arithmetic;
  · the excluded members must be exactly the series minus the conclusion;
  · the conclusion must equal n mod d.

Swap any number — a member of the series, an excluded one, the conclusion —
and the court catches it by counting, knowing nothing of what the house meant.
The world is CLOSED: a line matching a frame with wrong numbers is a lie.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import disjforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"disj"})
_ДЫРА = re.compile(r"\{(\w+)\}")
_ЧИСЛО = re.compile(r"\d+")
# дыры-числа читаются как число, дыры-ряды — как всё до точки
_РЯДЫ = ("ряд", "нет", "голый")


def _образцы():
    вон = []
    for язык in F.ЯЗЫКИ:
        for форма in ("ряд", "исключение", "вопрос_исключения"):
            рамка = (F.РАМКИ[язык]["вопрос"] + " " + F.РАМКИ[язык]["исключение"]
                     if форма == "вопрос_исключения" else F.РАМКИ[язык][форма])
            дыры, куски, конец = [], [], 0
            for м in _ДЫРА.finditer(рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                имя = м.group(1)
                дыры.append(имя)
                куски.append(r"([^.?!]+?)" if имя in _РЯДЫ else r"(\d+)")
                конец = м.end()
            куски.append(re.escape(рамка[конец:]))
            вон.append((форма, tuple(дыры), re.compile("^" + "".join(куски) + "$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _верно(поля):
    """ПЕРЕСЧЁТ: ряд исчерпывающ, исключённые суть дополнение вывода, вывод есть остаток."""
    n, d = поля.get("n"), поля.get("d")
    if not d or d < 2:
        return False
    ряд = поля.get("ряд")
    if ряд is not None and ряд != set(range(d)):
        return False
    r = n % d
    if "r" in поля and поля["r"] != r:
        return False
    лишние = set(range(d)) - {r}
    for имя in ("нет", "голый"):
        if имя in поля and поля[имя] != лишние:
            return False
    return True


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for форма, дыры, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        поля, сходится = {}, True
        for имя, кусок in zip(дыры, м.groups()):
            значение = ({int(ч) for ч in _ЧИСЛО.findall(кусок)} if имя in _РЯДЫ
                        else int(кусок))
            if имя in поля and поля[имя] != значение:
                сходится = False
                break
            поля[имя] = значение
        if not сходится:
            return True, False          # одна дыра — два разных содержания
        return True, _верно(поля)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): подменённый вывод, укороченный ряд,
    # лишний исключённый член — каждая подсадка ловится ПЕРЕСЧЁТОМ.
    подсадки = ("остаток от деления 17 на 5 — одно из чисел 0, 1, 2, 3 или 4. он не 0, не 1, не 3 и не 4. значит он 3.",
                "остаток от деления 17 на 5 — одно из чисел 0, 1, 2 или 3. он не 0, не 1 и не 3. значит он 2.",
                "остаток от деления 17 на 5 — одно из чисел 0, 1, 2, 3 или 4. он не 0, не 1 и не 3. значит он 2.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:100]}")
        print(f"ИСКЛЮЧЕНИЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_disj.txt":
            continue
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip() or с.startswith("\x0c"):
                continue
            судимо, истинно = судить(с)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(с)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ИСКЛЮЧЕНИЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
