#!/usr/bin/env python3
"""[PERSONALITY COURT] — the voice may change, the fact may not; CLOSED WORLD.

A show of the personality world (tools/personforms.py) is one page of the seventh market of
the agent's architecture: a slow state variable with a provenance, and the two things it is
lawfully allowed to touch — the FORM of an answer and the CHOICE BETWEEN EQUALS.

The court reads each line back through the house's frames. A page is true when the tape's
ledger recomputes, when each count form is the form of ITS number and all forms are forms of
one thing, when the copula of a place bends with the number it stands at, when the terse and
the verbose answer of one page carry THE SAME number (a personality that changes the fact is
a lie, and the corpus says so on the page itself), when a choice by character is offered only
where the two ways leave the SAME count — recomputed by the court — and when the way chosen
is the one the trait requires: the cautious personality takes the way that destroys nothing,
the quick one takes the way named first. A line of a frame that breaks any of these is a lie;
a line of no frame is a lie of the closed world.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import personforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"personforms"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): краткий ответ чужим числом; леджер подробного не сходится;
    # два ответа разошлись числом (личность изменила ФАКТ); осторожная выбрала удаление;
    # скорая взяла второй путь; равенство исходов объявлено, а числа не сходятся.
    подсадки = (
        "personality: terse. there are 10 files in the folder. the first act creates 3 files. how many files are in the folder? 14.",
        "personality: verbose. there are 10 files in the folder. the first act creates 3 files. how many files are in the folder? there are 13 files in the folder: 10 + 3 = 14.",
        "there are 10 files in the folder. the first act creates 3 files. how many files are in the folder? terse personality answers 13. verbose personality answers: there are 14 files in the folder: 10 + 3 = 14. is it the same number? yes: 13 and 14 — one number.",
        "personality: cautious. there are 10 files in the folder. two ways: to delete 3 files or to move 3 files. both leave 7 files in the folder: 10 − 3 = 7. which way is chosen? to delete 3 files: a cautious personality does not delete.",
        "personality: quick. there are 10 files in the folder. two ways: to delete 3 files or to move 3 files. both leave 7 files in the folder: 10 − 3 = 7. which way is chosen? to move 3 files: a quick personality takes the first way.",
        "personality: cautious. there are 10 files in the folder. two ways: to delete 3 files or to move 3 files. both leave 8 files in the folder: 10 − 3 = 8. which way is chosen? to move 3 files: a cautious personality does not delete.",
        "личность: краткая. в папке 10 файлов. первый акт создаёт 3 файла. сколько файлов в папке? 12.",
        "osobowość: zwięzła. w folderze jest 10 plików. pierwszy akt tworzy 3 pliki. ile plików jest w folderze? 12.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:160]}")
        print(f"ЛИЧНОСТЬ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_personforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_personforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_personforms.txt по имени")
    for путь in пути:
        for стр in путь.read_text(encoding="utf-8").splitlines():
            if not стр.strip() or стр.startswith("\x0c"):
                continue
            судимо, истинно = _судить(стр)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(стр)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:160]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ЛИЧНОСТЬ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
