#!/usr/bin/env python3
"""THE HOUSE OF MONEY STORIES — a page of money in three languages.

e9's order (03.09, the organ of money, wave 8): the market bought the
bridges «$3.40 is 340 cents» from the money world, but the stories of money
were mute — the svod showed no PAGE «tom has $5.20. he spends $1.50. how
much money does he have now? 520 − 150 = 370 cents. 370 cents is $3.70.»:
the signs of the money verbs (spends/spent, pays/paid — minus; earns/earned,
saves/saved — plus) were never bought, the act with a price («buys a pen
for $1.50» — the number after «for», not after the verb) never shown, and
«money» never stood as the asked head over facts in dollars and cents.

This house declares, per language (en, ru, de), the fact of holding in two
holdings, the verbs with their signs as phrases around the amount, the
purchase with a price, the three questions (now / left / how much does X
have), the ledger in the small unit and the bridge back to the decimal
writing. The generator fills the holes; the court turns the same templates
into patterns, reads the holes back, REGENERATES the page and compares it
letter by letter — a wrong sign, a wrong form of the kopeck, a pronoun of
the wrong gender, a corrupted name, is a page the house would not write.
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


def _лица(язык):
    """(name, gender, genitive) of the declared persons of the pack — the
    first sixteen with a declared gender (the money world takes sixteen)."""
    п = _пакет(язык)
    формы = п.get("person_forms") or {}
    вон = []
    for имя in п.get("person_names", ()):
        ф = формы.get(имя) or formы_guess(формы, имя)
        if not ф or ф.get("gender") not in ("m", "f"):
            continue
        показ = имя.capitalize() if язык == "ru" else имя
        род = (ф.get("gen") or "").capitalize() if язык == "ru" else показ
        вон.append((показ, ф["gender"], род))
        if len(вон) == 16:
            break
    return tuple(вон)


def formы_guess(формы, имя):
    return формы.get(имя.lower()) or формы.get(имя.capitalize())


# per language: the holdings (key → fact template), the verbs (key → sign,
# phrase template around the amount; a Russian past tense bends by gender),
# the purchase, the three questions, the ledger, the bridge, the pronouns,
# the things of the purchase (en a-form / ru accusative / de with article)
ЯЗЫКИ = {
    "en": dict(
        держит={"has": "{X} has {A}.", "holds": "{X} holds {A}."},
        глаголы={"spends": ("−", "spends {B}"), "spent": ("−", "spent {B}"), "pays": ("−", "pays {B}"), "paid": ("−", "paid {B}"),
                 "earns": ("+", "earns {B}"), "earned": ("+", "earned {B}"), "saves": ("+", "saves {B}"), "saved": ("+", "saved {B}")},
        акт="{он} {V}.", покупка="{он} buys a {Т} for {B}.",
        теперь="how much money does {он} have now?", осталось="how much money is left?", имеет="how much money does {X} have?",
        леджер="{a} {S} {b} = {r} cents.", мост="{r} cents is {R}.",
        он={"m": "he", "f": "she"}, вещи=("pen", "book", "apple", "pencil", "cup"),
    ),
    "ru": dict(
        держит={"у": "у {Xр} {A}.", "имеет": "{X} имеет {A}."},
        глаголы={"тратит": ("−", "тратит {B}"), "потратил": ("−", {"m": "потратил {B}", "f": "потратила {B}"}),
                 "платит": ("−", "платит {B}"), "заплатил": ("−", {"m": "заплатил {B}", "f": "заплатила {B}"}),
                 "зарабатывает": ("+", "зарабатывает {B}"), "заработал": ("+", {"m": "заработал {B}", "f": "заработала {B}"}),
                 "откладывает": ("+", "откладывает {B}"), "отложил": ("+", {"m": "отложил {B}", "f": "отложила {B}"})},
        акт="{он} {V}.", покупка="{он} покупает {Т} за {B}.",
        теперь="сколько денег {у_него} теперь?", осталось="сколько денег осталось?", имеет="сколько денег у {Xр}?",
        леджер="{a} {S} {b} = {r} {м}.", мост="{r} {м} — это {R}.",
        он={"m": "он", "f": "она"}, у_него={"m": "у него", "f": "у неё"}, вещи=("ручку", "книгу", "яблоко", "карандаш", "чашку"),
    ),
    "de": dict(
        держит={"hat": "{X} hat {A}.", "besitzt": "{X} besitzt {A}."},
        глаголы={"gibt aus": ("−", "gibt {B} aus"), "gab aus": ("−", "gab {B} aus"), "bezahlt": ("−", "bezahlt {B}"), "bezahlte": ("−", "bezahlte {B}"),
                 "verdient": ("+", "verdient {B}"), "verdiente": ("+", "verdiente {B}"), "spart": ("+", "spart {B}"), "sparte": ("+", "sparte {B}")},
        акт="{он} {V}.", покупка="{он} kauft {Т} für {B}.",
        теперь="wie viel Geld hat {он} jetzt?", осталось="wie viel Geld bleibt übrig?", имеет="wie viel Geld hat {X}?",
        леджер="{a} {S} {b} = {r} Cent.", мост="{r} Cent sind {R}.",
        он={"m": "er", "f": "sie"}, вещи=("einen Stift", "ein Buch", "einen Apfel", "einen Bleistift", "eine Tasse"),
    ),
}
ЛИЦА = {язык: _лица(язык) for язык in ЯЗЫКИ}
СЕМЕЙСТВА = ("акт", "покупка", "имеет")
ВОПРОСЫ_АКТА = ("теперь", "осталось")


def сумма(язык, d, c, k=0):
    """The decimal writing of d units and c cents: «$5.20» / «5.20 dollars»
    (k odd / even — the two writings of the money world), «5 рублей 20
    копеек», «5,20 Euro»."""
    if язык == "en":
        return f"${d}.{c:02d}" if k % 2 else f"{d}.{c:02d} dollars"
    if язык == "ru":
        return f"{d} {rugram.форма('рубль', d)} {c} {rugram.форма('копейка', c)}"
    return f"{d},{c:02d} Euro"


def _мелкая_ru(n):
    return rugram.форма("копейка", n)


def _глагол(язык, ключ, пол):
    знак, фраза = ЯЗЫКИ[язык]["глаголы"][ключ]
    return знак, (фраза[пол] if isinstance(фраза, dict) else фраза)


def страница(язык, сем, имя, держ, k=0, A=None, B=None, глагол=None, вопрос="теперь", вещь=0):
    """The page as the house writes it. A, B — (units, cents)."""
    я = ЯЗЫКИ[язык]
    лицо = next(л for л in ЛИЦА[язык] if л[0] == имя)
    X, пол, Xр = лицо
    он = я["он"][пол]
    з = dict(X=X, Xр=Xр, он=он, у_него=я.get("у_него", {}).get(пол, ""))
    факт = я["держит"][держ].format(A=сумма(язык, *A, k), **з)
    if сем == "имеет":
        return f"{факт} {я['имеет'].format(**з)} {факт}"
    a = A[0] * 100 + A[1]
    b = B[0] * 100 + B[1]
    if сем == "покупка":
        знак = "−"
        акт = я["покупка"].format(Т=я["вещи"][вещь], B=сумма(язык, *B, k), **з)
    else:
        знак, фраза = _глагол(язык, глагол, пол)
        акт = я["акт"].format(V=фраза.format(B=сумма(язык, *B, k)), **з)
    r = a - b if знак == "−" else a + b
    м = _мелкая_ru(r) if язык == "ru" else ""
    леджер = я["леджер"].format(a=a, S=знак, b=b, r=r, м=м)
    мост = я["мост"].format(r=r, м=м, R=сумма(язык, r // 100, r % 100, k))
    return f"{факт} {акт} {я[вопрос].format(**з)} {леджер} {мост}"


# --- the court's side: the same templates as patterns ---
_СУММА = {"en": r"(?:\$\d+\.\d\d|\d+\.\d\d dollars)", "ru": r"\d+ рубл(?:ь|я|ей) \d+ копе(?:йка|йки|ек)", "de": r"\d+,\d\d Euro"}


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    лица = ЛИЦА[язык]
    фразы = []
    for ключ, (знак, фраза) in я["глаголы"].items():
        for ф in (фраза.values() if isinstance(фраза, dict) else (фраза,)):
            фразы.append(phrases.образец(ф, {"B": _СУММА[язык]}))
    return {"X": "(" + _альт([л[0] for л in лица]) + ")", "Xр": "(" + _альт([л[2] for л in лица]) + ")",
            "он": "(" + _альт(я["он"].values()) + ")", "у_него": "(" + _альт(я.get("у_него", {"m": "у него"}).values()) + ")",
            "A": "(" + _СУММА[язык] + ")", "B": "(" + _СУММА[язык] + ")", "R": "(" + _СУММА[язык] + ")",
            "V": "(" + "|".join(sorted(set(фразы), key=len, reverse=True)) + ")", "Т": "(" + _альт(я["вещи"]) + ")",
            "a": r"(\d+)", "b": r"(\d+)", "r": r"(\d+)", "S": r"([−+])", "м": r"(копе(?:йка|йки|ек))"}


def _шаблоны(язык):
    """(family, holding, question, template) for every page shape."""
    я = ЯЗЫКИ[язык]
    вон = []
    for держ, факт in я["держит"].items():
        вон.append(("имеет", держ, "имеет", f"{факт} {я['имеет']} {факт}"))
        for вопрос in ВОПРОСЫ_АКТА:
            вон.append(("акт", держ, вопрос, f"{факт} {я['акт']} {я[вопрос]} {я['леджер']} {я['мост']}"))
        вон.append(("покупка", держ, "теперь", f"{факт} {я['покупка']} {я['теперь']} {я['леджер']} {я['мост']}"))
    return вон


def образцы(язык):
    дыры = _дыры(язык)
    return [(re.compile("^" + phrases.образец(ш, дыры) + "$"), phrases.порядок(ш), сем, держ, вопрос)
            for сем, держ, вопрос, ш in _шаблоны(язык)]


ОБРАЗЦЫ = {язык: образцы(язык) for язык in ЯЗЫКИ}


def _читать_сумму(язык, з):
    """(units, cents, k) from the writing."""
    числа = [int(x) for x in re.findall(r"\d+", з)]
    return числа[0], числа[1], (1 if з.startswith("$") else 0)


def разобрать(язык, строка):
    """The parameters of the page, or None — not a page of this house."""
    я = ЯЗЫКИ[язык]
    for образец, имена, сем, держ, вопрос in ОБРАЗЦЫ[язык]:
        м = образец.match(строка)
        if not м:
            continue
        з = {}
        for имя, г in zip(имена, м.groups()):
            if имя in з and з[имя] != г:
                return None  # a repeated hole filled twice differently
            з[имя] = г
        if "Xр" in з and "X" not in з:
            з["X"] = next((л[0] for л in ЛИЦА[язык] if л[2] == з["Xр"]), None)
        if з.get("X") is None:
            return None
        d, c, k = _читать_сумму(язык, з["A"])
        п = dict(сем=сем, имя=з["X"], держ=держ, k=k, A=(d, c), вопрос=вопрос)
        if сем == "имеет":
            return п
        if сем == "покупка":
            d2, c2, _ = _читать_сумму(язык, з["B"])
            п["B"] = (d2, c2)
            п["вещь"] = я["вещи"].index(з["Т"])
            return п
        # the verb key by its phrase — the amount stands inside the phrase
        # («gibt 1,42 Euro aus»), so it is read from the phrase itself
        for ключ, (знак, фраза) in я["глаголы"].items():
            for ф in (фраза.values() if isinstance(фраза, dict) else (фраза,)):
                м2 = re.fullmatch(phrases.образец(ф, {"B": "(" + _СУММА[язык] + ")"}), з["V"])
                if м2:
                    d2, c2, _ = _читать_сумму(язык, м2.group(1))
                    п["глагол"] = ключ
                    п["B"] = (d2, c2)
                    return п
        return None
    return None


def судить(строка):
    """(судимо, истинно): a page of the house, true when the house writes it so."""
    с = строка.strip()
    for язык in ЯЗЫКИ:
        п = разобрать(язык, с)
        if п is not None:
            try:
                return True, страница(язык, **п) == с
            except (StopIteration, KeyError, IndexError, ValueError):
                return True, False
    return False, False
