#!/usr/bin/env python3
"""THE HOUSE OF UNIT NAMES — conversions in eight languages.

The house of units (tools/units.py) holds the units and their ratios and
names them in English and Russian; the conversion worlds say «2 hours are
120 minutes: 2 × 60 = 120» and «в 2 часах 120 минут». This house names the
same units in de/fr/es/it/pt/nl/pl/tr with their count forms (German and
Dutch invariable after a numeral, Polish one/few/many by the pack's
count_agreement, Turkish bare with the copula suffix by vowel harmony) and
their gender where the question word agrees with it (¿cuántos minutos /
¿cuántas horas), and the two phrases of a conversion — the statement and
the question answered by it. Generator and court read one table; the ratio
comes from the house of units, never from the line.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holes  # noqa: E402
import units  # noqa: E402

# the pairs shown: (big unit, small unit) — the ratio is the house of units'
ПАРЫ = (("hour", "minute"), ("day", "hour"), ("week", "day"), ("year", "month"),
        ("kilometre", "metre"), ("metre", "centimetre"), ("kilogram", "gram"), ("minute", "second"))

# forms: (one, many) — or (one, few, many) for pl — and the gender (m/f)
ЕДИНИЦЫ = {
    "de": dict(hour=("Stunde", "Stunden", "f"), minute=("Minute", "Minuten", "f"), day=("Tag", "Tage", "m"), week=("Woche", "Wochen", "f"),
               year=("Jahr", "Jahre", "n"), month=("Monat", "Monate", "m"), kilometre=("Kilometer", "Kilometer", "m"), metre=("Meter", "Meter", "m"),
               centimetre=("Zentimeter", "Zentimeter", "m"), kilogram=("Kilogramm", "Kilogramm", "n"), gram=("Gramm", "Gramm", "n"), second=("Sekunde", "Sekunden", "f")),
    "fr": dict(hour=("heure", "heures", "f"), minute=("minute", "minutes", "f"), day=("jour", "jours", "m"), week=("semaine", "semaines", "f"),
               year=("an", "ans", "m"), month=("mois", "mois", "m"), kilometre=("kilomètre", "kilomètres", "m"), metre=("mètre", "mètres", "m"),
               centimetre=("centimètre", "centimètres", "m"), kilogram=("kilogramme", "kilogrammes", "m"), gram=("gramme", "grammes", "m"), second=("seconde", "secondes", "f")),
    "es": dict(hour=("hora", "horas", "f"), minute=("minuto", "minutos", "m"), day=("día", "días", "m"), week=("semana", "semanas", "f"),
               year=("año", "años", "m"), month=("mes", "meses", "m"), kilometre=("kilómetro", "kilómetros", "m"), metre=("metro", "metros", "m"),
               centimetre=("centímetro", "centímetros", "m"), kilogram=("kilogramo", "kilogramos", "m"), gram=("gramo", "gramos", "m"), second=("segundo", "segundos", "m")),
    "it": dict(hour=("ora", "ore", "f"), minute=("minuto", "minuti", "m"), day=("giorno", "giorni", "m"), week=("settimana", "settimane", "f"),
               year=("anno", "anni", "m"), month=("mese", "mesi", "m"), kilometre=("chilometro", "chilometri", "m"), metre=("metro", "metri", "m"),
               centimetre=("centimetro", "centimetri", "m"), kilogram=("chilogrammo", "chilogrammi", "m"), gram=("grammo", "grammi", "m"), second=("secondo", "secondi", "m")),
    "pt": dict(hour=("hora", "horas", "f"), minute=("minuto", "minutos", "m"), day=("dia", "dias", "m"), week=("semana", "semanas", "f"),
               year=("ano", "anos", "m"), month=("mês", "meses", "m"), kilometre=("quilómetro", "quilómetros", "m"), metre=("metro", "metros", "m"),
               centimetre=("centímetro", "centímetros", "m"), kilogram=("quilograma", "quilogramas", "m"), gram=("grama", "gramas", "m"), second=("segundo", "segundos", "m")),
    "nl": dict(hour=("uur", "uur", "n"), minute=("minuut", "minuten", "f"), day=("dag", "dagen", "m"), week=("week", "weken", "f"),
               year=("jaar", "jaar", "n"), month=("maand", "maanden", "f"), kilometre=("kilometer", "kilometer", "m"), metre=("meter", "meter", "m"),
               centimetre=("centimeter", "centimeter", "m"), kilogram=("kilogram", "kilogram", "n"), gram=("gram", "gram", "n"), second=("seconde", "seconden", "f")),
    "pl": dict(hour=("godzina", "godziny", "godzin", "f"), minute=("minuta", "minuty", "minut", "f"), day=("dzień", "dni", "dni", "m"), week=("tydzień", "tygodnie", "tygodni", "m"),
               year=("rok", "lata", "lat", "m"), month=("miesiąc", "miesiące", "miesięcy", "m"), kilometre=("kilometr", "kilometry", "kilometrów", "m"), metre=("metr", "metry", "metrów", "m"),
               centimetre=("centymetr", "centymetry", "centymetrów", "m"), kilogram=("kilogram", "kilogramy", "kilogramów", "m"), gram=("gram", "gramy", "gramów", "m"), second=("sekunda", "sekundy", "sekund", "f")),
    "tr": dict(hour=("saat", "saattir"), minute=("dakika", "dakikadır"), day=("gün", "gündür"), week=("hafta", "haftadır"),
               year=("yıl", "yıldır"), month=("ay", "aydır"), kilometre=("kilometre", "kilometredir"), metre=("metre", "metredir"),
               centimetre=("santimetre", "santimetredir"), kilogram=("kilogram", "kilogramdır"), gram=("gram", "gramdır"), second=("saniye", "saniyedir")),
}
# the two phrases: {n} {б} — the big amount, {итог} {м} — the small, {k} the
# ratio, {мм} the small unit asked (many form), {ск} the question word
ФРАЗЫ = {
    "de": ("{n} {б} sind {итог} {м}: {n} × {k} = {итог}.", "wie viele {мм} sind {n} {б}?"),
    "fr": ("{n} {б} font {итог} {м} : {n} × {k} = {итог}.", "combien {де}{мм} font {n} {б} ?"),
    "es": ("{n} {б} son {итог} {м}: {n} × {k} = {итог}.", "¿{ск} {мм} son {n} {б}?"),
    "it": ("{n} {б} sono {итог} {м}: {n} × {k} = {итог}.", "{ск} {мм} sono {n} {б}?"),
    "pt": ("{n} {б} são {итог} {м}: {n} × {k} = {итог}.", "{ск} {мм} são {n} {б}?"),
    "nl": ("{n} {б} is {итог} {м}: {n} × {k} = {итог}.", "hoeveel {мм} is {n} {б}?"),
    "pl": ("{n} {б} to {итог} {м}: {n} × {k} = {итог}.", "ile {мм} to {n} {б}?"),
    "tr": ("{n} {б} {итог} {м}: {n} × {k} = {итог}.", "{n} {б} kaç {м}?"),
}
СКОЛЬКО = {"es": ("cuántos", "cuántas"), "it": ("quanti", "quante"), "pt": ("quantos", "quantas")}


def форма(язык, единица, n):
    """The unit beside the count n, as the language writes it."""
    ф = ЕДИНИЦЫ[язык][единица]
    if язык == "pl":
        return ф[("one", "few", "many").index(holes.форма_счёта("pl", n))]
    if язык == "tr":
        return ф[0]
    return ф[0] if n == 1 else ф[1]


def _сколько(язык, единица):
    if язык not in СКОЛЬКО:
        return ""
    return СКОЛЬКО[язык][1 if ЕДИНИЦЫ[язык][единица][-1] == "f" else 0]


def утверждение(язык, б, м, n):
    k = units.отношение(б, м)
    итог = n * k
    м_ = ЕДИНИЦЫ["tr"][м][1] if язык == "tr" else форма(язык, м, итог)
    return ФРАЗЫ[язык][0].format(n=n, б=форма(язык, б, n), итог=итог, м=м_, k=k)


def вопрос(язык, б, м, n):
    """The question of the small amount, answered by the statement (М-153)."""
    мм = ЕДИНИЦЫ[язык][м][1] if язык == "tr" else (ЕДИНИЦЫ[язык][м][2] if язык == "pl" else ЕДИНИЦЫ[язык][м][1])
    # French elides «de» before a vowel or a mute h: «combien d'heures»
    де = "d'" if мм[0] in "aeiouhé" else "de "
    q = ФРАЗЫ[язык][1].format(n=n, б=форма(язык, б, n), мм=мм, м=мм, ск=_сколько(язык, м), де=де)
    return f"{q} {утверждение(язык, б, м, n)}"


def _слово(язык):
    """Every unit form of the language as one alternative."""
    формы = {ф for е in ЕДИНИЦЫ[язык].values() for ф in е if len(ф) > 1 or язык == "tr"}
    формы = {ф for ф in формы if ф not in ("m", "f", "n")}
    return "(" + "|".join(re.escape(ф) for ф in sorted(формы, key=len, reverse=True)) + ")"


_ДЫРА = re.compile(r"\{(n|б|м|мм|k|итог|ск|де)\}")


def _образец(язык, шаблон):
    слово = _слово(язык)
    дыры = {"n": r"(\d+)", "итог": r"(\d+)", "k": r"(\d+)", "б": слово, "м": слово, "мм": слово,
            "ск": "(" + "|".join(СКОЛЬКО.get(язык, ("",))) + ")", "де": "(de |d')"}
    куски, конец = [], 0
    for м in _ДЫРА.finditer(шаблон):
        куски.append(re.escape(шаблон[конец:м.start()]))
        куски.append(дыры[м.group(1)])
        конец = м.end()
    куски.append(re.escape(шаблон[конец:]))
    return "".join(куски)


def образцы(язык):
    """[(regex, asked)] — statement groups: n, б, итог, м, n2, k, итог2;
    question groups first: (ск,) мм, n, б — then the statement's."""
    утв, воп = ФРАЗЫ[язык]
    return [(re.compile("^" + _образец(язык, утв) + "$"), False),
            (re.compile("^" + _образец(язык, воп) + " " + _образец(язык, утв) + "$"), True)]


