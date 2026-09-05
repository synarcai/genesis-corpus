#!/usr/bin/env python3
"""THE HOUSE OF THE PERSONALITY — the same fact, another voice (05.09).

The seventh and last market of the agent's architecture, and the one most easily built wrong.
A personality is not a mood and not a style sheet: by the architecture it is a set of SLOW
STATE VARIABLES WITH PROVENANCE, and its whole lawful power is this —

    A PERSONALITY CHANGES THE FORM OF AN ANSWER AND THE CHOICE BETWEEN EQUALS. IT NEVER
    CHANGES THE FACT.

So the house shows one tape twice. The terse personality answers «8.»; the verbose one
answers «there are 8 files in the folder: 5 + 3 = 8.» — and a third page puts both answers
side by side and asks whether it is the same number, answering «yes: 8 and 8 are one number».
The law is thereby ON THE PAGE, not only in the court: the corpus states that the fact
survived the change of voice.

THE CHOICE BETWEEN EQUALS IS WHERE A PERSONALITY IS ALLOWED TO DECIDE. Two ways are offered
whose OUTCOME IS THE SAME NUMBER (delete three files, or move three files out — the folder
keeps two either way, and the page recomputes it). A cautious personality takes the way that
destroys nothing; a quick personality takes the first way named. Neither may be shown where
the outcomes differ: choosing by character between unequal outcomes is choosing by taste
against the fact, and the judge refuses such a page.

EVERY TRAIT CARRIES ITS PROVENANCE. «my brevity comes from the shows», «my caution comes from
a mistake», «my caution comes from an order» — a slow variable whose origin is unnamed is a
preference; named, it is a state with a history, and the house asks about it directly.

WHAT IS BORROWED: nine languages, the things and places from the house of the tool, the acts
and their ordinals and the tape's ledger from the house of the episode, the question openers
from the house of the pair. Declared here: the four traits in their two axes (form of answer,
choice between equals), the ways of a choice, the grounds a trait gives for its choice, and
the three provenances.

WHAT IS NOT MEASURED, NAMED: whether a personality SHOULD be terse here, how a trait changes
over time, and any trait that would bend a fact (there is none — that is the point).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import episodeforms as E  # noqa: E402 — the acts of a tape, their ordinals and the ledger
import svampforms as S  # noqa: E402 — the count cell of a pack
import toolforms as T  # noqa: E402 — things of acts, their places, the copula of a place

ЯЗЫКИ = T.ЯЗЫКИ
НАЧАЛА = (5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20)
ШАГИ = (2, 3, 4, 5, 6, 7)
ЧЕРТЫ_ФОРМЫ = ("краткая", "подробная")
ЧЕРТЫ_ВЫБОРА = ("осторожная", "скорая")
ИСТОЧНИКИ = ("показы", "ошибка", "приказ")

СЛОВА = {
    "ru": dict(личность="личность", краткая="краткая", подробная="подробная",
               осторожная="осторожная", скорая="скорая",
               два_пути="два пути", или="или", оба="оба оставляют",
               вопрос_счёт="сколько {Тмн} {М}?", вопрос_путь="которая дорога выбрана?",
               вопрос_одно="одно ли это число?", вопрос_откуда="откуда моя {ЧЕРТА}?",
               отвечает="отвечает", одно_число="одно число",
               путь_удалить="удалить {n} {Т}", путь_переместить="переместить {n} {Т}",
               довод_осторожная="осторожная личность не удаляет",
               довод_скорая="скорая личность берёт первый путь",
               черта_форма="краткость", черта_выбор="осторожность",
               из_показов="из показов", из_ошибки="из ошибки", из_приказа="из приказа",
               объявление="моя {ЧЕРТА} {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "en": dict(личность="personality", краткая="terse", подробная="verbose",
               осторожная="cautious", скорая="quick",
               два_пути="two ways", или="or", оба="both leave",
               вопрос_счёт="how many {Тмн} are {М}?", вопрос_путь="which way is chosen?",
               вопрос_одно="is it the same number?", вопрос_откуда="where does my {ЧЕРТА} come from?",
               отвечает="answers", одно_число="one number",
               путь_удалить="to delete {n} {Т}", путь_переместить="to move {n} {Т}",
               довод_осторожная="a cautious personality does not delete",
               довод_скорая="a quick personality takes the first way",
               черта_форма="brevity", черта_выбор="caution",
               из_показов="from the shows", из_ошибки="from a mistake", из_приказа="from an order",
               объявление="my {ЧЕРТА} comes {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "de": dict(личность="Persönlichkeit", краткая="knappe", подробная="ausführliche",
               осторожная="vorsichtige", скорая="schnelle",
               два_пути="zwei Wege", или="oder", оба="beide lassen",
               вопрос_счёт="wie viele {Тмн} sind {М}?", вопрос_путь="welcher Weg wird gewählt?",
               вопрос_одно="ist es dieselbe Zahl?", вопрос_откуда="woher kommt meine {ЧЕРТА}?",
               отвечает="antwortet", одно_число="eine Zahl",
               путь_удалить="{n} {Т} zu löschen", путь_переместить="{n} {Т} zu verschieben",
               довод_осторожная="eine vorsichtige Persönlichkeit löscht nicht",
               довод_скорая="eine schnelle Persönlichkeit nimmt den ersten Weg",
               черта_форма="Kürze", черта_выбор="Vorsicht",
               из_показов="aus den Zeigungen", из_ошибки="aus einem Fehler", из_приказа="aus einem Befehl",
               объявление="meine {ЧЕРТА} kommt {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "fr": dict(личность="personnalité", краткая="brève", подробная="détaillée",
               осторожная="prudente", скорая="rapide",
               два_пути="deux chemins", или="ou", оба="les deux laissent",
               вопрос_счёт="combien de {Тмн} y a-t-il {М} ?", вопрос_путь="quel chemin est choisi ?",
               вопрос_одно="est-ce le même nombre ?", вопрос_откуда="d'où vient ma {ЧЕРТА} ?",
               отвечает="répond", одно_число="un seul nombre",
               путь_удалить="supprimer {n} {Т}", путь_переместить="déplacer {n} {Т}",
               довод_осторожная="une personnalité prudente ne supprime pas",
               довод_скорая="une personnalité rapide prend le premier chemin",
               черта_форма="brièveté", черта_выбор="prudence",
               из_показов="des montrages", из_ошибки="d'une erreur", из_приказа="d'un ordre",
               объявление="ma {ЧЕРТА} vient {ОТКУДА}.", двоеточие=" : ", вопрос=" ?"),
    "es": dict(личность="personalidad", краткая="breve", подробная="detallada",
               осторожная="prudente", скорая="rápida",
               два_пути="dos caminos", или="o", оба="ambos dejan",
               вопрос_счёт="¿cuántos {Тмн} hay {М}?", вопрос_путь="¿qué camino se elige?",
               вопрос_одно="¿es el mismo número?", вопрос_откуда="¿de dónde viene mi {ЧЕРТА}?",
               отвечает="responde", одно_число="un solo número",
               путь_удалить="borrar {n} {Т}", путь_переместить="mover {n} {Т}",
               довод_осторожная="una personalidad prudente no borra",
               довод_скорая="una personalidad rápida toma el primer camino",
               черта_форма="brevedad", черта_выбор="prudencia",
               из_показов="de las muestras", из_ошибки="de un error", из_приказа="de una orden",
               объявление="mi {ЧЕРТА} viene {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "it": dict(личность="personalità", краткая="breve", подробная="dettagliata",
               осторожная="prudente", скорая="rapida",
               два_пути="due vie", или="o", оба="entrambe lasciano",
               вопрос_счёт="quanti {Тмн} ci sono {М}?", вопрос_путь="quale via si sceglie?",
               вопрос_одно="è lo stesso numero?", вопрос_откуда="da dove viene la mia {ЧЕРТА}?",
               отвечает="risponde", одно_число="un solo numero",
               путь_удалить="cancellare {n} {Т}", путь_переместить="spostare {n} {Т}",
               довод_осторожная="una personalità prudente non cancella",
               довод_скорая="una personalità rapida prende la prima via",
               черта_форма="brevità", черта_выбор="prudenza",
               из_показов="dalle mostre", из_ошибки="da un errore", из_приказа="da un ordine",
               объявление="la mia {ЧЕРТА} viene {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "pt": dict(личность="personalidade", краткая="breve", подробная="detalhada",
               осторожная="prudente", скорая="rápida",
               два_пути="dois caminhos", или="ou", оба="ambos deixam",
               вопрос_счёт="quantos {Тмн} há {М}?", вопрос_путь="que caminho é escolhido?",
               вопрос_одно="é o mesmo número?", вопрос_откуда="de onde vem a minha {ЧЕРТА}?",
               отвечает="responde", одно_число="um só número",
               путь_удалить="apagar {n} {Т}", путь_переместить="mover {n} {Т}",
               довод_осторожная="uma personalidade prudente não apaga",
               довод_скорая="uma personalidade rápida toma o primeiro caminho",
               черта_форма="brevidade", черта_выбор="prudência",
               из_показов="das mostras", из_ошибки="de um erro", из_приказа="de uma ordem",
               объявление="a minha {ЧЕРТА} vem {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "nl": dict(личность="persoonlijkheid", краткая="beknopte", подробная="uitvoerige",
               осторожная="voorzichtige", скорая="snelle",
               два_пути="twee wegen", или="of", оба="beide laten",
               вопрос_счёт="hoeveel {Тмн} liggen {М}?", вопрос_путь="welke weg wordt gekozen?",
               вопрос_одно="is het hetzelfde getal?", вопрос_откуда="waar komt mijn {ЧЕРТА} vandaan?",
               отвечает="antwoordt", одно_число="één getal",
               путь_удалить="{n} {Т} verwijderen", путь_переместить="{n} {Т} verplaatsen",
               довод_осторожная="een voorzichtige persoonlijkheid verwijdert niet",
               довод_скорая="een snelle persoonlijkheid neemt de eerste weg",
               черта_форма="beknoptheid", черта_выбор="voorzichtigheid",
               из_показов="uit de toningen", из_ошибки="uit een fout", из_приказа="uit een opdracht",
               объявление="mijn {ЧЕРТА} komt {ОТКУДА}.", двоеточие=": ", вопрос="?"),
    "pl": dict(личность="osobowość", краткая="zwięzła", подробная="szczegółowa",
               осторожная="ostrożna", скорая="szybka",
               два_пути="dwie drogi", или="albo", оба="obie zostawiają",
               вопрос_счёт="ile {Тмн} jest {М}?", вопрос_путь="która droga jest wybrana?",
               вопрос_одно="czy to ta sama liczba?", вопрос_откуда="skąd bierze się moja {ЧЕРТА}?",
               отвечает="odpowiada", одно_число="jedna liczba",
               путь_удалить="usunąć {n} {Т}", путь_переместить="przenieść {n} {Т}",
               довод_осторожная="ostrożna osobowość nie usuwa",
               довод_скорая="szybka osobowość wybiera pierwszą drogę",
               черта_форма="zwięzłość", черта_выбор="ostrożność",
               из_показов="z pokazów", из_ошибки="z błędu", из_приказа="z rozkazu",
               объявление="moja {ЧЕРТА} bierze się {ОТКУДА}.", двоеточие=": ", вопрос="?"),
}
# ИМЯ ЧЕРТЫ — СВОЁ У КАЖДОЙ: без него две черты одной оси спрашивались бы одним словом,
# и половина показов происхождения схлопывалась в копии («откуда моя краткость?» стояло и
# при подробной личности). Черта, у которой нет имени, не медленная переменная, а ярлык.
ИМЯ_ЧЕРТЫ = {
    "ru": dict(краткая="краткость", подробная="подробность", осторожная="осторожность", скорая="скорость"),
    "en": dict(краткая="brevity", подробная="thoroughness", осторожная="caution", скорая="speed"),
    "de": dict(краткая="Kürze", подробная="Ausführlichkeit", осторожная="Vorsicht", скорая="Schnelligkeit"),
    "fr": dict(краткая="brièveté", подробная="précision", осторожная="prudence", скорая="rapidité"),
    "es": dict(краткая="brevedad", подробная="minuciosidad", осторожная="prudencia", скорая="rapidez"),
    "it": dict(краткая="brevità", подробная="precisione", осторожная="prudenza", скорая="rapidità"),
    "pt": dict(краткая="brevidade", подробная="minúcia", осторожная="prudência", скорая="rapidez"),
    "nl": dict(краткая="beknoptheid", подробная="uitvoerigheid", осторожная="voorzichtigheid", скорая="snelheid"),
    "pl": dict(краткая="zwięzłość", подробная="szczegółowość", осторожная="ostrożność", скорая="szybkość"),
}
ФОРМЫ = ("кратко", "подробно", "два_ответа", "выбор_при_равных", "происхождение")


def _вещь(язык, Т, c):
    return S._счёт(T.ВЕЩИ[язык][Т % len(T.ВЕЩИ[язык])], c, язык)


def _голова(язык, черта):
    """«личность: краткая.» — the slow variable, written before anything it touches."""
    с = СЛОВА[язык]
    return с["личность"] + с["двоеточие"] + с[черта] + "."


def _история(язык, М):
    """The tape: a place holds n things and one act adds m — the episode house's own words."""
    начало = E.РЕЧЬ[язык]["начало"].replace("{М}", М)
    шаг = (E.РЕЧЬ[язык]["шаг_плюс"].replace("{П}", E.ПОРЯДОК[язык][0])
           .replace("{m}", "{m1}").replace("{Тm}", "{Тm1}"))
    return начало + " " + шаг


