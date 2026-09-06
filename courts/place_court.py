#!/usr/bin/env python3
"""[PLACE COURT] — the converse, the transitive and the middle, on two axes; CLOSED WORLD.

A show of the place world (tools/placeforms.py) is a chain of things on one axis and one of three
questions over it. The court reads the things out of the line — each in the case its axis demands
— and REBUILDS the page the laws require from them: an answer that names the wrong side, the
wrong thing, or grounds the middle on the same side twice rebuilds into a different page and is a
lie. A thing wearing the wrong case is not a page of this world at all.

The census found zero lines of «слева от» and four of «above the» in the whole свод before this
house.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import placeforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"place"})


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): обратное не обращено; обращено о чужой вещи; переходное
    # назвало вещь вне цепи; вывод перевёрнут; серединой названа крайняя вещь; основание
    # середины взято с одной стороны дважды; верхняя ось не обращена; вопрос о чужом конце.
    подсадки = (
        "книга находится слева от чашки. где находится чашка? слева от книги: слева и справа — обратные стороны.",
        "the book is to the left of the cup. where is the cup? to the right of the lamp: to the left and to the right are opposite sides.",
        "das Buch ist links von der Tasse, die Tasse ist links von der Lampe. was ist links von der Lampe? das Buch und der Schlüssel: also ist das Buch links von der Lampe.",
        "das Buch ist links von der Tasse, die Tasse ist links von der Lampe. was ist links von der Lampe? das Buch und die Tasse: also ist die Lampe links von der Lampe.",
        "le livre est à gauche de la tasse, la tasse est à gauche de la lampe. qu'y a-t-il entre le livre et la lampe ? la lampe : la lampe est à droite du livre et à gauche de la lampe.",
        "il libro si trova a sinistra della tazza, la tazza si trova a sinistra della lampada. che cosa si trova tra il libro e la lampada? la tazza: la tazza si trova a sinistra del libro e a sinistra della lampada.",
        "lampa jest nad kluczem. gdzie jest klucz? nad lampą: nad i pod to strony przeciwne.",
        "книга находится слева от чашки, чашка находится слева от лампы. что находится слева от чашки? книга и чашка: значит, книга находится слева от лампы.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:150]}")
        print(f"МЕСТО FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_place.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_place.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_place.txt по имени")
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
        print(f"  ЛОЖЬ: {п[:150]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"МЕСТО {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
