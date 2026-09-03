#!/usr/bin/env python3
"""[ДЕНЬГИ] — цена в центах и её десятичная запись сходятся счётом.

Мир денег (tools/gen_genesis_money.py) считает в центах и копейках — целых
числах одной оси — и показывает десятичную запись цены МОСТОМ с леджером
рядом: «16.50 dollars is 1650 cents: 16 × 100 = 1600, 1600 + 50 = 1650».
Суд читает доллары и центы из десятичной записи сам (d × 100 + c), считает
все звенья леджера и итог; пара «вопрос → ответ» связана домом пары (ответ
открывается первой величиной вопроса). Русские формы копейки и рубля — по
дому форм; имена — из пакетов.
"""
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
import families  # noqa: E402
import rugram  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛОЖНЫХ_РУБЕЖ = 0
ЛОЖНЫХ_РУБЕЖ = 0

_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
ИМЕНА_EN = frozenset(_EN["person_names"])
ИМЕНА_RU = {n.capitalize(): ф["gender"] for n, ф in _RU["person_forms"].items()}
Ч = r"(\d+)"
Д = r"(\d+)\.(\d\d)"
# a price in either writing: «16.50 dollars» or «$16.50» — two number groups either way
ДЛ = r"(?:\$(\d+)\.(\d\d)|(\d+)\.(\d\d) dollars)"
# THE THING IS ONE OF THE WORLD'S DECLARED THINGS (mutation 04.09: «a penci
# costs 295 cents» passed — the thing was any word): the closed set comes
# from the generator's table, singular and plural.
import gen_genesis_money as _дом
С = "(" + "|".join(sorted({ф for в in _дом.ВЕЩИ for ф in в[:2]} | set(_дом.ИМЕНА_EN), key=len, reverse=True)) + ")"
СЛ = r"([а-яё]+)"


def _коп(n, слово):
    """The counted form of a kopeck/rouble word agrees with its number."""
    return слово in (rugram.форма("копейка", n), rugram.форма("рубль", n))


def _мост(d, c, всего, d2, s100, s100b, c2, всего2):
    return (всего == d * 100 + c and d2 == d and s100 == s100b == d * 100 and c2 == c and всего2 == всего)


