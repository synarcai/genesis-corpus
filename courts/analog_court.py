#!/usr/bin/env python3
"""[ПОДОБИЕ COURT] — the oracle is the CROSS PRODUCT.

The fourth world judged by computation. Each frame becomes a pattern whose
number holes are read back, and the claim is recomputed:

  утв, воп   «a is to b as c is to d»            —  a × d must equal b × c
  нет        «is a to b as c is to x? no: …»     —  the two products printed
             must be the products claimed, AND they must differ (otherwise the
             refusal refuses a true analogy)

The last check matters most: a refutation that names two EQUAL products would
be a lie of the strongest kind — it would teach the organism to reject a true
analogy while showing it the correct test. The court catches it by counting.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import analogforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"analog"})
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
    a, b, c = п["a"], п["b"], п["c"]
    if форма in ("утв", "воп"):
        return a * п["d"] == b * c
    x, p, q = п["x"], п["p"], п["q"]
    return a * x == p and b * c == q and p != q


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
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): подобие неподобных, подменённое
    # произведение и — самое опасное — отказ, называющий РАВНЫЕ произведения.
    подсадки = ("2 относится к 6, как 5 к 16.",
                "2 относится к 6, как 5 к 16? нет: 2 × 16 = 30, а 6 × 5 = 30.",
                "2 относится к 6, как 5 к 15? нет: 2 × 15 = 30, а 6 × 5 = 30.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п}")
        print(f"ПОДОБИЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_analog.txt":
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
    print(f"ПОДОБИЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
