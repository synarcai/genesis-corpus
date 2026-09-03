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
        # genus 3 of g1 (e9): a rate toward a goal, a sum of products
        ставка="{X} has {A}. {он} earns {B} per day. a {Ц} costs {C}. how many days does {он} need?",
        цели=("bike", "phone", "guitar", "tablet", "camera"),
        покупка1="{X} buys {n1} {Т1} at {P1} each. how much does {он} pay in all?",
        покупка2="{X} buys {n1} {Т1} at {P1} each and {n2} {Т2} at {P2} each. how much does {он} pay in all?",
        товары=("pens", "books", "cups", "pencils", "apples"),
        один_товар=("one pen", "one book", "one cup", "one pencil", "one apple"),
        покупка3="{X} buys {n1} {Т1}, {n2} {Т2} and {n3} {Т3}. {О1} costs {P1}, {О2} costs {P2}, {О3} costs {P3}. how much does {он} pay in all?",
        леджер_ставки="{c} − {a} = {r1}, {r1} ÷ {b} = {n}. so the answer is {n}.",
        леджер_покупки="{л} cents.",
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
        ставка="у {Xр} {A}. {он} зарабатывает {B} в день. {Ц} стоит {C}. сколько дней {ему} нужно?",
        ему={"m": "ему", "f": "ей"},
        цели=("велосипед", "телефон", "гитара", "планшет", "фотоаппарат"),
        покупка1="{X} покупает {n1} {Т1} по цене {P1} за штуку. сколько {он} платит всего?",
        покупка2="{X} покупает {n1} {Т1} по цене {P1} за штуку и {n2} {Т2} по цене {P2} за штуку. сколько {он} платит всего?",
        товары=("ручка", "книга", "чашка", "карандаш", "яблоко"),
        один_товар=("одна ручка", "одна книга", "одна чашка", "один карандаш", "одно яблоко"),
        покупка3="{X} покупает {n1} {Т1}, {n2} {Т2} и {n3} {Т3}. {О1} стоит {P1}, {О2} стоит {P2}, {О3} стоит {P3}. сколько {он} платит всего?",
        леджер_ставки="{c} − {a} = {r1}, {r1} ÷ {b} = {n}. значит ответ: {n}.",
        леджер_покупки="{л} {м}.",
    ),
    "de": dict(
        держит={"hat": "{X} hat {A}.", "besitzt": "{X} besitzt {A}."},
        глаголы={"gibt aus": ("−", "gibt {B} aus"), "gab aus": ("−", "gab {B} aus"), "bezahlt": ("−", "bezahlt {B}"), "bezahlte": ("−", "bezahlte {B}"),
                 "verdient": ("+", "verdient {B}"), "verdiente": ("+", "verdiente {B}"), "spart": ("+", "spart {B}"), "sparte": ("+", "sparte {B}")},
        акт="{он} {V}.", покупка="{он} kauft {Т} für {B}.",
        теперь="wie viel Geld hat {он} jetzt?", осталось="wie viel Geld bleibt übrig?", имеет="wie viel Geld hat {X}?",
        леджер="{a} {S} {b} = {r} Cent.", мост="{r} Cent sind {R}.",
        он={"m": "er", "f": "sie"}, вещи=("einen Stift", "ein Buch", "einen Apfel", "einen Bleistift", "eine Tasse"),
        ставка="{X} hat {A}. {он} verdient {B} pro Tag. {Ц} kostet {C}. wie viele Tage braucht {он}?",
        цели=("ein Fahrrad", "ein Handy", "eine Gitarre", "ein Tablet", "eine Kamera"),
        покупка1="{X} kauft {n1} {Т1} zu je {P1}. wie viel bezahlt {он} insgesamt?",
        покупка2="{X} kauft {n1} {Т1} zu je {P1} und {n2} {Т2} zu je {P2}. wie viel bezahlt {он} insgesamt?",
        товары=("Stifte", "Bücher", "Tassen", "Bleistifte", "Äpfel"),
        один_товар=("ein Stift", "ein Buch", "eine Tasse", "ein Bleistift", "ein Apfel"),
        покупка3="{X} kauft {n1} {Т1}, {n2} {Т2} und {n3} {Т3}. {О1} kostet {P1}, {О2} kostet {P2}, {О3} kostet {P3}. wie viel bezahlt {он} insgesamt?",
        леджер_ставки="{c} − {a} = {r1}, {r1} ÷ {b} = {n}. also ist die Antwort {n}.",
        леджер_покупки="{л} Cent.",
    ),
}
ЛИЦА = {язык: _лица(язык) for язык in ЯЗЫКИ}
СЕМЕЙСТВА = ("акт", "покупка", "имеет", "ставка", "покупка1", "покупка2", "покупка3")
ВОПРОСЫ_АКТА = ("теперь", "осталось")


