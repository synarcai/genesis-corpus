#!/usr/bin/env python3
"""THE HOUSE OF WEEKDAY PHRASES — «k days after X comes Y» in eight languages.

The calendar world says «3 days after tuesday comes friday» and «через 3
дня после понедельника наступает четверг» in en/ru — the shows from which
the organism buys the weekly cycle without names and without the seven.
This house names the days in de/fr/es/it/pt/nl/pl/tr with the oblique form
the phrase needs (Polish locative after «po», Turkish ablative «-dan»,
Spanish «del» + the article) and the count form of «day», and the two
phrases — the statement and the question answered by it (М-153). Generator
and court read one table; the court counts the cycle itself.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# per language: days (nominative), oblique days where the phrase bends them,
# the count forms of «day» (one, many), the statement and the question
ЯЗЫКИ = {
    "de": dict(послезавтра_воп="heute ist {X}. welcher Tag ist übermorgen?", позавчера_воп="heute ist {X}. welcher Tag war vorgestern?",
               вчера_воп="heute ist {X}. welcher Tag war gestern?", завтра_воп="heute ist {X}. welcher Tag ist morgen?",
               дни=("Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"),
               день=("Tag", "Tage"), утв="{n} {д} nach {X} kommt {Y}: {л}.", воп="welcher Tag kommt {n} {д} nach {X}?", сосед_воп="welcher Tag kommt nach {X}?", сосед_утв="nach {X} kommt {Y}."),
    "fr": dict(послезавтра_воп="aujourd'hui c'est {X}. quel jour sera-ce après-demain ?", позавчера_воп="aujourd'hui c'est {X}. quel jour était-ce avant-hier ?",
               вчера_воп="aujourd'hui c'est {X}. quel jour était-ce hier ?", завтра_воп="aujourd'hui c'est {X}. quel jour sera-ce demain ?",
               дни=("lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"),
               день=("jour", "jours"), утв="{n} {д} après {X} vient {Y}: {л}.", воп="quel jour vient {n} {д} après {X} ?", сосед_воп="quel jour vient après {X} ?", сосед_утв="après {X} vient {Y}."),
    "es": dict(послезавтра_воп="hoy es {X}. ¿qué día será pasado mañana?", позавчера_воп="hoy es {X}. ¿qué día fue anteayer?",
               вчера_воп="hoy es {X}. ¿qué día fue ayer?", завтра_воп="hoy es {X}. ¿qué día será mañana?",
               дни=("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"),
               день=("día", "días"), утв="{n} {д} después del {X} viene el {Y}: {л}.", воп="¿qué día viene {n} {д} después del {X}?", сосед_воп="¿qué día viene después del {X}?", сосед_утв="después del {X} viene el {Y}."),
    "it": dict(послезавтра_воп="oggi è {X}. che giorno sarà dopodomani?", позавчера_воп="oggi è {X}. che giorno era l'altro ieri?",
               вчера_воп="oggi è {X}. che giorno era ieri?", завтра_воп="oggi è {X}. che giorno sarà domani?",
               дни=("lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"),
               день=("giorno", "giorni"), утв="{n} {д} dopo {X} viene {Y}: {л}.", воп="che giorno viene {n} {д} dopo {X}?", сосед_воп="che giorno viene dopo {X}?", сосед_утв="dopo {X} viene {Y}."),
    "pt": dict(послезавтра_воп="hoje é {X}. que dia será depois de amanhã?", позавчера_воп="hoje é {X}. que dia foi anteontem?",
               вчера_воп="hoje é {X}. que dia foi ontem?", завтра_воп="hoje é {X}. que dia será amanhã?",
               дни=("segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira", "sábado", "domingo"),
               день=("dia", "dias"), утв="{n} {д} depois de {X} vem {Y}: {л}.", воп="que dia vem {n} {д} depois de {X}?", сосед_воп="que dia vem depois de {X}?", сосед_утв="depois de {X} vem {Y}."),
    "nl": dict(послезавтра_воп="vandaag is het {X}. welke dag is het overmorgen?", позавчера_воп="vandaag is het {X}. welke dag was het eergisteren?",
               вчера_воп="vandaag is het {X}. welke dag was het gisteren?", завтра_воп="vandaag is het {X}. welke dag is het morgen?",
               дни=("maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"),
               день=("dag", "dagen"), утв="{n} {д} na {X} komt {Y}: {л}.", воп="welke dag komt {n} {д} na {X}?", сосед_воп="welke dag komt na {X}?", сосед_утв="na {X} komt {Y}."),
    "pl": dict(послезавтра_воп="dziś jest {X}. jaki dzień będzie pojutrze?", позавчера_воп="dziś jest {X}. jaki dzień był przedwczoraj?",
               вчера_воп="dziś jest {X}. jaki dzień był wczoraj?", завтра_воп="dziś jest {X}. jaki dzień będzie jutro?",
               дни=("poniedziałek", "wtorek", "środa", "czwartek", "piątek", "sobota", "niedziela"),
               косв=("poniedziałku", "wtorku", "środzie", "czwartku", "piątku", "sobocie", "niedzieli"),
               день=("dzień", "dni"), утв="{n} {д} po {X} przypada {Y}: {л}.", воп="jaki dzień przypada {n} {д} po {X}?", сосед_воп="jaki dzień jest po {X}?", сосед_утв="po {X} jest {Y}."),
    "tr": dict(послезавтра_воп="bugün {X}. öbür gün hangi gün?", позавчера_воп="bugün {X}. evvelsi gün hangi gündü?",
               вчера_воп="bugün {X}. dün hangi gündü?", завтра_воп="bugün {X}. yarın hangi gün?",
               дни=("pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"),
               косв=("pazartesiden", "salıdan", "çarşambadan", "perşembeden", "cumadan", "cumartesinden", "pazardan"),
               день=("gün", "gün"), утв="{X} {n} {д} sonra {Y} gelir: {л}.", воп="{X} {n} {д} sonra hangi gün gelir?", сосед_воп="{X} sonra hangi gün gelir?", сосед_утв="{X} sonra {Y} gelir."),
}


# the phrase of the day number in the ledger («Tag 5 ist Freitag»)
ДЕНЬ_НОМЕР = {"de": "Tag {j} ist {Y}", "fr": "le jour {j} est {Y}", "es": "el día {j} es {Y}", "it": "il giorno {j} è {Y}",
              "pt": "o dia {j} é {Y}", "nl": "dag {j} is {Y}", "pl": "dzień {j} to {Y}", "tr": "{j}. gün {Y}"}


def леджер(язык, i, n):
    """THE LEDGER OF THE CYCLE (holon 03.09): «2 + 3 = 5, Tag 5 ist Freitag»,
    over the edge «6 + 3 = 9, 9 − 7 = 2, Tag 2 ist Dienstag»."""
    s = i + 1 + n
    j = s - 7 if s > 7 else s
    шаги = [f"{i + 1} + {n} = {s}"] + ([f"{s} − 7 = {j}"] if s > 7 else [])
    return ", ".join(шаги + [ДЕНЬ_НОМЕР[язык].format(j=j, Y=ЯЗЫКИ[язык]["дни"][j - 1])])


def _косв(язык, i):
    я = ЯЗЫКИ[язык]
    return я.get("косв", я["дни"])[i]


def _день(язык, n):
    ф = ЯЗЫКИ[язык]["день"]
    return ф[0] if n == 1 else ф[1]


def утверждение(язык, i, n):
    я = ЯЗЫКИ[язык]
    return я["утв"].format(n=n, д=_день(язык, n), X=_косв(язык, i), Y=я["дни"][(i + n) % 7], л=леджер(язык, i, n))


def вопрос(язык, i, n):
    я = ЯЗЫКИ[язык]
    return f"{я['воп'].format(n=n, д=_день(язык, n), X=_косв(язык, i))} {утверждение(язык, i, n)}"


def сосед(язык, i):
    """СОСЕДНИЙ ДЕНЬ БЕЗ ЧИСЛА (полоса BESEDA-2, 05.09: род NEXT-DAY — 1 из 9).
    Человек спрашивает «какой день идёт после понедельника?» без «через n дней»;
    дом знал только счёт через n дней. Страница: вопрос и утверждение соседства."""
    я = ЯЗЫКИ[язык]
    X, Y = _косв(язык, i), я["дни"][(i + 1) % 7]
    return f"{я['сосед_воп'].format(X=X)} {я['сосед_утв'].format(X=X, Y=Y)}"


def вчера(язык, i, куда="вчера"):
    """YESTERDAY AND TOMORROW FROM A NAMED TODAY (sixth band, 05.09: «сегодня среда.
    какой день был вчера?» — mute in all nine languages). The day of the question
    stands in the nominative after «is»; the answer is the bare neighbour."""
    я = ЯЗЫКИ[язык]
    X = я["дни"][i]
    Y = я["дни"][(i + ШАГ_ДНЯ[куда]) % 7]
    return f"{я[куда + '_воп'].format(X=X)} {Y}."


ШАГ_ДНЯ = {"вчера": -1, "завтра": 1, "послезавтра": 2, "позавчера": -2}


def _образец(язык, шаблон):
    я = ЯЗЫКИ[язык]
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    дыры = {"n": r"(\d+)", "д": alt(я["день"]), "X": alt(я.get("косв", я["дни"])), "Y": alt(я["дни"]),
            "л": r"(\d+ \+ \d+ = \d+(?:, \d+ − 7 = \d+)?, .+?)"}   # «2. gün salı» carries a period
    return phrases.образец(шаблон, дыры)


def образцы(язык):
    я = ЯЗЫКИ[язык]
    утв = _образец(язык, я["утв"])
    return [(re.compile("^" + утв + "$"), False),
            (re.compile("^" + _образец(язык, я["воп"]) + " " + утв + "$"), True),
            (re.compile("^" + _образец(язык, я["сосед_воп"]) + " " + _образец(язык, я["сосед_утв"]) + "$"), "сосед"),
            (re.compile("^" + _образец(язык, я["вчера_воп"]).replace(_дни_косв(язык), _дни_им(язык), 1) + " " + _дни_им(язык) + r"\.$"), "вчера"),
            (re.compile("^" + _образец(язык, я["завтра_воп"]).replace(_дни_косв(язык), _дни_им(язык), 1) + " " + _дни_им(язык) + r"\.$"), "завтра"),
            (re.compile("^" + _образец(язык, я["послезавтра_воп"]).replace(_дни_косв(язык), _дни_им(язык), 1) + " " + _дни_им(язык) + r"\.$"), "послезавтра"),
            (re.compile("^" + _образец(язык, я["позавчера_воп"]).replace(_дни_косв(язык), _дни_им(язык), 1) + " " + _дни_им(язык) + r"\.$"), "позавчера")]


def _дни_им(язык):
    return "(" + "|".join(re.escape(с) for с in sorted(set(ЯЗЫКИ[язык]["дни"]), key=len, reverse=True)) + ")"


def _дни_косв(язык):
    я = ЯЗЫКИ[язык]
    return "(" + "|".join(re.escape(с) for с in sorted(set(я.get("косв", я["дни"])), key=len, reverse=True)) + ")"


def судить_группы(язык, спрошено, группы):
    я = ЯЗЫКИ[язык]
    if спрошено in ШАГ_ДНЯ:
        г = list(группы)
        дни = я["дни"]
        if len(г) != 2 or г[0] not in дни:
            return False
        i = дни.index(г[0])
        return дни[(i + ШАГ_ДНЯ[спрошено]) % 7] == г[1]
    if спрошено == "сосед":
        # группы: X вопроса, X утверждения, Y — сосед есть следующий день круга
        г = list(группы)
        косв = я.get("косв", я["дни"])
        if len(г) != 3 or г[0] != г[1] or г[0] not in косв:
            return False
        return я["дни"][(косв.index(г[0]) + 1) % 7] == г[2]
    порядок = phrases.порядок(я["утв"])
    г = list(группы)
    if спрошено:
        в_порядок = phrases.порядок(я["воп"])
        спрош = dict(zip(в_порядок, г[:len(в_порядок)])); г = г[len(в_порядок):]
    else:
        спрош = {}
    з = dict(zip(порядок, г))
    n = int(з["n"])
    if not 1 <= n <= 6 or з["д"] != _день(язык, n):
        return False
    косв = я.get("косв", я["дни"])
    i = косв.index(з["X"])
    if я["дни"][(i + n) % 7] != з["Y"]:
        return False
    if з.get("л") is not None and з["л"] != леджер(язык, i, n):
        return False
    if спрош and (int(спрош["n"]) != n or спрош["X"] != з["X"] or спрош["д"] != з["д"]):
        return False
    return True
