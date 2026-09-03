#!/usr/bin/env python3
"""[UNIT CONVERSIONS IN EIGHT LANGUAGES COURT] — the ratio is the house of
units', the count forms are the house of unit names', the product is
recomputed; nothing is looked up from the line."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import unitforms as U  # noqa: E402

ПРАВИЛА = {язык: U.образцы(язык) for язык in U.ЕДИНИЦЫ}


def судить(строка):
    с = строка.strip()
    for язык, правила in ПРАВИЛА.items():
        for образец, спрошено in правила:
            м = образец.match(с)
            if м:
                return True, U.судить_группы(язык, спрошено, м.groups())
    return False, False


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_units_langs.txt":
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
        print(f"  ЛОЖЬ: {п[:110]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ЕДИНИЦЫ НА ЯЗЫКАХ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
