#!/usr/bin/env python3
"""[ACTION MEASURE IN SEVEN LANGUAGES] — the unit is the verb's, the count forms are the number's, the sums hold.

A show of the world (tools/measurelangs.py) is d5's genus of action measure said
in de/fr/es/it/pt/nl/pl: «der Frosch sprang 12 Zentimeter. wie weit sprang der
Frosch? 12 Zentimeter.», its sum, and the bearers at a place with an arrival or
a departure. The court reads each page through the same frames: the unit must be
of the verb's kind, every count form must be its number's, sums and bearer counts
must recompute. The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import measurelangs as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"action_measure_langs"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): единица не по глаголу; сумма не сходится; носители не сходятся; польская форма не по числу
    # С 23.09 подсадки выводит ДОМ из своих таблиц (`measurelangs.подсадки`): литералы прежних
    # сцен после переписи сцен стали чужими строками, и суд не поймал ни одной — 0 из 4.
    подсадки = tuple(битая for _, битая in F.подсадки())
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"МЕРА ДЕЙСТВИЯ НА ЯЗЫКАХ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_action_measure_langs.txt":
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
    print(f"МЕРА ДЕЙСТВИЯ НА ЯЗЫКАХ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
