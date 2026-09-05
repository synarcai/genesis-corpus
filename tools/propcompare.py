#!/usr/bin/env python3
"""THE HOUSE OF PROPERTY COMPARISON — «which is heavier: a stone or a feather?
a stone.» in nine languages.

Born from the fifth band of conversation (BESEDA-5, 05.09): «что тяжелее:
камень или перо?» was mute in all nine languages — the comparison worlds
compare COUNTS («8 more coins»), never things by a property. Five properties (heavy, hard, hot, fast, tall — size belongs to the house of the scale), each with one declared pair (winner, loser)
per language and its two comparatives (heavier / lighter); the question is
asked in both orders and both directions, and the answer is the thing the
comparative picks. Generator and court read one table; the world is CLOSED.

    python3 tools/propcompare.py    # self-check with mutants
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# ВЕЛИЧИНА ПРИНАДЛЕЖИТ ДОМУ ШКАЛЫ (мышь < кошка < … < слон в en/de/fr/nl/pl): его суд читает
# «which is bigger: a mouse or an elephant?» своей рамкой и звал голый ответ ложью — два дома об
# одном роде суть захват. Свойство заменено твёрдостью (камень — подушка).
СВОЙСТВА = ("тяжесть", "твёрдость", "жар", "скорость", "рост")

# per language: the question frame «which is {C}: {X} or {Y}? {W}.», and per
# property the comparatives (more, less) and the pair (winner, loser)
ЯЗЫКИ = {
    "ru": dict(рамка=("что {C}: {X} или {Y}?", "{W}."),
               сравн={"тяжесть": ("тяжелее", "легче"), "твёрдость": ("твёрже", "мягче"), "жар": ("горячее", "холоднее"),
                      "скорость": ("быстрее", "медленнее"), "рост": ("выше", "ниже")},
               пары={"тяжесть": ("камень", "перо"), "твёрдость": ("камень", "подушка"), "жар": ("огонь", "лёд"),
                     "скорость": ("заяц", "черепаха"), "рост": ("жираф", "кошка")}),
    "en": dict(рамка=("which is {C}: {X} or {Y}?", "{W}."),
               сравн={"тяжесть": ("heavier", "lighter"), "твёрдость": ("harder", "softer"), "жар": ("hotter", "colder"),
                      "скорость": ("faster", "slower"), "рост": ("taller", "shorter")},
               пары={"тяжесть": ("a stone", "a feather"), "твёрдость": ("a stone", "a pillow"), "жар": ("fire", "ice"),
                     "скорость": ("a hare", "a tortoise"), "рост": ("a giraffe", "a cat")}),
    "de": dict(рамка=("was ist {C}: {X} oder {Y}?", "{W}."),
               сравн={"тяжесть": ("schwerer", "leichter"), "твёрдость": ("härter", "weicher"), "жар": ("heißer", "kälter"),
                      "скорость": ("schneller", "langsamer"), "рост": ("höher", "niedriger")},
               пары={"тяжесть": ("ein Stein", "eine Feder"), "твёрдость": ("ein Stein", "ein Kissen"), "жар": ("Feuer", "Eis"),
                     "скорость": ("ein Hase", "eine Schildkröte"), "рост": ("eine Giraffe", "eine Katze")}),
    "fr": dict(рамка=("qu'est-ce qui est {C} : {X} ou {Y} ?", "{W}."), рамка2=("lequel est le {C} : {X} ou {Y} ?", "{W}."),
               сравн={"тяжесть": ("plus lourd", "plus léger"), "твёрдость": ("plus dur", "plus mou"), "жар": ("plus chaud", "plus froid"),
                      "скорость": ("plus rapide", "plus lent"), "рост": ("plus haut", "plus bas")},
               пары={"тяжесть": ("une pierre", "une plume"), "твёрдость": ("une pierre", "un coussin"), "жар": ("le feu", "la glace"),
                     "скорость": ("un lièvre", "une tortue"), "рост": ("une girafe", "un chat")}),
    "es": dict(рамка=("¿qué {C}: {X} o {Y}?", "{W}."),
               сравн={"тяжесть": ("pesa más", "pesa menos"), "твёрдость": ("es más duro", "es más blando"), "жар": ("está más caliente", "está más frío"),
                      "скорость": ("es más rápido", "es más lento"), "рост": ("es más alto", "es más bajo")},
               пары={"тяжесть": ("una piedra", "una pluma"), "твёрдость": ("una piedra", "una almohada"), "жар": ("el fuego", "el hielo"),
                     "скорость": ("una liebre", "una tortuga"), "рост": ("una jirafa", "un gato")}),
    "it": dict(рамка=("cosa è {C}: {X} o {Y}?", "{W}."),
               сравн={"тяжесть": ("più pesante", "più leggero"), "твёрдость": ("più duro", "più morbido"), "жар": ("più caldo", "più freddo"),
                      "скорость": ("più veloce", "più lento"), "рост": ("più alto", "più basso")},
               пары={"тяжесть": ("una pietra", "una piuma"), "твёрдость": ("una pietra", "un cuscino"), "жар": ("il fuoco", "il ghiaccio"),
                     "скорость": ("una lepre", "una tartaruga"), "рост": ("una giraffa", "un gatto")}),
    "pt": dict(рамка=("o que é {C}: {X} ou {Y}?", "{W}."),
               сравн={"тяжесть": ("mais pesado", "mais leve"), "твёрдость": ("mais duro", "mais macio"), "жар": ("mais quente", "mais frio"),
                      "скорость": ("mais rápido", "mais lento"), "рост": ("mais alto", "mais baixo")},
               пары={"тяжесть": ("uma pedra", "uma pena"), "твёрдость": ("uma pedra", "uma almofada"), "жар": ("o fogo", "o gelo"),
                     "скорость": ("uma lebre", "uma tartaruga"), "рост": ("uma girafa", "um gato")}),
    "nl": dict(рамка=("wat is {C}: {X} of {Y}?", "{W}."),
               сравн={"тяжесть": ("zwaarder", "lichter"), "твёрдость": ("harder", "zachter"), "жар": ("heter", "kouder"),
                      "скорость": ("sneller", "langzamer"), "рост": ("hoger", "lager")},
               пары={"тяжесть": ("een steen", "een veer"), "твёрдость": ("een steen", "een kussen"), "жар": ("vuur", "ijs"),
                     "скорость": ("een haas", "een schildpad"), "рост": ("een giraf", "een kat")}),
    "pl": dict(рамка=("co jest {C}: {X} czy {Y}?", "{W}."),
               сравн={"тяжесть": ("cięższe", "lżejsze"), "твёрдость": ("twardsze", "bardziej miękkie"), "жар": ("gorętsze", "zimniejsze"),
                      "скорость": ("szybsze", "wolniejsze"), "рост": ("wyższe", "niższe")},
               пары={"тяжесть": ("kamień", "pióro"), "твёрдость": ("kamień", "poduszka"), "жар": ("ogień", "lód"),
                     "скорость": ("zając", "żółw"), "рост": ("żyrafa", "kot")}),
}

for _яз, _я in ЯЗЫКИ.items():
    assert set(_я["сравн"]) == set(СВОЙСТВА) == set(_я["пары"]), _яз
    _слова = [с for п in _я["сравн"].values() for с in п]
    assert len(_слова) == len(set(_слова)), (_яз, "сравнительное в двух свойствах")


def страница(язык, свойство, порядок=0, направление=0, рамка="рамка"):
    """порядок 0/1 — the pair asked as (winner, loser) or reversed; направление 0/1 —
    the «more» comparative (answer: the winner) or the «less» one (answer: the loser)."""
    я = ЯЗЫКИ[язык]
    w, l = я["пары"][свойство]
    C = я["сравн"][свойство][направление]
    X, Y = (w, l) if порядок == 0 else (l, w)
    W = w if направление == 0 else l
    воп, отв = я[рамка]
    return f"{воп.format(C=C, X=X, Y=Y)} {отв.format(W=W)}"


def _показы():
    return {страница(язык, св, п, н, р): (язык, св)
            for язык, я in ЯЗЫКИ.items() for р in ("рамка", "рамка2") if р in я
            for св in СВОЙСТВА for п in (0, 1) for н in (0, 1)}


ПОКАЗЫ = _показы()


def _образцы():
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    for язык, я in ЯЗЫКИ.items():
        вещи = [в for п in я["пары"].values() for в in п]
        дыры = {"C": "(?P<C>" + alt(с for п in я["сравн"].values() for с in п)[3:],
                "X": "(?P<X>" + alt(вещи)[3:], "Y": "(?P<Y>" + alt(вещи)[3:], "W": "(?P<W>" + alt(вещи)[3:]}
        for р in ("рамка", "рамка2"):
            if р not in я:
                continue
            шаблон = " ".join(я[р])
            куски = [дыры[к[1:-1]] if к.startswith("{") else re.escape(к) for к in re.split(r"(\{[^}]+\})", шаблон)]
            вон.append((re.compile("^" + "".join(куски) + "$"), язык))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): the comparative names a property, the two things are its
    declared pair, and the answer is the thing that comparative picks."""
    с = строка.strip()
    for образ, язык in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        я = ЯЗЫКИ[язык]; г = м.groupdict()
        свойство = next((св for св, п in я["сравн"].items() if г["C"] in п), None)
        if свойство is None:
            return True, False
        w, l = я["пары"][свойство]
        if {г["X"], г["Y"]} != {w, l}:
            return True, False
        направление = я["сравн"][свойство].index(г["C"])
        return True, г["W"] == (w if направление == 0 else l)
    return False, False


def _самопроверка():
    for показ, (язык, св) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, св, показ)
    мутанты = 0
    for язык, я in ЯЗЫКИ.items():
        w, l = я["пары"]["тяжесть"]
        # MUTANT: the loser named as the heavier; the pair of another property
        воп, отв = я["рамка"]
        битая = f"{воп.format(C=я['сравн']['тяжесть'][0], X=w, Y=l)} {отв.format(W=l)}"
        assert судить(битая) == (True, False), битая
        с = страница(язык, "тяжесть", 0, 0)
        w2, l2 = я["пары"]["скорость"]
        битая = с.replace(l, l2, 1)
        assert судить(битая) == (True, False), битая
        мутанты += 2
    for язык in ("ru", "en", "fr", "pl"):
        print("  ", страница(язык, "тяжесть", 0, 0)); print("  ", страница(язык, "тяжесть", 1, 1))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, свойств {len(СВОЙСТВА)})")


if __name__ == "__main__":
    _самопроверка()
