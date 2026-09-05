#!/usr/bin/env python3
"""THE HOUSE OF THE MANDATE — a standing rule against an order (05.09).

The sixth market of the agent's architecture. An agent is not only asked to do things: it is
also TOLD, once, what it may never do — and every later order must be read against that
standing rule. The corpus shows exactly that reading and nothing else:

    A RULE, AN ORDER, A VERDICT WITH ITS GROUND. «rule: do not delete files. delete 3 files.
    may the order be carried out? no: the rule forbids deleting.» The verdict never stands
    bare: it names the act the rule forbids, so a page that says «no» over an order the rule
    does not cover is a lie the court can see.

    THE PERMITTED ORDER IS SHOWN AS OFTEN AS THE FORBIDDEN ONE. «rule: do not delete files.
    create 3 files. may the order be carried out? yes: the rule forbids deleting, but this is
    creating.» A market that only ever refuses buys refusal, not reading.

    WHICH RULE, OUT OF TWO. Two rules stand, one order breaks one of them, and the answer
    names the ordinal and the act («the second rule: it forbids moving») — the agent must
    point at the rule, not merely feel bound.

    AND THE GAP IS HONEST. An order that neither rule mentions is answered «yes: no rule
    forbids creating» — the mandate's silence is a permission, and it says why.

    THE MANDATE IS COUNTABLE. «how many rules are there? two rules: they forbid deleting and
    moving.» — the count and the list are the judge's law, not the frame's decoration.

WHAT IS BORROWED: the nine languages, the things of acts and their count forms from the house
of the tool, the words of yes and no from the language packs, and the question openers from
the house of the pair. Declared here: each act in three shapes a language needs — the
prohibition («do not delete files»), the name after «forbids» («deleting», «di cancellare»,
«usuwania») and the name after «this is» («creating», «usuwanie») — the ordinals of a rule,
and the words of an empty mandate.

WHAT IS NOT MEASURED, NAMED: an order that breaks a rule PARTLY (three files of which one is
forbidden), a rule with an exception, and the priority of two rules that both apply. The
house shows the reading of a mandate, never its negotiation.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import svampforms as S  # noqa: E402 — the count cell of a pack
import toolforms as T  # noqa: E402 — the things of acts and their count forms

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"
ЯЗЫКИ = T.ЯЗЫКИ
ДЕЙСТВИЯ = ("удалить", "создать", "переместить")
ЧИСЛА = (2, 3, 5, 7)
ПАРЫ_ПРАВИЛ = ((0, 1), (0, 2), (1, 2))

# ЗАПРЕТ — повеление мандата; ИМЯ_ЗАПРЕТА — имя действия после «запрещает»; ИМЯ_ЭТО — имя
# действия после «а это»; ПРИКАЗ — повеление приказа с числом и вещью. Три формы, ибо язык
# требует трёх: «vieta di cancellare», но «questo è cancellare»; «zabrania usuwania», но
# «to jest usuwanie».
ЗАПРЕТ = {
    "ru": ("не удаляй файлы", "не создавай файлы", "не перемещай файлы"),
    "en": ("do not delete files", "do not create files", "do not move files"),
    "de": ("lösche keine Dateien", "erstelle keine Dateien", "verschiebe keine Dateien"),
    "fr": ("ne supprime pas de fichiers", "ne crée pas de fichiers", "ne déplace pas de fichiers"),
    "es": ("no borres archivos", "no crees archivos", "no muevas archivos"),
    "it": ("non cancellare file", "non creare file", "non spostare file"),
    "pt": ("não apagues ficheiros", "não cries ficheiros", "não movas ficheiros"),
    "nl": ("verwijder geen bestanden", "maak geen bestanden aan", "verplaats geen bestanden"),
    "pl": ("nie usuwaj plików", "nie twórz plików", "nie przenoś plików"),
}
ИМЯ_ЗАПРЕТА = {
    "ru": ("удаление", "создание", "перемещение"),
    "en": ("deleting", "creating", "moving"),
    "de": ("das Löschen", "das Erstellen", "das Verschieben"),
    "fr": ("la suppression", "la création", "le déplacement"),
    "es": ("borrar", "crear", "mover"),
    "it": ("di cancellare", "di creare", "di spostare"),
    "pt": ("apagar", "criar", "mover"),
    "nl": ("verwijderen", "aanmaken", "verplaatsen"),
    "pl": ("usuwania", "tworzenia", "przenoszenia"),
}
ИМЯ_ЭТО = {
    "ru": ("удаление", "создание", "перемещение"),
    "en": ("deleting", "creating", "moving"),
    "de": ("das Löschen", "das Erstellen", "das Verschieben"),
    "fr": ("la suppression", "la création", "le déplacement"),
    "es": ("borrar", "crear", "mover"),
    "it": ("cancellare", "creare", "spostare"),
    "pt": ("apagar", "criar", "mover"),
    "nl": ("verwijderen", "aanmaken", "verplaatsen"),
    "pl": ("usuwanie", "tworzenie", "przenoszenie"),
}
ПРИКАЗ = {
    "ru": ("удали {n} {Т}", "создай {n} {Т}", "перемести {n} {Т}"),
    "en": ("delete {n} {Т}", "create {n} {Т}", "move {n} {Т}"),
    "de": ("lösche {n} {Т}", "erstelle {n} {Т}", "verschiebe {n} {Т}"),
    "fr": ("supprime {n} {Т}", "crée {n} {Т}", "déplace {n} {Т}"),
    "es": ("borra {n} {Т}", "crea {n} {Т}", "mueve {n} {Т}"),
    "it": ("cancella {n} {Т}", "crea {n} {Т}", "sposta {n} {Т}"),
    "pt": ("apaga {n} {Т}", "cria {n} {Т}", "move {n} {Т}"),
    "nl": ("verwijder {n} {Т}", "maak {n} {Т} aan", "verplaats {n} {Т}"),
    "pl": ("usuń {n} {Т}", "utwórz {n} {Т}", "przenieś {n} {Т}"),
}
РЕЧЬ = {
    "ru": dict(правило="правило", первое="первое правило", второе="второе правило",
               вопрос="можно ли выполнить приказ?", вопрос_какое="какое правило запрещает это?",
               вопрос_сколько="сколько правил в мандате?",
               запрещает="правило запрещает", оно_запрещает="оно запрещает",
               а_это="а это", ни_одно="ни одно правило не запрещает",
               правил="два правила", они="они запрещают", союз="и", двоеточие=": ", вопрос_знак="?"),
    "en": dict(правило="rule", первое="the first rule", второе="the second rule",
               вопрос="may the order be carried out?", вопрос_какое="which rule forbids this?",
               вопрос_сколько="how many rules are there?",
               запрещает="the rule forbids", оно_запрещает="it forbids",
               а_это="but this is", ни_одно="no rule forbids",
               правил="two rules", они="they forbid", союз="and", двоеточие=": ", вопрос_знак="?"),
    "de": dict(правило="Regel", первое="die erste Regel", второе="die zweite Regel",
               вопрос="darf der Befehl ausgeführt werden?", вопрос_какое="welche Regel verbietet das?",
               вопрос_сколько="wie viele Regeln gibt es?",
               запрещает="die Regel verbietet", оно_запрещает="sie verbietet",
               а_это="aber das ist", ни_одно="keine Regel verbietet",
               правил="zwei Regeln", они="sie verbieten", союз="und", двоеточие=": ", вопрос_знак="?"),
    "fr": dict(правило="règle", первое="la première règle", второе="la deuxième règle",
               вопрос="est-ce que l'ordre peut être exécuté ?", вопрос_какое="quelle règle l'interdit ?",
               вопрос_сколько="combien de règles y a-t-il ?",
               запрещает="la règle interdit", оно_запрещает="elle interdit",
               а_это="mais ceci est", ни_одно="aucune règle n'interdit",
               правил="deux règles", они="elles interdisent", союз="et", двоеточие=" : ", вопрос_знак=" ?"),
    "es": dict(правило="regla", первое="la primera regla", второе="la segunda regla",
               вопрос="¿puede ejecutarse la orden?", вопрос_какое="¿qué regla lo prohíbe?",
               вопрос_сколько="¿cuántas reglas hay?",
               запрещает="la regla prohíbe", оно_запрещает="prohíbe",
               а_это="pero esto es", ни_одно="ninguna regla prohíbe",
               правил="dos reglas", они="prohíben", союз="y", двоеточие=": ", вопрос_знак="?"),
    "it": dict(правило="regola", первое="la prima regola", второе="la seconda regola",
               вопрос="si può eseguire l'ordine?", вопрос_какое="quale regola lo vieta?",
               вопрос_сколько="quante regole ci sono?",
               запрещает="la regola vieta", оно_запрещает="vieta",
               а_это="ma questo è", ни_одно="nessuna regola vieta",
               правил="due regole", они="vietano", союз="e", двоеточие=": ", вопрос_знак="?"),
    "pt": dict(правило="regra", первое="a primeira regra", второе="a segunda regra",
               вопрос="a ordem pode ser executada?", вопрос_какое="que regra o proíbe?",
               вопрос_сколько="quantas regras há?",
               запрещает="a regra proíbe", оно_запрещает="proíbe",
               а_это="mas isto é", ни_одно="nenhuma regra proíbe",
               правил="duas regras", они="proíbem", союз="e", двоеточие=": ", вопрос_знак="?"),
    "nl": dict(правило="regel", первое="de eerste regel", второе="de tweede regel",
               вопрос="kan de opdracht worden uitgevoerd?", вопрос_какое="welke regel verbiedt dit?",
               вопрос_сколько="hoeveel regels zijn er?",
               запрещает="de regel verbiedt", оно_запрещает="die verbiedt",
               а_это="maar dit is", ни_одно="geen enkele regel verbiedt",
               правил="twee regels", они="ze verbieden", союз="en", двоеточие=": ", вопрос_знак="?"),
    "pl": dict(правило="zasada", первое="pierwsza zasada", второе="druga zasada",
               вопрос="czy można wykonać polecenie?", вопрос_какое="która zasada tego zabrania?",
               вопрос_сколько="ile jest zasad?",
               запрещает="zasada zabrania", оно_запрещает="zabrania",
               а_это="a to jest", ни_одно="żadna zasada nie zabrania",
               правил="dwie zasady", они="zabraniają", союз="i", двоеточие=": ", вопрос_знак="?"),
}
ФОРМЫ = ("запрещено", "позволено", "какое_правило", "мандат_молчит", "сколько_правил")


def _пакет(язык):
    return json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))


ДА = {язык: str((_пакет(язык).get("polarity") or {}).get("yes", ["да"])[0]) for язык in ЯЗЫКИ}
НЕТ = {язык: str((_пакет(язык).get("polarity") or {}).get("no", ["нет"])[0]) for язык in ЯЗЫКИ}
for _яз in ЯЗЫКИ:
    assert ДА[_яз] and НЕТ[_яз] and "None" not in (ДА[_яз], НЕТ[_яз]), _яз


def _вещь(язык, Т, c):
    return S._счёт(T.ВЕЩИ[язык][Т % len(T.ВЕЩИ[язык])], c, язык)


def рамка(язык, форма, запреты, приказ):
    """The page's template: the mandate's rules stand written, the order is one act, and the
    verdict names the act it is grounded on."""
    р = РЕЧЬ[язык]
    if len(запреты) == 1:
        мандат = р["правило"] + р["двоеточие"] + ЗАПРЕТ[язык][запреты[0]] + "."
    else:
        мандат = " ".join(р[имя] + р["двоеточие"] + ЗАПРЕТ[язык][д] + "."
                          for имя, д in zip(("первое", "второе"), запреты))
    приказная = ПРИКАЗ[язык][приказ] + "."
    начало = мандат + " " + приказная
    if форма == "запрещено":
        вопрос, ответ = р["вопрос"], (НЕТ[язык] + р["двоеточие"] + р["запрещает"] + " "
                                      + ИМЯ_ЗАПРЕТА[язык][приказ] + ".")
    elif форма == "позволено":
        вопрос = р["вопрос"]
        ответ = (ДА[язык] + р["двоеточие"] + р["запрещает"] + " " + ИМЯ_ЗАПРЕТА[язык][запреты[0]]
                 + ", " + р["а_это"] + " " + ИМЯ_ЭТО[язык][приказ] + ".")
    elif форма == "какое_правило":
        вопрос = р["вопрос_какое"]
        какое = "первое" if запреты[0] == приказ else "второе"
        ответ = (р[какое] + р["двоеточие"] + р["оно_запрещает"] + " "
                 + ИМЯ_ЗАПРЕТА[язык][приказ] + ".")
    elif форма == "мандат_молчит":
        вопрос = р["вопрос"]
        ответ = ДА[язык] + р["двоеточие"] + р["ни_одно"] + " " + ИМЯ_ЗАПРЕТА[язык][приказ] + "."
    else:                                   # сколько_правил
        вопрос = р["вопрос_сколько"]
        ответ = (р["правил"] + р["двоеточие"] + р["они"] + " " + ИМЯ_ЗАПРЕТА[язык][запреты[0]]
                 + " " + р["союз"] + " " + ИМЯ_ЗАПРЕТА[язык][запреты[1]] + ".")
    return начало + " " + вопрос + " " + ответ


def страница(язык, форма, запреты, приказ, Т, n):
    return рамка(язык, форма, запреты, приказ).format(n=n, Т=_вещь(язык, Т, n))


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        видов = len(T.ВЕЩИ[язык])
        for Т in range(видов):
            for n in ЧИСЛА:
                for д in range(len(ДЕЙСТВИЯ)):
                    вон[страница(язык, "запрещено", (д,), д, Т, n)] = (язык, "запрещено")
                    for иной in range(len(ДЕЙСТВИЯ)):
                        if иной != д:
                            вон[страница(язык, "позволено", (д,), иной, Т, n)] = (язык, "позволено")
                for пара in ПАРЫ_ПРАВИЛ:
                    for приказ in пара:
                        вон[страница(язык, "какое_правило", пара, приказ, Т, n)] = (язык, "какое_правило")
                    третий = [д for д in range(len(ДЕЙСТВИЯ)) if д not in пара][0]
                    вон[страница(язык, "мандат_молчит", пара, третий, Т, n)] = (язык, "мандат_молчит")
                    вон[страница(язык, "сколько_правил", пара, третий, Т, n)] = (язык, "сколько_правил")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон):
    дыры = {"n": r"\d+", "Т": _альт(T.ФОРМЫ_ВЕЩЕЙ[язык])}
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
    """Every concrete shape: the frame says WHICH rules stand and WHICH act is ordered, so a
    page whose verdict contradicts its own mandate is judged by the law, not silenced."""
    вон = []
    for язык in ЯЗЫКИ:
        for д in range(len(ДЕЙСТВИЯ)):
            for приказ in range(len(ДЕЙСТВИЯ)):
                for форма in ("запрещено", "позволено"):
                    вон.append((_образец(язык, рамка(язык, форма, (д,), приказ)),
                                язык, форма, (д,), приказ))
        for пара in ПАРЫ_ПРАВИЛ:
            for приказ in range(len(ДЕЙСТВИЯ)):
                for форма in ("какое_правило", "мандат_молчит", "сколько_правил"):
                    вон.append((_образец(язык, рамка(язык, форма, пара, приказ)),
                                язык, форма, пара, приказ))
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


def _вердикт(язык, форма, запреты, приказ, зн):
    n = int(зн["n"])
    if n < 1:
        return False
    свои = {Т for Т in T.ФОРМЫ_ВЕЩЕЙ[язык].get(зн["Т"], set())
            if Т != "строка" and S._счёт(T.ВЕЩИ[язык][Т], n, язык) == зн["Т"]}
    if not свои:
        return False
    if форма == "запрещено":
        # «НЕТ» СТОИТ ЛИШЬ НАД ПРИКАЗОМ, КОТОРЫЙ ПРАВИЛО И ЗАПРЕЩАЕТ
        return приказ in запреты
    if форма == "позволено":
        # «ДА» СТОИТ ЛИШЬ НАД ПРИКАЗОМ, КОТОРОГО ПРАВИЛО НЕ КАСАЕТСЯ
        return приказ not in запреты
    if форма == "какое_правило":
        # НАЗВАННОЕ ПРАВИЛО ОБЯЗАНО БЫТЬ ТЕМ, ЧТО ЗАПРЕЩАЕТ ПРИКАЗАННОЕ, И ОНО ОДНО
        return приказ in запреты and запреты[0] != запреты[1]
    if форма == "мандат_молчит":
        # МОЛЧАНИЕ МАНДАТА ОБЪЯВЛЯЕТСЯ ЛИШЬ О ДЕЙСТВИИ, КОТОРОГО НЕТ НИ В ОДНОМ ПРАВИЛЕ
        return приказ not in запреты
    # СЧЁТ ПРАВИЛ И ИХ СПИСОК СТОЯТ В РАМКЕ: два правила — два имени, и они разные
    return len(запреты) == 2 and запреты[0] != запреты[1]


def судить(строка):
    """(судимо, истинно): a page of a frame of the house whose verdict follows its mandate."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, форма, запреты, приказ in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        return True, _вердикт(язык, форма, запреты, приказ, зн)
    return False, False


