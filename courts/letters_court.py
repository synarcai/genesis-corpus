#!/usr/bin/env python3
"""[LETTERS COURT] — the count, the spelling and the letter are the word's own, RECOUNTED.

A show of the letters world (tools/letters.py) is «how many letters are
there in the word "cat"? 3: c, a, t.», «what is the first letter of the word
"cat"? "c".» or the last letter, in nine languages. The court reads each page
through the same house: the word must be a declared one, the count must be
its length, the spelling its letters in order, the letter its first or last.
The world is CLOSED: every honest line of it is a page of this house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import letters as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"letters"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): счёт не по слову; буквы не по порядку; первая буква — последняя;
    # последняя — первая; слово, не объявленное домом
    подсадки = (
        'how many letters are there in the word "cat"? 4: c, a, t.',
        "сколько букв в слове «кот»? 3: к, т, о.",
        'what is the first letter of the word "dog"? "g".',
        "jaka jest ostatnia litera słowa „kot”? „k”.",
        "wie viele Buchstaben hat das Wort „Maus“? 4: M, a, u, s.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"БУКВЫ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_letters.txt":
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
    print(f"БУКВЫ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