def сумма(язык, d, c, k=0):
    """The decimal writing of d units and c cents: «$5.20» / «5.20 dollars»
    (k odd / even — the two writings of the money world), «5 рублей 20
    копеек», «5,20 Euro»."""
    if c is None:   # a whole amount («$10 per day», «10 рублей», «10 Euro» — genus 3 of g1 counts in units)
        if язык == "en":
            return f"${d}" if k % 2 else f"{d} dollars"
        if язык == "ru":
            return f"{d} {rugram.форма('рубль', d)}"
        return f"{d} Euro"
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


def _товар(язык, i, n):
    """The bought thing beside its count: English/German plural, Russian by the house of count."""
    т = ЯЗЫКИ[язык]["товары"][i]
    return rugram.форма(т, n) if язык == "ru" else т


def страница(язык, сем, имя, держ=None, k=0, A=None, B=None, глагол=None, вопрос="теперь", вещь=0, п_C=None,
             п_n1=None, п_n2=None, п_n3=None, п_P3=None, вещь2=0, вещь3=0):
    """The page as the house writes it. A, B — (units, cents); for «ставка» A, B
    are whole units (units, None) and п_C the goal; for the purchases п_n1, п_n2
    the counts, A, B the prices, вещь/вещь2 the goods."""
    я = ЯЗЫКИ[язык]
    лицо = next(л for л in ЛИЦА[язык] if л[0] == имя)
    X, пол, Xр = лицо
    он = я["он"][пол]
    з = dict(X=X, Xр=Xр, он=он, у_него=я.get("у_него", {}).get(пол, ""))
    if сем == "ставка":
        # whole units: a, b, c in dollars/roubles/euros; the days are whole (c − a divisible by b)
        a, b, c = A[0], B[0], п_C
        r1 = c - a; n = r1 // b
        утв = я["ставка"].format(A=сумма(язык, a, None, k), B=сумма(язык, b, None, k), C=сумма(язык, c, None, k), Ц=я["цели"][вещь], ему=я.get("ему", {}).get(пол, ""), **з)
        return f"{утв} {я['леджер_ставки'].format(c=c, a=a, r1=r1, b=b, n=n)}"
    if сем == "покупка3":
        # THREE GOODS, THE PRICE OF EACH IN ITS OWN SENTENCE (e9's profile,
        # genus 6: «3 pairs of shorts … one pair of shorts costs $16.50»)
        n1, n2, n3 = п_n1, п_n2, п_n3
        P1, P2, P3 = A, B, п_P3
        ц1, ц2, ц3 = (P1[0] * 100 + P1[1], P2[0] * 100 + P2[1], P3[0] * 100 + P3[1])
        q1, q2, q3 = n1 * ц1, n2 * ц2, n3 * ц3
        S = q1 + q2 + q3
        утв = я["покупка3"].format(n1=n1, n2=n2, n3=n3, Т1=_товар(язык, вещь, n1), Т2=_товар(язык, вещь2, n2), Т3=_товар(язык, вещь3, n3),
                                   О1=я["один_товар"][вещь], О2=я["один_товар"][вещь2], О3=я["один_товар"][вещь3],
                                   P1=сумма(язык, *P1, k), P2=сумма(язык, *P2, k), P3=сумма(язык, *P3, k), **з)
        леджер = f"{n1} × {ц1} = {q1}, {n2} × {ц2} = {q2}, {n3} × {ц3} = {q3}, {q1} + {q2} = {q1 + q2}, {q1 + q2} + {q3} = {S}"
        м = _мелкая_ru(S) if язык == "ru" else ""
        return f"{утв} {я['леджер_покупки'].format(л=леджер, м=м)} {я['мост'].format(r=S, м=м, R=сумма(язык, S // 100, S % 100, k))}"
    if сем in ("покупка1", "покупка2"):
        n1, P1 = п_n1, A; q1 = n1 * (P1[0] * 100 + P1[1])
        Т1 = _товар(язык, вещь, n1)
        if сем == "покупка1":
            утв = я["покупка1"].format(n1=n1, Т1=Т1, P1=сумма(язык, *P1, k), **з)
            леджер = f"{n1} × {P1[0] * 100 + P1[1]} = {q1}"
            S = q1
        else:
            n2, P2 = п_n2, B; q2 = n2 * (P2[0] * 100 + P2[1]); S = q1 + q2
            утв = я["покупка2"].format(n1=n1, Т1=Т1, P1=сумма(язык, *P1, k), n2=n2, Т2=_товар(язык, вещь2, n2), P2=сумма(язык, *P2, k), **з)
            леджер = f"{n1} × {P1[0] * 100 + P1[1]} = {q1}, {n2} × {P2[0] * 100 + P2[1]} = {q2}, {q1} + {q2} = {S}"
        м = _мелкая_ru(S) if язык == "ru" else ""
        return f"{утв} {я['леджер_покупки'].format(л=леджер, м=м)} {я['мост'].format(r=S, м=м, R=сумма(язык, S // 100, S % 100, k))}"
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
# a whole amount («$10», «10 dollars», «10 рублей», «10 Euro») — genus 3 counts in units
_ЦЕЛАЯ = {"en": r"(?:\$\d+|\d+ dollars)", "ru": r"\d+ рубл(?:ь|я|ей)", "de": r"\d+ Euro"}


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    лица = ЛИЦА[язык]
    товары = set()
    for i in range(len(я.get("товары", ()))):
        for n in range(1, 60):
            товары.add(_товар(язык, i, n))
    фразы = []
    for ключ, (знак, фраза) in я["глаголы"].items():
        for ф in (фраза.values() if isinstance(фраза, dict) else (фраза,)):
            фразы.append(phrases.образец(ф, {"B": _СУММА[язык]}))
    return {"X": "(" + _альт([л[0] for л in лица]) + ")", "Xр": "(" + _альт([л[2] for л in лица]) + ")",
            "он": "(" + _альт(я["он"].values()) + ")", "у_него": "(" + _альт(я.get("у_него", {"m": "у него"}).values()) + ")",
            "A": "(" + _СУММА[язык] + ")", "B": "(" + _СУММА[язык] + ")", "R": "(" + _СУММА[язык] + ")",
            "V": "(" + "|".join(sorted(set(фразы), key=len, reverse=True)) + ")", "Т": "(" + _альт(я["вещи"]) + ")",
            "a": r"(\d+)", "b": r"(\d+)", "r": r"(\d+)", "S": r"([−+])", "м": r"(копе(?:йка|йки|ек))",
            "C": "(" + _ЦЕЛАЯ[язык] + ")", "Ц": "(" + _альт(я.get("цели", ())) + ")", "ему": "(" + _альт(я.get("ему", {"m": "—"}).values()) + ")",
            "c": r"(\d+)", "r1": r"(\d+)", "n": r"(\d+)", "n1": r"(\d+)", "n2": r"(\d+)",
            "Т1": "(" + _альт(товары) + ")", "Т2": "(" + _альт(товары) + ")", "Т3": "(" + _альт(товары) + ")",
            "P1": "(" + _СУММА[язык] + ")", "P2": "(" + _СУММА[язык] + ")", "P3": "(" + _СУММА[язык] + ")", "n3": r"(\d+)",
            "О1": "(" + _альт(я.get("один_товар", ())) + ")", "О2": "(" + _альт(я.get("один_товар", ())) + ")", "О3": "(" + _альт(я.get("один_товар", ())) + ")",
            "л": r"((?:\d+ [×+] \d+ = \d+(?:, )?)+)"}