ОБРАЗЦЫ = (
    (rf"^{ДЛ} is {Ч} cents: {Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч}\.$",
     lambda d, c, всего, d2, s1, s2, c2, в2: _мост(d, c, всего, d2, s1, s2, c2, в2)),
    (rf"^how many cents is {ДЛ}\? {Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч} cents\.$",
     lambda d, c, d2, s1, s2, c2, в2: _мост(d, c, в2, d2, s1, s2, c2, в2)),
    (rf"^{Ч} {СЛ} {Ч} {СЛ} — это {Ч} {СЛ}: {Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч}\.$",
     lambda d, р, c, к, всего, к2, d2, s1, s2, c2, в2: _мост(d, c, всего, d2, s1, s2, c2, в2) and _коп(d, р) and _коп(c, к) and _коп(всего, к2)),
    (rf"^сколько копеек составляют {Ч} {СЛ} {Ч} {СЛ}\? {Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч} {СЛ}\.$",
     lambda d, р, c, к, d2, s1, s2, c2, в2, к2: _мост(d, c, в2, d2, s1, s2, c2, в2) and _коп(d, р) and _коп(c, к) and _коп(в2, к2)),
    (rf"^{Ч} cents is (?:\$(\d+)\.(\d\d)|(\d+) dollars (\d+) cents): {Ч} × 100 = {Ч}, {Ч} − {Ч} = {Ч}\.$",
     lambda всего, d, c, d2, s1, в2, s2, c2: всего == d * 100 + c and d2 == d and s1 == s2 == d * 100 and в2 == всего and c2 == c),
    (rf"^a {С} costs {Ч} cents and a {С} costs {Ч} cents; together they cost {Ч} cents: {Ч} \+ {Ч} = {Ч}\.$",
     lambda т1, p1, т2, p2, s, o1, o2, s2: (o1, o2) == (p1, p2) and s == s2 == p1 + p2),
    (rf"^a {С} costs {Ч} cents and a {С} costs {Ч} cents\. how much do they cost together\? {Ч} \+ {Ч} = {Ч} cents\.$",
     lambda т1, p1, т2, p2, o1, o2, s2: (o1, o2) == (p1, p2) and s2 == p1 + p2),
    (rf"^{СЛ} стоит {Ч} {СЛ}, а {СЛ} стоит {Ч} {СЛ}; вместе они стоят {Ч} {СЛ}: {Ч} \+ {Ч} = {Ч}\.$",
     lambda т1, p1, к1, т2, p2, к2, s, к3, o1, o2, s2: (o1, o2) == (p1, p2) and s == s2 == p1 + p2 and _коп(p1, к1) and _коп(p2, к2) and _коп(s, к3)),
    (rf"^{СЛ} стоит {Ч} {СЛ}, а {СЛ} стоит {Ч} {СЛ}\. сколько они стоят вместе\? {Ч} \+ {Ч} = {Ч} {СЛ}\.$",
     lambda т1, p1, к1, т2, p2, к2, o1, o2, s2, к3: (o1, o2) == (p1, p2) and s2 == p1 + p2 and _коп(p1, к1) and _коп(p2, к2) and _коп(s2, к3)),
    (rf"^a {С} costs {Ч} cents\. how much do {Ч} {С} cost\? {Ч} × {Ч} = {Ч} cents\.$",
     lambda т, p, k, тs, o1, o2, s: (o1, o2) == (p, k) and s == p * k),
    (rf"^a {С} costs {Ч} cents; {Ч} {С} cost {Ч} cents: {Ч} × {Ч} = {Ч}\.$",
     lambda т, p, k, тs, s, o1, o2, s2: (o1, o2) == (p, k) and s == s2 == p * k),
    # БЕЗ ОБРАТНЫХ ССЫЛОК: семейство сливает образцы в одно перечисление, и «\1»
    # указывало бы на чужую группу — имя ловится дважды и сверяется судьёй
    (rf"^{С} paid {Ч} cents for a {С} that costs {Ч} cents; {С} got {Ч} cents change: {Ч} − {Ч} = {Ч}\.$",
     lambda имя, paid, т, p, имя2, сд, o1, o2, сд2: имя in ИМЕНА_EN and имя2 == имя and (o1, o2) == (paid, p) and сд == сд2 == paid - p > 0),
    (rf"^{С} paid {Ч} cents for a {С} that costs {Ч} cents\. how much change did {С} get\? {Ч} − {Ч} = {Ч} cents\.$",
     lambda имя, paid, т, p, имя2, o1, o2, сд2: имя in ИМЕНА_EN and имя2 == имя and (o1, o2) == (paid, p) and сд2 == paid - p > 0),
    (rf"^([А-ЯЁ][а-яё]+) (заплатил|заплатила) {Ч} {СЛ}, а {СЛ} стоила {Ч} {СЛ}; сдача — {Ч} {СЛ}: {Ч} − {Ч} = {Ч}\.$",
     lambda имя, г, paid, к1, т, p, к2, сд, к3, o1, o2, сд2: имя in ИМЕНА_RU and (г == "заплатила") == (ИМЕНА_RU[имя] == "f") and (o1, o2) == (paid, p) and сд == сд2 == paid - p > 0 and _коп(paid, к1) and _коп(p, к2) and _коп(сд, к3)),
    (rf"^([А-ЯЁ][а-яё]+) (заплатил|заплатила) {Ч} {СЛ}, а {СЛ} стоила {Ч} {СЛ}\. сколько сдачи (получил|получила) ([А-ЯЁ][а-яё]+)\? {Ч} − {Ч} = {Ч} {СЛ}\.$",
     lambda имя, г, paid, к1, т, p, к2, г2, имя2, o1, o2, сд2, к3: имя in ИМЕНА_RU and имя2 == имя and (г == "заплатила") == (г2 == "получила") == (ИМЕНА_RU[имя] == "f") and (o1, o2) == (paid, p) and сд2 == paid - p > 0 and _коп(paid, к1) and _коп(p, к2) and _коп(сд2, к3)),
    (rf"^{ДЛ} \+ {ДЛ} = {ДЛ}: {Ч} \+ {Ч} = {Ч} cents\.$",
     lambda a, ac, b, bc, s, sc, A, B, S: A == a * 100 + ac and B == b * 100 + bc and S == A + B == s * 100 + sc),
    (rf"^how much is {ДЛ} \+ {ДЛ}\? {ДЛ} \+ {ДЛ} = {ДЛ}: {Ч} \+ {Ч} = {Ч} cents\.$",
     lambda a, ac, b, bc, a2, ac2, b2, bc2, s, sc, A, B, S: (a2, ac2, b2, bc2) == (a, ac, b, bc) and A == a * 100 + ac and B == b * 100 + bc and S == A + B == s * 100 + sc),
)


