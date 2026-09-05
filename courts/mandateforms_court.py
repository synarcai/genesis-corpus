#!/usr/bin/env python3
"""[MANDATE COURT] — the verdict follows the standing rule, or the page lies; CLOSED WORLD.

A show of the mandate world (tools/mandateforms.py) is one page of INSTRUCTION FOLLOWING: one
or two standing rules, an order of one act, and a verdict that names the act it is grounded
on — «no: the rule forbids deleting», «yes: the rule forbids deleting, but this is creating»,
«the second rule: it forbids moving», «yes: no rule forbids creating», «two rules: they forbid
deleting and moving».

The court reads each line back through the house's frames, and every frame says WHICH rules
stand and WHICH act is ordered. A page is true when a «no» stands over an order the mandate
does forbid, when a «yes» stands only over an order no rule covers, when the rule named as
forbidding is the one whose act is the ordered act, when a claim that the mandate is silent is
made only about an act no rule names, when the count of rules is the count and their listed
acts are theirs, and when the count form of the thing is the form of its number. A line of a
frame that breaks any of these is a lie; a line of no frame is a lie of the closed world.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import mandateforms as F  # noqa: E402
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"mandateforms"})

# СВОБОДНОЕ ЧИСЛО (М-…, 05.09): счёт приказа НЕ НЕСЁТ ИСТИНЫ ВЕРДИКТА. «удали 3 файла» и
# «удали 4 файла» одинаково запрещены правилом «не удаляй файлы» — мандат говорит о
# ДЕЙСТВИИ, а не о величине, и подмена цифры не делает страницу ложной. Истину числа здесь
# несёт лишь его СЧЁТНАЯ ФОРМА («удали 3 файлов» — ложь), и её судит закон дома; подсадка
# такой формы стоит в списке ниже шестой строкой.
СВОБОДНОЕ_ЧИСЛО = [re.compile(r"(\d+)")]


def _судить(строка):
    return F.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): отказ над приказом, которого правило не касается; согласие
    # над запрещённым приказом; названо правило, этого не запрещающее; молчание мандата над
    # запрещённым приказом; счётная форма чужого числа.
    подсадки = (
        "rule: do not delete files. create 3 files. may the order be carried out? no: the rule forbids creating.",
        "правило: не удаляй файлы. создай 3 файла. можно ли выполнить приказ? нет: правило запрещает создание.",
        "rule: do not delete files. delete 3 files. may the order be carried out? yes: the rule forbids deleting, but this is deleting.",
        "the first rule: do not delete files. the second rule: do not move files. create 3 files. which rule forbids this? the second rule: it forbids creating.",
        "the first rule: do not delete files. the second rule: do not move files. delete 3 files. may the order be carried out? yes: no rule forbids deleting.",
        "правило: не удаляй файлы. удали 3 файлов. можно ли выполнить приказ? нет: правило запрещает удаление.",
        "zasada: nie usuwaj plików. usuń 3 plików. czy można wykonać polecenie? nie: zasada zabrania usuwania.",
        "regel: verwijder geen bestanden. verwijder 3 bestand. kan de opdracht worden uitgevoerd? nee: de regel verbiedt verwijderen.",
    )
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:160]}")
        print(f"МАНДАТ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    пути = [п for п in worlds(kind="shows") if п.name == "genesis_mandateforms.txt"]
    if not пути:  # мир ещё не в манифесте — суд читает свой файл по имени
        свой = pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_mandateforms.txt"
        пути = [свой] if свой.exists() else []
        print("  мир не в манифесте — суд читает datasets/genesis_mandateforms.txt по имени")
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
    print(f"МАНДАТ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
