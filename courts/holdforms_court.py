#!/usr/bin/env python3
"""[HOLDINGS-WITHOUT-A-VERB COURT] — the frame's holes agree, or the page lies; CLOSED WORLD.

A show of the holdings world (tools/holdforms.py) is one of four frames with a question
surface and a full-sentence answer: a bearer holds n things; a person is n years old; two
bearers hold two numbers and the question names the second; a bearer holds none. The court
reads each line through the house's frames: a page whose repeated holes carry one value
(the answer's number and thing are the story's, the bearer of the question is the bearer of
the story), whose count form is the form of its number and whose year is the form of its age
is true; a line of a frame that breaks any of these is a lie; a line of no frame is a lie of
the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import holdforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"holdforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): the answer's number is not the story's; the answer's count
    # form is not the form of its number; the second bearer answered with the first one's number;
    # the age answered in the wrong form of the year; «none» answered with another thing
    подсадки = (
        "Ann has 12 coins. how many coins does Ann have? Ann has 13 coins.",
        "у Ани 12 монет. сколько монет у Ани? у Ани 12 монета.",
        "Ann has 12 coins and Ben has 5 coins. how many coins does Ben have? Ben has 12 coins.",
        "Ann is 12 years old. how old is Ann? Ann is 12 year old.",
        "Lena hat keine Münzen. wie viele Münzen hat Lena? null: Lena hat keine Bälle.",
        "Marta tiene 12 monedas. ¿cuántos monedas tiene Marta? Marta tiene 12 monedas.",
        # ВОЛНА 2 (05.09): вопрос о ВТОРОМ товаре, отвеченный числом первого; владелец назван
        # чужим именем; вещь названа чужой вещью; место названо чужим местом; связка места не
        # по числу («there are 1 book»); вопрос «где» о единственном — шов, дом его не пишет
        "Ann has 12 coins and 5 books. how many books does Ann have? Ann has 12 books.",
        "у Ани 12 монет. у кого 12 монет? у Анны.",
        "Ann has 12 coins. what does Ann have? Ann has books.",
        "there are 12 books on the shelf. where are the 12 books? in the box.",
        "there are 1 book on the shelf. how many books are on the shelf? there are 1 book on the shelf.",
        "there is 1 book on the shelf. where is the 1 book? on the shelf.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ДЕРЖАНИЯ БЕЗ ГЛАГОЛА FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_holdforms.txt"]
    if not пути:  # the world is not in the manifest yet — the court reads its file by name
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_holdforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_holdforms.txt по имени")
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
    print(f"ДЕРЖАНИЯ БЕЗ ГЛАГОЛА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