def _г(m):
    return [int(x) if re.fullmatch(r"\d+", x) else x for x in m.groups() if x is not None]


def _судья(закон):
    def судить_(м):
        try:
            return bool(закон(*_г(м)))
        except (TypeError, ValueError):
            return False
    return судить_


# СЕМЕЙСТВО ЕСТЬ РОД (М-146): утверждение и вопрос одного рода — один якорный
# образец на язык; вердикт даёт совпавшая форма.
_Ф = [(о, _судья(п)) for о, п in ОБРАЗЦЫ]
СЕМЕЙСТВА = (
    ("мост", _Ф[0:5]),
    ("цены", _Ф[5:9]),
    ("кратные", _Ф[9:11]),
    ("сдача", _Ф[11:15]),
    ("суммы", _Ф[15:17]),
)
ПРАВИЛА = families.правила(СЕМЕЙСТВА)
# THE SAME SHAPES WITH ANY WORD FOR A THING OR A NAME: a line of this shape
# that the closed rules do not take names a thing or a person the world did
# not declare — a lie, not silence (mutation 04.09: «a penci costs 295
# cents» fell to the count court and passed).
def _открыть(о):
    """The pattern with any word where a thing, a name or a unit form stands."""
    о = о.replace(С, r"(?:[a-zа-яё]+(?: [a-zа-яё]+)?)")
    о = о.replace("dollars", "dollars?").replace("cents", "cents?")
    return re.compile(о)


ОТКРЫТЫЕ = tuple(_открыть(о) for о, _ in ОБРАЗЦЫ)
# the Russian thing of this world stands as the SUBJECT («книга стоит») — the
# lemma, not any count form («книг стоит» — mutation 04.09)
ВЕЩИ_RU = frozenset(в[2] for в in _дом.ВЕЩИ)


import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — the palata hands the world's name
# THE WORLD IS CLOSED: every honest line of «money» is a shape of this court
# (measured 04.09), so a line of it this court does not recognise is a lie.
ЗАМКНУТЫЕ_МИРЫ = frozenset({"money"})


def _судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    for образец, судья in ПРАВИЛА:
        m = образец.match(с)
        if m:
            # ПАРА О ТОМ ЖЕ (дом пары, М-145): ответ открывается первой величиной вопроса
            пара = asking.пара(с)
            if пара and not asking.о_том_же(пара[0], пара[1]):
                return True, False
            # A RUSSIAN THING IS ONE OF THE WORLD'S DECLARED THINGS (mutation 04.09:
            # «ручк стоит 190 копеек» passed — the Russian slot took any word).
            for г in m.groups():
                if (г and re.fullmatch(r"[а-яё]+", г) and not г.startswith(("копе", "рубл"))
                        and г not in ВЕЩИ_RU and г not in ("заплатил", "заплатила", "получил", "получила")):
                    return True, False
            return True, bool(судья(m))
    if any(о.match(с) for о in ОТКРЫТЫЕ):
        return True, False
    return False, False



судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)

def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_money.txt":
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
    print(f"ДЕНЬГИ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