def рамка(язык, форма, черта=None, М=None, источник=None, выбор=None):
    с = СЛОВА[язык]
    if форма == "происхождение":
        # МЕДЛЕННАЯ ПЕРЕМЕННАЯ НАЗЫВАЕТ СВОЁ ПРОИСХОЖДЕНИЕ, иначе это вкус, а не состояние
        имя = ИМЯ_ЧЕРТЫ[язык][черта]
        откуда = {"показы": с["из_показов"], "ошибка": с["из_ошибки"], "приказ": с["из_приказа"]}[источник]
        объявление = с["объявление"].replace("{ЧЕРТА}", имя).replace("{ОТКУДА}", откуда)
        вопрос = с["вопрос_откуда"].replace("{ЧЕРТА}", имя)
        return объявление + " " + вопрос + " " + откуда + "."
    if форма == "выбор_при_равных":
        # ВЫБОР ЛИЧНОСТИ ЗАКОНЕН ЛИШЬ ТАМ, ГДЕ ИСХОДЫ РАВНЫ, И РАВЕНСТВО ПЕРЕСЧИТЫВАЕТСЯ
        путь1 = с["путь_удалить"].replace("{n}", "{m1}").replace("{Т}", "{Тm1}")
        путь2 = с["путь_переместить"].replace("{n}", "{m1}").replace("{Т}", "{Тm1}")
        начало = E.РЕЧЬ[язык]["начало"].replace("{М}", М)
        пути = "%s%s%s %s %s." % (с["два_пути"], с["двоеточие"], путь1, с["или"], путь2)
        равно = "%s {v} {Тv} %s%s{n} − {m1} = {v}." % (с["оба"], М, с["двоеточие"])
        взят = путь1 if выбор == "удалить" else путь2
        довод = с["довод_осторожная"] if черта == "осторожная" else с["довод_скорая"]
        ответ = взят + с["двоеточие"] + довод + "."
        return (_голова(язык, черта) + " " + начало + " " + пути + " " + равно + " "
                + с["вопрос_путь"] + " " + ответ)
    история = _история(язык, М)
    вопрос = с["вопрос_счёт"].replace("{Тмн}", "{Тмн}").replace("{М}", М)
    состояние = E.РЕЧЬ[язык]["состояние"].replace("{М}", М)
    леджер = "{n} + {m1} = {v}"
    if форма == "кратко":
        # КРАТКАЯ ЛИЧНОСТЬ ОТВЕЧАЕТ ОДНИМ ЧИСЛОМ — ни предложения, ни леджера
        return _голова(язык, "краткая") + " " + история + " " + вопрос + " {v}."
    if форма == "подробно":
        return (_голова(язык, "подробная") + " " + история + " " + вопрос + " "
                + состояние + с["двоеточие"] + леджер + ".")
    # ДВА ОТВЕТА НА ОДНОЙ СТРАНИЦЕ: закон стоит в корпусе, а не только в суде
    краткий = "%s %s %s {v}." % (с["краткая"], с["личность"], с["отвечает"])
    подробный = "%s %s %s%s%s%s%s." % (с["подробная"], с["личность"], с["отвечает"],
                                       с["двоеточие"], состояние, с["двоеточие"], леджер)
    ответ = "{ДА}%s{v} %s {v} — %s." % (с["двоеточие"], СОЮЗ[язык], с["одно_число"])
    return (история + " " + вопрос + " " + краткий + " " + подробный + " "
            + с["вопрос_одно"] + " " + ответ)


