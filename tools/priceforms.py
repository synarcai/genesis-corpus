#!/usr/bin/env python3
"""THE HOUSE OF PRICE — «one apple costs 2 dollars. how much do 3 apples cost?
6 dollars: 3 × 2 = 6.» in nine languages.

Born from the seventh band of conversation (BESEDA-7, 06.09): the price of
several things at one price was answered only by the ru/en money worlds. Here
the thing and the currency bend by the count, and the RULE of bending is the
pack's (count_agreement) — this file declares only the forms, named by the
pack's own names («one / few / many»: яблоко / яблока / яблок, рубль / рубля /
рублей; jabłko / jabłka / jabłek). The total is recomputed by the court, and
so are both count forms. The world is CLOSED.

    python3 tools/priceforms.py    # self-check with mutants
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import langpack  # noqa: E402

_ПАКЕТЫ = pathlib.Path(__file__).resolve().parent / "langpacks"

# per language: things — the «one» phrase (with its numeral, so the gender lives
# in the declared phrase) and the count forms; the currency forms; the frame
ЯЗЫКИ = {
    "ru": dict(вещи=(dict(one="одно яблоко", few="яблока", many="яблок"), dict(one="одна книга", few="книги", many="книг"),
                    dict(one="один карандаш", few="карандаша", many="карандашей")),
               валюта=dict(one="рубль", few="рубля", many="рублей"),
               рамка=("{В1} стоит {n} {Р}. сколько стоят {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
    "en": dict(вещи=(dict(one="one apple", many="apples"), dict(one="one book", many="books"), dict(one="one pencil", many="pencils")),
               валюта=dict(one="dollar", many="dollars"),
               рамка=("{В1} costs {n} {Р}. how much do {k} {Вk} cost?", "{v} {Рv}: {k} × {n} = {v}.")),
    "de": dict(вещи=(dict(one="ein Apfel", many="Äpfel"), dict(one="ein Buch", many="Bücher"), dict(one="ein Bleistift", many="Bleistifte")),
               валюта=dict(one="Euro", many="Euro"),
               рамка=("{В1} kostet {n} {Р}. wie viel kosten {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
    "fr": dict(вещи=(dict(one="une pomme", many="pommes"), dict(one="un livre", many="livres"), dict(one="un crayon", many="crayons")),
               валюта=dict(one="euro", many="euros"),
               рамка=("{В1} coûte {n} {Р}. combien coûtent {k} {Вk} ?", "{v} {Рv} : {k} × {n} = {v}.")),
    "es": dict(вещи=(dict(one="una manzana", many="manzanas"), dict(one="un libro", many="libros"), dict(one="un lápiz", many="lápices")),
               валюта=dict(one="euro", many="euros"),
               рамка=("{В1} cuesta {n} {Р}. ¿cuánto cuestan {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
    "it": dict(вещи=(dict(one="una mela", many="mele"), dict(one="un libro", many="libri"), dict(one="una matita", many="matite")),
               валюта=dict(one="euro", many="euro"),
               рамка=("{В1} costa {n} {Р}. quanto costano {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
    "pt": dict(вещи=(dict(one="uma maçã", many="maçãs"), dict(one="um livro", many="livros"), dict(one="um lápis", many="lápis")),
               валюта=dict(one="euro", many="euros"),
               рамка=("{В1} custa {n} {Р}. quanto custam {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
    "nl": dict(вещи=(dict(one="een appel", many="appels"), dict(one="een boek", many="boeken"), dict(one="een potlood", many="potloden")),
               валюта=dict(one="euro", many="euro"),
               рамка=("{В1} kost {n} {Р}. hoeveel kosten {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
    "pl": dict(вещи=(dict(one="jedno jabłko", few="jabłka", many="jabłek"), dict(one="jedna książka", few="książki", many="książek"),
                    dict(one="jeden ołówek", few="ołówki", many="ołówków")),
               валюта=dict(one="złoty", few="złote", many="złotych"),
               рамка=("{В1} kosztuje {n} {Р}. ile kosztują {k} {Вk}?", "{v} {Рv}: {k} × {n} = {v}.")),
}
ЦЕНЫ = (2, 3, 5)           # the price of one
СЧЁТ = (2, 3, 4, 5)        # how many are bought
_ПАКЕТ = {}


def _пакет(язык):
    if язык not in _ПАКЕТ:
        _ПАКЕТ[язык] = json.loads((_ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    return _ПАКЕТ[язык]


def форма(язык, таблица, k):
    """The count form of a thing or the currency for k — by the pack's rule."""
    формы = list(таблица)
    i = langpack.count_form_index(_пакет(язык), {"forms": формы}, k)
    return таблица[формы[i]]


