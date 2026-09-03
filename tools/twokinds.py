#!/usr/bin/env python3
"""THE HOUSE OF TWO KINDS — a system of two unknowns, and its chain of primitives.

e9's order (03.09, the profile of muteness, genus 5): the band asks «there
are 20 animals … 70 legs, how many cows?» and the organism is mute — not
because the arithmetic is hard, but because the page never says how many
legs a cow has. His condition, word for word: the page must NAME the numbers
of the genus, «without “a chicken has 2 legs” on the page the organism has
nowhere to take the two from», and the answer must be a chain of primitives,
not a guess:

  «there are 20 animals in a farm, chickens and cows. a chicken has 2 legs
   and a cow has 4 legs. there are 70 legs in all. how many cows are there?
   2 × 20 = 40, 70 − 40 = 30, 4 − 2 = 2, 30 ÷ 2 = 15. so the answer is 15.»
  «… how many chickens are there? 2 × 20 = 40, 70 − 40 = 30, 4 − 2 = 2,
   30 ÷ 2 = 15, 20 − 15 = 5. so the answer is 5.»

The chain is the substitution written out: all of the lesser kind would give
2 × 20 legs; the surplus 70 − 40 is bought by swaps, each swap adding 4 − 2;
hence the number of the greater kind. Every step is a primitive the organism
owns, and the two numbers of the genus stand on the page.

THE FORMS ARE DECLARED, NOT DERIVED. Russian counts «2 ноги» and «5 ног»,
German «2 Beine»; the house declares every count form it uses, because no
case and no plural is ever guessed (the same law as in the house of action
pages).
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]


def _счёт(формы, n):
    """The count form: (one, few, many) for Russian, (one, many) elsewhere, and
    a single declared form where the language does not bend it."""
    if len(формы) == 1:
        return формы[0]
    if len(формы) == 3:
        сотня, десяток = n % 100, n % 10
        if 11 <= сотня <= 14:
            return формы[2]
        if десяток == 1:
            return формы[0]
        if 2 <= десяток <= 4:
            return формы[1]
        return формы[2]
    return формы[0] if n == 1 else формы[1]


# per language: the pairs of kinds with their «weights» (legs, wheels, pages),
# every count form declared
ЯЗЫКИ = {
    "en": dict(
        пары=(
            dict(род=("animals",), мал=("chicken", "chickens"), бол=("cow", "cows"), вес=("leg", "legs"), в_мал=2, в_бол=4, место="a farm"),
            dict(род=("vehicles",), мал=("bicycle", "bicycles"), бол=("car", "cars"), вес=("wheel", "wheels"), в_мал=2, в_бол=4, место="a yard"),
            # the LESSER kind carries the LESSER weight, or the chain would run
            # through negative numbers — the substitution counts swaps upward
            dict(род=("insects",), мал=("beetle", "beetles"), бол=("spider", "spiders"), вес=("leg", "legs"), в_мал=6, в_бол=8, место="a box"),
        ),
        целое="there are {n} {Р} in {П}, {МАЛ} and {БОЛ}.",
        веса="{Мод} has {вм} {Вм} and {Бод} has {вб} {Вб}.",
        всего="there are {L} {В} in all.",
        воп_бол="how many {БОЛ} are there?", воп_мал="how many {МАЛ} are there?",
        один=("a ", "a "), ответ="so the answer is {r}.",
    ),
    "ru": dict(
        пары=(
            dict(род=("животное", "животных", "животных"), мал=("курица", "курицы", "куриц"), бол=("корова", "коровы", "коров"),
                 вес=("нога", "ноги", "ног"), в_мал=2, в_бол=4, место="на ферме", мал_од="курицы", бол_од="коровы"),
            dict(род=("машина", "машины", "машин"), мал=("велосипед", "велосипеда", "велосипедов"), бол=("автомобиль", "автомобиля", "автомобилей"),
                 вес=("колесо", "колеса", "колёс"), в_мал=2, в_бол=4, место="во дворе", мал_од="велосипеда", бол_од="автомобиля"),
            dict(род=("насекомое", "насекомых", "насекомых"), мал=("жук", "жука", "жуков"), бол=("паук", "паука", "пауков"),
                 вес=("нога", "ноги", "ног"), в_мал=6, в_бол=8, место="в коробке", мал_од="жука", бол_од="паука"),
        ),
        целое="{П} {n} {Р}, {МАЛ} и {БОЛ}.",
        веса="у {Мод} {вм} {Вм}, а у {Бод} {вб} {Вб}.",
        всего="всего {L} {В}.",
        воп_бол="сколько {БОЛм}?", воп_мал="сколько {МАЛм}?",
        ответ="значит ответ: {r}.",
    ),
    "de": dict(
        пары=(
            dict(род=("Tiere",), мал=("Huhn", "Hühner"), бол=("Kuh", "Kühe"), вес=("Bein", "Beine"), в_мал=2, в_бол=4,
                 место="einem Hof", мал_од="ein Huhn", бол_од="eine Kuh"),
            dict(род=("Fahrzeuge",), мал=("Fahrrad", "Fahrräder"), бол=("Auto", "Autos"), вес=("Rad", "Räder"), в_мал=2, в_бол=4,
                 место="einem Hof", мал_од="ein Fahrrad", бол_од="ein Auto"),
            dict(род=("Insekten",), мал=("Käfer", "Käfer"), бол=("Spinne", "Spinnen"), вес=("Bein", "Beine"), в_мал=6, в_бол=8,
                 место="einer Kiste", мал_од="ein Käfer", бол_од="eine Spinne"),
        ),
        целое="es gibt {n} {Р} in {П}, {МАЛ} und {БОЛ}.",
        веса="{Мод} hat {вм} {Вм} und {Бод} hat {вб} {Вб}.",
        всего="es gibt insgesamt {L} {В}.",
        воп_бол="wie viele {БОЛ} gibt es?", воп_мал="wie viele {МАЛ} gibt es?",
        ответ="also ist die Antwort {r}.",
    ),
}


def _мн(пара, ключ, язык):
    """The plural of a kind — the form that names the kind itself."""
    формы = пара[ключ]
    return формы[-1] if язык == "ru" else формы[1]


def _одиночный(пара, ключ, язык):
    """«a chicken», «у курицы», «ein Huhn» — the bearer of the weight."""
    if язык == "ru":
        return пара[ключ + "_од"]
    if язык == "de":
        return пара[ключ + "_од"]
    return "a " + пара[ключ][0]


def страница(язык, пара, n, бол, спрос="бол"):
    """n of both kinds, `бол` of the greater kind; the ledger of substitution."""
    я = ЯЗЫКИ[язык]
    п = я["пары"][пара]
    вм, вб = п["в_мал"], п["в_бол"]
    if вм >= вб or not 0 <= бол <= n:
        raise ValueError("цепочка ушла бы в отрицательные числа")
    мал = n - бол
    L = вм * мал + вб * бол
    все_мал = вм * n
    остаток = L - все_мал
    шаг = вб - вм
    r = бол if спрос == "бол" else мал
    з = dict(n=n, L=L, Р=_счёт(п["род"], n), П=п["место"],
             МАЛ=_мн(п, "мал", язык), БОЛ=_мн(п, "бол", язык),
             МАЛм=_мн(п, "мал", язык), БОЛм=_мн(п, "бол", язык),
             Мод=_одиночный(п, "мал", язык), Бод=_одиночный(п, "бол", язык),
             вм=вм, вб=вб, Вм=_счёт(п["вес"], вм), Вб=_счёт(п["вес"], вб), В=_счёт(п["вес"], L))
    факт = " ".join((я["целое"].format(**з), я["веса"].format(**з), я["всего"].format(**з)))
    воп = (я["воп_бол"] if спрос == "бол" else я["воп_мал"]).format(**з)
    шаги = [f"{вм} × {n} = {все_мал}", f"{L} − {все_мал} = {остаток}", f"{вб} − {вм} = {шаг}", f"{остаток} ÷ {шаг} = {бол}"]
    if спрос == "мал":
        шаги.append(f"{n} − {бол} = {мал}")
    return f"{факт} {воп} {', '.join(шаги)}. {я['ответ'].format(r=r)}"


# --- the court's side ---
def _альт(слова):
    return "(" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    роды, малые, большие, веса, места, одиночные = set(), set(), set(), set(), set(), set()
    for п in я["пары"]:
        места.add(п["место"])
        for n in range(1, 400):
            роды.add(_счёт(п["род"], n))
        малые.add(_мн(п, "мал", язык)); большие.add(_мн(п, "бол", язык))
        одиночные.add(_одиночный(п, "мал", язык)); одиночные.add(_одиночный(п, "бол", язык))
        for n in range(1, 400):
            веса.add(_счёт(п["вес"], n))
    ч = r"(\d+)"
    return {"n": ч, "L": ч, "вм": ч, "вб": ч, "r": ч,
            "Р": _альт(роды), "П": _альт(места), "МАЛ": _альт(малые), "БОЛ": _альт(большие),
            "МАЛм": _альт(малые), "БОЛм": _альт(большие), "Мод": _альт(одиночные), "Бод": _альт(одиночные),
            "Вм": _альт(веса), "Вб": _альт(веса), "В": _альт(веса),
            "л": r"((?:\d+ [+−×÷] \d+ = \d+(?:, )?)+\.)"}


def образцы(язык):
    я = ЯЗЫКИ[язык]
    дыры = _дыры(язык)
    вон = []
    for спрос, воп in (("бол", я["воп_бол"]), ("мал", я["воп_мал"])):
        ш = f"{я['целое']} {я['веса']} {я['всего']} {воп} {{л}} {я['ответ']}"
        вон.append((re.compile("^" + phrases.образец(ш, дыры) + "$"), phrases.порядок(ш), спрос))
    return вон


ОБРАЗЦЫ = {л: образцы(л) for л in ЯЗЫКИ}


def разобрать(язык, строка):
    я = ЯЗЫКИ[язык]
    for образец, имена, спрос in ОБРАЗЦЫ[язык]:
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
        пара = next((i for i, п in enumerate(я["пары"])
                     if _счёт(п["род"], int(з["n"])) == з["Р"] and _мн(п, "мал", язык) == з["МАЛ"] and _мн(п, "бол", язык) == з["БОЛ"]), None)
        if пара is None:
            continue
        п = я["пары"][пара]
        try:
            n, L, вм, вб = int(з["n"]), int(з["L"]), int(з["вм"]), int(з["вб"])
        except (KeyError, ValueError):
            continue
        if (вм, вб) != (п["в_мал"], п["в_бол"]) or вб == вм:
            continue
        остаток = L - вм * n
        if остаток < 0 or остаток % (вб - вм):
            continue
        бол = остаток // (вб - вм)
        if not 0 <= бол <= n:
            continue
        return dict(пара=пара, n=n, бол=бол, спрос=спрос)
    return None


def судить(строка):
    с = строка.strip()
    for язык in ЯЗЫКИ:
        п = разобрать(язык, с)
        if п is not None:
            try:
                return True, страница(язык, **п) == с
            except (KeyError, IndexError, ValueError, ZeroDivisionError):
                return True, False
    return False, False
