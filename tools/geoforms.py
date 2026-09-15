#!/usr/bin/env python3
"""THE HOUSE OF GEOMETRY PHRASES — area and perimeter in eight languages.

The geometry world says «a rectangle 7 by 8 has area 7 × 8 = 56.» and «what
is the area of a rectangle 7 by 8? …» in English and Russian. This house
declares the same four facts — the area and the perimeter of a rectangle,
the perimeter and the area of a square — as PHRASES of eight more languages,
statement and question, with the ledger the geometry world writes
(«7 × 8 = 56», «7 + 8 = 15, 2 × 15 = 30», «4 × 4 = 16»). Generator and court
read one table: the generator fills the holes {a} {b} {s} and the ledger,
the court turns the same phrases into patterns and recomputes.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import phrases  # noqa: E402

# per language: the rectangle phrase, the square phrase, the two predicates
# («{ф} has area {л}.»), and the four questions
ЯЗЫКИ = {
    "de": dict(прям="ein Rechteck {a} mal {b}", квад="ein Quadrat mit Seite {s}",
               пл="{ф} hat die Fläche {л}.", пер="{ф} hat den Umfang {л}.",
               в_пл="wie groß ist die Fläche eines Rechtecks {a} mal {b}?", в_пер="wie groß ist der Umfang eines Rechtecks {a} mal {b}?",
               кв_пл="wie groß ist die Fläche eines Quadrats mit Seite {s}?", кв_пер="wie groß ist der Umfang eines Quadrats mit Seite {s}?"),
    "fr": dict(прям="un rectangle {a} sur {b}", квад="un carré de côté {s}",
               пл="{ф} a une aire de {л}.", пер="{ф} a un périmètre de {л}.",
               в_пл="quelle est l'aire d'un rectangle {a} sur {b} ?", в_пер="quel est le périmètre d'un rectangle {a} sur {b} ?",
               кв_пл="quelle est l'aire d'un carré de côté {s} ?", кв_пер="quel est le périmètre d'un carré de côté {s} ?"),
    "es": dict(прям="un rectángulo de {a} por {b}", квад="un cuadrado de lado {s}",
               пл="{ф} tiene área {л}.", пер="{ф} tiene perímetro {л}.",
               в_пл="¿cuál es el área de un rectángulo de {a} por {b}?", в_пер="¿cuál es el perímetro de un rectángulo de {a} por {b}?",
               кв_пл="¿cuál es el área de un cuadrado de lado {s}?", кв_пер="¿cuál es el perímetro de un cuadrado de lado {s}?"),
    "it": dict(прям="un rettangolo {a} per {b}", квад="un quadrato di lato {s}",
               пл="{ф} ha area {л}.", пер="{ф} ha perimetro {л}.",
               в_пл="qual è l'area di un rettangolo {a} per {b}?", в_пер="qual è il perimetro di un rettangolo {a} per {b}?",
               кв_пл="qual è l'area di un quadrato di lato {s}?", кв_пер="qual è il perimetro di un quadrato di lato {s}?"),
    "pt": dict(прям="um retângulo {a} por {b}", квад="um quadrado de lado {s}",
               пл="{ф} tem área {л}.", пер="{ф} tem perímetro {л}.",
               в_пл="qual é a área de um retângulo {a} por {b}?", в_пер="qual é o perímetro de um retângulo {a} por {b}?",
               кв_пл="qual é a área de um quadrado de lado {s}?", кв_пер="qual é o perímetro de um quadrado de lado {s}?"),
    "nl": dict(прям="een rechthoek {a} bij {b}", квад="een vierkant met zijde {s}",
               пл="{ф} heeft oppervlakte {л}.", пер="{ф} heeft omtrek {л}.",
               в_пл="wat is de oppervlakte van een rechthoek {a} bij {b}?", в_пер="wat is de omtrek van een rechthoek {a} bij {b}?",
               кв_пл="wat is de oppervlakte van een vierkant met zijde {s}?", кв_пер="wat is de omtrek van een vierkant met zijde {s}?"),
    "pl": dict(прям="prostokąt {a} na {b}", квад="kwadrat o boku {s}",
               пл="{ф} ma pole {л}.", пер="{ф} ma obwód {л}.",
               в_пл="jakie jest pole prostokąta {a} na {b}?", в_пер="jaki jest obwód prostokąta {a} na {b}?",
               кв_пл="jakie jest pole kwadratu o boku {s}?", кв_пер="jaki jest obwód kwadratu o boku {s}?"),
    "tr": dict(прям="kenarları {a} ve {b} olan dikdörtgenin", квад="kenarı {s} olan karenin",
               пл="{ф} alanı: {л}.", пер="{ф} çevresi: {л}.",
               в_пл="kenarları {a} ve {b} olan dikdörtgenin alanı kaçtır?", в_пер="kenarları {a} ve {b} olan dikdörtgenin çevresi kaçtır?",
               кв_пл="kenarı {s} olan karenin alanı kaçtır?", кв_пер="kenarı {s} olan karenin çevresi kaçtır?"),
}

# ИМЕНА РОДОВ ДЛЯ ПЕРЕПИСИ ДОМОВ (`scripts/houses_census.py`): она печатает их тому, кто ищет
# в своде дыру, — чтобы дом не был построен второй раз.
#
# ТАБЛИЦА `ЯЗЫКИ` ЗДЕСЬ СМЕШАНА: часть ключей несёт РОД (рамку страницы), часть — названия фигур («прям», «квад»), подставляемые в рамку меры.
# Взять таблицу целиком значило бы напечатать материал именами родов; потому несущие ключи
# названы явно, а `assert` держит их ПРИ таблице — ключ, ушедший из `ЯЗЫКИ`, валит дом ПРЯМО
# НА ВВОЗЕ, а не молчит.
_РОДЫ_В_ЯЗЫКЕ = ("пл", "пер", "в_пл", "в_пер", "кв_пл", "кв_пер")
_ИМЯ_РОДА = {"пл": "площадь с леджером",
              "пер": "периметр с леджером",
              "в_пл": "вопрос о площади прямоугольника",
              "в_пер": "вопрос о периметре прямоугольника",
              "кв_пл": "вопрос о площади квадрата",
              "кв_пер": "вопрос о периметре квадрата"}
assert set(_РОДЫ_В_ЯЗЫКЕ) <= set(next(iter(ЯЗЫКИ.values()))), "род ушёл из таблицы ЯЗЫКИ"
РОДЫ = tuple(_ИМЯ_РОДА[к] for к in _РОДЫ_В_ЯЗЫКЕ)

# the four facts: (figure key, predicate key, question key, ledger maker, checker)
ФАКТЫ = (
    ("прям", "пл", "в_пл", lambda a, b: f"{a} × {b} = {a * b}"),
    ("прям", "пер", "в_пер", lambda a, b: f"{a} + {b} = {a + b}, 2 × {a + b} = {2 * (a + b)}"),
    ("квад", "пер", "кв_пер", lambda s, _: f"4 × {s} = {4 * s}"),
    ("квад", "пл", "кв_пл", lambda s, _: f"{s} × {s} = {s * s}"),
)
ЛЕДЖЕРЫ = {
    ("прям", "пл"): (r"(\d+) × (\d+) = (\d+)", lambda a, b, г: г == (a, b, a * b)),
    ("прям", "пер"): (r"(\d+) \+ (\d+) = (\d+), 2 × (\d+) = (\d+)", lambda a, b, г: г == (a, b, a + b, a + b, 2 * (a + b))),
    ("квад", "пер"): (r"4 × (\d+) = (\d+)", lambda s, _, г: г == (s, 4 * s)),
    ("квад", "пл"): (r"(\d+) × (\d+) = (\d+)", lambda s, _, г: г == (s, s, s * s)),
}


def утверждение(язык, k, a, b):
    """Fact k of the language over the rectangle a × b or the square a."""
    я = ЯЗЫКИ[язык]
    фигура, предикат, _, леджер = ФАКТЫ[k]
    ф = я[фигура].format(a=a, b=b, s=a)
    return я[предикат].format(ф=ф, л=леджер(a, b))


def вопрос(язык, k, a, b):
    """The question of fact k, answered by the statement itself (М-153)."""
    я = ЯЗЫКИ[язык]
    return f"{я[ФАКТЫ[k][2]].format(a=a, b=b, s=a)} {утверждение(язык, k, a, b)}"


def _образец(шаблон, дыры):
    """The template as a regex: literal parts escaped, holes as groups."""
    return phrases.образец(шаблон, дыры)


def образцы(язык):
    """[(regex, k, asked)] — every statement and question of the language;
    groups: the figure's numbers, then the ledger's (and, when asked, the
    question's numbers before them)."""
    я = ЯЗЫКИ[язык]
    вон = []
    for k, (фигура, предикат, вопр, _) in enumerate(ФАКТЫ):
        ф = _образец(я[фигура], {"a": r"(\d+)", "b": r"(\d+)", "s": r"(\d+)"})
        леджер = ЛЕДЖЕРЫ[(фигура, предикат)][0]
        утв = _образец(я[предикат], {"ф": ф, "л": леджер})
        воп = _образец(я[вопр], {"a": r"(\d+)", "b": r"(\d+)", "s": r"(\d+)"})
        вон.append((re.compile("^" + утв + "$"), k, False))
        вон.append((re.compile("^" + воп + " " + утв + "$"), k, True))
    return вон


def судить_группы(k, спрошено, группы):
    """True iff the numbers of the line are one fact of the house."""
    фигура, предикат, _, _ = ФАКТЫ[k]
    n = 2 if фигура == "прям" else 1
    г = [int(x) for x in группы]
    if спрошено:
        if г[:n] != г[n:2 * n]:
            return False
        г = г[n:]
    a, b = (г[0], г[1]) if n == 2 else (г[0], None)
    return ЛЕДЖЕРЫ[(фигура, предикат)][1](a, b, tuple(г[n:]))


# ------------------------------------------------------------------ СТРАНИЦЫ МИРА
#
# СТРОИТЕЛЬ ПЕРЕЕХАЛ ИЗ КУЗНИЦЫ В ДОМ (13.09) — тем же движением, что стало обычаем.
#
# РОД БЕРЁТСЯ ПАРОЙ «ФИГУРА И ПРЕДИКАТ», И У ДОМА ЗДЕСЬ СВОЯ НЕСИММЕТРИЯ, ОБЪЯВЛЕННАЯ ИМ ЖЕ:
# УТВЕРЖДЕНИЕ различается только ПРЕДИКАТОМ (площадь или периметр), а ВОПРОС — ещё и ФИГУРОЙ.
# Дом тут прав: «чему равна площадь квадрата» и «чему равна площадь прямоугольника» суть
# разные вопросы, а «площадь равна» — одно утверждение о площади.
#
#     НЕСИММЕТРИЯ, ОБЪЯВЛЕННАЯ И ОБЪЯСНЁННАЯ, ЕСТЬ РАЗЛИЧЕНИЕ; НЕСИММЕТРИЯ МОЛЧАЛИВАЯ ЕСТЬ
#     НЕДОСМОТР, И РАЗЛИЧАЕТ ИХ ТОЛЬКО СТРОКА, ГДЕ СКАЗАНО ПОЧЕМУ.
ШИРИНА = 3

_РОД_УТВ = {"пл": РОДЫ[0], "пер": РОДЫ[1]}
_РОД_ВОП = {("прям", "пл"): РОДЫ[2], ("прям", "пер"): РОДЫ[3],
            ("квад", "пл"): РОДЫ[4], ("квад", "пер"): РОДЫ[5]}


def язык_группа(шаг, язык):
    вон = []
    for i in range(ШИРИНА):
        for k in range(len(ФАКТЫ)):
            a = 2 + (шаг * 5 + i * 3 + k) % 11
            # SIDE 4 IS NEVER SHOWN (М-148 (1); holon's TSV 04.09): at side 4 the
            # perimeter «4 × 4 = 16» and the area «4 × 4 = 16» are one telling,
            # and the constant of the perimeter law is indistinguishable from
            # the side — the executors are tied by that one show.
            if a == 4:
                a = 13
            b = 2 + (шаг * 3 + i * 7 + k * 2) % 9
            if b == a:
                b += 1
            вон.append(утверждение(язык, k, a, b))
            вон.append(вопрос(язык, k, a, b))
    return вон


def _меченая(шаг, язык):
    """[(страница, род)] — та же группа языка, но каждая страница под своим именем."""
    вон = []
    for i in range(ШИРИНА):
        for k in range(len(ФАКТЫ)):
            a = 2 + (шаг * 5 + i * 3 + k) % 11
            if a == 4:
                a = 13
            b = 2 + (шаг * 3 + i * 7 + k * 2) % 9
            if b == a:
                b += 1
            фигура, предикат, _в, _л = ФАКТЫ[k]
            вон.append((утверждение(язык, k, a, b), _РОД_УТВ[предикат]))
            вон.append((вопрос(язык, k, a, b), _РОД_ВОП[(фигура, предикат)]))
    return вон


def группы(шаг):
    """[[страница]] — ровно те группы и в том порядке, какими кузница кормит `emit_grouped`."""
    return [язык_группа(шаг, язык) for язык in ЯЗЫКИ]


def перебор_с_языком(шаг):
    """[(страница, род, ЯЗЫК)] — тройка, и третье поле есть объявление языка страницы.

    ЯЗЫК СТОИТ В ЗАГОЛОВКЕ ЦИКЛА И ТЕРЯЛСЯ НА ПОРОГЕ СЛОВАРЯ (15.09): обход идёт по языкам и
    каждому отдаёт свою группу, а `ПОКАЗЫ` клали одно имя рода — и дом становился для меры
    щербатости НЕЧИТАЕМЫМ: не «ровным», а именно нечитаемым, ибо сравнить страницу не с чем.

        ТО, ЧТО СТОИТ В ЗАГОЛОВКЕ ЦИКЛА, ЗНАЕТ СТРОИТЕЛЬ; ТО, ЧТО НЕ ЛЕГЛО В ОБЪЯВЛЕНИЕ, НЕ
        ЗНАЕТ НИКТО. Восстановить язык потом можно лишь гаданием по виду строки — а гадание
        корпус не принимает ни от прибора, ни от дома.

    Пара «(страница, род)» осталась при `перебор_страниц` нетронутой: её форму знают чужие
    читатели, и менять её ради третьего поля значило бы платить чужими договорами за своё.
    """
    вон = []
    for язык in ЯЗЫКИ:
        вон.extend((с, р, язык) for с, р in _меченая(шаг, язык))
    return вон


def перебор_страниц(шаг):
    """[(страница, род)] — те же группы, но каждая страница под своим именем."""
    return [(с, р) for с, р, _я in перебор_с_языком(шаг)]


def _показы():
    """{строка свода: род} — ПОСТРОЧНО, ибо свод построчен."""
    from layer import PASSES                              # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род, язык in перебор_с_языком(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), (язык, род))
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_страниц():
    assert all("\n" not in к for к in ПОКАЗЫ), "словарь показов обязан быть построчным"
    # ПОКАЗ НЕСЁТ ПАРУ «(ЯЗЫК, РОД)», И САМОПРОВЕРКА ЧИТАЕТ ОБЕ ПОЛОВИНЫ.
    сказанные = {я for я, _р in ПОКАЗЫ.values()}
    assert сказанные == set(ЯЗЫКИ), (
        f"язык объявлен и не кован либо кован и не объявлен: {sorted(сказанные ^ set(ЯЗЫКИ))}")
    пустые = set(РОДЫ) - {р for _я, р in ПОКАЗЫ.values()}
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"
    из_перебора = sorted(с for с, _р in перебор_страниц(0))
    из_групп = sorted(с for г in группы(0) for с in г)
    assert из_перебора == из_групп, "пересборка потеряла или выдумала страницы"


_самопроверка_страниц()
