#!/usr/bin/env python3
"""THE HOUSE OF ACTION MEASURE IN SEVEN MORE LANGUAGES — d5's genus (tools/actionmeasure.py,
en/ru) said in de/fr/es/it/pt/nl/pl: the number that MEASURES the act («der Frosch
sprang 12 Zentimeter»), its sum, and the number that counts BEARERS at a place
(«auf dem Zaun saßen 6 Vögel. 4 weitere Vögel kamen dazu.»).

The unit belongs to the verb (jump — length, weigh — weight) and is declared with
its count forms (Polish three, Romance two, German and Dutch one); the actor's
gender bends the Polish past; the Polish verb of the bearers bends with the count
form («siedziały 3 ptaki» / «siedziało 6 ptaków») — declared both, chosen by the
pack's agreement rule. Frames are declared per language and read by the court
through the same tables (tools/phrases.py); sums and counts are recomputed.
The world is CLOSED.

    python3 tools/measurelangs.py    # self-check with mutants
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import langpack  # noqa: E402
import phrases  # noqa: E402

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЧИСЛА_МЕРЫ = (12, 5, 27, 8, 15, 31, 9, 20, 46)
ПАРЫ_СУММЫ = ((12, 8), (5, 9), (27, 13), (15, 6), (31, 19), (9, 4), (20, 25), (46, 14), (8, 8))
НОСИТЕЛИ_ЧИСЛА = ((6, 4), (43, 21), (12, 5), (9, 3), (28, 14), (7, 6), (15, 8), (30, 12), (11, 9))

# per language: actors (name, gender), verbs (past[, past f], bare, kind), units by kind
# (count forms), prepositions by kind, frames; bearers (forms…, place, was, came, left)
ЯЗЫКИ = {
    "de": dict(деятели=(("der Frosch", "m"), ("das Känguru", "n"), ("der Hund", "m"), ("die Katze", "f")),
               глаголы=(("sprang", "springen", "длина"), ("wog", "wiegen", "вес")),
               единицы={"длина": (("Zentimeter",), ("Meter",)), "вес": (("Kilogramm",), ("Gramm",))}, пр={},
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "wie weit {Гп} {A}?", "вес": "wie viel {Гп} {A}?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa} und dann {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "wie weit {Гп} {A} insgesamt?", "вес": "wie viel {Гп} {A} insgesamt?"},
               сумма_ответ="{ПР}{s} {ЕДs}: {a} + {b} = {s}.",
               носители=((("Vogel", "Vögel"), "auf dem Zaun", ("saßen",), ("kamen dazu",), ("flogen weg",)),
                         (("Kind", "Kinder"), "im Bus", ("waren",), ("stiegen ein",), ("stiegen aus",)),
                         (("Boot", "Boote"), "im Hafen", ("lagen",), ("kamen an",), ("fuhren weg",))),
               было="{ГДЕ} {БЫЛИ} {n} {Нn}.", прибыль="{k} weitere {Нk} {ПРИШЛИ}.", убыль="{k} {Нk} {УШЛИ}.",
               носители_вопрос="wie viele {Нмн} sind jetzt {ГДЕ}?", носители_ответ="{r} {Нr}: {n} {знак} {k} = {r}."),
    "fr": dict(деятели=(("la grenouille", "f"), ("le kangourou", "m"), ("le chien", "m"), ("le chat", "m")),
               глаголы=(("a sauté", "sauter", "длина"), ("pesait", "peser", "вес")),
               единицы={"длина": (("centimètre", "centimètres"), ("mètre", "mètres")), "вес": (("kilogramme", "kilogrammes"), ("gramme", "grammes"))}, пр={"длина": "de "},
               # the question opens with «combien» (the script court's opener), not with the actor
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "combien de {ЕДмн} {A} {Гп} ?", "вес": "combien de {ЕДмн} {A} {Гп} ?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa} puis {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "combien de {ЕДмн} {A} {Гп} en tout ?", "вес": "combien de {ЕДмн} {A} {Гп} en tout ?"},
               сумма_ответ="{ПР}{s} {ЕДs} : {a} + {b} = {s}.",
               носители=((("oiseau", "oiseaux"), "sur la clôture", ("étaient perchés",), ("sont arrivés",), ("se sont envolés",)),
                         (("enfant", "enfants"), "dans le bus", ("étaient",), ("sont montés",), ("sont descendus",)),
                         (("bateau", "bateaux"), "dans le port", ("étaient amarrés",), ("sont arrivés",), ("sont partis",))),
               было="{n} {Нn} {БЫЛИ} {ГДЕ}.", прибыль="{k} {Нk} de plus {ПРИШЛИ}.", убыль="{k} {Нk} {УШЛИ}.",
               носители_вопрос="combien {ДЕ}{Нмн} y a-t-il {ГДЕ} maintenant ?", носители_ответ="{r} {Нr} : {n} {знак} {k} = {r}."),
    "es": dict(деятели=(("la rana", "f"), ("el canguro", "m"), ("el perro", "m"), ("el gato", "m")),
               глаголы=(("saltó", "saltar", "длина"), ("pesaba", "pesar", "вес")),
               единицы={"длина": (("centímetro", "centímetros"), ("metro", "metros")), "вес": (("kilogramo", "kilogramos"), ("gramo", "gramos"))}, пр={},
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "¿cuánto {Гп} {A}?", "вес": "¿cuánto {Гп} {A}?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa} y luego {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "¿cuánto {Гп} {A} en total?", "вес": "¿cuánto {Гп} {A} en total?"},
               сумма_ответ="{ПР}{s} {ЕДs}: {a} + {b} = {s}.",
               носители=((("pájaro", "pájaros"), "en la valla", ("había",), ("llegaron",), ("se fueron volando",)),
                         (("niño", "niños"), "en el autobús", ("había",), ("subieron",), ("bajaron",)),
                         (("barco", "barcos"), "en el puerto", ("había",), ("llegaron",), ("se fueron",))),
               было="{БЫЛИ} {n} {Нn} {ГДЕ}.", прибыль="{ПРИШЛИ} {k} {Нk} más.", убыль="{УШЛИ} {k} {Нk}.",
               носители_вопрос="¿cuántos {Нмн} hay {ГДЕ} ahora?", носители_ответ="{r} {Нr}: {n} {знак} {k} = {r}."),
    "it": dict(деятели=(("la rana", "f"), ("il canguro", "m"), ("il cane", "m"), ("il gatto", "m")),
               глаголы=(("ha saltato", "saltare", "длина"), ("pesava", "pesare", "вес")),
               единицы={"длина": (("centimetro", "centimetri"), ("metro", "metri")), "вес": (("chilogrammo", "chilogrammi"), ("grammo", "grammi"))}, пр={},
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "quanto {Гп} {A}?", "вес": "quanto {Гп} {A}?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa} e poi {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "quanto {Гп} {A} in tutto?", "вес": "quanto {Гп} {A} in tutto?"},
               сумма_ответ="{ПР}{s} {ЕДs}: {a} + {b} = {s}.",
               носители=((("uccello", "uccelli"), "sul recinto", ("c'erano",), ("sono arrivati altri",), ("sono volati via",)),
                         (("bambino", "bambini"), "sull'autobus", ("c'erano",), ("sono saliti altri",), ("sono scesi",)),
                         (("barca", "barche"), "nel porto", ("c'erano",), ("sono arrivate altre",), ("sono partite",))),
               было="{БЫЛИ} {n} {Нn} {ГДЕ}.", прибыль="{ПРИШЛИ} {k} {Нk}.", убыль="{k} {Нk} {УШЛИ}.",
               носители_вопрос="quanti {Нмн} ci sono {ГДЕ} adesso?", носители_ответ="{r} {Нr}: {n} {знак} {k} = {r}."),
    "pt": dict(деятели=(("a rã", "f"), ("o canguru", "m"), ("o cão", "m"), ("o gato", "m")),
               глаголы=(("saltou", "saltar", "длина"), ("pesava", "pesar", "вес")),
               единицы={"длина": (("centímetro", "centímetros"), ("metro", "metros")), "вес": (("quilograma", "quilogramas"), ("grama", "gramas"))}, пр={},
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "quanto {Гп} {A}?", "вес": "quanto {Гп} {A}?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa} e depois {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "quanto {Гп} {A} no total?", "вес": "quanto {Гп} {A} no total?"},
               сумма_ответ="{ПР}{s} {ЕДs}: {a} + {b} = {s}.",
               носители=((("pássaro", "pássaros"), "na vedação", ("havia",), ("chegaram mais",), ("voaram embora",)),
                         (("criança", "crianças"), "no autocarro", ("havia",), ("entraram mais",), ("saíram",)),
                         (("barco", "barcos"), "no porto", ("havia",), ("chegaram mais",), ("partiram",))),
               было="{БЫЛИ} {n} {Нn} {ГДЕ}.", прибыль="{ПРИШЛИ} {k} {Нk}.", убыль="{k} {Нk} {УШЛИ}.",
               носители_вопрос="quantos {Нмн} há {ГДЕ} agora?", носители_ответ="{r} {Нr}: {n} {знак} {k} = {r}."),
    "nl": dict(деятели=(("de kikker", "m"), ("de kangoeroe", "m"), ("de hond", "m"), ("de kat", "f")),
               глаголы=(("sprong", "springen", "длина"), ("woog", "wegen", "вес")),
               единицы={"длина": (("centimeter",), ("meter",)), "вес": (("kilogram",), ("gram",))}, пр={},
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "hoe ver {Гп} {A}?", "вес": "hoeveel {Гп} {A}?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa} en daarna {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "hoe ver {Гп} {A} in totaal?", "вес": "hoeveel {Гп} {A} in totaal?"},
               сумма_ответ="{ПР}{s} {ЕДs}: {a} + {b} = {s}.",
               носители=((("vogel", "vogels"), "op het hek", ("zaten",), ("kwamen erbij",), ("vlogen weg",)),
                         (("kind", "kinderen"), "in de bus", ("zaten",), ("stapten in",), ("stapten uit",)),
                         (("boot", "boten"), "in de haven", ("lagen",), ("kwamen aan",), ("vertrokken",))),
               было="er {БЫЛИ} {n} {Нn} {ГДЕ}.", прибыль="er {ПРИШЛИ} {k} {Нk}.", убыль="{k} {Нk} {УШЛИ}.",
               носители_вопрос="hoeveel {Нмн} zijn er nu {ГДЕ}?", носители_ответ="{r} {Нr}: {n} {знак} {k} = {r}."),
    "pl": dict(деятели=(("żaba", "f"), ("kangur", "m"), ("pies", "m"), ("kot", "m")),
               глаголы=(("skoczył", "skoczyła", "skoczyć", "длина"), ("ważył", "ważyła", "ważyć", "вес")),
               единицы={"длина": (("centymetr", "centymetry", "centymetrów"), ("metr", "metry", "metrów")),
                        "вес": (("kilogram", "kilogramy", "kilogramów"), ("gram", "gramy", "gramów"))}, пр={"длина": "na "},
               факт="{A} {Гп} {ПР}{n} {ЕДn}.", вопрос={"длина": "ile {ЕДмн} {Гп} {A}?", "вес": "ile {ЕДмн} {Гп} {A}?"}, ответ="{ПР}{n} {ЕДn}.",
               сумма_факт="{A} {Гп} {ПР}{a} {ЕДa}, a potem {ПР}{b} {ЕДb}.", сумма_вопрос={"длина": "ile {ЕДмн} {Гп} {A} łącznie?", "вес": "ile {ЕДмн} {Гп} {A} łącznie?"},
               сумма_ответ="{ПР}{s} {ЕДs}: {a} + {b} = {s}.",
               # the verb of the bearers bends with the count form: (few, many)
               носители=((("ptak", "ptaki", "ptaków"), "na płocie", ("siedziały", "siedziało"), ("przyleciały jeszcze", "przyleciało jeszcze"), ("odleciały", "odleciało")),
                         (("dziecko", "dzieci", "dzieci"), "w autobusie", ("były", "było"), ("wsiadły jeszcze", "wsiadło jeszcze"), ("wysiadły", "wysiadło")),
                         (("łódź", "łodzie", "łodzi"), "w porcie", ("stały", "stało"), ("przypłynęły jeszcze", "przypłynęło jeszcze"), ("odpłynęły", "odpłynęło"))),
               было="{ГДЕ} {БЫЛИ} {n} {Нn}.", прибыль="{ПРИШЛИ} {k} {Нk}.", убыль="{УШЛИ} {k} {Нk}.",
               носители_вопрос="ile {Нмн} jest teraz {ГДЕ}?", носители_ответ="{r} {Нr}: {n} {знак} {k} = {r}."),
}
ФОРМЫ = ("мера", "сумма", "прибыль", "убыль")
_ПАКЕТ = {}


def _пакет(язык):
    if язык not in _ПАКЕТ:
        _ПАКЕТ[язык] = json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return _ПАКЕТ[язык]


def _индекс(язык, формы, n):
    """Which count form n selects: one form — always it; two — one/many; three — the pack's rule."""
    if len(формы) == 1:
        return 0
    if len(формы) == 2:
        return 0 if n == 1 else 1
    return langpack.count_form_index(_пакет(язык), {"forms": ["one", "few", "many"]}, n)