def страница(язык, в, n, k):
    я = ЯЗЫКИ[язык]; вещь = я["вещи"][в]
    v = n * k
    п = dict(В1=вещь["one"], n=n, Р=форма(язык, я["валюта"], n), k=k, Вk=форма(язык, вещь, k), v=v, Рv=форма(язык, я["валюта"], v))
    воп, отв = я["рамка"]
    return f"{воп.format(**п)} {отв.format(**п)}"


def _показы():
    return {страница(язык, в, n, k): (язык, "цена")
            for язык, я in ЯЗЫКИ.items() for в in range(len(я["вещи"])) for n in ЦЕНЫ for k in СЧЁТ}


ПОКАЗЫ = _показы()


def _образцы():
    вон = []
    alt = lambda слова: "(" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"
    for язык, я in ЯЗЫКИ.items():
        вещи_формы = [ф for в in я["вещи"] for ф in в.values()]
        дыры = {"В1": "(?P<В1>" + alt(в["one"] for в in я["вещи"])[1:], "Вk": "(?P<Вk>" + alt(вещи_формы)[1:],
                "Р": "(?P<Р>" + alt(я["валюта"].values())[1:], "Рv": "(?P<Рv>" + alt(я["валюта"].values())[1:],
                "n": r"(?P<n>\d+)", "k": r"(?P<k>\d+)", "v": r"(?P<v>\d+)"}
        видены, куски = set(), []
        for кусок in re.split(r"(\{[^}]+\})", " ".join(я["рамка"])):
            if кусок.startswith("{"):
                имя = кусок[1:-1]
                куски.append(f"(?P={имя})" if имя in видены else дыры[имя]); видены.add(имя)
            else:
                куски.append(re.escape(кусок))
        вон.append((re.compile("^" + "".join(куски) + "$"), язык))
    return вон


ОБРАЗЦЫ = _образцы()


def судить(строка):
    """(судимо, истинно): the total is the product, and every count form is the pack's."""
    с = строка.strip()
    for образ, язык in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        я = ЯЗЫКИ[язык]; г = м.groupdict()
        n, k, v = int(г["n"]), int(г["k"]), int(г["v"])
        вещь = next((в for в in я["вещи"] if в["one"] == г["В1"]), None)
        if вещь is None or v != n * k:
            return True, False
        return True, (г["Вk"], г["Р"], г["Рv"]) == (форма(язык, вещь, k), форма(язык, я["валюта"], n), форма(язык, я["валюта"], v))
    return False, False


def _самопроверка():
    for показ, (язык, _) in ПОКАЗЫ.items():
        assert судить(показ) == (True, True), (язык, показ)
    мутанты = 0
    for язык in ЯЗЫКИ:
        # MUTANT: the total off by one in BOTH places (6 → 7 keeps the currency form),
        # so that the frame still matches and the count catches it
        с = страница(язык, 0, 2, 3)
        битая = с.replace(" 6 ", " 7 ", 1).replace("= 6.", "= 7.")
        assert судить(битая) == (True, False), битая
        мутанты += 1
    for язык in ("ru", "en", "pl", "de"):
        print("  ", страница(язык, 0, 2, 3)); print("  ", страница(язык, 1, 5, 5))
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)})")


if __name__ == "__main__":
    _самопроверка()
