#!/usr/bin/env python3
"""[COUNT FACTS COURT] — a thing is defined or asked by its one count, and the count is RECOUNTED.

A show of the count-facts world (tools/countfacts.py) is «what is a triangle?
a triangle is a shape with three sides.», «how many sides does a pentagon
have? a pentagon has five sides.» or «how many legs does a dog have? a dog
has four legs.» in nine languages. The court reads each page through the
same house: the entity must be a declared one, and the count phrase must be
the declared phrase of ITS number («a square has five sides», «a spider has
six legs» are lies before any grammar is checked). The world is CLOSED:
every honest line of it is a page of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import countfacts as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"countfacts"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): счёт чужой сущности — в определении, в вопросе о сторонах, в вопросе о ногах
    подсадки = (
        "what is a triangle? a triangle is a shape with four sides.",
        "how many sides does a square have? a square has five sides.",
        "что такое шестиугольник? шестиугольник — это фигура, у которой восемь сторон.",
        "сколько ног у паука? у паука шесть ног.",
        "how many legs does a chicken have? a chicken has four legs.",
        "ile nóg ma mrówka? mrówka ma osiem nóg.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"СЧЁТНЫЕ ФАКТЫ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_countfacts.txt":
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
    print(f"СЧЁТНЫЕ ФАКТЫ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
