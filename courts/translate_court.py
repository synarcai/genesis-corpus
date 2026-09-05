#!/usr/bin/env python3
"""[TRANSLATION COURT] — the answer is the same word or phrase in the named language, RECHECKED.

A show of the translation world (tools/translateforms.py) is «как будет «кот»
по-английски? cat.» or «how do you say "thank you" in french? merci.» — nine
languages, each into each. The court reads each page through the same tables
(the letters house's aligned words, the dialogue house's first thanks, greeting
and farewell, and this house's names of languages): the named language must be
a declared one and not the asking one, the word must be the asking language's,
and the answer must be ITS counterpart in the named language («cat» for «кот»
in english — «dog» is a lie by the table). The world is CLOSED.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import translateforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"translate"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): чужое слово того же языка; слово третьего языка; тот же язык
    подсадки = (
        "как будет «кот» по-английски? dog.",
        'what is "cat" in russian? Katze.',
        "wie sagt man „danke“ auf Französisch? gracias.",
        "как будет «кот» по-русски? кот.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ПЕРЕВОД FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_translate.txt":
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
    print(f"ПЕРЕВОД {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
