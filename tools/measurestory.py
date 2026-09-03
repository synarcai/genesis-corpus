#!/usr/bin/env python3
"""THE HOUSE OF MEASURED STORIES — a distance compared, and a pair priced.

Two of holon's three orders from the last lines of the attack (03.09), both
standing on a MEASURE rather than a count:

  «the frog jumped 31 inches. the grasshopper jumped 25 inches. how many more
   inches did the frog jump than the grasshopper? 31 − 25 = 6.»

  «a house and a lot cost 120 dollars together. the house costs three times as
   much as the lot. how much does the lot cost? 3 + 1 = 4, 120 ÷ 4 = 30.»

The first buys the VERB as part of the frame: the corpus had «if the
grasshopper jumped 8 inches and the mouse jumped 2 inches …» with one verb,
and a verb met once is learnt as a word, not as a place. Six verbs walk here,
each with its bare form for the question («how many more inches did the frog
JUMP»), and Russian says the same with the past tense agreeing with its actor
(«лягушка прыгнула», «кузнечик прыгнул»).

The second buys «as MUCH as» beside «times»: the corpus said «as many as» on
countables and never «as much as» on a price, so the whole «a and b cost S
together» was mute. Both ends are asked — the lesser and the greater — and the
greater costs one step more, for its answer runs through the lesser.

EVERY FORM IS DECLARED. The Russian measure names three count forms, the past
tense two genders, the second good its genitive; nothing is derived from an
ending. The house writes a FINITE set of shows, and the court knows it whole:
a line of these shapes that the table does not hold is a lie.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

# пары чисел меры: разность всегда положительна, и оба конца спрашиваются
ПАРЫ_МЕРЫ = ((31, 25), (48, 19), (27, 12), (54, 36), (73, 41), (18, 9),
             (65, 28), (92, 47))
# основания цены и множители: сумма есть (k + 1) × основание
ОСНОВАНИЯ_ЦЕНЫ = (30, 45, 60, 25, 15, 40)
МНОЖИТЕЛИ = (2, 3, 4, 5)

ЯЗЫКИ = {
    "en": dict(
        деятели=(("the frog", "m"), ("the grasshopper", "m"), ("the kangaroo", "m"),
                 ("the mouse", "m"), ("the cat", "m"), ("the dog", "m")),
        глаголы=(("jumped", "jump"), ("ran", "run"), ("walked", "walk"),
                 ("swam", "swim"), ("flew", "fly"), ("crawled", "crawl")),
        меры=(("inch", "inches"), ("foot", "feet"), ("metre", "metres")),
        мера_утв="{A} {Гп} {n} {МЕРАn}.",
        мера_воп_больше="how many more {МЕРА} did {A} {Гб} than {B}?",
        мера_воп_меньше="how many fewer {МЕРА} did {B} {Гб} than {A}?",
        # пара, оценённая одна другою
        товары=(("a house", "the house", "a lot", "the lot"),
                ("a car", "the car", "a bicycle", "the bicycle"),
                ("a ring", "the ring", "a chain", "the chain"),
                ("a table", "the table", "a chair", "the chair")),
        деньги=("dollar", "dollars"),
        кратные={2: "twice as much as", 3: "three times as much as",
                 4: "four times as much as", 5: "five times as much as"},
        пара_утв="{Б1} and {М1} cost {S} {ДЕНЬГИ} together. {Б2} costs {K} {М2}.",
        пара_воп_мал="how much does {М2} cost?",
        пара_воп_бол="how much does {Б2} cost?",
        ответ="so the answer is {r}.",
    ),
    "ru": dict(
        деятели=(("лягушка", "f"), ("кузнечик", "m"), ("кенгуру", "m"),
                 ("мышь", "f"), ("кот", "m"), ("пёс", "m")),
        # ПРЕДЛОГ ПРИНАДЛЕЖИТ ГЛАГОЛУ, А НЕ РАМКЕ: «прыгнул НА 31 сантиметр»,
        # но «пробежал 31 метр» — и объявлен он при каждом глаголе, третьей
        # формой, рядом с мужской и женской
        глаголы=(("прыгнул", "прыгнула", "на "), ("пробежал", "пробежала", ""),
                 ("прошёл", "прошла", ""), ("проплыл", "проплыла", ""),
                 ("пролетел", "пролетела", ""), ("прополз", "проползла", "")),
        меры=(("сантиметр", "сантиметра", "сантиметров"),
              ("метр", "метра", "метров"), ("шаг", "шага", "шагов")),
        мера_утв="{A} {Гп} {ПР}{n} {МЕРАn}.",
        мера_воп_больше="на сколько больше {МЕРАМ} {Гп} {A}, чем {B}?",
        мера_воп_меньше="на сколько меньше {МЕРАМ} {Гв} {B}, чем {A}?",
        товары=(("дом", "дом", "участок", "участка"),
                ("автомобиль", "автомобиль", "велосипед", "велосипеда"),
                ("кольцо", "кольцо", "цепочка", "цепочки"),
                ("стол", "стол", "стул", "стула")),
        деньги=("доллар", "доллара", "долларов"),
        кратные={2: "вдвое дороже", 3: "втрое дороже",
                 4: "вчетверо дороже", 5: "впятеро дороже"},
        пара_утв="{Б1} и {М1} вместе стоят {S} {ДЕНЬГИ}. {Б2} {K} {М2}.",
        пара_воп_мал="сколько стоит {М1}?",
        пара_воп_бол="сколько стоит {Б1}?",
        ответ="значит ответ: {r}.",
    ),
}
ФОРМЫ = ("мера_больше", "мера_меньше", "пара_мал", "пара_бол")


def счётная(формы, n):
    """The declared form of a unit beside its count (two forms or three)."""
    if len(формы) == 2:
        return формы[0] if n == 1 else формы[1]
    if n % 100 in range(11, 15):
        return формы[2]
    последняя = n % 10
    if последняя == 1:
        return формы[0]
    if последняя in (2, 3, 4):
        return формы[1]
    return формы[2]


def _глагол(язык, г, деятель):
    """Прошедшее время: русское согласуется с деятелем в роде."""
    формы = ЯЗЫКИ[язык]["глаголы"][г]
    if язык != "ru":
        return формы[0]
    _, род = ЯЗЫКИ[язык]["деятели"][деятель]
    return формы[0] if род == "m" else формы[1]


def мера(язык, форма, a, b, м=0, г=0, деятель=0, второй=1):
    """«the frog jumped 31 inches. … how many more inches …? 31 − 25 = 6.»"""
    я = ЯЗЫКИ[язык]
    if деятель == второй or a <= b:
        raise ValueError("нужны разные деятели и положительная разность")
    A, B = я["деятели"][деятель][0], я["деятели"][второй][0]
    формы = я["меры"][м]
    з = dict(A=A, B=B, МЕРА=счётная(формы, 2), МЕРАМ=счётная(формы, 5))
    пр = я["глаголы"][г][2] if len(я["глаголы"][г]) > 2 else ""
    факт = (я["мера_утв"].format(**з, Гп=_глагол(язык, г, деятель), ПР=пр, n=a, МЕРАn=счётная(формы, a))
            + " " + я["мера_утв"].format(**dict(з, A=B), Гп=_глагол(язык, г, второй), ПР=пр, n=b, МЕРАn=счётная(формы, b)))
    воп = я["мера_воп_больше" if форма == "мера_больше" else "мера_воп_меньше"].format(
        **з, Гб=я["глаголы"][г][1] if язык == "en" else "",
        Гп=_глагол(язык, г, деятель), Гв=_глагол(язык, г, второй))
    return f"{факт} {воп} {a} − {b} = {a - b}. {я['ответ'].format(r=a - b)}"


def пара(язык, форма, товар=0, k=2, основание=30):
    """«a house and a lot cost 120 dollars together. the house costs three
    times as much as the lot. how much does the lot cost? 3 + 1 = 4, 120 ÷ 4 = 30.»"""
    я = ЯЗЫКИ[язык]
    Б1, Б2, М1, М2 = я["товары"][товар]
    S = (k + 1) * основание
    з = dict(Б1=Б1, Б2=Б2, М1=М1, М2=М2, S=S, K=я["кратные"][k],
             ДЕНЬГИ=счётная(я["деньги"], S))
    факт = я["пара_утв"].format(**з)
    if форма == "пара_мал":
        r = основание
        леджер = f"{k} + 1 = {k + 1}, {S} ÷ {k + 1} = {r}."
        воп = я["пара_воп_мал"].format(**з)
    else:
        r = k * основание
        леджер = f"{k} + 1 = {k + 1}, {S} ÷ {k + 1} = {основание}, {k} × {основание} = {r}."
        воп = я["пара_воп_бол"].format(**з)
    return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"


def _образцы(язык):
    """Образцы разбора: поверхность узнаётся, а истина проверяется ПЕРЕПИСЬЮ.

    Дом бесконечен по парам деятелей, и таблицей его не описать; потому суд
    ЧИТАЕТ строку в её величины и ПИШЕТ страницу заново — совпала буква в
    букву, значит дом её и написал.
    """
    я = ЯЗЫКИ[язык]
    Д = _альт(д for д, _ in я["деятели"])
    Г = _альт([ф for формы in я["глаголы"] for ф in формы[:2]])
    М = _альт([ф for формы in я["меры"] for ф in формы])
    Т = _альт([ф for т in я["товары"] for ф in т])
    ДЕН = _альт(я["деньги"])
    К = _альт(я["кратные"].values())
    ч = r"(\d+)"
    if язык == "en":
        мера_ = re.compile(
            rf"^({Д}) ({Г}) {ч} ({М})\. ({Д}) ({Г}) {ч} ({М})\. "
            rf"how many (more|fewer) ({М}) did ({Д}) (\w+) than ({Д})\? .*$")
    else:
        мера_ = re.compile(
            rf"^({Д}) ({Г}) (?:на )?{ч} ({М})\. ({Д}) ({Г}) (?:на )?{ч} ({М})\. "
            rf"на сколько (больше|меньше) ({М}) ({Г}) ({Д}), чем ({Д})\? .*$")
    пара_ = re.compile(
        rf"^({Т}) (?:and|и) ({Т}) [^.]*?{ч} {ДЕН}[^.]*\. ({Т}) [^.]*?({К}) ({Т})\. .*$")
    return мера_, пара_


ОБРАЗЦЫ = {л: _образцы(л) for л in ЯЗЫКИ}


def _разобрать_меру(язык, м):
    """Величины меры по поверхности, или None."""
    я = ЯЗЫКИ[язык]
    имена = [д for д, _ in я["деятели"]]
    A, г1, a, м1, B, г2, b, м2 = (м.group(1), м.group(2), int(м.group(3)), м.group(4),
                                  м.group(5), м.group(6), int(м.group(7)), м.group(8))
    if A not in имена or B not in имена:
        return None
    деятель, второй = имена.index(A), имена.index(B)
    глагол = next((г for г in range(len(я["глаголы"]))
                   if _глагол(язык, г, деятель) == г1 and _глагол(язык, г, второй) == г2), None)
    мера_и = next((i for i, формы in enumerate(я["меры"])
                   if счётная(формы, a) == м1 and счётная(формы, b) == м2), None)
    if глагол is None or мера_и is None:
        return None
    форма = "мера_больше" if м.group(9) in ("more", "больше") else "мера_меньше"
    return dict(форма=форма, a=a, b=b, м=мера_и, г=глагол,
                деятель=деятель, второй=второй)


def _разобрать_пару(язык, м):
    я = ЯЗЫКИ[язык]
    Б1, М1, S, Б2, K, М2 = (м.group(1), м.group(2), int(м.group(3)),
                            м.group(4), м.group(5), м.group(6))
    товар = next((i for i, т in enumerate(я["товары"])
                  if т[0] == Б1 and т[2] == М1 and т[1] == Б2 and т[3] == М2), None)
    k = next((к for к, слово in я["кратные"].items() if слово == K), None)
    if товар is None or k is None or S % (k + 1):
        return None
    return dict(товар=товар, k=k, основание=S // (k + 1))


def судить(строка):
    """(судимо, истинно): страница читается в величины и пишется заново."""
    с = строка.strip()
    for язык in ЯЗЫКИ:
        мера_, пара_ = ОБРАЗЦЫ[язык]
        м = мера_.match(с)
        if м:
            п = _разобрать_меру(язык, м)
            if п is None:
                return True, False
            try:
                return True, мера(язык, **п) == с
            except (KeyError, IndexError, ValueError, ZeroDivisionError):
                return True, False
        м = пара_.match(с)
        if м:
            п = _разобрать_пару(язык, м)
            if п is None:
                return True, False
            for форма in ("пара_мал", "пара_бол"):
                try:
                    if пара(язык, форма, **п) == с:
                        return True, True
                except (KeyError, IndexError, ValueError, ZeroDivisionError):
                    return True, False
            return True, False
    return False, False


def _проверка():
    for язык in ЯЗЫКИ:
        print(мера(язык, "мера_больше", 31, 25, м=0, г=0, деятель=0, второй=1))
        print(мера(язык, "мера_меньше", 31, 25, м=1, г=1, деятель=2, второй=3))
        print(пара(язык, "пара_мал", товар=0, k=3, основание=30))
        print(пара(язык, "пара_бол", товар=1, k=2, основание=45))
    свои = []
    for язык in ЯЗЫКИ:
        для = ЯЗЫКИ[язык]
        for г in range(len(для["глаголы"])):
            свои.append(мера(язык, "мера_больше", 31, 25, м=г % len(для["меры"]), г=г, деятель=0, второй=(г % 5) + 1))
            свои.append(мера(язык, "мера_меньше", 48, 19, м=(г + 1) % len(для["меры"]), г=г, деятель=2, второй=(г % 3) + 3))
        for k in МНОЖИТЕЛИ:
            свои.append(пара(язык, "пара_мал", товар=k % 4, k=k, основание=ОСНОВАНИЯ_ЦЕНЫ[k % len(ОСНОВАНИЯ_ЦЕНЫ)]))
            свои.append(пара(язык, "пара_бол", товар=(k + 1) % 4, k=k, основание=ОСНОВАНИЯ_ЦЕНЫ[(k + 2) % len(ОСНОВАНИЯ_ЦЕНЫ)]))
    плохих = [с for с in свои if судить(с) != (True, True)]
    мутанты = [
        "the frog jumped 31 inches. the grasshopper jumped 25 inches. how many more inches did the frog jump than the grasshopper? 31 − 25 = 7. so the answer is 7.",
        "лягушка прыгнула на 31 сантиметр. кузнечик прыгнул на 25 сантиметров. на сколько больше сантиметров прыгнул лягушка, чем кузнечик? 31 − 25 = 6. значит ответ: 6.",
        "a house and a lot cost 120 dollars together. the house costs three times as much as the lot. how much does the lot cost? 3 + 1 = 4, 120 ÷ 4 = 40. so the answer is 40.",
    ]
    поймано = [м for м in мутанты if судить(м) == (True, False)]
    print(f"проб дома: {len(свои)}, не признано: {len(плохих)}, "
          f"мутантов поймано: {len(поймано)} из {len(мутанты)}")


if __name__ == "__main__":
    _проверка()
