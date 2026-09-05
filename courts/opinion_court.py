#!/usr/bin/env python3
"""[ФАКТ И МНЕНИЕ COURT] — the fact is checked against the NEIGHBOUR'S list.

The house never declares a fact of its own: it quotes the world-facts house.
The court therefore does not trust this house's list — it reads the statement
out of the line and asks the neighbour whether that statement is a fact.

  «X — is that a fact or an opinion? a fact: it can be checked.»
       true  ⟺  X stands among the first ФАКТОВ facts of worldfacts
  «X — is that a fact or an opinion? an opinion: another person may…»
       true  ⟺  X stands among the declared opinions of this house

A line of this SHAPE carrying a statement from the wrong side is claimed and
FALSE, not silent — that is what makes the world closed, and it is the whole
point: a corpus must not be able to call an opinion a fact, and the guard
against it is the neighbour's declaration, not this house's good intentions.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import opinionforms as F  # noqa: E402
import worldfacts as W  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"opinion"})

# {язык: (образец, хвост_факта, хвост_мнения)} — рамка с ОДНОЙ дырой под утверждение
ОБРАЗЦЫ = {}
for _яз, _я in F.РАМКИ.items():
    # ВСЕ ПОВЕРХНОСТИ ВОПРОСА ДОМА — одним образцом (05.09: польская вторая
    # поверхность «to fakt czy opinia?» сделала 12 честных строк ложью замкнутого
    # мира, ибо суд держал рамку второй рукой и знал одну поверхность)
    _куски = []
    for _п in ("вопрос", "вопрос2"):
        if _п in _я:
            _голова, _, _хвост = _я[_п].partition("{у}")
            _куски.append(re.escape(_голова) + "(.+?)" + re.escape(_хвост))
    ОБРАЗЦЫ[_яз] = (re.compile("^(?:" + "|".join(_куски) + ")" +
                               r"\s+(" + re.escape(_я["факт"]) + "|" + re.escape(_я["мнение"]) + ")$"),
                    _я["факт"], _я["мнение"])

_ФАКТЫ = {яз: {з[0] for з in W.ФАКТЫ[яз][:F.ФАКТОВ]} for яз in F.ЯЗЫКИ}
_МНЕНИЯ = {яз: set(F.МНЕНИЯ[яз]) for яз in F.ЯЗЫКИ}


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for яз, (образец, хвост_факта, хвост_мнения) in ОБРАЗЦЫ.items():
        м = образец.match(с)
        if not м:
            continue
        # из двух поверхностей заполнена одна — берём непустую группу утверждения
        группы = [г for г in м.groups()[:-1] if г is not None]
        утверждение, хвост = группы[0], м.groups()[-1]
        если_факт = хвост == хвост_факта
        нужный = _ФАКТЫ[яз] if если_факт else _МНЕНИЯ[яз]
        чужой = _МНЕНИЯ[яз] if если_факт else _ФАКТЫ[яз]
        if утверждение in нужный:
            return True, True
        if утверждение in чужой:
            return True, False      # род назван наоборот — ложь, а не молчание
        return True, False          # утверждения не объявлял никто — тоже ложь
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): мнение, названное фактом; факт, названный
    # мнением; утверждение, которого сосед фактом не объявлял.
    я = F.РАМКИ["ru"]
    подсадки = (f"{я['вопрос'].format(у=F.МНЕНИЯ['ru'][0])} {я['факт']}",
                f"{я['вопрос'].format(у=W.ФАКТЫ['ru'][0][0])} {я['мнение']}",
                f"{я['вопрос'].format(у=W.ФАКТЫ['ru'][6][0])} {я['факт']}")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п[:110]}")
        print(f"ФАКТ И МНЕНИЕ FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_opinion.txt":
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
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"ФАКТ И МНЕНИЕ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
