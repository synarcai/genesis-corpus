#!/usr/bin/env python3
"""THE HOUSE OF ACTION PAGES — a ledger for every countable act, in three languages.

The collegium of a hundred per cent (owner, 03.09; holon's first task):
12 537 lines of the svod answer with a VALUE and no ledger. The reader's
worlds of e9 (heads, aggregate, gsmwide, gsmlex, compare, depletion, verbs,
realverbs, verbal) are computable by nature — «peter had 8 coins. peter
gave 4 coins away. how many coins are left? peter keeps 4 coins.» — but
their form must not change: his markets buy skeletons from those very
lines, and a changed answer would move the canon numbers of every svod. So
the ledger comes as NEW PAGES of the same genera (his own word: «add new
pages, do not rewrite old ones»), the way the world of forms does it.

Five genera, each a chain of primitives, each ≥ 9 pages per language:

  · THE REMAINDER — «peter had 8 coins. peter gave 4 coins away. how many
    coins are left? 8 − 4 = 4. so the answer is 4.»;
  · THE INCREASE — «nick had 9 balls. nick got 2 balls more. how many balls
    does nick have now? 9 + 2 = 11. so the answer is 11.»;
  · THE SHARE THAT WENT — «ida had 70 books. half of the books went. how
    many books are left? 70 ÷ 2 = 35. so the answer is 35.» (the words of
    the fractions come from the house of shares, tools/fracforms.py);
  · THE TWO BEARERS — «elena has 2 children. ava has 3 children. how many
    children do they have together? 2 + 3 = 5. so the answer is 5.»;
  · THE MULTIPLE — «elena has 2 eggs. ben has three times as many eggs as
    elena. how many eggs does ben have? 3 × 2 = 6. so the answer is 6.»

The court reads the page back through the same templates, REGENERATES it
and compares letter by letter.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fracforms  # noqa: E402
import phrases  # noqa: E402
import rugram  # noqa: E402

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
ПАКЕТЫ = КОРЕНЬ / "tools" / "langpacks"


def _лица(язык):
    п = json.loads((ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    формы = п.get("person_forms") or {}
    вон = []
    for имя in п.get("person_names", ()):
        ф = формы.get(имя) or формы.get(имя.capitalize())
        if not ф or ф.get("gender") not in ("m", "f"):
            continue
        показ = имя.capitalize() if язык == "ru" else имя
        род = (ф.get("gen") or "").capitalize() if язык == "ru" else показ
        вон.append((показ, ф["gender"], род))
        if len(вон) == 14:
            break
    return tuple(вон)


ЯЗЫКИ = {
    "en": dict(
        # THE THING AGREES WITH ITS COUNT: «1 coin» / «4 coins» (the pack's own
        # law of number; Russian takes it from the house of forms)
        вещи=(("coin", "coins"), ("ball", "balls"), ("book", "books"), ("card", "cards"),
              ("flower", "flowers"), ("egg", "eggs"), ("pen", "pens"), ("apple", "apples")),
        имел="{X} had {n} {Тn}.", имеет="{X} has {n} {Тn}.",
        отдал="{X} gave {k} {Тk} away.", получил="{X} got {k} {Тk} more.",
        ушло="{Ч} of the {Т} {У}.", ушли=("went", "went"), второй="{Y} has {m} {Т}.",
        кратно="{Y} has {K} as many {Т} as {X}.", кратные={2: "twice", 3: "three times", 4: "four times"},
        воп_ост="how many {Т} are left?", воп_теперь="how many {Т} does {X} have now?",
        воп_вместе="how many {Т} do they have together?", воп_второй="how many {Т} does {Y} have?",
        # e9's profile of muteness (03.09): the whole of a good named by its
        # PLACE and without «in all»; a rate «every day»; a sum said by «they»
        место="there are {n} {Тn} in {П}.", места=("a box", "a garden", "a park", "a room", "a shelf"),
        часть_их="{k} of them are {С}.", свойства=("red", "new", "small", "green", "old"),
        воп_не="how many are not {С}?", воп_остальные="how many of them are not {С}?",
        ставка="{X} {Г} {n} {Тn} every day.", ставки=("collects", "sells", "packs", "counts", "sorts"),
        воп_за="how many {Т} in {k} {Д}?", воп_дней="how many days for {m} {Т}?", дни=("day", "days"),
        вместе_они="{X} has {n} {Тn}. {Y} has {m} {Тm}. together they have {r} {Тr}: {л}",
        ответ="so the answer is {r}.",
    ),
    "ru": dict(
        вещи=("монета", "шар", "книга", "карта", "цветок", "яблоко", "ручка", "чашка"),
        имел="у {Xр} было {n} {Тn}.", имеет="у {Xр} {n} {Тn}.",
        отдал="{X} отдал{а} {k} {Твk}.", получил="{X} получил{а} ещё {k} {Твk}.",
        ушло="{Ч} {Тм} {У}.", ушли=("ушла", "ушли"), второй="у {Yр} {m} {Тm}.",
        кратно="у {Yр} {K} больше {Тм}, чем у {Xр}.", кратные={2: "вдвое", 3: "втрое", 4: "вчетверо"},
        воп_ост="сколько {Тм} осталось?", воп_теперь="сколько {Тм} у {Xр} теперь?",
        воп_вместе="сколько {Тм} у них вместе?", воп_второй="сколько {Тм} у {Yр}?",
        место="в {П} {n} {Тn}.", места=("коробке", "саду", "парке", "комнате", "полке"),
        часть_их="{k} из них {С}.", свойства=("красные", "новые", "маленькие", "зелёные", "старые"),
        воп_не="сколько из них не {С}?", воп_остальные="сколько из них не {С}?",
        ставка="{X} {Г} {n} {Тn} каждый день.", ставки=("собирает", "продаёт", "упаковывает", "считает", "сортирует"),
        воп_за="сколько {Тм} за {k} {Д}?", воп_дней="сколько дней нужно на {m} {Тm}?", дни=("день", "дня", "дней"),
        вместе_они="у {Xр} {n} {Тn}. у {Yр} {m} {Тm}. вместе у них {r} {Тr}: {л}",
        ответ="значит ответ: {r}.",
    ),
    "de": dict(
        вещи=(("Münze", "Münzen"), ("Ball", "Bälle"), ("Buch", "Bücher"), ("Karte", "Karten"),
              ("Blume", "Blumen"), ("Ei", "Eier"), ("Stift", "Stifte"), ("Tasse", "Tassen")),
        имел="{X} hatte {n} {Тn}.", имеет="{X} hat {n} {Тn}.",
        отдал="{X} gab {k} {Тk} weg.", получил="{X} bekam {k} {Тk} mehr.",
        ушло="{Ч} der {Т} {У}.", ушли=("ging weg", "gingen weg"), второй="{Y} hat {m} {Т}.",
        кратно="{Y} hat {K} so viele {Т} wie {X}.", кратные={2: "doppelt", 3: "dreimal", 4: "viermal"},
        воп_ост="wie viele {Т} bleiben übrig?", воп_теперь="wie viele {Т} hat {X} jetzt?",
        воп_вместе="wie viele {Т} haben sie zusammen?", воп_второй="wie viele {Т} hat {Y}?",
        место="es gibt {n} {Тn} in {П}.", места=("einer Kiste", "einem Garten", "einem Park", "einem Zimmer", "einem Regal"),
        часть_их="{k} davon sind {С}.", свойства=("rot", "neu", "klein", "grün", "alt"),
        воп_не="wie viele sind nicht {С}?", воп_остальные="wie viele davon sind nicht {С}?",
        ставка="{X} {Г} jeden Tag {n} {Тn}.", ставки=("sammelt", "verkauft", "packt", "zählt", "sortiert"),
        воп_за="wie viele {Т} in {k} {Д}?", воп_дней="wie viele Tage für {m} {Т}?", дни=("Tag", "Tagen"),
        вместе_они="{X} hat {n} {Тn}. {Y} hat {m} {Тm}. zusammen haben sie {r} {Тr}: {л}",
        ответ="also ist die Antwort {r}.",
    ),
}
ЛИЦА = {л: _лица(л) for л in ЯЗЫКИ}
ФОРМЫ = ("остаток", "прибавка", "доля", "вместе", "кратное", "место", "ставка", "вместе_они")
# the shares that may «go»: the house of shares says their words in every language
ДОЛИ = ((1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (1, 5), (2, 5))


def _вещь(язык, i, n):
    в = ЯЗЫКИ[язык]["вещи"][i]
    if язык == "ru":
        return rugram.форма(в, n)
    один, много = в
    return один if n == 1 else много


def _вещь_вин(язык, i, n):
    """THE THING AFTER A VERB STANDS IN THE ACCUSATIVE WHERE THE COUNT SAYS
    «ONE»: «отдала 1 монету», while «2 монеты» and «5 монет» are the count
    forms themselves. The paradigm is declared (tools/rugram.py), not guessed."""
    if язык != "ru":
        return _вещь(язык, i, n)
    лемма = ЯЗЫКИ[язык]["вещи"][i]
    счётная = rugram.форма(лемма, n)
    пар = rugram.ПАРАДИГМЫ.get(лемма)
    if счётная == rugram.форма(лемма, 1):
        # the count says «one», so the verb wants the accusative; a thing whose
        # paradigm the house has not declared DOES NOT SAY IT (the law of the
        # declared form: no case is ever guessed) — the page is not written
        return пар[3] if пар else None
    return счётная


def _лицо(язык, имя):
    return next(л for л in ЛИЦА[язык] if л[0] == имя)


def _день(язык, k):
    """The word «day» agrees with its count: «1 day» / «4 days», «1 день» /
    «4 дня» / «5 дней», «1 Tag» / «4 Tagen» (the Russian form comes from the
    declared house of count, tools/rugram.py)."""
    формы = ЯЗЫКИ[язык]["дни"]
    if язык == "ru":
        return rugram.форма("день", k)
    return формы[0] if k == 1 else формы[1]


def _а(язык, пол):
    """The Russian past tense bends by gender: «отдал» / «отдала»."""
    return "а" if (язык == "ru" and пол == "f") else ""


def страница(язык, форма, X, Т=0, n=0, k=0, m=0, Y=None, доля=None, кратность=2,
             место=0, свойство=0, глагол_ставки=0, дней=True):
    я = ЯЗЫКИ[язык]
    имя, пол, род = _лицо(язык, X)
    з = dict(X=имя, Xр=род, а=_а(язык, пол))
    if Y is not None:
        имяY, полY, родY = _лицо(язык, Y)
        з.update(Y=имяY, Yр=родY)
    def вещь(сколько):
        return _вещь(язык, Т, сколько)
    вин = _вещь_вин(язык, Т, k)
    if форма in ("остаток", "прибавка") and вин is None:
        raise ValueError("форма вещи не объявлена")   # the page is not written
    общ = dict(з, Т=вещь(2), Тn=вещь(n), Тk=вещь(k), Тm=вещь(m), Тм=вещь(5), Твk=вин)
    if форма == "вместе_они" and Y is None:
        raise ValueError("второй носитель не назван")
    if форма == "остаток":
        r = n - k
        факт = я["имел"].format(**общ, n=n) + " " + я["отдал"].format(**общ, k=k)
        воп = я["воп_ост"].format(**общ)
        леджер = f"{n} − {k} = {r}."
    elif форма == "прибавка":
        r = n + k
        факт = я["имел"].format(**общ, n=n) + " " + я["получил"].format(**общ, k=k)
        воп = я["воп_теперь"].format(**общ)
        леджер = f"{n} + {k} = {r}."
    elif форма == "доля":
        чс, зн = доля
        ушло_ = n * чс // зн
        r = n - ушло_
        слово = fracforms.доля_слово(язык, чс, зн)
        факт = я["имел"].format(**общ, n=n) + " " + я["ушло"].format(**общ, Ч=слово, У=я["ушли"][0 if чс == 1 else 1])
        воп = я["воп_ост"].format(**общ)
        леджер = (f"{n} ÷ {зн} = {n // зн}, {n // зн} × {чс} = {ушло_}, {n} − {ушло_} = {r}."
                  if чс > 1 else f"{n} ÷ {зн} = {ушло_}, {n} − {ушло_} = {r}.")
    elif форма == "вместе":
        r = n + m
        факт = я["имеет"].format(**общ, n=n) + " " + я["второй"].format(**общ, m=m)
        воп = я["воп_вместе"].format(**общ)
        леджер = f"{n} + {m} = {r}."
    elif форма == "кратное":
        r = кратность * n
        факт = я["имеет"].format(**общ, n=n) + " " + я["кратно"].format(**общ, K=я["кратные"][кратность])
        воп = я["воп_второй"].format(**общ)
        леджер = f"{кратность} × {n} = {r}."
    elif форма == "место":
        # THE WHOLE NAMED BY ITS PLACE, AND A PART OF IT (e9's profile 03.09:
        # «there are 700 bees in a hive» is the whole without «in all»)
        r = n - k
        С = я["свойства"][свойство]
        факт = я["место"].format(**общ, n=n, П=я["места"][место]) + " " + я["часть_их"].format(**общ, k=k, С=С)
        воп = я["воп_не"].format(С=С)
        леджер = f"{n} − {k} = {r}."
    elif форма == "ставка":
        # A RATE WITHOUT MONEY: «every day», the days asked or the amount asked
        Г = я["ставки"][глагол_ставки]
        факт = я["ставка"].format(**общ, Г=Г, n=n)
        if дней:
            r = n * k
            воп = я["воп_за"].format(**общ, k=k, Д=_день(язык, k))
            леджер = f"{n} × {k} = {r}."
        else:
            r = m // n
            воп = я["воп_дней"].format(**общ, m=m)
            леджер = f"{m} ÷ {n} = {r}."
    else:
        # THE SUM SAID BY «THEY» after the bearers are named
        r = n + m
        л = f"{n} + {m} = {r}."
        return я["вместе_они"].format(**общ, n=n, m=m, r=r, Тr=вещь(r), л=л) + " " + я["ответ"].format(r=r)
    return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"


# --- the court's side ---
def _альт(слова):
    return "(" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    вещи = set()
    for i in range(len(я["вещи"])):
        for n in range(0, 400):
            вещи.add(_вещь(язык, i, n))
            в = _вещь_вин(язык, i, n)
            if в:
                вещи.add(в)
    доли = {fracforms.доля_слово(язык, чс, зн) for чс, зн in ДОЛИ}
    лица = ЛИЦА[язык]
    ч = r"(\d+)"
    return {"X": _альт(л[0] for л in лица), "Y": _альт(л[0] for л in лица),
            "Xр": _альт(л[2] for л in лица), "Yр": _альт(л[2] for л in лица),
            "Т": _альт(вещи), "Тn": _альт(вещи), "Тk": _альт(вещи), "Тm": _альт(вещи), "Тм": _альт(вещи), "Твk": _альт(вещи),
            "Ч": _альт(доли), "K": _альт(я["кратные"].values()), "а": r"(а?)", "У": _альт(я["ушли"]),
            "П": _альт(я["места"]), "С": _альт(я["свойства"]), "Г": _альт(я["ставки"]), "Тr": _альт(вещи),
            "Д": _альт([_день(язык, k) for k in range(1, 60)]),
            "n": ч, "k": ч, "m": ч, "r": ч}


def _шаблоны(язык):
    я = ЯЗЫКИ[язык]
    л = "{л}"
    return [("остаток", f"{я['имел']} {я['отдал']} {я['воп_ост']} {л} {я['ответ']}"),
            ("прибавка", f"{я['имел']} {я['получил']} {я['воп_теперь']} {л} {я['ответ']}"),
            ("доля", f"{я['имел']} {я['ушло']} {я['воп_ост']} {л} {я['ответ']}"),
            ("вместе", f"{я['имеет']} {я['второй']} {я['воп_вместе']} {л} {я['ответ']}"),
            ("кратное", f"{я['имеет']} {я['кратно']} {я['воп_второй']} {л} {я['ответ']}"),
            ("место", f"{я['место']} {я['часть_их']} {я['воп_не']} {л} {я['ответ']}"),
            ("ставка_за", f"{я['ставка']} {я['воп_за']} {л} {я['ответ']}"),
            ("ставка_дней", f"{я['ставка']} {я['воп_дней']} {л} {я['ответ']}"),
            ("вместе_они", f"{я['вместе_они']} {я['ответ']}")]


def образцы(язык):
    дыры = dict(_дыры(язык), л=r"((?:\d+ [+−×÷] \d+ = \d+(?:, )?)+\.)")
    return [(re.compile("^" + phrases.образец(ш, дыры) + "$"), phrases.порядок(ш), форма)
            for форма, ш in _шаблоны(язык)]


ОБРАЗЦЫ = {л: образцы(л) for л in ЯЗЫКИ}


def _имя(з, язык, ключ):
    for к in (ключ, ключ + "р"):
        if з.get(к):
            return next((л[0] for л in ЛИЦА[язык] if з[к] in (л[0], л[2])), None)
    return None


def _вещь_по_формам(язык, з):
    """Which declared thing wears ALL the forms the line shows: the plural, the
    count form beside n, k, m, and the accusative after the verb."""
    я = ЯЗЫКИ[язык]
    for i in range(len(я["вещи"])):
        годно = True
        for ключ, форма in (("Т", lambda: _вещь(язык, i, 2)), ("Тм", lambda: _вещь(язык, i, 5)),
                            ("Тn", lambda: _вещь(язык, i, int(з["n"]))), ("Тk", lambda: _вещь(язык, i, int(з["k"]))),
                            ("Тm", lambda: _вещь(язык, i, int(з["m"]))), ("Твk", lambda: _вещь_вин(язык, i, int(з["k"])) or "")):
            if з.get(ключ) is None:
                continue
            try:
                if з[ключ] != форма():
                    годно = False
                    break
            except (KeyError, ValueError):
                годно = False
                break
        if годно:
            return i
    return None


def разобрать(язык, строка):
    я = ЯЗЫКИ[язык]
    for образец, имена, форма in ОБРАЗЦЫ[язык]:
        м = образец.match(строка)
        if not м:
            continue
        з = {}
        плохо = False
        for имя, г in zip(имена, м.groups()):
            if имя in з and з[имя] != г:
                плохо = True
                break
            з[имя] = г
        if плохо:
            continue
        X = _имя(з, язык, "X")
        if X is None and форма != "место":
            continue          # «место» has no bearer: the whole is named by its place
        Т = _вещь_по_формам(язык, з)
        if Т is None:
            continue
        п = dict(форма=форма, X=X or ЛИЦА[язык][0][0], Т=Т)
        try:
            if форма in ("остаток", "прибавка"):
                п.update(n=int(з["n"]), k=int(з["k"]))
            elif форма == "доля":
                доля = next(((чс, зн) for чс, зн in ДОЛИ if fracforms.доля_слово(язык, чс, зн) == з["Ч"]), None)
                if доля is None:
                    continue
                п.update(n=int(з["n"]), доля=доля)
            elif форма == "вместе":
                Y = _имя(з, язык, "Y")
                if Y is None:
                    continue
                п.update(n=int(з["n"]), m=int(з["m"]), Y=Y)
            elif форма == "кратное":
                Y = _имя(з, язык, "Y")
                кратность = next((k for k, с in я["кратные"].items() if с == з["K"]), None)
                if Y is None or кратность is None:
                    continue
                п.update(n=int(з["n"]), Y=Y, кратность=кратность)
            elif форма == "место":
                п.update(форма="место", n=int(з["n"]), k=int(з["k"]),
                         место=я["места"].index(з["П"]), свойство=я["свойства"].index(з["С"]))
            elif форма in ("ставка_за", "ставка_дней"):
                за = форма == "ставка_за"
                п.update(форма="ставка", n=int(з["n"]), глагол_ставки=я["ставки"].index(з["Г"]), дней=за)
                п.update(k=int(з["k"])) if за else п.update(m=int(з["m"]))
            else:
                Y = _имя(з, язык, "Y")
                if Y is None:
                    continue
                п.update(форма="вместе_они", n=int(з["n"]), m=int(з["m"]), Y=Y)
        except (KeyError, ValueError):
            continue
        return п
    return None


def судить(строка):
    с = строка.strip()
    for язык in ЯЗЫКИ:
        п = разобрать(язык, с)
        if п is not None:
            форма = п.pop("форма")
            try:
                return True, страница(язык, форма, **п) == с
            except (StopIteration, KeyError, IndexError, ValueError, ZeroDivisionError):
                return True, False
    return False, False
