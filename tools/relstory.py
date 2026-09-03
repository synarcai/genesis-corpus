#!/usr/bin/env python3
"""THE HOUSE OF RELATION PAGES — a multiple, a difference and a sum, in three languages.

e9's order (03.09, G1-ATTACK: the owner's word — the whole college to 100 %
of g1; genus 1, «multiplicative relation + sum», 21 tasks) — the school
pages the svod never showed:

  · THE SUM OF A MULTIPLE — «there are twice as many worker bees as baby
    bees. there are 750 bees in all. how many baby bees are there? 1 + 2 = 3,
    750 ÷ 3 = 250. so the answer is 250.» (and the larger part asked, and the
    same fact said «half as many baby bees as worker bees»);
  · A DIFFERENCE OVER A MULTIPLE — «bobby has 5 fewer than three times as
    many games as brian. brian has 20 games. how many games does bobby have?
    3 × 20 = 60, 60 − 5 = 55. so the answer is 55.»;
  · THE SAME RELATION BACKWARDS — «janey has 3 more than twice the number of
    books sally has. janey has 21 books. how many books does sally have?
    21 − 3 = 18, 18 ÷ 2 = 9. so the answer is 9.»;
  · AGES — «ruby is three times as old as sam. sam is 4 years old. how old is
    ruby? 3 × 4 = 12. so the answer is 12.», «… together they are 32 years
    old. how old is sam? 1 + 3 = 4, 32 ÷ 4 = 8. so the answer is 8.» (and the
    g1 idiom «three times older than»).

Every answer is whole (the sum is a multiple of 1 + k), every step a
primitive, the last number the answer. The words of multiplicity are
declared, not derived («twice» is lexicon). The court reads the page back
through the same templates, REGENERATES it and compares letter by letter.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402
import rugram  # noqa: E402

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
ПАКЕТЫ = КОРЕНЬ / "tools" / "langpacks"


def _пакет(язык):
    return json.loads((ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))


# THE RUSSIAN NAME BENDS, AND THE CASES ARE DECLARED (as the age world does):
# nominative, dative («Сэму 4 года»), genitive («старше Сэма») — the genitive
# from the pack, the dative here.
_ДАТЕЛЬНЫЙ_RU = {"анна": "анне", "аня": "ане", "вера": "вере", "дима": "диме", "иван": "ивану", "коля": "коле", "лена": "лене",
                 "маша": "маше", "миша": "мише", "оля": "оле", "петя": "пете", "том": "тому", "юра": "юре", "саша": "саше"}


def _лица(язык):
    п = _пакет(язык)
    формы = п.get("person_forms") or {}
    вон = []
    for имя in п.get("person_names", ()):
        ф = формы.get(имя) or formы_guess(формы, имя)
        if язык == "ru":
            if имя not in _ДАТЕЛЬНЫЙ_RU or not ф or not ф.get("gen"):
                continue
            вон.append((имя.capitalize(), ф["gen"].capitalize(), _ДАТЕЛЬНЫЙ_RU[имя].capitalize()))
        else:
            вон.append((имя, имя, имя))
        if len(вон) == 12:
            break
    return tuple(вон)


def formы_guess(формы, имя):
    return формы.get(имя.lower()) or формы.get(имя.capitalize())


ЯЗЫКИ = {
    "en": dict(
        пары=(("worker bees", "baby bees", "bees"), ("adults", "children", "people"), ("red marbles", "blue marbles", "marbles"),
              ("roses", "tulips", "flowers"), ("cats", "dogs", "animals"), ("boys", "girls", "pupils")),
        вещи=("games", "books", "cards", "coins", "stickers", "pens"),
        кратно={2: "twice", 3: "three times", 4: "four times"}, доля={2: "half as many", 3: "a third as many"},
        сумма_утв="there are {K} as many {Б} as {М}. there are {N} {В} in all.",
        сумма_утв2="there are {Д} {М} as {Б}. there are {N} {В} in all.",
        сумма_воп_м="how many {М} are there?", сумма_воп_б="how many {Б} are there?",
        больше="{X} has {d} {З} than {K} as many {Т} as {Y}. {Y} has {n} {Т}. how many {Т} does {X} have?",
        обратно="{X} has {d} {З} than {K} the number of {Т} {Y} has. {X} has {m} {Т}. how many {Т} does {Y} have?",
        знаки={"−": "fewer", "+": "more"},
        возраст="{X} is {K} as old as {Y}.", возраст2="{X} is {K} older than {Y}.",
        возраст_воп_x="{Y} is {n} years old. how old is {X}?", возраст_воп_сум="together they are {N} years old. how old is {Y}?",
        сумма_обр="there are {x} {М}. there are {K} as many {Б} as {М}. how many {В} are there in all?",
        трое="together {X}, {Y} and {Z} have {N} {Т}. {X} has {K} as many as {Y}. {Y} has {d} {З} than {Z}. how many {Т} does {W} have?",
        # e9's profile of muteness, genus 4 (03.09): the age AFTER k years,
        # asked forward, backward, and over a multiple
        через="{X} is {n} years old. how old will {X} be in {k} years?",
        через_обратно="in {k} years {X} will be {m} years old. how old is {X} now?",
        кратное_через="{X} is {n} years old. {Y} is {K} as old as {X}. how old will {Y} be in {k} years?",
        ответ="so the answer is {r}.",
    ),
    "ru": dict(
        пары=(("рабочих пчёл", "молодых пчёл", "пчёл"), ("взрослых", "детей", "людей"), ("красных шариков", "синих шариков", "шариков"),
              ("роз", "тюльпанов", "цветов"), ("кошек", "собак", "животных"), ("мальчиков", "девочек", "учеников")),
        вещи=("игра", "книга", "карта", "монета", "ручка", "шарик"),
        кратно={2: "вдвое", 3: "втрое", 4: "вчетверо"}, доля={2: "вдвое", 3: "втрое"},
        удвоенное={2: "удвоенное", 3: "утроенное", 4: "учетверённое"},
        сумма_утв="{Б} {K} больше, чем {М}. всего {В} {N}.",
        сумма_утв2="{М} {Д} меньше, чем {Б}. всего {В} {N}.",
        сумма_воп_м="сколько {М}?", сумма_воп_б="сколько {Б}?",
        больше="у {Xр} на {d} {Тd} {З}, чем {У} число {Тм} у {Yр}. у {Yр} {n} {Тn}. сколько {Тм} у {Xр}?",
        обратно="у {Xр} на {d} {Тd} {З}, чем {У} число {Тм} у {Yр}. у {Xр} {m} {Тm}. сколько {Тм} у {Yр}?",
        знаки={"−": "меньше", "+": "больше"},
        возраст="{X} {K} старше {Yр}.",
        возраст_воп_x="{Yд} {n} {Л}. сколько лет {Xд}?", возраст_воп_сум="вместе им {N} {Л}. сколько лет {Yд}?",
        сумма_обр="{М} {x}. {Б} {K} больше, чем {М}. сколько всего {В}?",
        трое="вместе у {Xр}, {Yр} и {Zр} {N} {Тn}. у {Xр} {K} больше, чем у {Yр}. у {Yр} на {d} {Тd} {З}, чем у {Zр}. сколько {Тм} у {Wр}?",
        через="{Xд} {n} {Л}. сколько лет будет {Xд} через {k} {Лk}?",
        через_обратно="через {k} {Лk} {Xд} будет {m} {Лm}. сколько лет {Xд} сейчас?",
        кратное_через="{Xд} {n} {Л}. {Y} {K} старше {Xр}. сколько лет будет {Yд} через {k} {Лk}?",
        ответ="значит ответ: {r}.",
    ),
    "de": dict(
        пары=(("Arbeiterbienen", "junge Bienen", "Bienen"), ("Erwachsene", "Kinder", "Personen"), ("rote Murmeln", "blaue Murmeln", "Murmeln"),
              ("Rosen", "Tulpen", "Blumen"), ("Katzen", "Hunde", "Tiere"), ("Jungen", "Mädchen", "Schüler")),
        вещи=("Spiele", "Bücher", "Karten", "Münzen", "Sticker", "Stifte"),
        кратно={2: "doppelt", 3: "dreimal", 4: "viermal"}, доля={2: "halb", 3: "ein Drittel"},
        сумма_утв="es gibt {K} so viele {Б} wie {М}. insgesamt sind es {N} {В}.",
        сумма_утв2="es gibt {Д} so viele {М} wie {Б}. insgesamt sind es {N} {В}.",
        сумма_воп_м="wie viele {М} gibt es?", сумма_воп_б="wie viele {Б} gibt es?",
        больше="{X} hat {d} {Т} {З} als {K} so viele wie {Y}. {Y} hat {n} {Т}. wie viele {Т} hat {X}?",
        обратно="{X} hat {d} {Т} {З} als {K} so viele wie {Y}. {X} hat {m} {Т}. wie viele {Т} hat {Y}?",
        знаки={"−": "weniger", "+": "mehr"},
        возраст="{X} ist {K} so alt wie {Y}.",
        возраст_воп_x="{Y} ist {n} Jahre alt. wie alt ist {X}?", возраст_воп_сум="zusammen sind sie {N} Jahre alt. wie alt ist {Y}?",
        сумма_обр="es gibt {x} {М}. es gibt {K} so viele {Б} wie {М}. wie viele {В} gibt es insgesamt?",
        трое="zusammen haben {X}, {Y} und {Z} {N} {Т}. {X} hat {K} so viele wie {Y}. {Y} hat {d} {Т} {З} als {Z}. wie viele {Т} hat {W}?",
        через="{X} ist {n} Jahre alt. wie alt wird {X} in {k} Jahren sein?",
        через_обратно="in {k} Jahren wird {X} {m} Jahre alt sein. wie alt ist {X} jetzt?",
        кратное_через="{X} ist {n} Jahre alt. {Y} ist {K} so alt wie {X}. wie alt wird {Y} in {k} Jahren sein?",
        ответ="also ist die Antwort {r}.",
    ),
}
ЛИЦА = {язык: _лица(язык) for язык in ЯЗЫКИ}
ФОРМЫ = ("сумма", "сумма_обр", "больше", "обратно", "трое", "возраст", "через", "через_обратно", "кратное_через")


def _лицо(язык, имя):
    return next(л for л in ЛИЦА[язык] if л[0] == имя)


def _вещь(язык, i, n):
    """The thing beside n: English/German plural (n ≥ 2 always), Russian by the house of count."""
    в = ЯЗЫКИ[язык]["вещи"][i]
    return rugram.форма(в, n) if язык == "ru" else в


def _лет(n):
    return rugram.форма("год", n)


def страница(язык, форма, **п):
    я = ЯЗЫКИ[язык]
    k = п["k"]
    if форма == "сумма":
        Б, М, В = я["пары"][п["пара"]]
        x = п["x"]; N = x * (1 + k)
        утв = (я["сумма_утв2"].format(Д=я["доля"][k], М=М, Б=Б, N=N, В=В) if п.get("долей")
               else я["сумма_утв"].format(K=я["кратно"][k], Б=Б, М=М, N=N, В=В))
        if п["спрос"] == "м":
            воп, леджер, r = я["сумма_воп_м"].format(М=М), f"1 + {k} = {1 + k}, {N} ÷ {1 + k} = {x}.", x
        else:
            воп, леджер, r = я["сумма_воп_б"].format(Б=Б), f"1 + {k} = {1 + k}, {N} ÷ {1 + k} = {x}, {x} × {k} = {x * k}.", x * k
        return f"{утв} {воп} {леджер} {я['ответ'].format(r=r)}"
    if форма == "сумма_обр":
        # the small part is given, the whole asked: «2 × 250 = 500, 250 + 500 = 750»
        Б, М, В = я["пары"][п["пара"]]
        x = п["x"]; y = x * k; N = x + y
        утв = я["сумма_обр"].format(x=x, М=М, K=я["кратно"][k], Б=Б, В=В)
        return f"{утв} {k} × {x} = {y}, {x} + {y} = {N}. {я['ответ'].format(r=N)}"
    if форма == "трое":
        # X = k·a, Y = a, Z = a ± d (Y has d fewer/more than Z); N = (k + 2)·a ± d
        X, Xр, Xд = _лицо(язык, п["X"]); Y, Yр, Yд = _лицо(язык, п["Y"]); Z, Zр, Zд = _лицо(язык, п["Z"])
        d, знак, i, a = п["d"], п["знак"], п["вещь"], п["a"]
        z = a + d if знак == "−" else a - d
        N = k * a + a + z
        W, Wр = {"X": (X, Xр), "Y": (Y, Yр), "Z": (Z, Zр)}[п["спрос"]]
        з = dict(X=X, Xр=Xр, Y=Y, Yр=Yр, Z=Z, Zр=Zр, W=W, Wр=Wр, N=N, K=я["кратно"][k], d=d, З=я["знаки"][знак],
                 Т=_вещь(язык, i, 2), Тn=_вещь(язык, i, N), Тd=_вещь(язык, i, d), Тм=_вещь(язык, i, 5))
        # the difference is taken out of the sum (or put back), the shares are counted, the base found
        шаг1 = f"{N} − {d} = {N - d}" if знак == "−" else f"{N} + {d} = {N + d}"
        база = (N - d) if знак == "−" else (N + d)
        шаги = [шаг1, f"{k} + 1 + 1 = {k + 2}", f"{база} ÷ {k + 2} = {a}"]
        if п["спрос"] == "X":
            шаги.append(f"{k} × {a} = {k * a}"); r = k * a
        elif п["спрос"] == "Z":
            шаги.append(f"{a} + {d} = {z}" if знак == "−" else f"{a} − {d} = {z}"); r = z
        else:
            r = a
        return f"{я['трое'].format(**з)} {', '.join(шаги)}. {я['ответ'].format(r=r)}"
    if форма in ("больше", "обратно"):
        X, Xр, Xд = _лицо(язык, п["X"]); Y, Yр, Yд = _лицо(язык, п["Y"])
        d, знак, i = п["d"], п["знак"], п["вещь"]
        З = я["знаки"][знак]
        if форма == "больше":
            n = п["n"]; kn = k * n; r = kn - d if знак == "−" else kn + d
            з = dict(X=X, Xр=Xр, Y=Y, Yр=Yр, d=d, З=З, K=я["кратно"][k], У=я.get("удвоенное", {}).get(k, ""), n=n,
                     Т=_вещь(язык, i, 2), Тd=_вещь(язык, i, d), Тn=_вещь(язык, i, n), Тм=_вещь(язык, i, 5))
            леджер = f"{k} × {n} = {kn}, {kn} {знак} {d} = {r}."
            return f"{я['больше'].format(**з)} {леджер} {я['ответ'].format(r=r)}"
        r = п["r"]; kr = k * r; m = kr + d if знак == "+" else kr - d
        обр = "−" if знак == "+" else "+"
        з = dict(X=X, Xр=Xр, Y=Y, Yр=Yр, d=d, З=З, K=(я["кратно"][k] + (" the number of" if язык == "en" else "")) if язык != "en" else я["кратно"][k],
                 У=я.get("удвоенное", {}).get(k, ""), m=m, Т=_вещь(язык, i, 2), Тd=_вещь(язык, i, d), Тm=_вещь(язык, i, m), Тм=_вещь(язык, i, 5))
        леджер = f"{m} {обр} {d} = {kr}, {kr} ÷ {k} = {r}."
        return f"{я['обратно'].format(**з)} {леджер} {я['ответ'].format(r=r)}"
    if форма in ("через", "через_обратно", "кратное_через"):
        # THE AGE AFTER k YEARS (e9's profile, genus 4): forward, backward, and
        # over a multiple — every step a primitive, the last number the answer
        X, Xр, Xд = _лицо(язык, п["X"])
        з = dict(X=X, Xр=Xр, Xд=Xд)
        if форма == "через":
            n, kk = п["n"], п["k"]
            r = n + kk
            воп = я["через"].format(**з, n=n, k=kk, Л=_лет(n), Лk=_лет(kk))
            леджер = f"{n} + {kk} = {r}."
        elif форма == "через_обратно":
            m, kk = п["m"], п["k"]
            r = m - kk
            воп = я["через_обратно"].format(**з, m=m, k=kk, Лm=_лет(m), Лk=_лет(kk))
            леджер = f"{m} − {kk} = {r}."
        else:
            Y, Yр, Yд = _лицо(язык, п["Y"])
            n, kk = п["n"], п["лет"]
            a = k * n
            r = a + kk
            воп = я["кратное_через"].format(**з, Y=Y, Yр=Yр, Yд=Yд, n=n, k=kk, K=я["кратно"][k], Л=_лет(n), Лk=_лет(kk))
            леджер = f"{k} × {n} = {a}, {a} + {kk} = {r}."
        return f"{воп} {леджер} {я['ответ'].format(r=r)}"
    # ages
    X, Xр, Xд = _лицо(язык, п["X"]); Y, Yр, Yд = _лицо(язык, п["Y"])
    K = я["кратно"][k]
    утв = (я["возраст2"] if п.get("идиома") and "возраст2" in я else я["возраст"]).format(X=X, Y=Y, Yр=Yр, K=K)
    if п["спрос"] == "x":
        n = п["n"]; r = k * n
        воп = я["возраст_воп_x"].format(Y=Y, Yд=Yд, X=X, Xд=Xд, n=n, Л=_лет(n))
        леджер = f"{k} × {n} = {r}."
    else:
        x = п["x"]; N = x * (1 + k); r = x
        воп = я["возраст_воп_сум"].format(Y=Y, Yд=Yд, N=N, Л=_лет(N))
        леджер = f"1 + {k} = {1 + k}, {N} ÷ {1 + k} = {x}."
    return f"{утв} {воп} {леджер} {я['ответ'].format(r=r)}"


# --- the court's side: the same templates as patterns, the page regenerated ---
def _альт(слова):
    return "(" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    лица = ЛИЦА[язык]
    вещи = set()
    for i in range(len(я["вещи"])):
        for n in range(1, 400):
            вещи.add(_вещь(язык, i, n))
    ч = r"(\d+)"
    return {"X": _альт(л[0] for л in лица), "Y": _альт(л[0] for л in лица), "Xр": _альт(л[1] for л in лица), "Yр": _альт(л[1] for л in лица),
            "Xд": _альт(л[2] for л in лица), "Yд": _альт(л[2] for л in лица),
            "Z": _альт(л[0] for л in лица), "Zр": _альт(л[1] for л in лица), "W": _альт(л[0] for л in лица), "Wр": _альт(л[1] for л in лица),
            "Б": _альт(п[0] for п in я["пары"]), "М": _альт(п[1] for п in я["пары"]), "В": _альт(п[2] for п in я["пары"]),
            "K": _альт(list(я["кратно"].values()) + ([k + " the number of" for k in я["кратно"].values()] if язык == "en" else [])),
            "Д": _альт(я["доля"].values()), "У": _альт(я.get("удвоенное", {"": "—"}).values()), "З": _альт(я["знаки"].values()),
            "Т": _альт(вещи), "Тd": _альт(вещи), "Тn": _альт(вещи), "Тm": _альт(вещи), "Тм": _альт(вещи), "Л": _альт(["год", "года", "лет"]),
            "N": ч, "n": ч, "d": ч, "m": ч, "r": ч, "x": ч, "y": ч, "k": ч,
            "Л": _альт(["год", "года", "лет"]), "Лk": _альт(["год", "года", "лет"]), "Лm": _альт(["год", "года", "лет"])}


def _шаблоны(язык):
    """(form, variant, template of the whole page with a ledger hole «л»)."""
    я = ЯЗЫКИ[язык]
    л = "{л}"
    вон = [("сумма", "м", f"{я['сумма_утв']} {я['сумма_воп_м']} {л} {я['ответ']}"), ("сумма", "б", f"{я['сумма_утв']} {я['сумма_воп_б']} {л} {я['ответ']}"),
           ("сумма", "дм", f"{я['сумма_утв2']} {я['сумма_воп_м']} {л} {я['ответ']}"), ("сумма", "дб", f"{я['сумма_утв2']} {я['сумма_воп_б']} {л} {я['ответ']}"),
           ("сумма_обр", "", f"{я['сумма_обр']} {л} {я['ответ']}"), ("трое", "", f"{я['трое']} {л} {я['ответ']}"),
           ("больше", "", f"{я['больше']} {л} {я['ответ']}"), ("обратно", "", f"{я['обратно']} {л} {я['ответ']}"),
           ("возраст", "x", f"{я['возраст']} {я['возраст_воп_x']} {л} {я['ответ']}"), ("возраст", "сум", f"{я['возраст']} {я['возраст_воп_сум']} {л} {я['ответ']}")]
    вон += [("через", "", f"{я['через']} {л} {я['ответ']}"),
            ("через_обратно", "", f"{я['через_обратно']} {л} {я['ответ']}"),
            ("кратное_через", "", f"{я['кратное_через']} {л} {я['ответ']}")]
    if "возраст2" in я:
        вон += [("возраст", "x2", f"{я['возраст2']} {я['возраст_воп_x']} {л} {я['ответ']}"), ("возраст", "сум2", f"{я['возраст2']} {я['возраст_воп_сум']} {л} {я['ответ']}")]
    return вон


def образцы(язык):
    # a step may carry several operands («2 + 1 + 1 = 4» — the shares counted)
    дыры = dict(_дыры(язык), л=r"((?:\d+(?: [+−×÷] \d+)+ = \d+(?:, )?)+\.)")
    return [(re.compile("^" + phrases.образец(ш, дыры) + "$"), phrases.порядок(ш), форма, вид) for форма, вид, ш in _шаблоны(язык)]


ОБРАЗЦЫ = {язык: образцы(язык) for язык in ЯЗЫКИ}


def _обратно(таблица, слово):
    return next((k for k, v in таблица.items() if v == слово), None)


def разобрать(язык, строка):
    """The parameters of the page, or None — not a page of this house. Every
    template is tried in turn: the first sentence of «больше» and «обратно» is
    one phrase in ru/de, and the repeated hole («у Анны … у Анны») decides."""
    я = ЯЗЫКИ[язык]
    for образец, имена, форма, вид in ОБРАЗЦЫ[язык]:
        м = образец.match(строка)
        if not м:
            continue
        з = {}
        for имя, г in zip(имена, м.groups()):
            if имя in з and з[имя] != г:
                з = None
                break
            з[имя] = г
        if з is None:
            continue
        п = _параметры(язык, форма, вид, з)
        if п is not None:
            return п
    return None


def _параметры(язык, форма, вид, з):
    я = ЯЗЫКИ[язык]
    try:
        if форма == "сумма":
            пара = next(i for i, п in enumerate(я["пары"]) if п[0] == з["Б"] and п[1] == з["М"] and п[2] == з["В"])
            долей = вид.startswith("д")
            k = _обратно(я["доля"], з["Д"]) if долей else _обратно(я["кратно"], з["K"])
            N = int(з["N"])
            if k is None or N % (1 + k):
                return None
            return dict(форма="сумма", пара=пара, k=k, долей=долей, спрос=("м" if вид.endswith("м") else "б"), x=N // (1 + k))
        if форма == "сумма_обр":
            пара = next(i for i, п in enumerate(я["пары"]) if п[0] == з["Б"] and п[1] == з["М"] and п[2] == з["В"])
            k = _обратно(я["кратно"], з["K"])
            if k is None:
                return None
            return dict(форма="сумма_обр", пара=пара, k=k, x=int(з["x"]))
        X = imя_or(з, язык, "X")
        if X is None:
            return None
        if форма in ("через", "через_обратно"):
            п = dict(форма=форма, X=X, k=int(з["k"]))
            п["n" if форма == "через" else "m"] = int(з["n" if форма == "через" else "m"])
            return п
        Y = imя_or(з, язык, "Y")
        if Y is None:
            return None
        if форма == "трое":
            Z = imя_or(з, язык, "Z"); W = imя_or(з, язык, "W")
            k = _обратно(я["кратно"], з["K"]); знак = _обратно(я["знаки"], з["З"])
            вещь = next(i for i in range(len(я["вещи"])) if _вещь(язык, i, 5) == (з.get("Тм") or _вещь(язык, i, 2)) and (з.get("Т") in (None, _вещь(язык, i, 2))))
            if None in (Z, W, k, знак) or len({X, Y, Z}) < 3:
                return None
            спрос = {X: "X", Y: "Y", Z: "Z"}.get(W)
            N, d = int(з["N"]), int(з["d"])
            база = N - d if знак == "−" else N + d
            if спрос is None or база <= 0 or база % (k + 2):
                return None
            return dict(форма="трое", X=X, Y=Y, Z=Z, k=k, знак=знак, d=d, вещь=вещь, a=база // (k + 2), спрос=спрос)
        if форма in ("больше", "обратно"):
            k = _обратно(я["кратно"], з["K"].replace(" the number of", "")) if язык != "ru" else _обратно(я["удвоенное"], з["У"])
            знак = _обратно(я["знаки"], з["З"])
            вещь = next(i for i in range(len(я["вещи"])) if _вещь(язык, i, 5) == (з.get("Тм") or _вещь(язык, i, 2)) and (з.get("Т") in (None, _вещь(язык, i, 2))))
            if k is None or знак is None:
                return None
            if форма == "больше":
                return dict(форма="больше", X=X, Y=Y, k=k, знак=знак, d=int(з["d"]), вещь=вещь, n=int(з["n"]))
            m, d = int(з["m"]), int(з["d"])
            kr = m - d if знак == "+" else m + d
            if kr % k:
                return None
            return dict(форма="обратно", X=X, Y=Y, k=k, знак=знак, d=d, вещь=вещь, r=kr // k)
        k = _обратно(я["кратно"], з["K"])
        if k is None:
            return None
        if форма == "кратное_через":
            return dict(форма="кратное_через", X=X, Y=Y, k=k, n=int(з["n"]), лет=int(з["k"]))
        п = dict(форма="возраст", X=X, Y=Y, k=k, идиома=вид.endswith("2"))
        if vид_x(вид):
            п.update(спрос="x", n=int(з["n"]))
        else:
            N = int(з["N"])
            if N % (1 + k):
                return None
            п.update(спрос="сум", x=N // (1 + k))
        return п
    except (StopIteration, KeyError, ValueError):
        return None


def imя_or(з, язык, ключ):
    for к in (ключ, ключ + "р", ключ + "д"):
        if з.get(к):
            return next(л[0] for л in ЛИЦА[язык] if з[к] in л)
    return None


def vид_x(вид):
    return вид in ("x", "x2")


def судить(строка):
    с = строка.strip()
    for язык in ЯЗЫКИ:
        п = разобрать(язык, с)
        if п is not None:
            форма = п.pop("форма")
            try:
                return True, страница(язык, форма, **п) == с
            except (StopIteration, KeyError, IndexError, ValueError):
                return True, False
    return False, False