def счётная(язык, формы, n):
    return формы[_индекс(язык, формы, n)]


def _глагол(язык, г, деятель):
    формы = ЯЗЫКИ[язык]["глаголы"][г]
    if len(формы) == 4:                       # Polish: (m, f, bare, kind) — bends with the actor
        род = ЯЗЫКИ[язык]["деятели"][деятель][1]
        return (формы[0] if род == "m" else формы[1]), формы[2], формы[3]
    return формы[0], формы[1], формы[2]


def _пр(язык, вид):
    return ЯЗЫКИ[язык]["пр"].get(вид, "")


def страница(язык, форма, i):
    я = ЯЗЫКИ[язык]
    if форма in ("мера", "сумма"):
        деятель = i % len(я["деятели"]); г = (i // len(я["деятели"])) % len(я["глаголы"])
        A = я["деятели"][деятель][0]
        Гп, Гб, вид = _глагол(язык, г, деятель)
        ед = я["единицы"][вид][i % len(я["единицы"][вид])]
        ПР = _пр(язык, вид)
        if форма == "мера":
            n = ЧИСЛА_МЕРЫ[i % len(ЧИСЛА_МЕРЫ)]
            факт = я["факт"].format(A=A, Гп=Гп, ПР=ПР, n=n, ЕДn=счётная(язык, ед, n))
            воп = я["вопрос"][вид].format(A=A, Гп=Гп, Гб=Гб, ЕДмн=счётная(язык, ед, 5))
            return f"{факт} {воп} {я['ответ'].format(ПР=ПР, n=n, ЕДn=счётная(язык, ед, n))}"
        a, b = ПАРЫ_СУММЫ[i % len(ПАРЫ_СУММЫ)]; s = a + b
        факт = я["сумма_факт"].format(A=A, Гп=Гп, ПР=ПР, a=a, ЕДa=счётная(язык, ед, a), b=b, ЕДb=счётная(язык, ед, b))
        воп = я["сумма_вопрос"][вид].format(A=A, Гп=Гп, Гб=Гб, ЕДмн=счётная(язык, ед, 5))
        return f"{факт} {воп} {я['сумма_ответ'].format(ПР=ПР, s=s, ЕДs=счётная(язык, ед, s), a=a, b=b)}"
    формы_н, ГДЕ, были, пришли, ушли = я["носители"][i % len(я["носители"])]
    n, k = НОСИТЕЛИ_ЧИСЛА[i % len(НОСИТЕЛИ_ЧИСЛА)]
    прибыль = форма == "прибыль"
    if not прибыль and k > n:
        n, k = k, n
    r = n + k if прибыль else n - k
    гл = lambda формы, c: формы[0] if len(формы) == 1 else формы[0 if _индекс(язык, ("a", "b", "c"), c) == 1 else 1]
    было = я["было"].format(ГДЕ=ГДЕ, БЫЛИ=гл(были, n), n=n, Нn=счётная(язык, формы_н, n))
    ход = (я["прибыль"].format(k=k, Нk=счётная(язык, формы_н, k), ПРИШЛИ=гл(пришли, k)) if прибыль
           else я["убыль"].format(k=k, Нk=счётная(язык, формы_н, k), УШЛИ=гл(ушли, k)))
    # French «de» contracts before a vowel: «combien d'oiseaux», «combien de bateaux» — declared rule
    ДЕ = ("d'" if формы_н[-1][:1].lower() in "aeiouyhéèê" else "de ") if язык == "fr" else ""
    воп = я["носители_вопрос"].format(Нмн=формы_н[-1], ГДЕ=ГДЕ, ДЕ=ДЕ)
    отв = я["носители_ответ"].format(r=r, Нr=счётная(язык, формы_н, r), n=n, знак="+" if прибыль else "−", k=k)
    return f"{было} {ход} {воп} {отв}"


def _показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for форма in ФОРМЫ:
            шагов = len(я["деятели"]) * len(я["глаголы"]) * 3 if форма in ("мера", "сумма") else len(я["носители"]) * 3
            for i in range(шагов):
                вон[страница(язык, форма, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _alt(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"


def _образцы():
    вон = []
    for язык, я in ЯЗЫКИ.items():
        деятели = _alt(д[0] for д in я["деятели"])
        прош = _alt(г[0] for г in я["глаголы"]) if len(я["глаголы"][0]) == 3 else _alt(ф for г in я["глаголы"] for ф in г[:2])
        единицы = _alt(ф for вид in я["единицы"].values() for ряд in вид for ф in ряд)
        пр = "(?:" + "|".join(re.escape(п) for п in set(я["пр"].values())) + ")?" if я["пр"] else ""
        ч = r"(\d+)"
        дыры = {"A": "(" + деятели + ")", "Гп": "(" + прош + ")", "ПР": пр, "n": ч, "a": ч, "b": ч, "s": ч, "k": ч, "r": ч,
                "ЕДn": "(" + единицы + ")", "ЕДa": "(" + единицы + ")", "ЕДb": "(" + единицы + ")", "ЕДs": "(" + единицы + ")", "ЕДмн": "(" + единицы + ")",
                "Нn": "(" + _alt(ф for н in я["носители"] for ф in н[0]) + ")", "Нk": "(" + _alt(ф for н in я["носители"] for ф in н[0]) + ")",
                "Нr": "(" + _alt(ф for н in я["носители"] for ф in н[0]) + ")", "Нмн": "(" + _alt(н[0][-1] for н in я["носители"]) + ")",
                "ГДЕ": "(" + _alt(н[1] for н in я["носители"]) + ")", "БЫЛИ": "(" + _alt(ф for н in я["носители"] for ф in н[2]) + ")",
                "ПРИШЛИ": "(" + _alt(ф for н in я["носители"] for ф in н[3]) + ")", "УШЛИ": "(" + _alt(ф for н in я["носители"] for ф in н[4]) + ")",
                "знак": "([+−])", "ДЕ": "(?:de |d')"}
        for вид in ("длина", "вес"):
            мера = я["факт"] + " " + я["вопрос"][вид] + " " + я["ответ"]
            сумма = я["сумма_факт"] + " " + я["сумма_вопрос"][вид] + " " + я["сумма_ответ"]
            вон.append((re.compile("^" + phrases.образец(мера, дыры) + "$"), язык, "мера", phrases.порядок(мера)))
            вон.append((re.compile("^" + phrases.образец(сумма, дыры) + "$"), язык, "сумма", phrases.порядок(сумма)))
        for форма, ход in (("прибыль", я["прибыль"]), ("убыль", я["убыль"])):
            ш = я["было"] + " " + ход + " " + я["носители_вопрос"] + " " + я["носители_ответ"]
            вон.append((re.compile("^" + phrases.образец(ш, дыры) + "$"), язык, форма, phrases.порядок(ш)))
    return вон


ОБРАЗЦЫ = _образцы()


def _вид_единицы(язык, слово):
    for вид, ряды in ЯЗЫКИ[язык]["единицы"].items():
        for ряд in ряды:
            if слово in ряд:
                return вид, ряд
    return None, None


def _вид_глагола(язык, слово):
    for г in ЯЗЫКИ[язык]["глаголы"]:
        if слово in г[:-2] or слово == g_bare(г):
            return г[-1]
    return None


def g_bare(г):
    return г[-2]


def судить(строка):
    """(судимо, истинно): a page of the house; a line of its frame with the unit not of the
    verb's kind, a count form not of its number, or a sum that does not hold — a lie."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, порядок in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        г = dict(zip([п for п in порядок if п not in ("ПР", "ДЕ")], м.groups()))
        if форма in ("мера", "сумма"):
            вид = _вид_глагола(язык, г["Гп"])
            ключи = ("ЕДn",) if форма == "мера" else ("ЕДa", "ЕДb", "ЕДs")
            for ключ in ключи:
                в, ряд = _вид_единицы(язык, г[ключ])
                if в != вид:
                    return True, False
                число = int(г[ключ[2:]]) if ключ != "ЕДs" else int(г["s"])
                if г[ключ] != счётная(язык, ряд, число):
                    return True, False
            if форма == "сумма":
                return True, int(г["a"]) + int(г["b"]) == int(г["s"])
            return True, True
        n, k, r = int(г["n"]), int(г["k"]), int(г["r"])
        ряд = next((н[0] for н in ЯЗЫКИ[язык]["носители"] if г["Нn"] in н[0]), None)
        if ряд is None or г["Нk"] not in ряд or г["Нr"] not in ряд:
            return True, False
        if (г["Нn"], г["Нk"], г["Нr"]) != (счётная(язык, ряд, n), счётная(язык, ряд, k), счётная(язык, ряд, r)):
            return True, False
        return True, r == (n + k if форма == "прибыль" else n - k)
    return False, False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for язык in ЯЗЫКИ:
        с = страница(язык, "сумма", 0)
        битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
        assert судить(битая) == (True, False), битая
        с = страница(язык, "прибыль", 0)
        битая = re.sub(r"= (\d+)\.$", lambda м: f"= {int(м.group(1)) + 1}.", с)
        assert судить(битая) == (True, False), битая
        мутанты += 2
    for язык in ("de", "fr", "pl"):
        print("  ", страница(язык, "мера", 0)); print("  ", страница(язык, "прибыль", 0))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
