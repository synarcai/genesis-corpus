#!/usr/bin/env python3
"""GENESIS layer: A PART OF A TOTAL GOES, AND A PART REMAINS.

    ida counted 50 cards. ida counted 20 more cards.
    1/2 of the cards had gone. how many cards remain? 35 cards remain.
    у иды было 70 книг. половина книг ушла.
    сколько книг осталось? осталось 35 книг.

The benchmark's own shape (g1.36): a total is built in two steps, then
a FRACTION of it is removed, and the question asks what is left. Three
things happen in one show, and each is a place a learner can go wrong:

  · the TOTAL must be formed before the fraction applies — a fraction
    of the first part is not a fraction of the total;
  · the fraction names what GOES while the answer names what REMAINS,
    so the polarity is carried by the verb; both directions are asked,
    because a genus shown from one side teaches one side;
  · both readings of the fraction appear — the slash «1/2» and the word
    «a half of» — since the benchmark writes both.

TWO DECLARATIONS OF WORLD KNOWLEDGE, neither derivable (M-103):
  · only PACKAGEABLE goods are counted and depleted here — an acre is
    a measure, and «ida counted 50 acres» is a category error;
  · the depleting verb is declared WITH the items it can apply to —
    the first run said «the apps were eaten», which is flawless English
    about an impossible world.

EVERY DIVISION IS EXACT BY CONSTRUCTION: the total is trimmed to a
multiple of the denominator, so no answer is rounded. A layer that
rounds teaches the rounding.
"""

import json
import pathlib
import sys

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_depletion.txt"

ЗДЕСЬ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ЗДЕСЬ))
from gsm_items import PACKAGEABLE  # noqa: E402
from langpack import count_form_index  # noqa: E402
from layer import Сбор, emit  # noqa: E402
import mass  # noqa: E402

RU_PACK = json.loads((ЗДЕСЬ / "langpacks/ru.json").read_text(encoding="utf-8"))
RU_RULE = {"forms": ["one", "few", "many"],
           "count_agreement": RU_PACK["count_agreement"]}

NAMES = ["ida", "omar", "pia", "rosa", "sven", "tara", "umar", "vera"]
# (знаменатель, слово доли en, слово доли ru)
ДОЛИ = [(2, "a half", "половина"), (3, "a third", "треть"),
        (4, "a quarter", "четверть"), (5, "a fifth", "пятая часть")]
# ГЛАГОЛ УБЫЛИ ОБЪЯВЛЕН СО СВОИМИ ПРЕДМЕТАМИ: съесть можно съедобное,
# продать — товар, унести — что угодно счётное.
ЕДА = ["apples", "cookies", "sandwiches", "eggs", "cupcakes",
       "candies", "bananas", "chimichangas"]
УБЫЛЬ = [
    ("had gone", "remain", None),
    ("were sold", "are left", None),
    ("were taken", "remain", None),
    ("had left", "stay", None),
    ("were eaten", "are left", tuple(ЕДА)),
]
ТОВАРЫ = sorted(PACKAGEABLE)
# (имя, формы «одна/две/пять», родительный множественного)
ВЕЩИ_RU = [
    ("книга", ("книга", "книги", "книг"), "книг"),
    ("яблоко", ("яблоко", "яблока", "яблок"), "яблок"),
    ("монета", ("монета", "монеты", "монет"), "монет"),
    ("орех", ("орех", "ореха", "орехов"), "орехов"),
    ("марка", ("марка", "марки", "марок"), "марок"),
]
ИМЕНА_RU = ["иды", "омара", "пии", "розы", "свена", "тары"]
# МАССА ОТ ПРАВИЛА (tools/mass.py, М-148): части — из двух взаимно простых
# циклов шагом k, различных показов на рамку до 77 (было 10).
БОЛЬШИЕ = [50, 30, 24, 40, 18, 45, 28, 60, 35, 16, 21]
МАЛЫЕ = [20, 10, 12, 6, 8, 25, 15]
ШИРИНА = 10


def ру(формы, k):
    return формы[count_form_index(RU_PACK, RU_RULE, k)]


# РОДЫ НАЗВАНЫ КОММЕНТАРИЯМИ «# ---» И НЕ ВЫШЛИ НАРУЖУ. Спрошено об ОСТАВШЕМСЯ и спрошено
# об УШЕДШЕМ — две стороны одной полярности и два разных ответа; целое, собираемое из двух
# счётов, требует трёх шагов вместо двух; а закон доли сказан прямо и без чисел.
ОСТАТОК = "доля ушла, спрошено об остатке"
ЦЕЛОЕ_ИЗ_ДВУХ = "целое собрано из двух счётов, и лишь потом взята доля"
УШЕДШЕЕ = "та же доля, но спрошено об УШЕДШЕМ"


