#!/usr/bin/env python3
"""THE HOUSE OF PLACE — where a thing stands, and the three laws of standing (06.09).

The census found ZERO lines of «слева от» / «to the left of» in the whole свод, and four lines
carrying «above the». The corpus knows the GRID (tools/spacegrid.py: cells, symbols, turns) and
it knows the meta-language of relations (tools/relation.py: what goes into what, what corresponds
to what) — but it has never once said where an everyday thing stands with respect to another. A
reader that cannot place a cup beside a book cannot follow a page of any prose that describes a
room, a shelf, a diagram or a table.

WHAT THE HOUSE SHOWS — one axis, one set of things, three laws:
  обратное   — the CONVERSE: if the book is left of the cup, the cup is right of the book, and
               the page says WHY («left and right are opposite sides»);
  переходное — TRANSITIVITY: left of the left is left, with the conclusion drawn on the page;
  между      — BETWEENNESS: the thing in the middle is named, and its ground is that it stands on
               the far side of one and the near side of the other — the converse law used inside
               the answer to the between question.
The SAME three laws are shown on two axes — the horizontal (left/right) and the vertical
(above/below) — so that the law is seen as a law of an AXIS and not a property of one word.

WHAT IS DECLARED HERE: four things in nine languages, each in the three forms the axes demand —
the nominative, the form after the horizontal preposition (genitive in Russian and Polish, dative
in German, the plain article elsewhere) and the form after «above / below» (instrumental in
Russian and Polish, dative in German) — plus the form the languages take after «between», which
is the oblique in ru/de/pl and the plain one in the Romance languages. That is the whole cost of
nine languages: the LAWS are the same in all of them, only the case endings differ.

THE JUDGE RECOMPUTES BY REBUILDING: it reads the things and the relation out of the line, builds
the page the laws demand from them, and compares. A swapped answer, a converse that is not the
converse, a middle thing that is an end thing — each rebuilds into a different page and is a lie.

WHAT IS NOT MEASURED, NAMED: distance («two steps to the left»), the front/behind axis, the
observer whose left is another's right, and any arrangement of more than three things.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
ВЕЩИ = ("книга", "чашка", "лампа", "ключ")
# ТРИ ФОРМЫ КАЖДОЙ ВЕЩИ: именительная; после боковой связки (с предлогом); после верхней связки
СЛОВА = {
    "ru": {"книга": ("книга", "от книги", "книгой"), "чашка": ("чашка", "от чашки", "чашкой"),
           "лампа": ("лампа", "от лампы", "лампой"), "ключ": ("ключ", "от ключа", "ключом")},
    "en": {"книга": ("the book", "of the book", "the book"), "чашка": ("the cup", "of the cup", "the cup"),
           "лампа": ("the lamp", "of the lamp", "the lamp"), "ключ": ("the key", "of the key", "the key")},
    "de": {"книга": ("das Buch", "vom Buch", "dem Buch"), "чашка": ("die Tasse", "von der Tasse", "der Tasse"),
           "лампа": ("die Lampe", "von der Lampe", "der Lampe"),
           "ключ": ("der Schlüssel", "vom Schlüssel", "dem Schlüssel")},
    "fr": {"книга": ("le livre", "du livre", "du livre"), "чашка": ("la tasse", "de la tasse", "de la tasse"),
           "лампа": ("la lampe", "de la lampe", "de la lampe"), "ключ": ("la clé", "de la clé", "de la clé")},
    "es": {"книга": ("el libro", "del libro", "del libro"), "чашка": ("la taza", "de la taza", "de la taza"),
           "лампа": ("la lámpara", "de la lámpara", "de la lámpara"),
           "ключ": ("la llave", "de la llave", "de la llave")},
    "it": {"книга": ("il libro", "del libro", "il libro"), "чашка": ("la tazza", "della tazza", "la tazza"),
           "лампа": ("la lampada", "della lampada", "la lampada"),
           "ключ": ("la chiave", "della chiave", "la chiave")},
    "pt": {"книга": ("o livro", "do livro", "do livro"), "чашка": ("a chávena", "da chávena", "da chávena"),
           "лампа": ("a lâmpada", "da lâmpada", "da lâmpada"), "ключ": ("a chave", "da chave", "da chave")},
    "nl": {"книга": ("het boek", "van het boek", "het boek"), "чашка": ("de beker", "van de beker", "de beker"),
           "лампа": ("de lamp", "van de lamp", "de lamp"),
           "ключ": ("de sleutel", "van de sleutel", "de sleutel")},
    "pl": {"книга": ("książka", "od książki", "książką"), "чашка": ("filiżanka", "od filiżanki", "filiżanką"),
           "лампа": ("lampa", "od lampy", "lampą"), "ключ": ("klucz", "od klucza", "kluczem")},
}
# ДВЕ ОСИ, И НА КАЖДОЙ ДВЕ ОБРАТНЫЕ СТОРОНЫ; падеж вещи после связки — свой у оси
ОСИ = ("бок", "верх")
ПАДЕЖ = {"бок": 1, "верх": 2}
СВЯЗКИ = {
    "ru": {"бок": ("слева", "справа"), "верх": ("над", "под")},
    "en": {"бок": ("to the left", "to the right"), "верх": ("above", "below")},
    "de": {"бок": ("links", "rechts"), "верх": ("über", "unter")},
    "fr": {"бок": ("à gauche", "à droite"), "верх": ("au-dessus", "en dessous")},
    "es": {"бок": ("a la izquierda", "a la derecha"), "верх": ("encima", "debajo")},
    "it": {"бок": ("a sinistra", "a destra"), "верх": ("sopra", "sotto")},
    "pt": {"бок": ("à esquerda", "à direita"), "верх": ("acima", "abaixo")},
    "nl": {"бок": ("links", "rechts"), "верх": ("boven", "onder")},
    "pl": {"бок": ("na lewo", "na prawo"), "верх": ("nad", "pod")},
}
РЕЧЬ = {
    "ru": dict(есть="находится", и="и", между="между", между_и="и", вопрос_где="где находится {X}?",
               вопрос_что="что находится {M}?", закон="{R1} и {R2} — обратные стороны",
               вывод="значит, {A} находится {R1} {Co}", двоеточие=": ", мжд=2),
    "en": dict(есть="is", и="and", между="between", между_и="and", вопрос_где="where is {X}?",
               вопрос_что="what is {M}?", закон="{R1} and {R2} are opposite sides",
               вывод="so {A} is {R1} {Co}", двоеточие=": ", мжд=0),
    "de": dict(есть="ist", и="und", между="zwischen", между_и="und", вопрос_где="wo ist {X}?",
               вопрос_что="was ist {M}?", закон="{R1} und {R2} sind entgegengesetzte Seiten",
               вывод="also ist {A} {R1} {Co}", двоеточие=": ", мжд=2),
    "fr": dict(есть="est", и="et", между="entre", между_и="et", вопрос_где="où est {X} ?",
               вопрос_что="qu'y a-t-il {M} ?", закон="{R1} et {R2} sont des côtés opposés",
               вывод="donc {A} est {R1} {Co}", двоеточие=" : ", мжд=0),
    "es": dict(есть="está", и="y", между="entre", между_и="y", вопрос_где="¿dónde está {X}?",
               вопрос_что="¿qué está {M}?", закон="{R1} y {R2} son lados opuestos",
               вывод="así que {A} está {R1} {Co}", двоеточие=": ", мжд=0),
    "it": dict(есть="si trova", и="e", между="tra", между_и="e", вопрос_где="dove si trova {X}?",
               вопрос_что="che cosa si trova {M}?", закон="{R1} e {R2} sono lati opposti",
               вывод="quindi {A} si trova {R1} {Co}", двоеточие=": ", мжд=0),
    "pt": dict(есть="está", и="e", между="entre", между_и="e", вопрос_где="onde está {X}?",
               вопрос_что="o que está {M}?", закон="{R1} e {R2} são lados opostos",
               вывод="portanto {A} está {R1} {Co}", двоеточие=": ", мжд=0),
    "nl": dict(есть="is", и="en", между="tussen", между_и="en", вопрос_где="waar is {X}?",
               вопрос_что="wat is {M}?", закон="{R1} en {R2} zijn tegenovergestelde kanten",
               вывод="dus is {A} {R1} {Co}", двоеточие=": ", мжд=0),
    "pl": dict(есть="jest", и="i", между="między", между_и="a", вопрос_где="gdzie jest {X}?",
               вопрос_что="co jest {M}?", закон="{R1} i {R2} to strony przeciwne",
               вывод="więc {A} jest {R1} {Co}", двоеточие=": ", мжд=2),
}
ФОРМЫ = ("обратное", "переходное", "между")


def форма_вещи(язык, вещь, номер):
    return СЛОВА[язык][вещь][номер]


def _им(язык, вещь):
    return форма_вещи(язык, вещь, 0)


def _косв(язык, ось, вещь):
    """The form the axis demands after its relation word — genitive, dative or instrumental."""
    return форма_вещи(язык, вещь, ПАДЕЖ[ось])


def _мжд(язык, вещь):
    """The form the language takes after «between» — oblique in ru/de/pl, plain elsewhere."""
    return форма_вещи(язык, вещь, РЕЧЬ[язык]["мжд"])


def место(язык, ось, сторона, вещь):
    return СВЯЗКИ[язык][ось][сторона] + " " + _косв(язык, ось, вещь)


def факт(язык, ось, сторона, кто, где):
    return _им(язык, кто) + " " + РЕЧЬ[язык]["есть"] + " " + место(язык, ось, сторона, где)


def страница(язык, ось, форма, вещи, сторона=0):
    р, обр = РЕЧЬ[язык], 1 - сторона
    R1, R2 = СВЯЗКИ[язык][ось][сторона], СВЯЗКИ[язык][ось][обр]
    A = вещи[0]
    if форма == "обратное":
        B = вещи[1]
        # ОБРАТНОЕ: сторона поменялась, вещи поменялись местами
        return (факт(язык, ось, сторона, A, B) + ". " + р["вопрос_где"].format(X=_им(язык, B))
                + " " + место(язык, ось, обр, A) + р["двоеточие"]
                + р["закон"].format(R1=R1, R2=R2) + ".")
    B, C = вещи[1], вещи[2]
    цепь = факт(язык, ось, сторона, A, B) + ", " + факт(язык, ось, сторона, B, C) + ". "
    if форма == "переходное":
        # ПЕРЕХОДНОЕ: то, что стоит с той стороны от C, — это A и B, и вывод назван
        return (цепь + р["вопрос_что"].format(M=место(язык, ось, сторона, C)) + " "
                + _им(язык, A) + " " + р["и"] + " " + _им(язык, B) + р["двоеточие"]
                + р["вывод"].format(A=_им(язык, A), R1=R1, Co=_косв(язык, ось, C)) + ".")
    # МЕЖДУ: середина названа, и её основание — обратная сторона от одного и прямая к другому
    середина = р["между"] + " " + _мжд(язык, A) + " " + р["между_и"] + " " + _мжд(язык, C)
    return (цепь + р["вопрос_что"].format(M=середина) + " " + _им(язык, B) + р["двоеточие"]
            + _им(язык, B) + " " + р["есть"] + " " + место(язык, ось, обр, A) + " " + р["и"]
            + " " + место(язык, ось, сторона, C) + ".")


def _наборы():
    """Pairs for the converse, triples for the two laws that need a chain — halved, not repeated."""
    пары = [(a, b) for a in ВЕЩИ for b in ВЕЩИ if a != b]
    тройки = [(a, b, c) for a in ВЕЩИ for b in ВЕЩИ for c in ВЕЩИ if len({a, b, c}) == 3]
    return пары, тройки[::2]


ПАРЫ, ТРОЙКИ = _наборы()


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for ось in ОСИ:
            for сторона in (0, 1):
                for вещи in ПАРЫ:
                    вон[страница(язык, ось, "обратное", вещи, сторона)] = (язык, "обратное")
                for вещи in ТРОЙКИ:
                    for форма in ("переходное", "между"):
                        вон[страница(язык, ось, форма, вещи, сторона)] = (язык, форма)
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    сорт = sorted({с for с in слова}, key=lambda с: (-len(с), с))
    return "(?:" + "|".join(re.escape(с) for с in сорт) + ")"


def _дыры(язык, ось):
    им = _альт(_им(язык, в) for в in ВЕЩИ)
    return {"A": им, "B": им, "C": им, "X": им, "M": им,
            "Ao": _альт(_косв(язык, ось, в) for в in ВЕЩИ),
            "Bo": _альт(_косв(язык, ось, в) for в in ВЕЩИ),
            "Co": _альт(_косв(язык, ось, в) for в in ВЕЩИ),
            "Am": _альт(_мжд(язык, в) for в in ВЕЩИ), "Cm": _альт(_мжд(язык, в) for в in ВЕЩИ),
            "R1": _альт(СВЯЗКИ[язык][ось]), "R2": _альт(СВЯЗКИ[язык][ось])}


def рамка(язык, ось, форма):
    """The page with its values as named holes — the pattern and the page come from ONE template."""
    р = РЕЧЬ[язык]
    факт1 = "{A} " + р["есть"] + " {R1} {Bo}"
    if форма == "обратное":
        return (факт1 + ". " + р["вопрос_где"].format(X="{B}") + " {R2} {Ao}" + р["двоеточие"]
                + р["закон"].format(R1="{R1}", R2="{R2}") + ".")
    цепь = факт1 + ", {B} " + р["есть"] + " {R1} {Co}. "
    if форма == "переходное":
        return (цепь + р["вопрос_что"].format(M="{R1} {Co}") + " {A} " + р["и"] + " {B}"
                + р["двоеточие"] + р["вывод"].format(A="{A}", R1="{R1}", Co="{Co}") + ".")
    середина = р["между"] + " {Am} " + р["между_и"] + " {Cm}"
    return (цепь + р["вопрос_что"].format(M=середина) + " {B}" + р["двоеточие"]
            + "{B} " + р["есть"] + " {R2} {Ao} " + р["и"] + " {R1} {Co}.")


def _образец(язык, ось, форма):
    дыры, счёт, куски = _дыры(язык, ось), {}, []
    for кусок in re.split(r"(\{[^}]+\})", рамка(язык, ось, форма)):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, ось, форма), язык, ось, форма)
           for язык in ЯЗЫКИ for ось in ОСИ for форма in ФОРМЫ]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _вещь(язык, ось, дыра, слово):
    """Which thing wears this form — the form itself names the case, so the case is judged too."""
    номер = {"A": 0, "B": 0, "C": 0}.get(дыра)
    if номер is None:
        номер = РЕЧЬ[язык]["мжд"] if дыра.endswith("m") else ПАДЕЖ[ось]
    for в in ВЕЩИ:
        if форма_вещи(язык, в, номер) == слово:
            return в
    return None


def судить(строка):
    """(судимо, истинно): a page of the house whose three things rebuild it exactly; else silence."""
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образ, язык, ось, форма in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        зн = _значения(м)
        if зн is None:
            return True, False
        # ТРЕТЬЯ ВЕЩЬ ЖИВЁТ В КОСВЕННОЙ ФОРМЕ: цепь называет её только после связки
        ключи = ("A", "B") if форма == "обратное" else ("A", "B", "Co")
        вещи = tuple(_вещь(язык, ось, д, зн[д]) for д in ключи)
        if None in вещи or len(set(вещи)) != len(вещи):
            return True, False
        сторона = СВЯЗКИ[язык][ось].index(зн["R1"]) if зн["R1"] in СВЯЗКИ[язык][ось] else None
        if сторона is None:
            return True, False
        # ЗАКОН ПЕРЕСТРАИВАЕТ СТРАНИЦУ ИЗ ЕЁ ЖЕ ВЕЩЕЙ И СРАВНИВАЕТ
        return True, страница(язык, ось, форма, вещи, сторона) == с
    return False, False


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    мутанты = 0
    for язык in ЯЗЫКИ:
        for ось in ОСИ:
            R1, R2 = СВЯЗКИ[язык][ось]
            о = страница(язык, ось, "обратное", ("книга", "чашка"))
            # (1) ОБРАТНОЕ НЕ ОБРАЩЕНО: та же сторона в ответе
            битая = о.replace("? " + R2 + " ", "? " + R1 + " ", 1)
            assert судить(битая) == (True, False), битая
            # (2) ОБРАТНОЕ О ЧУЖОЙ ВЕЩИ: в ответе стоит не спрошенная вещь
            битая = о.replace(R2 + " " + _косв(язык, ось, "книга"), R2 + " " + _косв(язык, ось, "лампа"))
            assert судить(битая) == (True, False), битая
            п = страница(язык, ось, "переходное", ("книга", "чашка", "лампа"))
            assert судить(п) == (True, True), п
            # (3) ПЕРЕХОДНОЕ ЗАБЫЛО СЕРЕДИНУ: ответ назвал только крайнюю вещь
            битая = п.replace(" " + _им(язык, "книга") + " " + РЕЧЬ[язык]["и"] + " " + _им(язык, "чашка"),
                              " " + _им(язык, "книга") + " " + РЕЧЬ[язык]["и"] + " " + _им(язык, "ключ"))
            assert судить(битая) == (True, False), битая
            м = страница(язык, ось, "между", ("книга", "чашка", "лампа"))
            assert судить(м) == (True, True), м
            # (4) МЕЖДУ НАЗВАЛО КРАЙНЮЮ ВЕЩЬ СЕРЕДИНОЙ
            битая = м.replace("? " + _им(язык, "чашка"), "? " + _им(язык, "ключ"), 1)
            assert судить(битая) == (True, False), битая
            # (5) ОСНОВАНИЕ СЕРЕДИНЫ ВЗЯТО С ТОЙ ЖЕ СТОРОНЫ ДВАЖДЫ
            битая = м.replace(R2 + " " + _косв(язык, ось, "книга"), R1 + " " + _косв(язык, ось, "книга"))
            assert судить(битая) == (True, False), битая
            мутанты += 5
        # (6) ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
        for форма, вещи in (("обратное", ("книга", "чашка")), ("переходное", ("книга", "чашка", "лампа")),
                            ("между", ("книга", "чашка", "лампа"))):
            стр = страница(язык, "бок", форма, вещи)
            вопрос = [ч for ч in стр.split(". ") if "?" in ч][0]
            вопрос = вопрос[вопрос.rindex(", ") + 2:] if ", " in вопрос[:вопрос.index("?")] else вопрос
            вопрос = вопрос[:вопрос.index("?") + 1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "бок", "между", ("книга", "чашка", "лампа")))
    for язык in ("ru", "de", "pl"):
        print("  ", страница(язык, "верх", "обратное", ("лампа", "ключ")))
        print("  ", страница(язык, "верх", "переходное", ("книга", "чашка", "ключ"), 1))
    по_форме = {}
    for _, (_язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, осей {len(ОСИ)}, форм {len(ФОРМЫ)}, "
          f"образцов {len(ОБРАЗЦЫ)}): " + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))


if __name__ == "__main__":
    _самопроверка()