def _шаблоны(язык):
    """(family, holding, question, template) for every page shape."""
    я = ЯЗЫКИ[язык]
    вон = []
    if "ставка" in я:
        # the amounts of «ставка» are whole («$10 per day»): its own holes A/B/C read the whole writing
        вон.append(("ставка", None, None, f"{я['ставка']} {я['леджер_ставки']}"))
        вон.append(("покупка1", None, None, f"{я['покупка1']} {я['леджер_покупки']} {я['мост']}"))
        вон.append(("покупка2", None, None, f"{я['покупка2']} {я['леджер_покупки']} {я['мост']}"))
        вон.append(("покупка3", None, None, f"{я['покупка3']} {я['леджер_покупки']} {я['мост']}"))
    for держ, факт in я["держит"].items():
        вон.append(("имеет", держ, "имеет", f"{факт} {я['имеет']} {факт}"))
        for вопрос in ВОПРОСЫ_АКТА:
            вон.append(("акт", держ, вопрос, f"{факт} {я['акт']} {я[вопрос]} {я['леджер']} {я['мост']}"))
        вон.append(("покупка", держ, "теперь", f"{факт} {я['покупка']} {я['теперь']} {я['леджер']} {я['мост']}"))
    return вон


def образцы(язык):
    дыры = _дыры(язык)
    целые = dict(дыры, A="(" + _ЦЕЛАЯ[язык] + ")", B="(" + _ЦЕЛАЯ[язык] + ")")
    return [(re.compile("^" + phrases.образец(ш, целые if сем == "ставка" else дыры) + "$"), phrases.порядок(ш), сем, держ, вопрос)
            for сем, держ, вопрос, ш in _шаблоны(язык)]


