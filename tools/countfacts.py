#!/usr/bin/env python3
"""THE HOUSE OF COUNT FACTS — a thing defined or asked by the ONE number a court
can recount: the sides of a figure, the legs of an animal. Nine languages.

Born from the third band of conversation (BESEDA-3, 05.09): «что такое
треугольник?» and «сколько ног у собаки?» were mute in all nine languages —
the definitions world speaks only ru/en from the shelf, and the shelf counts
neither sides nor legs. Here every entity carries one declared count, read by
the generator and the court alike; the count stands in WORDS in the form the
phrase needs (Russian «три стороны / пять сторон», «две ноги / шесть ног»,
Polish «trzy boki / pięć boków») — declared, never derived. Two forms: the
count asked («how many legs does a dog have?») for every kind, and the
definition asked («what is a pentagon?») for the kind whose count defines it.

    python3 tools/countfacts.py    # self-check with mutants
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# KIND → (the one fact: entity → count; per language: entities in the order
# of the fact (nominative[, oblique]), count phrases by number, frames)
ВИДЫ = {
    "стороны": dict(
        факты={"треугольник": 3, "квадрат": 4, "пятиугольник": 5, "шестиугольник": 6, "восьмиугольник": 8},
        языки={
            "ru": dict(имена=(("треугольник", "треугольника"), ("квадрат", "квадрата"), ("пятиугольник", "пятиугольника"),
                              ("шестиугольник", "шестиугольника"), ("восьмиугольник", "восьмиугольника")),
                       счёт={3: "три стороны", 4: "четыре стороны", 5: "пять сторон", 6: "шесть сторон", 8: "восемь сторон"},
                       что=("что такое {Ф}?", "{Ф} — это фигура, у которой {С}."),
                       сколько=("сколько сторон у {Фр}?", "у {Фр} {С}.")),
            "en": dict(имена=(("a triangle",), ("a square",), ("a pentagon",), ("a hexagon",), ("an octagon",)),
                       счёт={3: "three sides", 4: "four sides", 5: "five sides", 6: "six sides", 8: "eight sides"},
                       что=("what is {Ф}?", "{Ф} is a shape with {С}."),
                       сколько=("how many sides does {Ф} have?", "{Ф} has {С}.")),
            "de": dict(имена=(("ein Dreieck",), ("ein Quadrat",), ("ein Fünfeck",), ("ein Sechseck",), ("ein Achteck",)),
                       счёт={3: "drei Seiten", 4: "vier Seiten", 5: "fünf Seiten", 6: "sechs Seiten", 8: "acht Seiten"},
                       что=("was ist {Ф}?", "{Ф} ist eine Figur mit {С}."),
                       сколько=("wie viele Seiten hat {Ф}?", "{Ф} hat {С}.")),
            "fr": dict(имена=(("un triangle",), ("un carré",), ("un pentagone",), ("un hexagone",), ("un octogone",)),
                       счёт={3: "trois côtés", 4: "quatre côtés", 5: "cinq côtés", 6: "six côtés", 8: "huit côtés"},
                       что=("qu'est-ce qu'{Ф} ?", "{Ф} est une figure à {С}."),
                       сколько=("combien de côtés a {Ф} ?", "{Ф} a {С}.")),
            "es": dict(имена=(("un triángulo",), ("un cuadrado",), ("un pentágono",), ("un hexágono",), ("un octágono",)),
                       счёт={3: "tres lados", 4: "cuatro lados", 5: "cinco lados", 6: "seis lados", 8: "ocho lados"},
                       что=("¿qué es {Ф}?", "{Ф} es una figura con {С}."),
                       сколько=("¿cuántos lados tiene {Ф}?", "{Ф} tiene {С}.")),
            "it": dict(имена=(("un triangolo",), ("un quadrato",), ("un pentagono",), ("un esagono",), ("un ottagono",)),
                       счёт={3: "tre lati", 4: "quattro lati", 5: "cinque lati", 6: "sei lati", 8: "otto lati"},
                       что=("che cos'è {Ф}?", "{Ф} è una figura con {С}."),
                       сколько=("quanti lati ha {Ф}?", "{Ф} ha {С}.")),
            "pt": dict(имена=(("um triângulo",), ("um quadrado",), ("um pentágono",), ("um hexágono",), ("um octógono",)),
                       счёт={3: "três lados", 4: "quatro lados", 5: "cinco lados", 6: "seis lados", 8: "oito lados"},
                       что=("o que é {Ф}?", "{Ф} é uma figura com {С}."),
                       сколько=("quantos lados tem {Ф}?", "{Ф} tem {С}.")),
            "nl": dict(имена=(("een driehoek",), ("een vierkant",), ("een vijfhoek",), ("een zeshoek",), ("een achthoek",)),
                       счёт={3: "drie zijden", 4: "vier zijden", 5: "vijf zijden", 6: "zes zijden", 8: "acht zijden"},
                       что=("wat is {Ф}?", "{Ф} is een figuur met {С}."),
                       сколько=("hoeveel zijden heeft {Ф}?", "{Ф} heeft {С}.")),
            "pl": dict(имена=(("trójkąt",), ("kwadrat",), ("pięciokąt",), ("sześciokąt",), ("ośmiokąt",)),
                       счёт={3: "trzy boki", 4: "cztery boki", 5: "pięć boków", 6: "sześć boków", 8: "osiem boków"},
                       что=("co to jest {Ф}?", "{Ф} to figura, która ma {С}."),
                       сколько=("ile boków ma {Ф}?", "{Ф} ma {С}.")),
        },
    ),
    "ноги": dict(
        факты={"собака": 4, "кошка": 4, "лошадь": 4, "корова": 4, "курица": 2, "птица": 2, "паук": 8, "жук": 6, "муравей": 6},
        языки={
            "ru": dict(имена=(("собака", "собаки"), ("кошка", "кошки"), ("лошадь", "лошади"), ("корова", "коровы"), ("курица", "курицы"),
                              ("птица", "птицы"), ("паук", "паука"), ("жук", "жука"), ("муравей", "муравья")),
                       счёт={2: "две ноги", 4: "четыре ноги", 6: "шесть ног", 8: "восемь ног"},
                       сколько=("сколько ног у {Фр}?", "у {Фр} {С}.")),
            "en": dict(имена=(("a dog",), ("a cat",), ("a horse",), ("a cow",), ("a chicken",), ("a bird",), ("a spider",), ("a beetle",), ("an ant",)),
                       счёт={2: "two legs", 4: "four legs", 6: "six legs", 8: "eight legs"},
                       сколько=("how many legs does {Ф} have?", "{Ф} has {С}.")),
            "de": dict(имена=(("ein Hund",), ("eine Katze",), ("ein Pferd",), ("eine Kuh",), ("ein Huhn",), ("ein Vogel",), ("eine Spinne",), ("ein Käfer",), ("eine Ameise",)),
                       счёт={2: "zwei Beine", 4: "vier Beine", 6: "sechs Beine", 8: "acht Beine"},
                       сколько=("wie viele Beine hat {Ф}?", "{Ф} hat {С}.")),
            "fr": dict(имена=(("un chien",), ("un chat",), ("un cheval",), ("une vache",), ("une poule",), ("un oiseau",), ("une araignée",), ("un scarabée",), ("une fourmi",)),
                       счёт={2: "deux pattes", 4: "quatre pattes", 6: "six pattes", 8: "huit pattes"},
                       сколько=("combien de pattes a {Ф} ?", "{Ф} a {С}.")),
            "es": dict(имена=(("un perro",), ("un gato",), ("un caballo",), ("una vaca",), ("una gallina",), ("un pájaro",), ("una araña",), ("un escarabajo",), ("una hormiga",)),
                       счёт={2: "dos patas", 4: "cuatro patas", 6: "seis patas", 8: "ocho patas"},
                       сколько=("¿cuántas patas tiene {Ф}?", "{Ф} tiene {С}.")),
            "it": dict(имена=(("un cane",), ("un gatto",), ("un cavallo",), ("una mucca",), ("una gallina",), ("un uccello",), ("un ragno",), ("uno scarabeo",), ("una formica",)),
                       счёт={2: "due zampe", 4: "quattro zampe", 6: "sei zampe", 8: "otto zampe"},
                       сколько=("quante zampe ha {Ф}?", "{Ф} ha {С}.")),
            "pt": dict(имена=(("um cão",), ("um gato",), ("um cavalo",), ("uma vaca",), ("uma galinha",), ("um pássaro",), ("uma aranha",), ("um escaravelho",), ("uma formiga",)),
                       счёт={2: "duas patas", 4: "quatro patas", 6: "seis patas", 8: "oito patas"},
                       сколько=("quantas patas tem {Ф}?", "{Ф} tem {С}.")),
            "nl": dict(имена=(("een hond",), ("een kat",), ("een paard",), ("een koe",), ("een kip",), ("een vogel",), ("een spin",), ("een kever",), ("een mier",)),
                       счёт={2: "twee poten", 4: "vier poten", 6: "zes poten", 8: "acht poten"},
                       сколько=("hoeveel poten heeft {Ф}?", "{Ф} heeft {С}.")),
            "pl": dict(имена=(("pies",), ("kot",), ("koń",), ("krowa",), ("kura",), ("ptak",), ("pająk",), ("chrząszcz",), ("mrówka",)),
                       счёт={2: "dwie nogi", 4: "cztery nogi", 6: "sześć nóg", 8: "osiem nóg"},
                       сколько=("ile nóg ma {Ф}?", "{Ф} ma {С}.")),
        },
    ),
}
ЯЗЫКИ = tuple(ВИДЫ["стороны"]["языки"])
ФОРМЫ = ("что", "сколько")

for _вид, _в in ВИДЫ.items():
    for _яз, _я in _в["языки"].items():
        assert len(_я["имена"]) == len(_в["факты"]), (_вид, _яз, "имён не по фактам")
        assert set(_в["факты"].values()) <= set(_я["счёт"]), (_вид, _яз, "счёт не объявлен")


def _имя(вид, язык, i):
    ф = ВИДЫ[вид]["языки"][язык]["имена"][i]
    return ф[0], (ф[1] if len(ф) > 1 else ф[0])


def страница(вид, язык, форма, i):
    в = ВИДЫ[вид]; я = в["языки"][язык]
    Ф, Фр = _имя(вид, язык, i)
    п = dict(Ф=Ф, Фр=Фр, С=я["счёт"][list(в["факты"].values())[i]])
    воп, отв = я[форма]
    return f"{воп.format(**п)} {отв.format(**п)}"


def _показы():
    вон = {}
    for вид, в in ВИДЫ.items():
        for язык, я in в["языки"].items():
            for форма in ФОРМЫ:
                if форма not in я:
                    continue
                for i in range(len(в["факты"])):
                    вон[страница(вид, язык, форма, i)] = (язык, f"{вид}_{форма}")
    return вон


ПОКАЗЫ = _показы()


def _образцы():
    """One pattern per (kind, language, form): the entity and the count are
    holes bound by back-reference where the page repeats them."""
    вон = []
    alt = lambda слова: "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    for вид, в in ВИДЫ.items():
        for язык, я in в["языки"].items():
            n = len(в["факты"])
            дыры = {"Ф": alt(_имя(вид, язык, i)[0] for i in range(n)), "Фр": alt(_имя(вид, язык, i)[1] for i in range(n)),
                    "С": alt(я["счёт"].values())}
            for форма in ФОРМЫ:
                if форма not in я:
                    continue
                видены, куски = set(), []
                for кусок in re.split(r"(\{[^}]+\})", " ".join(я[форма])):
                    if кусок.startswith("{"):
                        имя = кусок[1:-1]
                        if имя in видены:
                            куски.append(f"(?P={имя})")
                        else:
                            видены.add(имя); куски.append(f"(?P<{имя}>" + дыры[имя][3:])
                    else:
                        куски.append(re.escape(кусок))
                вон.append((re.compile("^" + "".join(куски) + "$"), вид, язык, форма))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): a page of a frame whose count is the entity's declared one."""
    с = строка.strip()
    for образ, вид, язык, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        в = ВИДЫ[вид]; я = в["языки"][язык]; г = м.groupdict()
        столбец = 0 if г.get("Ф") else 1
        имена = [_имя(вид, язык, i)[столбец] for i in range(len(в["факты"]))]
        сущ = г.get("Ф") or г.get("Фр")
        if сущ not in имена:
            return True, False
        число = list(в["факты"].values())[имена.index(сущ)]
        return True, я["счёт"].get(число) == г["С"]
    return False, False


def _самопроверка():
    for показ, (язык, форма) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, форма, показ)
    мутанты = 0
    for вид, в in ВИДЫ.items():
        for язык, я in в["языки"].items():
            числа = sorted(set(в["факты"].values()))
            с = страница(вид, язык, "сколько", 0)
            своё = я["счёт"][list(в["факты"].values())[0]]
            чужое = я["счёт"][next(x for x in числа if я["счёт"][x] != своё)]
            битая = с.replace(своё, чужое)
            assert судить(битая) == (True, False), битая
            мутанты += 1
    for язык in ("ru", "en", "pl"):
        print("  ", страница("стороны", язык, "что", 0)); print("  ", страница("ноги", язык, "сколько", 0))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (видов {len(ВИДЫ)}, языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
