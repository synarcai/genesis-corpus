#!/usr/bin/env python3
"""THE HOUSE OF HOLDINGS WITHOUT A VERB — the first show «only by frames» (05.09).

The owner's word (through holon): stop the small laws, prototype ONE BEARER — a story read
only by frames, one relation of the executor, a certificate. The first worlds such a reader
must buy are the plainest: a bearer holds a number of things and is asked how many; a
person has an age and is asked how old; two bearers hold two numbers and the question names
the second; a bearer holds none. No act, no ledger, no arithmetic: the answer is the story's
own number said back in a full sentence — the voice of the page (holon: a holding verb
becomes a HOLDING verb only when the answer is a sentence whose number folds to the story
by one choice, here by no choice at all).

WHAT THE HOUSE DECLARES AND WHAT IT BORROWS. Nine languages; bearers are the packs' persons
(the action-pages house declares them with gender and genitive; the Russian dative comes
from the pack's person_forms, the Polish dative and the Portuguese article from the SVAMP
house — one declaration, several readers); things are the action-pages things with their
count forms by the pack's agreement rule; the year bends by the number-line house's table;
the zero is the pack's numeral. Numbers run 1..40 — a wide row, not a table of eight pairs:
the goal is the VOLUME of frames, and the world is cut across the passes by the layer.

THE JUDGE IS THE FRAME ITSELF. A page is a frame whose holes are filled by declared
alternations; every hole that stands twice in the frame (the bearer of the question is the
bearer of the story, the answer's number is the story's, the answer's thing is the story's)
must carry the same value in both places; the count form must be the form of its number,
the year the form of its age, the question word the gender of the thing. The world is
CLOSED: a line the house does not recognise is a lie of the world, not a silence.

WHAT IS NOT MEASURED, NAMED: whether the reader can add or subtract — nothing here computes;
this world asks only whether a frame is READ, which is the prototype's first question.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as A  # noqa: E402
import numberline as N  # noqa: E402
import svampforms as S  # noqa: E402 — dative and article of the bearer, gender of the thing

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ВЕРХ = 40                      # the row of numbers the house walks: 1..40

РАМКИ = {
    "ru": dict(держание="у {Xр} {n} {Тn}. сколько {Тмн} у {Xр}? у {Xр} {n} {Тn}.",
               возраст="{Xд} {n} {Гn}. сколько лет {Xд}? {Xд} {n} {Гn}.",
               двое="у {Xр} {n} {Тn}, а у {Yр} {k} {Тk}. сколько {Тмн} у {Yр}? у {Yр} {k} {Тk}.",
               нет="у {Xр} нет {Тмн}. сколько {Тмн} у {Xр}? {ноль}: у {Xр} нет {Тмн}."),
    "en": dict(держание="{X} has {n} {Тn}. how many {Тмн} does {X} have? {X} has {n} {Тn}.",
               возраст="{X} is {n} {Гn} old. how old is {X}? {X} is {n} {Гn} old.",
               двое="{X} has {n} {Тn} and {Y} has {k} {Тk}. how many {Тмн} does {Y} have? {Y} has {k} {Тk}.",
               нет="{X} has no {Тмн}. how many {Тмн} does {X} have? {ноль}: {X} has no {Тмн}."),
    "de": dict(держание="{X} hat {n} {Тn}. wie viele {Тмн} hat {X}? {X} hat {n} {Тn}.",
               возраст="{X} ist {n} {Гn} alt. wie alt ist {X}? {X} ist {n} {Гn} alt.",
               двое="{X} hat {n} {Тn} und {Y} hat {k} {Тk}. wie viele {Тмн} hat {Y}? {Y} hat {k} {Тk}.",
               нет="{X} hat keine {Тмн}. wie viele {Тмн} hat {X}? {ноль}: {X} hat keine {Тмн}."),
    "fr": dict(держание="{X} a {n} {Тn}. combien de {Тмн} a {X} ? {X} a {n} {Тn}.",
               возраст="{X} a {n} {Гn}. quel âge a {X} ? {X} a {n} {Гn}.",
               двое="{X} a {n} {Тn} et {Y} a {k} {Тk}. combien de {Тмн} a {Y} ? {Y} a {k} {Тk}.",
               нет="{X} n'a pas de {Тмн}. combien de {Тмн} a {X} ? {ноль} : {X} n'a pas de {Тмн}."),
    "es": dict(держание="{X} tiene {n} {Тn}. ¿{кск} {Тмн} tiene {X}? {X} tiene {n} {Тn}.",
               возраст="{X} tiene {n} {Гn}. ¿cuántos años tiene {X}? {X} tiene {n} {Гn}.",
               двое="{X} tiene {n} {Тn} y {Y} tiene {k} {Тk}. ¿{кск} {Тмн} tiene {Y}? {Y} tiene {k} {Тk}.",
               нет="{X} no tiene {Тмн}. ¿{кск} {Тмн} tiene {X}? {ноль}: {X} no tiene {Тмн}."),
    "it": dict(держание="{X} ha {n} {Тn}. {quante} {Тмн} ha {X}? {X} ha {n} {Тn}.",
               возраст="{X} ha {n} {Гn}. quanti anni ha {X}? {X} ha {n} {Гn}.",
               двое="{X} ha {n} {Тn} e {Y} ha {k} {Тk}. {quante} {Тмн} ha {Y}? {Y} ha {k} {Тk}.",
               нет="{X} non ha {Тмн}. {quante} {Тмн} ha {X}? {ноль}: {X} non ha {Тмн}."),
    "pt": dict(держание="{X} tem {n} {Тn}. {quantas} {Тмн} tem {X}? {X} tem {n} {Тn}.",
               возраст="{X} tem {n} {Гn}. quantos anos tem {X}? {X} tem {n} {Гn}.",
               двое="{X} tem {n} {Тn} e {Y} tem {k} {Тk}. {quantas} {Тмн} tem {Y}? {Y} tem {k} {Тk}.",
               нет="{X} não tem {Тмн}. {quantas} {Тмн} tem {X}? {ноль}: {X} não tem {Тмн}."),
    "nl": dict(держание="{X} heeft {n} {Тn}. hoeveel {Тмн} heeft {X}? {X} heeft {n} {Тn}.",
               возраст="{X} is {n} {Гn} oud. hoe oud is {X}? {X} is {n} {Гn} oud.",
               двое="{X} heeft {n} {Тn} en {Y} heeft {k} {Тk}. hoeveel {Тмн} heeft {Y}? {Y} heeft {k} {Тk}.",
               нет="{X} heeft geen {Тмн}. hoeveel {Тмн} heeft {X}? {ноль}: {X} heeft geen {Тмн}."),
    "pl": dict(держание="{X} ma {n} {Тn}. ile {Тмн} ma {X}? {X} ma {n} {Тn}.",
               возраст="{X} ma {n} {Гn}. ile lat ma {X}? {X} ma {n} {Гn}.",
               двое="{X} ma {n} {Тn}, a {Y} ma {k} {Тk}. ile {Тмн} ma {Y}? {Y} ma {k} {Тk}.",
               нет="{X} nie ma {Тмн}. ile {Тмн} ma {X}? {ноль}: {X} nie ma {Тмн}."),
}
ФОРМЫ = ("держание", "возраст", "двое", "нет")
# THE SINGULAR IS FOR ONE ALONE in these languages («21 ans», «21 años», «21 anni», «21 anos»,
# «21 years»); a pack whose agreement rule bends 11/21/31 to the singular is wrong there, and
# the house does not write what the pack bends wrong: those ages are a DECLARED SEAM until the
# pack is corrected (the Polish rule was cured the same way, fa0db99). Nothing is skipped once
# the pack says «one» for 1 alone — the seam is read from the table, not from a list of numbers.
ЕДИНИЦА_ТОЛЬКО_ОДИН = frozenset({"en", "de", "fr", "es", "it", "pt", "nl"})


def _пакет(язык):
    return json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))


# THE ZERO IS THE PACK'S NUMERAL («ноль», «zero», «null», «zéro», «cero», «nul») — read, not declared here
НОЛЬ = {язык: str((_пакет(язык).get("numerals") or {}).get("0")) for язык in ЯЗЫКИ}
for _яз, _н in НОЛЬ.items():
    assert _н and _н != "None", (_яз, "the pack declares no zero")


def _дательный(язык, лицо):
    """The dative of the bearer where the language bends it («Ане», «Annie», «à Ana»)."""
    if язык == "ru":
        return S._дательный(лицо[0]) or лицо[0]
    if язык == "pl":
        return S.ДАТЕЛЬНЫЙ_PL.get(лицо[0], лицо[0])
    if язык == "pt":
        return S._дательный_pt(лицо)
    return лицо[0]


def _поля(язык, i, j, Т, n, k):
    X, Y = S._лицо(язык, i), S._лицо(язык, j)
    if Y[0] == X[0]:
        Y = S._лицо(язык, j + 1)
    вещь = lambda c: A._вещь(язык, Т, c)
    п = dict(X=X[0], Xр=X[2], Xд=_дательный(язык, X), Y=Y[0], Yр=Y[2],
             n=n, k=k, Тn=вещь(n), Тk=вещь(k), Тмн=вещь(5), Гn=N.год(язык, n), ноль=НОЛЬ[язык])
    род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(вещь(5), "f")
    for дыра, (м_, ж_) in S.РОДОВЫЕ.get(язык, {}).items():
        п[дыра] = м_ if род == "m" else ж_
    return п


def страница(язык, форма, i, j, Т, n, k=None):
    return РАМКИ[язык][форма].format(**_поля(язык, i, j, Т, n, k if k is not None else n))


def _пара(n):
    """The second bearer's number: never the first one's."""
    k = (n * 7 + 3) % ВЕРХ + 1
    return k if k != n else k % ВЕРХ + 1


def _год_согнут(язык, n):
    """True where the pack bends the year of n to the singular in a language that keeps it for 1
    alone; a year that never bends («jaar») is never bent."""
    один, два = N.год(язык, 1), N.год(язык, 2)
    return язык in ЕДИНИЦА_ТОЛЬКО_ОДИН and n != 1 and один != два and N.год(язык, n) == один


ШОВ_ГОДА = {язык: [n for n in range(1, ВЕРХ + 1) if _год_согнут(язык, n)] for язык in ЯЗЫКИ}


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        лиц, вещей = len(A.ЛИЦА[язык]), len(A.ЯЗЫКИ[язык]["вещи"])
        for n in range(1, ВЕРХ + 1):
            for i, Т in ((n % лиц, n % вещей), ((n * 3 + 1) % лиц, (n * 5 + 2) % вещей), ((n * 7 + 2) % лиц, (n * 3 + 1) % вещей)):
                вон[страница(язык, "держание", i, i + 1, Т, n)] = (язык, "держание")
            if not _год_согнут(язык, n):
                for i in (n % лиц, (n * 3 + 1) % лиц):
                    вон[страница(язык, "возраст", i, i + 1, 0, n)] = (язык, "возраст")
            for i, Т in ((n % лиц, (n * 5 + 1) % вещей), ((n * 5 + 3) % лиц, n % вещей)):
                вон[страница(язык, "двое", i, i + 3, Т, n, _пара(n))] = (язык, "двое")
        for i in range(лиц):
            for Т in range(вещей):
                вон[страница(язык, "нет", i, i + 1, Т, 1)] = (язык, "нет")
    return вон


ПОКАЗЫ = _показы()


def _формы_вещей(язык):
    """form of a thing → the things wearing it (a form may belong to several things' rows)."""
    вон = {}
    for Т in range(len(A.ЯЗЫКИ[язык]["вещи"])):
        for c in range(0, ВЕРХ + 2):
            вон.setdefault(A._вещь(язык, Т, c), set()).add(Т)
    return вон


ФОРМЫ_ВЕЩЕЙ = {язык: _формы_вещей(язык) for язык in ЯЗЫКИ}
ГОДЫ = {язык: {N.год(язык, c) for c in range(0, ВЕРХ + 2)} for язык in ЯЗЫКИ}
_ДЫРА = re.compile(r"\{([^}]+)\}")


def _образец(язык, рамка):
    """One pattern over the whole page; the i-th occurrence of a hole is the group «hole__i»."""
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=len, reverse=True)) + ")"
    лица = [S._лицо(язык, i) for i in range(len(A.ЛИЦА[язык]))]
    имена = alt(л[0] for л in лица); род = alt(л[2] for л in лица); дат = alt(_дательный(язык, л) for л in лица)
    вещи = alt(ФОРМЫ_ВЕЩЕЙ[язык]); годы = alt(ГОДЫ[язык])
    дыры = {"X": имена, "Y": имена, "Xр": род, "Yр": род, "Xд": дат, "n": r"\d+", "k": r"\d+",
            "Тn": вещи, "Тk": вещи, "Тмн": вещи, "Гn": годы, "ноль": re.escape(НОЛЬ[язык])}
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        дыры[дыра] = alt(пара)
    счёт = {}
    куски = []
    for кусок in re.split(r"(\{[^}]+\})", рамка):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<{_имя(дыра)}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _имя(дыра):
    """Group names must be identifiers: Cyrillic is fine, «р»/«д» suffixes too."""
    return "h_" + дыра


