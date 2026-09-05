#!/usr/bin/env python3
"""[COMPARISON-FRAMES COURT] — the marker's sign is recomputed, or the page lies; CLOSED WORLD.

A show of the comparison world (tools/cmpframes.py) is one of four frames — MORE-BY, LESS-BY,
TIMES, HOW-MANY-MORE — on a deed or a holding, with a question surface and a full-sentence
answer carrying its ledger. The court reads each line through the house's frames: the
ledger's sign must be the frame's (a MORE frame that subtracts is the reader's own lie, by
sign), the ledger must recompute from the story's numbers, the answer's number must be the
ledger's result, every goods form must be the form of its number and of one goods, and the
question word must bend by the goods' gender; a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import cmpframes as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"cmpframes"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): the lie by sign (a MORE frame whose ledger subtracts); the
    # ledger that does not add up; the answer that is not the ledger's result; LESS answered with
    # the sum; TIMES with a multiplier the word does not name; a count form not of its number;
    # the question word of the wrong gender
    подсадки = (
        "Marta hizo 16 flexiones. Pablo hizo 7 flexiones más que Marta. ¿cuántas flexiones hizo Pablo? Pablo hizo 9 flexiones: 16 − 7 = 9.",
        "Ann did 16 push-ups. Ben did 7 more push-ups than Ann. how many push-ups did Ben do? Ben did 24 push-ups: 16 + 7 = 24.",
        "Ann did 16 push-ups. Ben did 7 more push-ups than Ann. how many push-ups did Ben do? Ben did 22 push-ups: 16 + 7 = 23.",
        "Daan heeft 16 doppen. Lotte heeft 7 doppen minder dan Daan. hoeveel doppen heeft Lotte? Lotte heeft 23 doppen: 16 + 7 = 23.",
        "Anna ma 16 kapsli. Jan ma dwa razy więcej kapsli niż Anna. ile kapsli ma Jan? Jan ma 48 kapsli: 16 × 3 = 48.",
        "Анна сделала 16 отжиманий. Ваня сделал на 7 отжиманий больше, чем Анна. сколько отжиманий сделал Ваня? Ваня сделал 23 отжимание: 16 + 7 = 23.",
        "Marta hizo 16 flexiones. Pablo hizo 7 flexiones más que Marta. ¿cuántos flexiones hizo Pablo? Pablo hizo 23 flexiones: 16 + 7 = 23.",
        # WAVE 2 (05.09): the answer without arithmetic is a NAME read from the NUMBERS, and the
        # inverse of TIMES answers with the multiplier word of its own quotient
        "у Анны 26 крышек. у Веры 11 крышек. у кого крышек больше? у Веры крышек больше.",
        "Anna did 22 push-ups. Carla did 9 push-ups. who did fewer push-ups? Anna did fewer push-ups.",
        "Lena hat 33 Actionfiguren. Felix hat 32 Actionfiguren. wer hat mehr Actionfiguren? keiner: beide haben gleich viele — 32 Actionfiguren.",
        "Piotr zrobił 48 brzuszków. Ewa zrobiła 16 brzuszków. ile razy więcej brzuszków zrobił Piotr niż Ewa? dwa razy więcej: 48 ÷ 16 = 3.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"РАМКИ СРАВНЕНИЯ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_cmpframes.txt"]
    if not пути:  # the world is not in the manifest yet — the court reads its file by name
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_cmpframes.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_cmpframes.txt по имени")
    for путь in пути:
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = _судить(стр)  # silence counts as unjudged here; the gate closes it
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"РАМКИ СРАВНЕНИЯ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
