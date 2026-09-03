#!/usr/bin/env python3
"""THE HOUSE OF CHAINS — a ledger of two steps in twenty-nine languages.

The owner's word: every language in surplus. Ten languages carry houses of
phrases; the other nineteen (am, ar, el, fa, fi, he, hi, hu, id, ja, ka,
ko, sv, sw, ta, th, uk, vi, zh) had lexicon and single equalities only —
and NOT ONE CHAIN: «6 + 5 = 11. 11 − 3 = 8.» — the form the market of
reasoning buys (holon, ONE-CARRIER: the ledger is the program is the
proof).

NOT ONE NEW WORD IS INVENTED. Every pack already declares, in its
`show_kinds.arithmetic`, the TEMPLATES of its equalities with holes —
«{num:n} plus {num:m} equals {num:sum}.», «{num:sum} 减 {num:m} 等于
{num:n}。», «{num:n} 足す {num:m} は {num:sum}.» — and the numerals that
fill them. This house reads those templates, tells addition from
subtraction and multiplication from division BY THE PLACE OF THE HOLES,
and writes two steps in a row where the result of the first is an operand
of the second. The court reads the same templates back, reads the numerals
to their numbers by the pack, recounts every step and checks the seam:
the number that leaves the first step is the number that enters the
second — a chain whose seam is broken is a lie.
"""
import json
import pathlib
import re

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
ПАКЕТЫ = КОРЕНЬ / "tools" / "langpacks"
_ДЫРА = re.compile(r"\{(num:)?([nms]\w*|sum|prod)\}")


def _пакеты():
    вон = {}
    for путь in sorted(ПАКЕТЫ.glob("*.json")):
        try:
            вон[путь.stem] = json.loads(путь.read_text(encoding="utf-8"))
        except ValueError:
            continue
    return вон


ПАКЕТЫ_ВСЕ = _пакеты()


def числительные(язык):
    """{value: word} of the pack — the only numbers this language may say."""
    вон = {}
    for ключ, слово in (ПАКЕТЫ_ВСЕ[язык].get("numerals") or {}).items():
        к = str(ключ)
        if k_целое(к):
            вон[int(к)] = str(слово)
    return вон


def k_целое(к):
    return k_цифры(к) and int(к) >= 0


def k_цифры(к):
    return к.lstrip("-").isdigit()


def _вид(шаблон):
    """(operation, hole order) of a declared template, read by the PLACE of its
    holes: «{num:n} + {num:m} = {num:sum}» is addition, «{num:sum} − {num:m} =
    {num:n}» subtraction, «{num:n} × {num:m} = {num:prod}» multiplication,
    «{num:prod} ÷ {num:m} = {num:n}» division; the same four with bare holes
    are the same operations written in figures."""
    имена = [м.group(2) for м in _ДЫРА.finditer(шаблон)]
    словами = all(м.group(1) for м in _ДЫРА.finditer(шаблон))
    if len(имена) != 3:
        return None
    порядок = tuple(имена)
    if порядок == ("n", "m", "sum"):
        return "+", словами
    if порядок == ("sum", "m", "n"):
        return "−", словами
    if порядок == ("n", "m", "prod"):
        return "×", словами
    if порядок == ("prod", "m", "n"):
        return "÷", словами
    return None


def шаблоны(язык):
    """{(operation, in words): template} — the pack's own table."""
    вон = {}
    род = (ПАКЕТЫ_ВСЕ[язык].get("show_kinds") or {}).get("arithmetic") or {}
    for ш in род.get("templates") or ():
        в = _вид(ш)
        if в is not None and в not in вон:
            вон[в] = ш
    return вон


ЯЗЫКИ = {л: ш for л, ш in ((л, шаблоны(л)) for л in ПАКЕТЫ_ВСЕ) if len(ш) >= 4}
ЧИСЛА = {л: числительные(л) for л in ЯЗЫКИ}


def умеет(язык, оп, словами=True):
    """Does the pack declare THIS operation in THIS writing? A chain never
    mixes the two writings — «6 + 5 = 11。 十一减三等于八。» is no chain of one
    house, and a language whose figures say only addition says none."""
    return (оп, словами) in ЯЗЫКИ[язык]


def шаг(язык, оп, a, b, r, словами=True):
    """One declared equality with its numbers in place: a op b = r, where the
    template decides which hole holds which number."""
    ш = ЯЗЫКИ[язык][(оп, словами)]
    т = ЧИСЛА[язык]
    пиши = (lambda x: т[x]) if all(м.group(1) for м in _ДЫРА.finditer(ш)) else str
    з = {"+": {"n": a, "m": b, "sum": r}, "−": {"sum": a, "m": b, "n": r},
         "×": {"n": a, "m": b, "prod": r}, "÷": {"prod": a, "m": b, "n": r}}[оп]
    return _ДЫРА.sub(lambda м: пиши(з[м.group(2)]), ш)


