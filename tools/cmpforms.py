#!/usr/bin/env python3
"""THE HOUSE OF COMPARISON PHRASES — «more than» and «times as many» in
eight languages.

The comparison worlds say «mark has 12 coins and kate has 4 coins; mark has
8 more coins than kate: 12 − 4 = 8» and «… three times as many …: 12 ÷ 4 =
3» in en/ru. This house says both in de/fr/es/it/pt/nl/pl/tr — statement
and question answered by the statement (М-153) — with the actors from the
packs, the things with their count forms, and the multiplier said by the
language's own word (dreimal, trois fois, tres veces, tre volte, três vezes,
drie keer, trzy razy, üç kat). Generator and court read one table through
tools/phrases.py; the difference and the ratio are recomputed.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holes  # noqa: E402
import phrases  # noqa: E402

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]

# things: (one, many) — pl (one, few, many) — tr bare
ВЕЩИ = {
    "de": (("Apfel", "Äpfel"), ("Buch", "Bücher"), ("Stift", "Stifte"), ("Münze", "Münzen")),
    "fr": (("pomme", "pommes"), ("livre", "livres"), ("stylo", "stylos"), ("pièce", "pièces")),
    "es": (("manzana", "manzanas"), ("libro", "libros"), ("bolígrafo", "bolígrafos"), ("moneda", "monedas")),
    "it": (("mela", "mele"), ("libro", "libri"), ("penna", "penne"), ("moneta", "monete")),
    "pt": (("maçã", "maçãs"), ("livro", "livros"), ("caneta", "canetas"), ("moeda", "moedas")),
    "nl": (("appel", "appels"), ("boek", "boeken"), ("pen", "pennen"), ("munt", "munten")),
    "pl": (("jabłko", "jabłka", "jabłek"), ("książka", "książki", "książek"), ("długopis", "długopisy", "długopisów"), ("moneta", "monety", "monet")),
    "tr": (("elma",), ("kitap",), ("kalem",), ("top",)),
}
# the multiplier by its word, k = 2..5
КРАТНО = {
    "de": {2: "zweimal", 3: "dreimal", 4: "viermal", 5: "fünfmal"},
    "fr": {2: "deux fois", 3: "trois fois", 4: "quatre fois", 5: "cinq fois"},
    "es": {2: "dos veces", 3: "tres veces", 4: "cuatro veces", 5: "cinco veces"},
    "it": {2: "due volte", 3: "tre volte", 4: "quattro volte", 5: "cinque volte"},
    "pt": {2: "duas vezes", 3: "três vezes", 4: "quatro vezes", 5: "cinco vezes"},
    "nl": {2: "twee keer", 3: "drie keer", 4: "vier keer", 5: "vijf keer"},
    "pl": {2: "dwa razy", 3: "trzy razy", 4: "cztery razy", 5: "pięć razy"},
    "tr": {2: "iki kat", 3: "üç kat", 4: "dört kat", 5: "beş kat"},
}
# {A} {B} actors, {x} {y} the counts, {в} the thing beside x, {вy} beside y,
# {d} the difference, {вd} the thing beside d, {вм} the thing (many) of the
# question, {к} the multiplier word, {k} the ratio
ФРАЗЫ = {
    "de": dict(факт="{A} hat {x} {в} und {B} hat {y} {вy}",
               больше="{факт}; {A} hat {d} {вd} mehr als {B}: {x} − {y} = {d}.", в_больше="wie viele {вм} hat {A} mehr als {B}?",
               кратно="{факт}; {A} hat {к} so viele {вм} wie {B}: {x} ÷ {y} = {k}.", в_кратно="wievielmal so viele {вм} wie {B} hat {A}?"),
    "fr": dict(факт="{A} a {x} {в} et {B} a {y} {вy}",
               больше="{факт} ; {A} a {d} {вd} de plus que {B} : {x} − {y} = {d}.", в_больше="combien de {вм} {A} a-t-{он} de plus que {B} ?",
               кратно="{факт} ; {A} a {к} plus de {вм} que {B} : {x} ÷ {y} = {k}.", в_кратно="combien de fois {A} a-t-{он} plus de {вм} que {B} ?"),
    "es": dict(факт="{A} tiene {x} {в} y {B} tiene {y} {вy}",
               больше="{факт}; {A} tiene {d} {вd} más que {B}: {x} − {y} = {d}.", в_больше="¿cuántos {вм} más que {B} tiene {A}?",
               кратно="{факт}; {A} tiene {к} más {вм} que {B}: {x} ÷ {y} = {k}.", в_кратно="¿cuántas veces más {вм} que {B} tiene {A}?"),
    "it": dict(факт="{A} ha {x} {в} e {B} ha {y} {вy}",
               больше="{факт}; {A} ha {d} {вd} in più di {B}: {x} − {y} = {d}.", в_больше="quanti {вм} in più di {B} ha {A}?",
               кратно="{факт}; {A} ha {к} più {вм} di {B}: {x} ÷ {y} = {k}.", в_кратно="quante volte più {вм} di {B} ha {A}?"),
    "pt": dict(факт="{A} tem {x} {в} e {B} tem {y} {вy}",
               больше="{факт}; {A} tem {d} {вd} a mais do que {B}: {x} − {y} = {d}.", в_больше="quantos {вм} a mais do que {B} tem {A}?",
               кратно="{факт}; {A} tem {к} mais {вм} do que {B}: {x} ÷ {y} = {k}.", в_кратно="quantas vezes mais {вм} do que {B} tem {A}?"),
    "nl": dict(факт="{A} heeft {x} {в} en {B} heeft {y} {вy}",
               больше="{факт}; {A} heeft {d} {вd} meer dan {B}: {x} − {y} = {d}.", в_больше="hoeveel {вм} heeft {A} meer dan {B}?",
               кратно="{факт}; {A} heeft {к} zoveel {вм} als {B}: {x} ÷ {y} = {k}.", в_кратно="hoeveel keer zoveel {вм} als {B} heeft {A}?"),
    "pl": dict(факт="{A} ma {x} {в}, a {B} ma {y} {вy}",
               больше="{факт}; {A} ma o {d} {вd} więcej niż {B}: {x} − {y} = {d}.", в_больше="o ile {вм} więcej niż {B} ma {A}?",
               кратно="{факт}; {A} ma {к} więcej {вм} niż {B}: {x} ÷ {y} = {k}.", в_кратно="ile razy więcej {вм} niż {B} ma {A}?"),
    # Turkish holds with «var» and the names in the locative («Ayşe'de»),
    # the ablative («Ömer'den») and the genitive («Ömer'in») — suffixes by
    # vowel harmony and devoicing, written with the apostrophe as Turkish
    # writes suffixes on proper names
    "tr": dict(факт="{Aм} {x} {в} var ve {Bм} {y} {вy} var",
               больше="{факт}; {Aм} {Bот} {d} {вd} fazla var: {x} − {y} = {d}.", в_больше="{Aм} {Bот} kaç {вм} fazla var?",
               кратно="{факт}; {Aм} {Bр} {к}ı kadar {вм} var: {x} ÷ {y} = {k}.", в_кратно="{Aм} {Bр} kaç katı kadar {вм} var?"),
}


_ГЛАСНЫЕ = "aeıioöuü"
_ГЛУХИЕ = "pçtkfsşh"


def _последняя_гласная(слово):
    return next((б for б in reversed(слово.lower()) if б in _ГЛАСНЫЕ), "e")


def тр_суффикс(имя, падеж):
    """The Turkish name with its case suffix after the apostrophe:
    locative «de/da» (te/ta after a voiceless consonant), ablative
    «den/dan» (ten/tan), genitive «in/ın/un/ün» (nin/… after a vowel)."""
    г = _последняя_гласная(имя)
    задняя = г in "aıou"
    глухая = имя[-1].lower() in _ГЛУХИЕ
    if падеж == "gen":
        у = {"a": "ı", "ı": "ı", "e": "i", "i": "i", "o": "u", "u": "u", "ö": "ü", "ü": "ü"}[г]
        return f"{имя}'{'n' if имя[-1].lower() in _ГЛАСНЫЕ else ''}{у}n"
    согл = ("t" if глухая else "d")
    return f"{имя}'{согл}{'a' if задняя else 'e'}{'n' if падеж == 'abl' else ''}"


def _имена():
    вон = {}
    for язык in ВЕЩИ:
        п = json.loads((КОРЕНЬ / "tools" / "langpacks" / f"{язык}.json").read_text(encoding="utf-8"))
        вон[язык] = tuple(п["person_names"][:16])
    return вон


def _род():
    п = json.loads((КОРЕНЬ / "tools" / "langpacks" / "fr.json").read_text(encoding="utf-8"))
    return {н: ф["gender"] for н, ф in п["person_forms"].items()}


ИМЕНА = _имена()
РОД_FR = _род()


def вещь(язык, в, n):
    if язык == "tr":
        return в[0]
    if язык == "pl":
        return в[("one", "few", "many").index(holes.форма_счёта("pl", n))]
    return в[0] if n == 1 else в[1]


def _много(язык, в):
    return в[-1] if язык != "pl" else в[2]


def _роли(язык, A, B):
    """The actors in every form a phrase may ask for."""
    р = dict(A=A, B=B)
    if язык == "tr":
        р.update(Aм=тр_суффикс(A, "loc"), Bм=тр_суффикс(B, "loc"), Bот=тр_суффикс(B, "abl"), Bр=тр_суффикс(B, "gen"))
    if язык == "fr":
        р["он"] = "elle" if РОД_FR.get(A) == "f" else "il"
    return р


def _факт(язык, A, B, x, y, в):
    return ФРАЗЫ[язык]["факт"].format(x=x, y=y, в=вещь(язык, в, x), вy=вещь(язык, в, y), **_роли(язык, A, B))


def больше(язык, A, B, x, y, в):
    d = x - y
    return ФРАЗЫ[язык]["больше"].format(факт=_факт(язык, A, B, x, y, в), d=d, вd=вещь(язык, в, d), x=x, y=y, **_роли(язык, A, B))


def вопрос_больше(язык, A, B, x, y, в):
    return f"{ФРАЗЫ[язык]['в_больше'].format(вм=_много(язык, в), **_роли(язык, A, B))} {больше(язык, A, B, x, y, в)}"


def кратно(язык, A, B, x, y, в):
    k = x // y
    return ФРАЗЫ[язык]["кратно"].format(факт=_факт(язык, A, B, x, y, в), к=КРАТНО[язык][k], вм=_много(язык, в), x=x, y=y, k=k, **_роли(язык, A, B))


def вопрос_кратно(язык, A, B, x, y, в):
    return f"{ФРАЗЫ[язык]['в_кратно'].format(вм=_много(язык, в), **_роли(язык, A, B))} {кратно(язык, A, B, x, y, в)}"


def _дыры(язык):
    имя = "(" + "|".join(re.escape(и) for и in ИМЕНА[язык]) + ")"
    формы = sorted({ф for в in ВЕЩИ[язык] for ф in в}, key=len, reverse=True)
    слово = "(" + "|".join(re.escape(ф) for ф in формы) + ")"
    к = "(" + "|".join(re.escape(с) for с in sorted(КРАТНО[язык].values(), key=len, reverse=True)) + ")"
    д = {"A": имя, "B": имя, "x": r"(\d+)", "y": r"(\d+)", "в": слово, "вy": слово, "d": r"(\d+)", "вd": слово, "вм": слово, "к": к, "k": r"(\d+)", "он": "(il|elle)"}
    if язык == "tr":
        for ключ, падеж in (("Aм", "loc"), ("Bм", "loc"), ("Bот", "abl"), ("Bр", "gen")):
            д[ключ] = "(" + "|".join(re.escape(тр_суффикс(и, падеж)) for и in ИМЕНА[язык]) + ")"
    return д


def образцы(язык):
    я = ЯЗЫКИ = ФРАЗЫ[язык]
    д = _дыры(язык)
    факт = phrases.образец(я["факт"], д)
    вон = []
    for вид in ("больше", "кратно"):
        утв = phrases.образец(я[вид].replace("{факт}", "\x00"), д).replace(re.escape("\x00"), факт)
        вон.append((re.compile("^" + утв + "$"), вид, False))
        вон.append((re.compile("^" + phrases.образец(я["в_" + вид], д) + " " + утв + "$"), вид, True))
    return вон


def _порядок(язык, вид):
    я = ФРАЗЫ[язык]
    return [и if и != "факт" else None for и in phrases.порядок(я[вид])]


def судить_группы(язык, вид, спрошено, группы):
    я = ФРАЗЫ[язык]
    г = list(группы)
    спрош = {}
    if спрошено:
        имена = phrases.порядок(я["в_" + вид])
        спрош = dict(zip(имена, г[:len(имена)])); г = г[len(имена):]
    # A HOLE NAMED TWICE MUST BE FILLED TWICE THE SAME («{d} … = {d}»): the
    # head's value and the ledger's value are one number, or the line lies.
    з, дважды = {}, []
    имена = []
    for имя in phrases.порядок(я[вид]):
        имена.extend(phrases.порядок(я["факт"]) if имя == "факт" else [имя])
    for имя in имена:
        значение = г.pop(0)
        if имя in з and з[имя] != значение:
            return False
        з[имя] = значение
    if язык == "tr":
        A = next(и for и in ИМЕНА["tr"] if тр_суффикс(и, "loc") == з["Aм"])
        B = next(и for и in ИМЕНА["tr"] if тр_суффикс(и, "loc") == з["Bм"])
        if з.get("Bот", тр_суффикс(B, "abl")) != тр_суффикс(B, "abl") or з.get("Bр", тр_суффикс(B, "gen")) != тр_суффикс(B, "gen"):
            return False
        з["A"], з["B"] = A, B
        спрош = {("A" if к == "Aм" else "B" if к in ("Bм", "Bот", "Bр") else к): (A if к == "Aм" else B if к in ("Bм", "Bот", "Bр") else v) for к, v in спрош.items()}
    A, B, x, y = з["A"], з["B"], int(з["x"]), int(з["y"])
    if A == B or x <= y:
        return False
    if язык == "fr" and "он" in спрош and спрош["он"] != ("elle" if РОД_FR.get(A) == "f" else "il"):
        return False
    в = next((в for в in ВЕЩИ[язык] if з["в"] in в), None)
    if в is None or з["в"] != вещь(язык, в, x) or з["вy"] != вещь(язык, в, y):
        return False
    if вид == "больше":
        d = x - y
        if int(з["d"]) != d or з["вd"] != вещь(язык, в, d):
            return False
    else:
        if x % y or x // y not in КРАТНО[язык] or з["к"] != КРАТНО[язык][x // y] or int(з["k"]) != x // y or з["вм"] != _много(язык, в):
            return False
    if спрош:
        if спрош.get("A") != A or спрош.get("B") != B or спрош.get("вм") != _много(язык, в):
            return False
    return True
