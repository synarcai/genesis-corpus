#!/usr/bin/env python3
"""GENESIS layer: RATE, MONEY AND TIME — the bridge a word problem walks.

A band of thirty questions died on one bridge. «Gerald earns 30 dollars
every day; how much in a week?» needs FOUR things at once, and the corpus
carried each of them apart and none of them together:

    СТАВКА     — «30 dollars EVERY day» ties a money unit to a time unit;
                 the pair (dollars, day) must be LIVED, not merely stated;
    ЧИСЛОФОРМА — «a week has 7 DAYS» but «7 days make a WEEK»: singular and
                 plural of the SAME unit on the SAME numbers, side by side.
                 This is where the band actually stopped: the organism knew
                 «day» and knew «days» and did not know they are one word;
    ПЕРЕВОД    — hour↔minute, day↔hour, week↔day, dollar↔cent, walked as a
                 relation and not memorised as a pair;
    ГЛАГОЛ ДЕНЕГ — cost / spend / have left, with the polarity that spending
                 SUBTRACTS; and «X and Y cost N» — a sum said by a verb.

ONE FACT, THREE SURFACES, SAME NUMBERS. The rate, the total and the question
stand together on one triple of numbers, in English and in Russian, because
the bridge is crossed by seeing the same numbers wear three clothes.

RUSSIAN PAYS ITS OWN PRICE, AND IT IS PAID HERE. «сколько минут в двух
часах?» needs the numeral in an oblique form («двух», declared by the pack)
AND the noun in the prepositional plural («часах»), which no house carried:
counting triples are AGREEMENT under a number, not case. The prepositional
plural is now DERIVED from the declared paradigm (`rugram.предложный_мн`),
and the question can finally be asked in Russian at all.

EVERY RELATION IS WALKED, NOT WRITTEN: `units.отношение` finds the factor
through the declared graph, and the court walks it again.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numerals  # noqa: E402
import rugram  # noqa: E402
import units  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_rates.txt"

# (крупная единица, мелкая) — отношение НЕ пишется, оно проходится
ПЕРЕВОДЫ = (("hour", "minute"), ("day", "hour"), ("week", "day"),
            ("year", "month"), ("dollar", "cent"),
            ("rouble", "kopeck"), ("kilometre", "metre"))
# русское имя единицы для парадигмы — по английскому имени дома единиц
РУССКОЕ = {"hour": "час", "minute": "минута", "day": "день",
           "week": "неделя", "month": "месяц", "year": "год",
           "dollar": None, "cent": None, "rouble": "рубль",
           "kopeck": "копейка", "kilometre": "километр",
           "metre": None}
# ставка: что платят, за какую единицу времени, и кем
СТАВКИ = (("dollar", "day"), ("dollar", "hour"), ("cent", "minute"),
          ("rouble", "day"), ("rouble", "hour"))
ДЕЯТЕЛИ = (("a worker", "рабочий", "зарабатывает"),
           ("a driver", "водитель", "зарабатывает"),
           ("a baker", "пекарь", "зарабатывает"))
ВЕЩИ = (("book", "книга"), ("pen", "ручка"), ("card", "карта"))


# АРТИКЛЬ ИДЁТ ЗА ЗВУКОМ, А НЕ ЗА БУКВОЙ. «a hour» — ошибка, которую
# слой учил бы с полной судимостью: «h» в «hour» не звучит, и артикль
# берёт форму «an». Гласные названы правилом, немое «h» — именованным
# списком, ибо это факт ПРОИЗНОШЕНИЯ, из письма не выводимый.
_НЕМОЕ_H = ("hour", "honest", "heir")


def артикль(слово):
    """«a» или «an» — по звуку, с которого слово начинается."""
    if слово[0] in "aeiou" or слово.startswith(_НЕМОЕ_H):
        return "an"
    return "a"


def _мн(имя):
    return units.англ(имя, True)


def _ед(имя):
    return units.англ(имя)


def _по_счёту(n, имя):
    """Английская форма единицы при числе: единица — единственное.

    «1 dollars» есть та же ложь, что «a hour»: число один требует
    единственного, и слой, писавший множественное всегда, учил бы
    английскому согласованию наоборот.
    """
    return units.англ(имя, n != 1)


def числоформа(шаг):
    """Единственное и множественное ОДНОЙ единицы на одних числах.

    Мост, о который встала полоса: организм знал «day» и знал «days» и
    не знал, что это одно слово. Обе формы стоят рядом, и число между
    ними одно.
    """
    вон = []
    for i, (крупно, мелко) in enumerate(ПЕРЕВОДЫ):
        k = units.отношение(крупно, мелко)
        if k is None:
            continue
        n = 2 + (шаг + i) % 4
        вон.append(f"{артикль(_ед(крупно))} {_ед(крупно)} has "
                   f"{k} {_по_счёту(k, мелко)}.")
        вон.append(f"{k} {_по_счёту(k, мелко)} make "
                   f"{артикль(_ед(крупно))} {_ед(крупно)}.")
        вон.append(f"{n} {_по_счёту(n, крупно)} are "
                   f"{n * k} {_по_счёту(n * k, мелко)}.")
        вон.append(f"the plural of {_ед(крупно)} is {_мн(крупно)}, and "
                   f"1 {_ед(крупно)} is {k} {_по_счёту(k, мелко)}.")
        ру_к, ру_м = РУССКОЕ.get(крупно), РУССКОЕ.get(мелко)
        if ру_к and ру_м:
            вон.append(f"в {rugram.ПАРАДИГМЫ[ру_к][5]} "
                       f"{k} {units.рус(мелко, k)}.")
            вон.append(f"{k} {units.рус(мелко, k)} составляют "
                       f"{rugram.ПАРАДИГМЫ[ру_к][3]}.")
            вон.append(f"{n} {units.рус(крупно, n)} — это "
                       f"{n * k} {units.рус(мелко, n * k)}.")
    return вон


def вопрос_перевода(шаг):
    """«сколько минут в двух часах?» — числительное косвенно, имя в предложном."""
    вон = []
    табл = numerals.таблица("ru")
    косвенно = _косвенные()
    for i, (крупно, мелко) in enumerate(ПЕРЕВОДЫ):
        k = units.отношение(крупно, мелко)
        if k is None:
            continue
        n = 2 + (шаг * 2 + i) % 5
        вон.append(f"how many {_мн(мелко)} are in "
                   f"{n} {_по_счёту(n, крупно)}? "
                   f"{n} {_по_счёту(n, крупно)} are "
                   f"{n * k} {_по_счёту(n * k, мелко)}.")
        ру_к, ру_м = РУССКОЕ.get(крупно), РУССКОЕ.get(мелко)
        предл = rugram.предложный_мн(ру_к) if ру_к else None
        слово_n = косвенно.get(str(n))
        if предл and слово_n and ру_м:
            вон.append(f"сколько {units.рус(мелко, 5)} в {слово_n} "
                       f"{предл}? {n} {units.рус(крупно, n)} — это "
                       f"{n * k} {units.рус(мелко, n * k)}.")
    return вон


def _косвенные():
    import json
    ф = pathlib.Path(__file__).resolve().parent / "langpacks" / "ru.json"
    try:
        return json.loads(ф.read_text(encoding="utf-8")).get(
            "numeral_oblique") or {}
    except (OSError, ValueError):
        return {}


def ставки(шаг):
    """СТАВКА связывает единицу денег с единицей времени."""
    вон = []
    for i, (деньги, время) in enumerate(СТАВКИ):
        ставка = 2 + (шаг + i) % 9
        сколько = 2 + (шаг * 3 + i) % 6
        итог = ставка * сколько
        кто_en, кто_ru, глагол = ДЕЯТЕЛИ[(шаг + i) % len(ДЕЯТЕЛИ)]
        вон.append(f"{кто_en} earns {ставка} "
                   f"{_по_счёту(ставка, деньги)} every "
                   f"{_ед(время)}.")
        вон.append(f"{кто_en} earns {ставка} "
                   f"{_по_счёту(ставка, деньги)} per {_ед(время)}; in "
                   f"{сколько} {_по_счёту(сколько, время)} {кто_en} "
                   f"earns {итог} {_по_счёту(итог, деньги)}.")
        # THE QUESTION LINE IS WHOLE (М-147; holon 04.09, class tellings-differ:
        # the unit of the answer came from a neighbouring line): the rate
        # stands in the line, and the answer carries its product as a link.
        вон.append(f"{кто_en} earns {ставка} {_по_счёту(ставка, деньги)} every "
                   f"{_ед(время)}. how much does {кто_en} earn in {сколько} "
                   f"{_по_счёту(сколько, время)}? in {сколько} "
                   f"{_по_счёту(сколько, время)} {кто_en} earns "
                   f"{итог} {_по_счёту(итог, деньги)}: {ставка} × {сколько} = {итог}.")
        ру_вр = РУССКОЕ.get(время)
        if ру_вр:
            в_ед = rugram.ПАРАДИГМЫ[ру_вр][3]
            вон.append(f"{кто_ru} {глагол} {ставка} "
                       f"{units.рус(деньги, ставка)} в {в_ед}.")
            вон.append(f"{кто_ru} {глагол} {ставка} "
                       f"{units.рус(деньги, ставка)} в {в_ед}; за "
                       f"{сколько} {units.рус(время, сколько)} "
                       f"{кто_ru} {глагол} {итог} "
                       f"{units.рус(деньги, итог)}.")
            вон.append(f"{кто_ru} {глагол} {ставка} {units.рус(деньги, ставка)} в {в_ед}. "
                       f"сколько {units.рус(деньги, 5)} {кто_ru} "
                       f"{глагол} за {сколько} "
                       f"{units.рус(время, сколько)}? за {сколько} "
                       f"{units.рус(время, сколько)} {кто_ru} "
                       f"{глагол} {итог} {units.рус(деньги, итог)}: {ставка} × {сколько} = {итог}.")
    return вон


def за_штуку(шаг):
    """«each bolt costs 3 cents» — ставка за ШТУКУ, а не за время."""
    вон = []
    for i, (вещь_en, вещь_ru) in enumerate(ВЕЩИ):
        цена = 2 + (шаг + i) % 8
        сколько = 2 + (шаг * 2 + i) % 7
        итог = цена * сколько
        вон.append(f"each {вещь_en} costs {цена} dollars.")
        вон.append(f"each {вещь_en} costs {цена} dollars; {сколько} "
                   f"{вещь_en}s cost {итог} dollars.")
        вон.append(f"how much do {сколько} {вещь_en}s cost? {сколько} "
                   f"{вещь_en}s cost {итог} dollars.")
        вон.append(f"одна {вещь_ru} стоит {цена} "
                   f"{units.рус('rouble', цена)}; {сколько} "
                   f"{_ру_счёт(вещь_ru, сколько)} стоят {итог} "
                   f"{units.рус('rouble', итог)}.")
    return вон


def _ру_счёт(слово, счёт):
    """Форма русского имени при счёте — по объявленной тройке."""
    return rugram.форма(слово, счёт)


def трата(шаг):
    """ТРАТА ВЫЧИТАЕТ, и остаток назван вместе с основанием."""
    вон = []
    for i in range(6):
        было = 20 + (шаг * 7 + i * 5) % 60
        потрачено = 3 + (шаг + i * 3) % 15
        осталось = было - потрачено
        вон.append(f"he had {было} dollars and spent {потрачено} "
                   f"dollars; he has {осталось} dollars left.")
        вон.append(f"how much does he have left after spending "
                   f"{потрачено} dollars of {было} dollars? he has "
                   f"{осталось} dollars left.")
        вон.append(f"у него было {было} "
                   f"{units.рус('rouble', было)}, он потратил "
                   f"{потрачено} {units.рус('rouble', потрачено)}; у "
                   f"него осталось {осталось} "
                   f"{units.рус('rouble', осталось)}.")
    return вон


def вместе_стоят(шаг):
    """«X and Y cost N» — сумма, сказанная ГЛАГОЛОМ, а не знаком."""
    вон = []
    for i in range(5):
        а = 5 + (шаг * 3 + i * 7) % 40
        б = 4 + (шаг + i * 5) % 30
        (одна, ру_а), (вторая, ру_б) = (ВЕЩИ[i % len(ВЕЩИ)],
                                        ВЕЩИ[(i + 1) % len(ВЕЩИ)])
        вон.append(f"the {одна} costs {а} dollars and the {вторая} "
                   f"costs {б} dollars; the {одна} and the {вторая} "
                   f"cost {а + б} dollars.")
        вон.append(f"{ру_а} стоит {а} {units.рус('rouble', а)}, а "
                   f"{ру_б} стоит {б} {units.рус('rouble', б)}; "
                   f"вместе они стоят {а + б} "
                   f"{units.рус('rouble', а + б)}.")
    return вон


def доллары_и_центы(шаг):
    """Крупное и мелкое обеими сторонами: 105 центов и 1 доллар 5 центов."""
    вон = []
    k = units.отношение("dollar", "cent")
    for i in range(6):
        д = 1 + (шаг + i) % 9
        ц = 5 + (шаг * 7 + i * 11) % 90
        всего = д * k + ц
        дс, цс = _по_счёту(д, "dollar"), _по_счёту(ц, "cent")
        вон.append(f"{д} {дс} and {ц} {цс} are {всего} cents.")
        вон.append(f"{всего} cents are {д} {дс} and {ц} {цс}.")
        вон.append(f"how many cents are {д} {дс} and {ц} {цс}? "
                   f"{д} {дс} and {ц} {цс} are {всего} cents.")
        вон.append(f"{д} {units.рус('rouble', д)} {ц} "
                   f"{units.рус('kopeck', ц)} — это {всего} "
                   f"{units.рус('kopeck', всего)}.")
    return вон


ГРУППЫ = (числоформа, вопрос_перевода, ставки, за_штуку, трата,
          вместе_стоят, доллары_и_центы)


def pass_groups(шаг):
    return [сделать(шаг) for сделать in ГРУППЫ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