СОЮЗ = {"ru": "и", "en": "and", "de": "und", "fr": "et", "es": "y", "it": "e", "pt": "e",
        "nl": "en", "pl": "i"}
import json  # noqa: E402 — packs are read below, after the tables they fill
_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ДА = {язык: str((json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
                 .get("polarity") or {}).get("yes", ["да"])[0]) for язык in ЯЗЫКИ}


def страница(язык, форма, Т, n, m, М=None, черта=None, источник=None, выбор=None):
    с = СЛОВА[язык]
    М = М if М is not None else T.МЕСТА[язык][Т % len(T.МЕСТА[язык])]
    if форма == "происхождение":
        return рамка(язык, форма, черта=черта, источник=источник)
    if форма == "выбор_при_равных":
        v = n - m
        поля = dict(n=n, m1=m, v=v, Тm1=_вещь(язык, Т, m), Тv=_вещь(язык, Т, v),
                    Тn=_вещь(язык, Т, n))
        if язык in T.ЕСТЬ:
            поля["ЕСТЬn"] = T._есть(язык, n)
        return рамка(язык, форма, черта=черта, М=М, выбор=выбор).format(**поля)
    v = n + m
    поля = dict(n=n, m1=m, v=v, Тn=_вещь(язык, Т, n), Тm1=_вещь(язык, Т, m),
                Тv=_вещь(язык, Т, v), Тмн=_вещь(язык, Т, 5), ДА=ДА[язык])
    if язык in T.ЕСТЬ:
        поля["ЕСТЬn"] = T._есть(язык, n)
        поля["ЕСТЬv"] = T._есть(язык, v)
    return рамка(язык, форма, М=М).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(T.ВЕЩИ[язык])
        мест = len(T.МЕСТА[язык])
        for i, n in enumerate(НАЧАЛА):
            for j, m in enumerate(ШАГИ):
                Т = (i + j) % видов
                М = T.МЕСТА[язык][(i + j) % мест]
                for форма in ("кратко", "подробно", "два_ответа"):
                    вон[страница(язык, форма, Т, n, m, М)] = (язык, форма)
                if n - m >= 1:
                    for черта, выбор in (("осторожная", "переместить"), ("скорая", "удалить")):
                        вон[страница(язык, "выбор_при_равных", Т, n, m, М, черта=черта, выбор=выбор)] = (язык, "выбор_при_равных")
        for черта in ЧЕРТЫ_ФОРМЫ + ЧЕРТЫ_ВЫБОРА:
            for источник in ИСТОЧНИКИ:
                вон[страница(язык, "происхождение", 0, 0, 0, черта=черта, источник=источник)] = (язык, "происхождение")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    вещи = _альт(T.ФОРМЫ_ВЕЩЕЙ[язык])
    есть = _альт(T.ЕСТЬ[язык]) if язык in T.ЕСТЬ else None
    дыры = {"n": r"\d+", "m1": r"\d+", "v": r"\d+", "Тn": вещи, "Тm1": вещи, "Тv": вещи,
            "Тмн": вещи, "ДА": re.escape(ДА[язык])}
    if есть:
        дыры["ЕСТЬn"] = есть
        дыры["ЕСТЬv"] = есть
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


