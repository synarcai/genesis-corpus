#!/usr/bin/env python3
"""[ПРОВЕРКА ГИПОТЕЗЫ COURT] — the witness AND the verdict are recomputed.

Three things are counted on every line, and the third is the reason the world
exists:

  · держится — the witness must be divisible by BOTH divisors;
  · падает   — the witness must be divisible by the SMALLER and not by the
               larger, and the pair must really be a divisor pair;
  · and the VERDICT must match the outcome: a passing test may never be
    written with the rejecting tail, and a failing test may never be written
    with the holding tail.

The asymmetry itself — «it holds so far» for a pass, «so no» for a failure — is
carried by the frame, so a swapped tail is a swapped frame and simply does not
match. What the court adds is that the NUMBERS may not lie about which frame
they belong to.

The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import hypoforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"hypo"})
_ДЫРА = re.compile(r"\{(\w+)\}")


def _образцы():
    вон = []
    for язык in F.ЯЗЫКИ:
        for форма in F.ФОРМЫ:
            рамка = F.РАМКИ[язык][форма]
            дыры, куски, конец = [], [], 0
            for м in _ДЫРА.finditer(рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                дыры.append(м.group(1))
                куски.append(r"(\d+)")
                конец = м.end()
            куски.append(re.escape(рамка[конец:]))
            вон.append((форма, tuple(дыры), re.compile("^" + "".join(куски) + "$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _верно(форма, п):
    a, b = п["a"], п["b"]
    if b == 0 or a % b or a == b:
        return False                      # пара обязана быть парой делителей
    if форма == "держится":
        n = п["n"]
        return n % a == 0 and n % b == 0
    m = п["m"]
    return m % b == 0 and m % a != 0


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for форма, дыры, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        поля = {}
        for имя, значение in zip(дыры, м.groups()):
            значение = int(значение)
            if поля.setdefault(имя, значение) != значение:
                return True, False
        return True, _верно(форма, поля)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    я = F.РАМКИ["ru"]
    a, b = F.ПАРЫ[0]
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): свидетель, не делящийся на больший, назван
    # держащимся; свидетель, делящийся на больший, назван падающим (то есть
    # гипотеза отвергнута верным примером); пара, не являющаяся парой делителей.
    подсадки = (я["держится"].format(a=a, b=b, n=F.свидетель_падает(a, b)),
                я["падает"].format(a=a, b=b, m=F.свидетель_держится(a, b)),
                я["держится"].format(a=b, b=a, n=F.свидетель_держится(a, b)))
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ПРОВЕРКА ГИПОТЕЗЫ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_hypo.txt":
            continue
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ПРОВЕРКА ГИПОТЕЗЫ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