ОБРАЗЦЫ = {язык: образцы(язык) for язык in ЯЗЫКИ}


def _читать_сумму(язык, з):
    """(units, cents, k) from the writing; a whole writing («$10») gives cents None."""
    числа = [int(x) for x in re.findall(r"\d+", з)]
    return числа[0], (числа[1] if len(числа) > 1 else None), (1 if з.startswith("$") else 0)


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
        if сем == "ставка":
            a, _, k = _читать_сумму(язык, з["A"]); b, _, _ = _читать_сумму(язык, з["B"]); c, _, _ = _читать_сумму(язык, з["C"])
            if b < 1 or c <= a or (c - a) % b:
                return None
            return dict(сем=сем, имя=з["X"], k=k, A=(a, None), B=(b, None), п_C=c, вещь=я["цели"].index(з["Ц"]))
        if сем == "покупка3":
            d1, c1, k = _читать_сумму(язык, з["P1"]); d2, c2, _ = _читать_сумму(язык, з["P2"]); d3, c3, _ = _читать_сумму(язык, з["P3"])
            n1, n2, n3 = int(з["n1"]), int(з["n2"]), int(з["n3"])
            т = [next((i for i in range(len(я["товары"])) if _товар(язык, i, n) == з[к] and я["один_товар"][i] == з[о]), None)
                 for n, к, о in ((n1, "Т1", "О1"), (n2, "Т2", "О2"), (n3, "Т3", "О3"))]
            if None in т:
                return None
            return dict(сем=сем, имя=з["X"], k=k, A=(d1, c1), B=(d2, c2), п_P3=(d3, c3),
                        п_n1=n1, п_n2=n2, п_n3=n3, вещь=т[0], вещь2=т[1], вещь3=т[2])
        if сем in ("покупка1", "покупка2"):
            d1, c1, k = _читать_сумму(язык, з["P1"]); n1 = int(з["n1"])
            т1 = next(i for i in range(len(я["товары"])) if _товар(язык, i, n1) == з["Т1"])
            п = dict(сем=сем, имя=з["X"], k=k, A=(d1, c1), п_n1=n1, вещь=т1)
            if сем == "покупка2":
                d2, c2, _ = _читать_сумму(язык, з["P2"]); n2 = int(з["n2"])
                п.update(B=(d2, c2), п_n2=n2, вещь2=next(i for i in range(len(я["товары"])) if _товар(язык, i, n2) == з["Т2"]))
            return п
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