def _хвост(с):
    м = list(re.finditer(r"[?？] ", с))
    return м[-1].end() if м else 0


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        Т, n = 0, 3
        # (1) «НЕТ» НАД ПРИКАЗОМ, КОТОРОГО ПРАВИЛО НЕ КАСАЕТСЯ
        з = страница(язык, "запрещено", (0,), 0, Т, n)
        assert судить(з) == (True, True), з
        битая = страница(язык, "запрещено", (0,), 1, Т, n)
        assert судить(битая) == (True, False), битая
        # (2) «ДА» НАД ЗАПРЕЩЁННЫМ ПРИКАЗОМ
        п = страница(язык, "позволено", (0,), 1, Т, n)
        assert судить(п) == (True, True), п
        битая = страница(язык, "позволено", (0,), 0, Т, n)
        assert судить(битая) == (True, False), битая
        # (3) НАЗВАНО ПРАВИЛО, КОТОРОЕ ЭТОГО НЕ ЗАПРЕЩАЕТ
        к = страница(язык, "какое_правило", (0, 1), 1, Т, n)
        assert судить(к) == (True, True), к
        битая = страница(язык, "какое_правило", (0, 1), 2, Т, n)
        assert судить(битая) == (True, False), битая
        # (4) МОЛЧАНИЕ МАНДАТА ОБЪЯВЛЕНО НАД ЗАПРЕЩЁННЫМ ПРИКАЗОМ
        м = страница(язык, "мандат_молчит", (0, 1), 2, Т, n)
        assert судить(м) == (True, True), м
        битая = страница(язык, "мандат_молчит", (0, 1), 0, Т, n)
        assert судить(битая) == (True, False), битая
        # (5) СЧЁТНАЯ ФОРМА ВЕЩИ — ФОРМА ЧУЖОГО ЧИСЛА
        своя, чужая = _вещь(язык, Т, n), _вещь(язык, Т, 1)
        if своя != чужая:
            # ПОРЧА КЛАДЁТСЯ В ПРИКАЗ, А НЕ В ПРАВИЛО: слово запрета стоит в рамке буквой,
            # и подмена в нём есть иная страница, а не ложь этой
            битая = з.replace(f"{n} {своя}", f"{n} {чужая}", 1)
            assert судить(битая) == (True, False), битая
            мутанты += 1
        мутанты += 4
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        с = страница(язык, "сколько_правил", (0, 1), 2, Т, n)
        for стр in (з, п, к, м, с):
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "запрещено", (0,), 0, 0, 3))
    for язык, форма, зап, пр in (("ru", "позволено", (0,), 1), ("en", "какое_правило", (0, 2), 2),
                                 ("de", "мандат_молчит", (0, 1), 2), ("fr", "сколько_правил", (1, 2), 0),
                                 ("pl", "позволено", (2,), 0), ("it", "какое_правило", (1, 2), 1),
                                 ("es", "мандат_молчит", (0, 2), 1), ("pt", "сколько_правил", (0, 1), 2),
                                 ("nl", "позволено", (1,), 2)):
        print("  ", страница(язык, форма, зап, пр, 1, 5))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