def _все_рамки():
    вон = []
    for язык in ЯЗЫКИ:
        for М in T.МЕСТА[язык]:
            for форма in ("кратко", "подробно", "два_ответа"):
                вон.append((_образец(язык, рамка(язык, форма, М=М)), язык, форма, {}))
            for черта in ЧЕРТЫ_ВЫБОРА:
                for выбор in ("удалить", "переместить"):
                    вон.append((_образец(язык, рамка(язык, "выбор_при_равных", черта=черта, М=М, выбор=выбор)),
                                язык, "выбор_при_равных", {"черта": черта, "выбор": выбор}))
        for черта in ЧЕРТЫ_ФОРМЫ + ЧЕРТЫ_ВЫБОРА:
            for источник in ИСТОЧНИКИ:
                вон.append((_образец(язык, рамка(язык, "происхождение", черта=черта, источник=источник)),
                            язык, "происхождение", {"черта": черта, "источник": источник}))
    return вон


ОБРАЗЦЫ = _все_рамки()


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вердикт(язык, форма, добавка, зн):
    if форма == "происхождение":
        # ЧЕРТА И ЕЁ ИСТОЧНИК СТОЯТ В РАМКЕ; ЗАКОН — ЧТО ОСЬ ЧЕРТЫ СОВПАДАЕТ С ЕЁ ИМЕНЕМ
        return True
    n, m, v = int(зн["n"]), int(зн["m1"]), int(зн["v"])
    if n < 1 or m < 1:
        return False
    пары = [("Тn", n), ("Тm1", m), ("Тv", v)]
    виды = None
    for дыра, число in пары:
        if дыра not in зн:
            continue
        свои = {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн[дыра], set())
                if Т != "строка" and S._счёт(T.ВЕЩИ[язык][Т], число, язык) == зн[дыра]}
        if not свои:
            return False
        виды = свои if виды is None else виды & свои
        if not виды:
            return False
    if "Тмн" in зн and not ({Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн["Тмн"], set()) if Т != "строка"} & (виды or set())):
        return False
    if язык in T.ЕСТЬ:
        if "ЕСТЬn" in зн and зн["ЕСТЬn"] != T._есть(язык, n):
            return False
        if "ЕСТЬv" in зн and зн["ЕСТЬv"] != T._есть(язык, v):
            return False
    if форма == "выбор_при_равных":
        # РАВЕНСТВО ИСХОДОВ ПЕРЕСЧИТЫВАЕТСЯ: выбор по характеру законен ТОЛЬКО между равными
        if v != n - m or v < 1:
            return False
        # ОСТОРОЖНАЯ БЕРЁТ ТО, ЧТО НЕ РАЗРУШАЕТ; СКОРАЯ — ПЕРВЫЙ НАЗВАННЫЙ ПУТЬ
        нужный = "переместить" if добавка["черта"] == "осторожная" else "удалить"
        return добавка["выбор"] == нужный
    # ЛЕНТА ПЕРЕСЧИТЫВАЕТСЯ, И ФАКТ ОДИН ПРИ ЛЮБОЙ ЛИЧНОСТИ
    return v == n + m


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose fact recomputes; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, добавка in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, добавка, зн)
    return False, False


