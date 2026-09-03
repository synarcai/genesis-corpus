#!/usr/bin/env python3
"""[MONEY WITH THE DECIMAL COMMA COURT] — every writing is recomputed in cents.

A line of the money_langs world is one of four shapes in one of nine
languages: the bridge («16,50 Euro sind 1650 Cent: 16 × 100 = 1600, 1600 +
50 = 1650.»), the question of the small unit, the way back («1650 Cent sind
16,50 Euro: 16 × 100 = 1600, 1650 − 1600 = 50.») and the sum («7,10 Euro +
4,40 Euro = 11,50 Euro: 710 + 440 = 1150 Cent.»). The court reads the
units, copulas and questions from the house of money writings, reads the
decimal writing as (whole, cents) with exactly two digits of cents, and
recomputes every link and every count form; nothing is looked up from the
line.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import moneyforms as M  # noqa: E402

Ч = r"(\d+)"
Д = r"(\d+),(\d\d)"


def _alt(формы):
    return "(?:" + "|".join(re.escape(ф) for ф in sorted(set(формы), key=len, reverse=True)) + ")"


def _образцы(язык):
    я = M.ЯЗЫКИ[язык]
    б = _alt(я["б"])
    м = _alt(я["м"] if язык != "ru" else ("копейка", "копейки", "копеек"))
    дв = re.escape(я["дв"])
    если = " " + re.escape(я["есть"]) if я["есть"] else ""
    if язык == "tr":
        мост = rf"^{Д} lira {Ч} kuruştur{дв}{Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч}\.$"
        вопрос = rf"^{Д} lira kaç kuruştur\? {Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч} kuruş\.$"
        обратно = rf"^{Ч} kuruş {Д} liradır{дв}{Ч} × 100 = {Ч}, {Ч} − {Ч} = {Ч}\.$"
    else:
        вопрос_форма = re.escape(я["вопрос"]).replace(r"\{м\}", м).replace(r"\{б\}", rf"{Д} {б}")
        мост = rf"^{Д} {б}{если} {Ч} {м}{дв}{Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч}\.$"
        вопрос = rf"^{вопрос_форма} {Ч} × 100 = {Ч}, {Ч} \+ {Ч} = {Ч} {м}\.$"
        обратно = rf"^{Ч} {м}{если} {Д} {б}{дв}{Ч} × 100 = {Ч}, {Ч} − {Ч} = {Ч}\.$"
    сумма = rf"^{Д} {б} \+ {Д} {б} = {Д} {б}{дв}{Ч} \+ {Ч} = {Ч} {м}\.$"
    курс = "^" + re.escape(M.КУРС[язык]) + "$"
    return [(re.compile(мост), "мост"), (re.compile(вопрос), "вопрос"), (re.compile(обратно), "обратно"), (re.compile(сумма), "сумма"), (re.compile(курс), "курс")]


ПРАВИЛА = {язык: _образцы(язык) for язык in M.ЯЗЫКИ}


def _мелкая_верна(язык, n, строка):
    """The count form of the small unit beside n is the house's."""
    return f"{n} " + M.мелкая(язык, n).split(" ", 1)[1] in строка


def _судья(язык, вид, м, строка):
    if вид == "курс":
        return True                     # the declared sentence, letter for letter
    г = [int(x) for x in м.groups()]
    if вид == "мост":
        d, c, всего, d2, d100, d100b, c2, всего2 = г
        return (всего == d * 100 + c and (d2, d100, d100b, c2, всего2) == (d, d * 100, d * 100, c, всего)
                and _мелкая_верна(язык, всего, строка))
    if вид == "вопрос":
        d, c, d2, d100, d100b, c2, всего = г
        return (d2, d100, d100b, c2, всего) == (d, d * 100, d * 100, c, d * 100 + c)
    if вид == "обратно":
        всего, d, c, d2, d100, всего2, d100b, c2 = г
        return (всего == d * 100 + c and (d2, d100, всего2, d100b, c2) == (d, d * 100, всего, d * 100, c)
                and _мелкая_верна(язык, всего, строка))
    a, ac, b, bc, s, sc, A, B, S = г
    return (A, B) == (a * 100 + ac, b * 100 + bc) and S == A + B and (s, sc) == divmod(S, 100) and _мелкая_верна(язык, S, строка)


def _открытые():
    """The same shapes with any word where a unit or a copula stands: a line of
    such a shape that no closed rule takes names a unit form the house does
    not declare — a lie, not silence («1 рубл = 100 копеек», «5,15 рубл + …»)."""
    вон = []
    for язык, правила in ПРАВИЛА.items():
        я = M.ЯЗЫКИ[язык]
        слова = sorted({ф for ф in я["б"] + (я["м"] if язык != "ru" else ("копейка", "копейки", "копеек", "рубля", "рубль")) if ф}, key=len, reverse=True)
        for образец, _ in правила:
            о = образец.pattern
            for сл in слова:
                о = о.replace(re.escape(сл), r"[^\W\d_]+")
            вон.append(re.compile(о))
    return tuple(вон)


ОТКРЫТЫЕ = _открытые()


def судить(строка):
    с = строка.strip()
    for язык, правила in ПРАВИЛА.items():
        for образец, вид in правила:
            м = образец.match(с)
            if м:
                return True, bool(_судья(язык, вид, м, с))
    if any(о.match(с) for о in ОТКРЫТЫЕ):
        return True, False
    return False, False


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_money_langs.txt":
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
    print(f"ДЕНЬГИ НА ЯЗЫКАХ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