def pass_shows(pass_i):
    out = Сбор()
    for i in range(ШИРИНА):
        k0 = mass.шаг(pass_i, i, ШИРИНА)
        a, b = mass.пара(k0, БОЛЬШИЕ, МАЛЫЕ)
        зн, доля_en, доля_ru = ДОЛИ[k0 % len(ДОЛИ)]
        ушёл, остался, только = УБЫЛЬ[k0 % len(УБЫЛЬ)]
        кто = NAMES[k0 % len(NAMES)]
        пул = list(только) if только else ТОВАРЫ
        вещь = пул[k0 % len(пул)]
        всего = (a + b) - (a + b) % зн
        b = всего - a
        if всего <= зн or b <= 0:
            continue
        ушло, осталось = всего // зн, всего - всего // зн
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166): 300
        # показов доли без единого шага. Доля есть ДВА действия, и кузница
        # обязана показать оба порознь: сперва часть, потом остаток; там,
        # где целое ещё собирается из двух счётов, шагов три.
        кузн = f": {всего} ÷ {зн} = {ушло}, {всего} − {ушло} = {осталось}" if (k0 // 2) % 2 == 0 else ""
        кузн2 = (f": {a} + {b} = {всего}, {всего} ÷ {зн} = {ушло}, {всего} − {ушло} = {осталось}"
                 if (k0 // 2) % 2 == 0 else "")
        кузн_ушло = f": {всего} ÷ {зн} = {ушло}" if (k0 // 2) % 2 == 0 else ""
        # --- полная форма бенчмарка: два шага, доля, остаток
        for доля in (f"1/{зн}", доля_en):
            out.род = ЦЕЛОЕ_ИЗ_ДВУХ
            out.append(
                f"{кто} counted {a} {вещь}. {кто} counted {b} more {вещь}. "
                f"{доля} of the {вещь} {ушёл}. how many {вещь} {остался}? "
                f"{осталось} {вещь} {остался}{кузн2}."
            )
            out.род = ОСТАТОК
            out.append(
                f"{кто} had {всего} {вещь}. {доля} of the {вещь} {ушёл}. "
                f"how many {вещь} {остался}? {осталось} {вещь} {остался}{кузн}."
            )
        # --- ОБЕ СТОРОНЫ ПОЛЯРНОСТИ: спрошено и об ушедшем
        out.род = УШЕДШЕЕ
        out.append(
            f"{кто} had {всего} {вещь}. 1/{зн} of the {вещь} {ушёл}. "
            f"how many {вещь} went? {ушло} {вещь} went{кузн_ушло}."
        )
        # --- русская поверхность СВОИМИ словами, а не английскими
        имя_ru = ИМЕНА_RU[(pass_i + i) % len(ИМЕНА_RU)]
        _, формы, родит = ВЕЩИ_RU[(pass_i * 3 + i) % len(ВЕЩИ_RU)]
        out.род = ОСТАТОК
        out.append(
            f"у {имя_ru} было {всего} {ру(формы, всего)}. "
            f"{доля_ru} {родит} ушла. сколько {родит} осталось? "
            f"осталось {осталось} {ру(формы, осталось)}{кузн}."
        )
        # ЗАКОН ДОЛИ ПРИНАДЛЕЖИТ ДЕЛУ, КОТОРОЕ ОН ДЕЛАЕТ ВОЗМОЖНЫМ (14.09): две эти
        # строки одинаковы во всех проходах и родом дали бы миру род в ДВЕ страницы —
        # много ниже закона массы. «Что осталось есть целое минус ушедшее» есть страница
        # об остатке, и там ей место.
        out.род = ОСТАТОК
        out.append("a part goes and a part remains.")
        out.append("what is left is the whole minus what went.")
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = (ОСТАТОК, ЦЕЛОЕ_ИЗ_ДВУХ, УШЕДШЕЕ)

ЗАЧЕМ_РОДА = {
    ОСТАТОК: "«1/3 ушла, сколько осталось» — два шага: доля, затем остаток; и закон "
             "«что осталось есть целое минус ушедшее» сказан здесь же",
    ЦЕЛОЕ_ИЗ_ДВУХ: "целое ещё не дано: сперва сложить два счёта, и лишь потом делить — "
                   "три шага, и все три показаны",
    УШЕДШЕЕ: "вторая полярность той же рамки: спрошено об ушедшем, и шаг один",
}


def страницы(pass_i):
    return pass_shows(pass_i)


def перебор_страниц(pass_i):
    return pass_shows(pass_i).парами


def группы(pass_i):
    return [страницы(pass_i)]


def _показы():
    from layer import PASSES                             # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род in перебор_страниц(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), род)
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_дома():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    сбор = pass_shows(0)
    assert len(сбор) == len(сбор.роды), "показ остался без рода"
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
