#!/usr/bin/env python3
"""[HOLE MARKET COURT] — the question is recomputed from the fact, the
answer from the hole.

A line of the holes world is a fact frame («on monday anna put 5 cups on
the shelf.») alone, or that fact followed by ONE question and its answer.
The court parses the fact by the frame of the house of holes (time, actor,
verb, number, thing, place), builds every lawful question of it — one per
role — with its answer (the filler the question removed), and the line is
true iff its question and answer are one of those pairs. Nothing is looked
up from the line: the RU count forms come from the house of forms, the
verb's base and gender forms from the house of holes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import holes  # noqa: E402


def судить(строка):
    return holes.судить(строка)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_holes.txt":
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
    print(f"ДЫРЫ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
