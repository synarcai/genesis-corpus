#!/usr/bin/env python3
"""[СТРОГИЙ ВЫВОД COURT] — the oracle is DIVISION, not a list of shows.

Every other closed world of this corpus is judged by membership: the house
declares its shows and a line is true when the house names it. This world is
judged by ARITHMETIC. Each frame is compiled into a pattern whose holes are
NUMBERS; on a match the numbers are read out and the claim is recomputed:

  закон      «если число делится на {a}, оно делится на {b}.»   a % b == 0, a ≠ b
  поненс     «{n} делится на {a}. значит {n} делится на {b}.»    n % a == 0 (hence n % b == 0)
  толленс    «{m} не делится на {b}. значит {m} не делится на {a}.»  m % b ≠ 0
  (each of the three valid steps also carries a QUESTION surface — «12 делится
  на 4. делится ли 12 на 2? да.» — judged by the same recount)
  обращение  «{k} делится на {b}. значит ли, что {k} делится на {a}? нет: …»  k % b == 0, k % a ≠ 0
  отрицание  «{k} не делится на {a}. значит ли, что {k} не делится на {b}? нет: …»  same witness

The strength is that the court knows NOTHING of what the house meant to say:
swap any number and the court catches it by counting. A show of this world is
therefore true in the same sense an arithmetic line is true, and the two
FALLACY forms are true as REFUTATIONS — the witness they name really is
divisible by the smaller divisor and really is not divisible by the larger.

The world is CLOSED: a line matching a frame with wrong numbers is a lie, not
silence.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import inferforms as F  # noqa: E402

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name

ЗАМКНУТЫЕ_МИРЫ = frozenset({"infer"})
_ДЫРА = re.compile(r"\{(\w+)\}")


def _образцы():
    """[(форма, дыры, образец)] — рамка с числовыми дырами, обращённая в образец."""
    вон = []
    for язык in F.ЯЗЫКИ:
        for форма, рамка in F.РАМКИ[язык].items():
            дыры, куски, конец = [], [], 0
            for м in _ДЫРА.finditer(рамка):
                куски.append(re.escape(рамка[конец:м.start()]))
                дыры.append(м.group(1))
                куски.append(r"(\d+)")
                конец = м.end()
            куски.append(re.escape(рамка[конец:]))
            вон.append((форма, tuple(дыры), re.compile("^" + "".join(куски) + "$")))
    return tuple(вон)


ОБРАЗЦЫ = _образцы()


def _верно(форма, поля):
    """ПЕРЕСЧЁТ, а не список: истинность показа есть истинность деления."""
    a, b = поля.get("a"), поля.get("b")
    if a is None or b is None or b == 0 or a == b or a % b:
        return False                     # закон дома: больший делится на меньший
    if форма in ("закон", "закон_вопрос"):
        return True
    if форма in ("поненс", "поненс_вопрос"):
        return поля["n"] % a == 0
    if форма in ("толленс", "толленс_вопрос"):
        return поля["m"] % b != 0
    if форма in ("обращение", "отрицание"):
        k = поля["k"]
        return k % b == 0 and k % a != 0
    return False


def _судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for форма, дыры, образец in ОБРАЗЦЫ:
        м = образец.match(с)
        if not м:
            continue
        поля = {}
        for имя, значение in zip(дыры, м.groups()):
            значение = int(значение)
            if поля.setdefault(имя, значение) != значение:
                return True, False       # одна дыра — два разных числа
        return True, _верно(форма, поля)
    return False, False


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import collections
    from genesis import worlds
    # ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106): суд обязан поймать подсаженные числа
    подсадки = ("12 делится на 4. значит 12 делится на 5.",
                "6 не делится на 2. значит 6 не делится на 4.",
                "12 делится на 2. значит ли, что 12 делится на 4? нет: 12 не делится на 4.",
                "если число делится на 3, оно делится на 4.",
                "что следует из того, что 12 делится на 4? 12 делится на 4. значит 12 делится на 5.")
    пойманы = sum(1 for п in подсадки if _судить(п) == (True, False))
    if пойманы != len(подсадки):
        for п in подсадки:
            print(f"  ПОДСАДКА {_судить(п)}: {п}")
        print(f"СТРОГИЙ ВЫВОД FAIL: подсадок поймано {пойманы} из {len(подсадки)}")
        return 1
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_infer.txt":
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
    print(f"СТРОГИЙ ВЫВОД {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, "
          f"несудимых {итог['несудимых']}; подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
