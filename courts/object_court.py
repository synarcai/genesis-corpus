#!/usr/bin/env python3
"""[ВОЗРАЖЕНИЕ COURT] — the check is the INVERSE operation, recomputed.

The house shows what to do with what another person said: verify it and answer
by the verification. The court recomputes the verification itself.

  да   «you said {a} minus {b} makes {c}. is that so? yes: {c} + {b} = {a}.»
           true  ⟺  a − b = c  and  c + b = a
  нет  «… makes {x}. is that so? no: {x} + {b} = {y}, not {a}.»
           true  ⟺  a − b ≠ x  and  x + b = y  and  y ≠ a

The last two conditions matter most: an objection whose check COMES OUT RIGHT
would be an objection to a true statement — a lie that teaches both the method
of verification and the habit of arguing with correct people. The court forbids
it by counting.

The world is CLOSED.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import objectforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"object"})
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
    if форма == "да":
        c = п["c"]
        return a - b == c and c + b == a
    x, y = п["x"], п["y"]
    return a - b != x and x + b == y and y != a


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
    c = a - b
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): согласие с неверным остатком; проверка,
    # дающая не то число; возражение на ВЕРНОЕ (его проверка сошлась бы).
    подсадки = (я["да"].format(a=a, b=b, c=c + 1),
                я["нет"].format(a=a, b=b, x=c + 1, y=a),
                я["нет"].format(a=a, b=b, x=c, y=a))
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ВОЗРАЖЕНИЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_object.txt":
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
    print(f"ВОЗРАЖЕНИЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
