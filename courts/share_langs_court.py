#!/usr/bin/env python3
"""[SHARES IN EIGHT LANGUAGES COURT] — the share is read back from its name,
the ledger and the value are recomputed, the copula agrees with the numerator."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import shareforms as F  # noqa: E402

ПРАВИЛА = {язык: F.образцы(язык) for язык in F.ЯЗЫКИ}


def судить(строка):
    с = строка.strip()
    for язык, правила in ПРАВИЛА.items():
        for образец, спрошено in правила:
            м = образец.match(с)
            if м:
                return True, F.судить_группы(язык, спрошено, м.groups())
    return False, False


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_share_langs.txt":
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
    print(f"ДОЛИ НА ЯЗЫКАХ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
