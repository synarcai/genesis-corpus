#!/usr/bin/env python3
"""GENESIS layer: РОСТ ЛИЦ — кто выше и на сколько, опора до сравнения, сравниваемое после (24.09).

ПОВОД — заказ ведущего по переписи полос против свода (рука sides5, рынок подписей сравнения
`buy_cmp_markers`): «taller than» в своде 5 строк, «shorter than» — 30, и ни одной о росте лица с числом;
«shorter than» стоит лишь в геометрии («a way through a third point is not shorter than the straight
one»). Рынок читает четвёрку «A is n cm taller than B», значение B берёт из последнего факта ДО неё, значение
A — из первого ПОСЛЕ, и покупает подпись, когда звено показа её подтверждает. Мир роста даёт ему это на
четырёх языках: опора, сравнение, вопрос и ответ, называющий лицо, со звеном.

    КТО НИЖЕ, ТОТ НАЗВАН ОТ ВЫСОКОГО, И ОПОРА СКАЗАНА ПРЕЖДЕ, ЧЕМ СПРОШЕНО СРАВНИВАЕМОЕ.

ТРИ РОДА: опора — низкий, спрошен высокий («Ben is 120 cm tall. Carla is 8 cm taller than Ben. how tall
is Carla? Carla is 128 cm tall: 120 + 8 = 128.»); опора — высокий, спрошен низкий («… 8 cm shorter than
…»); разность спрошена словом сравнения («how much taller is Carla than Ben?»). Рост — сантиметрами,
сокращением («cm», «см»), которое при числе не склоняется ни в одном из четырёх языков; рост детей — от 95
до 179 см, разность — от 2 до 25.

ЛИЦА — ПАКЕТОВ, У ВСЯКОГО ЯЗЫКА СВОИ (как в мире областей): соответствие имён между языками здесь не нужно,
ибо страницы языков не переводят одна другую. Русский родительный («выше Ани») — пакета (`person_forms`).

СУД — `courts/height_court.py`, вторая рука: образец на язык и род, слово сравнения и знак звена — группы,
сверяемые между собою; перевёрнутое направление («8 cm shorter … 120 + 8 = 128») — ложь, а не немота.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import Сбор, emit  # noqa: E402

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09).
ЦЕЛЬ = "datasets/genesis_height.txt"

_ТУТ = pathlib.Path(__file__).resolve().parent
_ПАКЕТЫ = {я: json.loads((_ТУТ / "langpacks" / f"{я}.json").read_text(encoding="utf-8"))
           for я in ("en", "ru", "de", "nl")}
ИМЕНА = {"en": ("Ben", "Carla", "Dan", "Elena", "Felix", "Grace"),
         "ru": ("Ваня", "Вера", "Дима", "Лена", "Маша", "Петя"),
         "de": ("Jonas", "Lena", "Paul", "Mia", "Felix", "Laura"),
         "nl": ("Daan", "Emma", "Sem", "Lotte", "Bram", "Sanne")}
for _я, _имена in ИМЕНА.items():
    assert set(_имена) <= set(_ПАКЕТЫ[_я]["person_names"]), ("имя не объявлено пакетом", _я)
РОДИТЕЛЬНЫЙ = {и: _ПАКЕТЫ["ru"]["person_forms"][и]["gen"] for и in ИМЕНА["ru"]}

ВЫШЕ = "выше: опора — низкий, спрошен высокий"
НИЖЕ = "ниже: опора — высокий, спрошен низкий"
НАСКОЛЬКО = "насколько выше: разность спрошена словом сравнения"

# (опора и сравнение, вопрос, ответ) — рамки рода на языке; {A} — высокий, {B} — низкий, {a}/{b} — их рост,
# {d} — разность, {Bg}/{Ag} — русский родительный
РАМКИ = {
    "en": {ВЫШЕ: "{B} is {b} cm tall. {A} is {d} cm taller than {B}. how tall is {A}? {A} is {a} cm tall: "
                 "{b} + {d} = {a}.",
           НИЖЕ: "{A} is {a} cm tall. {B} is {d} cm shorter than {A}. how tall is {B}? {B} is {b} cm tall: "
                 "{a} − {d} = {b}.",
           НАСКОЛЬКО: "{A} is {a} cm tall and {B} is {b} cm tall. how much taller is {A} than {B}? {d} cm "
                      "taller: {a} − {b} = {d}."},
    "ru": {ВЫШЕ: "{B} ростом {b} см. {A} выше {Bg} на {d} см. какого роста {A}? {A} ростом {a} см: "
                 "{b} + {d} = {a}.",
           НИЖЕ: "{A} ростом {a} см. {B} ниже {Ag} на {d} см. какого роста {B}? {B} ростом {b} см: "
                 "{a} − {d} = {b}.",
           НАСКОЛЬКО: "{A} ростом {a} см, а {B} ростом {b} см. на сколько {A} выше {Bg}? на {d} см: "
                      "{a} − {b} = {d}."},
    "de": {ВЫШЕ: "{B} ist {b} cm groß. {A} ist {d} cm größer als {B}. wie groß ist {A}? {A} ist {a} cm groß: "
                 "{b} + {d} = {a}.",
           НИЖЕ: "{A} ist {a} cm groß. {B} ist {d} cm kleiner als {A}. wie groß ist {B}? {B} ist {b} cm groß: "
                 "{a} − {d} = {b}.",
           НАСКОЛЬКО: "{A} ist {a} cm groß und {B} ist {b} cm groß. wie viel größer ist {A} als {B}? {d} cm "
                      "größer: {a} − {b} = {d}."},
    "nl": {ВЫШЕ: "{B} is {b} cm lang. {A} is {d} cm langer dan {B}. hoe lang is {A}? {A} is {a} cm lang: "
                 "{b} + {d} = {a}.",
           НИЖЕ: "{A} is {a} cm lang. {B} is {d} cm kleiner dan {A}. hoe lang is {B}? {B} is {b} cm lang: "
                 "{a} − {d} = {b}.",
           НАСКОЛЬКО: "{A} is {a} cm lang en {B} is {b} cm lang. hoeveel langer is {A} dan {B}? {d} cm "
                      "langer: {a} − {b} = {d}."},
}
ЯЗЫКИ = tuple(РАМКИ)
СЛУЧАЕВ_ХОДОМ = 10


def случаи(шаг):
    """(i высокого, i низкого, рост высокого, рост низкого): два разных лица, разность 2..25."""
    вон = []
    for i in range(СЛУЧАЕВ_ХОДОМ):
        высокий = (шаг + i) % 6
        низкий = (высокий + 1 + (шаг * 2 + i) % 5) % 6
        b = 95 + (шаг * 7 + i * 11) % 60
        d = 2 + (шаг * 3 + i * 5) % 24
        вон.append((высокий, низкий, b + d, b))
    return вон


def страница(язык, род, случай):
    высокий, низкий, a, b = случай
    A, B = ИМЕНА[язык][высокий], ИМЕНА[язык][низкий]
    род_падеж = dict(Ag=РОДИТЕЛЬНЫЙ.get(A, ""), Bg=РОДИТЕЛЬНЫЙ.get(B, ""))
    return РАМКИ[язык][род].format(A=A, B=B, a=a, b=b, d=a - b, **род_падеж)


def pass_shows(pass_i):
    out = Сбор()
    for случай in случаи(pass_i):
        for род in (ВЫШЕ, НИЖЕ, НАСКОЛЬКО):
            out.род = род
            for язык in ЯЗЫКИ:
                out.язык = язык
                out.append(страница(язык, род, случай))
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = (ВЫШЕ, НИЖЕ, НАСКОЛЬКО)

ЗАЧЕМ_РОДА = {
    ВЫШЕ: "«Ben is 120 cm tall. Carla is 8 cm taller than Ben. how tall is Carla? Carla is 128 cm tall: "
          "120 + 8 = 128.» — опора до сравнения, ответ называет лицо",
    НИЖЕ: "«Carla is 128 cm tall. Ben is 8 cm shorter than Carla. how tall is Ben? … 128 − 8 = 120.» — та же "
          "разность с другого конца",
    НАСКОЛЬКО: "«how much taller is Carla than Ben? 8 cm taller: 128 − 120 = 8.» — разность, спрошенная словом",
}


def страницы(pass_i):
    return pass_shows(pass_i)


def перебор_с_языком(pass_i):
    """[(строка, род, ЯЗЫК)] — тот же обход, прочтённый тремя столбцами."""
    return pass_shows(pass_i).тройками


def перебор_страниц(pass_i):
    return pass_shows(pass_i).парами


def группы(pass_i):
    return [страницы(pass_i)]


def _показы():
    from layer import PASSES                             # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род, язык in перебор_с_языком(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), (язык, род))
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_дома():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    сбор = pass_shows(0)
    assert len(сбор) == len(сбор.роды), "показ остался без рода"
    пустые = set(РОДЫ) - {р for _я, р in ПОКАЗЫ.values()}
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"
    for высокий, низкий, a, b in (с for шаг in range(5) for с in случаи(шаг)):
        assert высокий != низкий and 2 <= a - b <= 25 and 95 <= b and a <= 179


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