def _единица(язык, слово):
    """(canonical unit, index of the form) of a unit word, or None."""
    for имя, формы in ЕДИНИЦЫ[язык].items():
        for i, ф in enumerate(формы):
            if ф == слово and ф not in ("m", "f", "n"):
                return имя, i
    return None


def судить_группы(язык, спрошено, группы):
    г = list(группы)
    if спрошено:
        if язык in СКОЛЬКО:
            ск, мм, n0, б0 = г[:4]; г = г[4:]
        elif язык == "tr":
            n0, б0, мм = г[:3]; г = г[3:]; ск = ""
        elif язык == "fr":
            де, мм, n0, б0 = г[:4]; г = г[4:]; ск = ""
            if де != ("d'" if мм[0] in "aeiouhé" else "de "):
                return False
        else:
            мм, n0, б0 = г[:3]; г = г[3:]; ск = ""
    n, б, итог, м, n2, k, итог2 = г
    n, итог, n2, k, итог2 = int(n), int(итог), int(n2), int(k), int(итог2)
    еб, ем = _единица(язык, б), _единица(язык, м)
    if еб is None or ем is None:
        return False
    if еб[0] == ем[0]:
        return False
    k0 = units.отношение(еб[0], ем[0])
    if k0 is None:
        return False
    if not (n2 == n and k == k0 and итог == итог2 == n * k0):
        return False
    if б != форма(язык, еб[0], n):
        return False
    м_ожид = ЕДИНИЦЫ["tr"][ем[0]][1] if язык == "tr" else форма(язык, ем[0], итог)
    if м != м_ожид:
        return False
    if спрошено:
        мм_ожид = ЕДИНИЦЫ[язык][ем[0]][1] if язык == "tr" else (ЕДИНИЦЫ[язык][ем[0]][2] if язык == "pl" else ЕДИНИЦЫ[язык][ем[0]][1])
        if мм != мм_ожид or int(n0) != n or б0 != б or ск != _сколько(язык, ем[0]):
            return False
    return True