def цепь(язык, шаги, словами=True):
    """«6 + 5 = 11. 11 − 3 = 8.» — the steps in a row, the seam between them
    the number itself: шаги = ((op, a, b, r), …)."""
    return " ".join(шаг(язык, оп, a, b, r, словами) for оп, a, b, r in шаги)


def годно(язык, значения, словами=True):
    """Are all the numbers sayable in this language (the pack's numerals)?"""
    if not словами:
        return True
    т = ЧИСЛА[язык]
    return all(з in т for з in значения)


def _счёт(оп, a, b):
    if оп == "+":
        return a + b
    if оп == "−":
        return a - b
    if оп == "×":
        return a * b
    return a // b if b and a % b == 0 else None


def цепи(язык, словами=True):
    """The chains this language can say: two steps, the seam a number of the
    pack; built from the declared numerals only."""
    if not (умеет(язык, "+", словами) and умеет(язык, "−", словами)):
        return []
    т = sorted(ЧИСЛА[язык]) if словами else list(range(2, 40))
    вон = []
    for a in т:
        for b in т:
            if b < 1 or a < 1:
                continue
            s = a + b
            if s not in т and словами:
                continue
            for c in т:
                if c < 1 or c >= s:
                    continue
                r = s - c
                if словами and r not in т:
                    continue
                вон.append((("+", a, b, s), ("−", s, c, r)))
    return вон


# --- the court's side ---
def _образец(язык, ш):
    """The template as a pattern: every hole a group of the language's numbers."""
    т = ЧИСЛА[язык]
    словами = all(м.group(1) for м in _ДЫРА.finditer(ш))
    дыра = ("(" + "|".join(re.escape(с) for с in sorted(set(т.values()), key=len, reverse=True)) + ")") if словами else r"(\d+)"
    куски, конец = [], 0
    for м in _ДЫРА.finditer(ш):
        куски.append(re.escape(ш[конец:м.start()])); куски.append(дыра); конец = м.end()
    куски.append(re.escape(ш[конец:]))
    return "".join(куски)


def образцы(язык):
    """[(pattern of one step, operation, hole order, in words)] — the pack's table."""
    вон = []
    for (оп, словами), ш in ЯЗЫКИ[язык].items():
        имена = [м.group(2) for м in _ДЫРА.finditer(ш)]
        вон.append((re.compile(_образец(язык, ш)), оп, имена, словами))
    return вон


ОБРАЗЦЫ = {л: образцы(л) for л in ЯЗЫКИ}
_ПО_СЛОВУ = {л: {с: з for з, с in ЧИСЛА[л].items()} for л in ЯЗЫКИ}


def разобрать_шаг(язык, кусок):
    """(operation, a, b, r) of one declared equality, or None."""
    for образец, оп, имена, словами in ОБРАЗЦЫ[язык]:
        м = образец.fullmatch(кусок.strip())
        if not м:
            continue
        читать = (lambda с: _ПО_СЛОВУ[язык].get(с)) if словами else (lambda с: int(с))
        з = {}
        for имя, г in zip(имена, м.groups()):
            v = читать(г)
            if v is None:
                return None
            з[имя] = v
        if оп == "+":
            return оп, з["n"], з["m"], з["sum"]
        if оп == "−":
            return оп, з["sum"], з["m"], з["n"]
        if оп == "×":
            return оп, з["n"], з["m"], з["prod"]
        return оп, з["prod"], з["m"], з["n"]
    return None


def _куски(строка):
    """The steps of a chain: a step ends where its template's own end stands
    («.», «。», «۔»), so the split is by the end mark plus a space."""
    return [к for к in re.split(r"(?<=[.。۔?؟!]) ", строка.strip()) if к.strip()]


def судить(строка):
    """(судимо, истинно): a chain of two or more declared equalities whose
    seam holds and whose every step counts."""
    с = строка.strip()
    куски = _куски(с)
    if len(куски) < 2:
        return False, False
    for язык in ЯЗЫКИ:
        шаги = [разобрать_шаг(язык, к) for к in куски]
        if any(ш is None for ш in шаги):
            continue
        for оп, a, b, r in шаги:
            if _счёт(оп, a, b) != r:
                return True, False
        # THE SEAM: the result of a step is an operand of the next
        for (о1, a1, b1, r1), (о2, a2, b2, r2) in zip(шаги, шаги[1:]):
            if r1 not in (a2, b2):
                return True, False
        return True, True
    return False, False
