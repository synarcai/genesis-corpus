#!/usr/bin/env python3
# GENESIS L4: science map as copula triples (holon's connective genus).
# P-1 sparse concretes / P-4 five shuffles + \f seams / single-word copulas
# so the [□ w □] court buys them; breadth over depth, >=LAW instances per genus.
import random
import sys
import pathlib as _pathlib

sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent))
import layer  # noqa: E402

# (RU-subject, RU-object) with EN twins; facts are schoolbook-safe.
FACTS = {
    # copula genus: definition (is / это)
    "def": [
        (("вода", "жидкость"), ("water", "a liquid")),
        (("железо", "металл"), ("iron", "a metal")),
        (("кислород", "газ"), ("oxygen", "a gas")),
        (("земля", "планета"), ("the earth", "a planet")),
        (("солнце", "звезда"), ("the sun", "a star")),
        (("сердце", "орган"), ("the heart", "an organ")),
        (("бактерия", "организм"), ("a bacterium", "an organism")),
        (("треугольник", "фигура"), ("a triangle", "a shape")),
        (("сложение", "операция"), ("addition", "an operation")),
        (("алгоритм", "процедура"), ("an algorithm", "a procedure")),
        (("глагол", "слово"), ("a verb", "a word")),
        (("медь", "металл"), ("copper", "a metal")),
    ],
    # genus: causes (вызывает / causes)
    "cause": [
        (("гравитация", "падение"), ("gravity", "falling")),
        (("нагрев", "расширение"), ("heating", "expansion")),
        (("трение", "нагрев"), ("friction", "heating")),
        (("вирус", "болезнь"), ("a virus", "disease")),
        (("дождь", "наводнение"), ("rain", "flooding")),
        (("ветер", "волны"), ("wind", "waves")),
        (("свет", "фотосинтез"), ("light", "photosynthesis")),
        (("ток", "магнетизм"), ("current", "magnetism")),
    ],
    # genus: contains (содержит / contains)
    "contain": [
        (("вода", "водород"), ("water", "hydrogen")),
        (("воздух", "азот"), ("air", "nitrogen")),
        (("клетка", "ядро"), ("a cell", "a nucleus")),
        (("атом", "протоны"), ("an atom", "protons")),
        (("кровь", "железо"), ("blood", "iron")),
        (("молоко", "кальций"), ("milk", "calcium")),
        (("гранит", "кварц"), ("granite", "quartz")),
        (("библиотека", "книги"), ("a library", "books")),
    ],
    # genus: part-of (часть / part) — RU "X — часть Y", EN "X is part of Y"
    "part": [
        (("ядро", "клетки"), ("the nucleus", "the cell")),
        (("сердце", "организма"), ("the heart", "the organism")),
        (("колесо", "машины"), ("a wheel", "the car")),
        (("листья", "растения"), ("leaves", "the plant")),
        (("луна", "неба"), ("the moon", "the sky")),
        (("цифра", "числа"), ("a digit", "the number")),
    ],
}


def ru_lines(rng):
    out = []
    for (s, o), _ in FACTS["def"]:
        out.append(f"{s} — это {o}.")
    for (s, o), _ in FACTS["cause"]:
        out.append(f"{s} вызывает {o}.")
    for (s, o), _ in FACTS["contain"]:
        out.append(f"{s} содержит {o}.")
    for (s, o), _ in FACTS["part"]:
        out.append(f"{s} — часть {o}.")
    # ВОПРОС У КАЖДОГО РОДА СВЯЗКИ, А НЕ У ОДНОГО (прибор широты вопроса
    # 03.09: род, говорящий одними утверждениями, учит отвечать молчанием —
    # спрашивалось только определение, а причина, содержание и часть молчали).
    # Вопрос назван словом своего рода: «что вызывает», «что содержит», «часть
    # чего», — и ответ повторяет утверждение целиком, как велит закон пары.
    qs = rng.sample(FACTS["def"], 4)
    for (s, o), _ in qs:
        out.append(f"что такое {s}? {s} — это {o}.")
    for (s, o), _ in rng.sample(FACTS["cause"], 4):
        out.append(f"что вызывает {o}? {s} вызывает {o}.")
    for (s, o), _ in rng.sample(FACTS["contain"], 4):
        out.append(f"что содержит {s}? {s} содержит {o}.")
    for (s, o), _ in rng.sample(FACTS["part"], 4):
        out.append(f"часть чего {s}? {s} — часть {o}.")
    return out


def en_lines(rng):
    out = []
    for _, (s, o) in FACTS["def"]:
        out.append(f"{s} is {o}.")
    for _, (s, o) in FACTS["cause"]:
        out.append(f"{s} causes {o}.")
    for _, (s, o) in FACTS["contain"]:
        out.append(f"{s} contains {o}.")
    for _, (s, o) in FACTS["part"]:
        out.append(f"{s} is part of {o}.")
    qs = rng.sample(FACTS["def"], 4)
    for _, (s, o) in qs:
        out.append(f"what is {s}? {s} is {o}.")
    for _, (s, o) in rng.sample(FACTS["cause"], 4):
        out.append(f"what causes {o}? {s} causes {o}.")
    for _, (s, o) in rng.sample(FACTS["contain"], 4):
        out.append(f"what does {s} contain? {s} contains {o}.")
    for _, (s, o) in rng.sample(FACTS["part"], 4):
        out.append(f"what is {s} part of? {s} is part of {o}.")
    return out


# ЦЕЛЬ ОБЪЯВЛЕНА ИМЕНЕМ МОДУЛЯ, А НЕ ПЕРЕМЕННОЙ ВНУТРИ ТЕЛА. Прибор
# воспроизводимости читает цель генератора объявлением; путь, живший
#лишь в теле функции, делал этот слой НЕВИДИМЫМ для меры — и он был
# невидим всё время её существования.
ЦЕЛЬ = "datasets/genesis_l4.txt"


def main():
    rng = random.Random(41)
    ru = ru_lines(rng)
    en = en_lines(rng)
    blocks = []
    for seed in range(5):
        r = random.Random(seed)
        b = ru[:]
        r.shuffle(b)
        blocks.append("\n".join(b))
    for seed in range(5):
        r = random.Random(100 + seed)
        b = en[:]
        r.shuffle(b)
        blocks.append("\n".join(b))
    text = "\n\f\n".join(blocks) + "\n"
    path = ЦЕЛЬ
    # ВОРОТА И ЗДЕСЬ (04.09): мир писал файл в обход палаты, и оттого сто
    # новых вопросных строк легли НЕСУДИМЫМИ — судимость свода упала со ста
    # процентов до девяноста девяти, и назвал это не суд, а мера. Мир, чей
    # генератор пишет мимо ворот, есть мир без «нет»: закон ворот общий, и
    # исключений у него нет.
    layer._ворота(path, text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"L4: RU={len(ru)} EN={len(en)} строк-базы, файл={path}, байт={len(text.encode('utf-8'))}")


if __name__ == "__main__":
    main()