def _хвост(с):
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        Т, n, m = 0, 10, 3
        М = T.МЕСТА[язык][0]
        # (1) КРАТКАЯ ЛИЧНОСТЬ НАЗВАЛА ЧУЖОЕ ЧИСЛО
        к = страница(язык, "кратко", Т, n, m, М)
        assert судить(к) == (True, True), к
        битая = к[:_хвост(к)] + к[_хвост(к):].replace("13", "14")
        assert судить(битая) == (True, False), битая
        # (2) ПОДРОБНАЯ ЛИЧНОСТЬ: ЛЕДЖЕР НЕ СХОДИТСЯ
        п = страница(язык, "подробно", Т, n, m, М)
        assert судить(п) == (True, True), п
        битая = п[:п.rindex("= ")] + "= 14."
        assert судить(битая) == (True, False), битая
        # (3) ДВА ОТВЕТА РАЗОШЛИСЬ ЧИСЛОМ — личность изменила ФАКТ
        д = страница(язык, "два_ответа", Т, n, m, М)
        assert судить(д) == (True, True), д
        битая = д.replace("13", "14", 1)
        assert судить(битая) == (True, False), битая
        # (4) ОСТОРОЖНАЯ ЛИЧНОСТЬ ВЫБРАЛА УДАЛЕНИЕ
        в = страница(язык, "выбор_при_равных", Т, n, m, М, черта="осторожная", выбор="переместить")
        assert судить(в) == (True, True), в
        битая = страница(язык, "выбор_при_равных", Т, n, m, М, черта="осторожная", выбор="удалить")
        assert судить(битая) == (True, False), битая
        # (5) СКОРАЯ ЛИЧНОСТЬ ВЗЯЛА ВТОРОЙ ПУТЬ
        битая = страница(язык, "выбор_при_равных", Т, n, m, М, черта="скорая", выбор="переместить")
        assert судить(битая) == (True, False), битая
        # (6) РАВЕНСТВО ИСХОДОВ ОБЪЯВЛЕНО, А ЧИСЛА НЕ СХОДЯТСЯ
        битая = в.replace("= 7.", "= 8.")
        assert судить(битая) == (True, False), битая
        мутанты += 6
        # (7) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        и = страница(язык, "происхождение", 0, 0, 0, черта="краткая", источник="показы")
        for стр in (к, п, д, в, и):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "кратко", 0, 10, 3, T.МЕСТА[язык][0]))
    for язык in ("ru", "en", "pl", "de"):
        print("  ", страница(язык, "подробно", 0, 10, 3, T.МЕСТА[язык][0]))
        print("  ", страница(язык, "два_ответа", 0, 10, 3, T.МЕСТА[язык][0]))
        print("  ", страница(язык, "выбор_при_равных", 0, 10, 3, T.МЕСТА[язык][0], черта="осторожная", выбор="переместить"))
        print("  ", страница(язык, "происхождение", 0, 0, 0, черта="осторожная", источник="ошибка"))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