ОБРАЗЦЫ = [(_образец(язык, рамка), язык, форма) for язык, рамки in РАМКИ.items() for форма, рамка in рамки.items()]


def _вердикт(язык, форма, м):
    """Every hole repeated in the frame carries one value; forms are the forms of their numbers."""
    значения = {}
    for ключ, v in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in значения and значения[дыра] != v:
            return False
        значения[дыра] = v
    n = int(значения["n"]) if "n" in значения else None
    if "Тn" in значения and not any(A._вещь(язык, Т, n) == значения["Тn"] for Т in ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], ())):
        return False
    if "Тk" in значения:
        k = int(значения["k"])
        if not any(A._вещь(язык, Т, k) == значения["Тk"] for Т in ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тk"], ())):
            return False
        # the two bearers' things are the same thing (Тмн is the plural of Тn and Тk)
        общие = ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тk"], set())
        if not общие:
            return False
    if "Тмн" in значения and "Тn" in значения:
        if not (ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тмн"], set()) & ФОРМЫ_ВЕЩЕЙ[язык].get(значения["Тn"], set())):
            return False
    if "Гn" in значения and N.год(язык, n) != значения["Гn"]:
        return False
    if форма in ("держание", "двое", "нет", "возраст") and n is not None and not (1 <= n <= ВЕРХ):
        return False
    for дыра, пара in S.РОДОВЫЕ.get(язык, {}).items():
        if дыра in значения and "Тмн" in значения:
            род = S.РОД_ВЕЩЕЙ.get(язык, {}).get(значения["Тмн"], "f")
            if значения[дыра] != (пара[0] if род == "m" else пара[1]):
                return False
    return True


def судить(строка):
    """(судимо, истинно): a page of a frame of the house, and its holes agree; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if м:
            return True, _вердикт(язык, форма, м)
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        д = страница(язык, "держание", 0, 1, 0, 12)
        # the answer's number is not the story's
        битая = re.sub(r"(\d+)(?=[^\d]*$)", lambda м: str(int(м.group(1)) + 1), д)
        assert судить(битая) == (True, False), битая
        # a foreign bearer is not a page of the house — silence here, a lie at the closed world's gate
        X = S._лицо(язык, 0)
        чужая = next(д.replace(ф, "Zorbo") for ф in (X[0], X[2], _дательный(язык, X)) if ф in д)
        assert судить(чужая) == (False, False), чужая
        # the second bearer's question answered with the first bearer's number
        дв = страница(язык, "двое", 0, 3, 0, 12, 5)
        assert судить(дв) == (True, True), дв
        assert судить(re.sub(r"(\d+)(?=[^\d]*$)", "12", дв)) == (True, False), дв
        # the age with the wrong form of the year (where the language bends the year)
        в = страница(язык, "возраст", 0, 1, 0, 12)
        for c in (1, 2):
            иная = N.год(язык, c)
            if иная != N.год(язык, 12):
                assert судить(в[:v_last(в)] + в[v_last(в):].replace(N.год(язык, 12), иная, 1)) == (True, False), в
                мутанты += 1
                break
        # «none» answered with a number is not a page of the house
        н = страница(язык, "нет", 0, 1, 0, 1)
        assert судить(н) == (True, True), н
        assert судить(н[:v_last(н)] + н[v_last(н):].replace(НОЛЬ[язык], "3", 1)) == (False, False), н
        мутанты += 4
    print("  ", страница("ru", "держание", 1, 2, 1, 3))
    print("  ", страница("ru", "возраст", 1, 2, 0, 22))
    print("  ", страница("en", "двое", 0, 3, 2, 12, 5))
    print("  ", страница("pl", "нет", 1, 2, 0, 1))
    print("  ", страница("pt", "возраст", 1, 2, 0, 28))
    print(f"  мутантов поймано: {мутанты}")
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    шов = {я: ч for я, ч in ШОВ_ГОДА.items() if ч}
    if шов:
        print(f"  ШОВ ГОДА (пакет гнёт к единице, дом не пишет): {шов}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


def v_last(с):
    """The start of the answer (after the last question mark)."""
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


if __name__ == "__main__":
    _самопроверка()
