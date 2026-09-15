#!/usr/bin/env python3
"""GENESIS layer: DIVISION WITH A REMAINDER (genus 9).

    17 = 5 × 3 + 2.
    17 divided by 5 is 3 remainder 2.
    17 apples shared among 5 kids leaves 2 left over.
    17 разделить на 5 будет 3, остаток 2.

THE GLYPH AXIS JUDGES ITSELF. A remainder has no glyph of its own, so
the weld is written as the identity it actually is — «a = b × q + r» —
and `scripts/arith_court.py` verifies every one of them without being
told anything about remainders. A surface that cannot be checked is a
surface that can lie twice.

EVERY PAIR IS INEXACT BY CONSTRUCTION: the divisor never divides the
dividend, because a «remainder 0» show would teach that the genus and
plain division are the same thing. The fractions layer says the exact
case, and says it exactly.

TWO DIFFERENT PAIRS PER SURFACE at least, as holon's market requires:
a surface shown on one pair teaches the pair, not the surface.

The sharer of the sharing surface is an ANIMATE word and the shared
thing is not — «17 apples shared among 5 kids» is true of the world,
«17 kids shared among 5 apples» is grammatical and false, and no
census can see the difference (M-103).
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402 — счётные формы объявлены пакетом, не домом
from gsm_items import ANIMATE, ITEMS  # noqa: E402
from layer import Сбор, emit  # noqa: E402
from plural import by_count  # noqa: E402

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_remainders.txt"

THINGS = [w for w in ITEMS if w not in ANIMATE]
SHARERS = sorted(ANIMATE)
# (dividend, divisor) — never exact, and each divisor twice over
PAIRS = [(17, 5), (23, 5), (14, 3), (20, 3), (19, 4), (26, 4),
         (13, 2), (21, 2), (34, 7), (30, 7), (29, 6), (38, 6),
         (25, 8), (39, 8), (28, 9), (40, 9)]
# ГОЛЫЕ СТРОКИ ОБЪЯВЛЕНЫ С ЯЗЫКОМ (15.09): четыре строки без рамки, и язык каждой виден
# читателю, но не прибору — пока не назван рядом.
BARE = [
    ("a remainder is what is left over.", "en"),
    ("what is a remainder?", "en"),
    ("остаток — это то, что не разделилось.", "ru"),
    ("что такое остаток?", "ru"),
]


# ТРИ РОДА: тождество деления, счёт частного с остатком и раздача между носителями.
# Определение остатка («остаток — это то, что не разделилось») идёт к счёту, который оно
# делает возможным: четырьмя строками на весь свод оно было бы родом ниже закона массы.
ТОЖДЕСТВО = "тождество деления: a = b × q + r"
ДЕЛЕНИЕ = "частное и остаток: сказано, спрошено и определено"
РАЗДАЧА = "раздача между носителями: что осталось лишним"
# ДОЛГ РУССКОЙ СТОРОНЫ НАЗВАН УТРОМ И ВЫПЛАЧЕН ВЕЧЕРОМ (15.09). Причина названа была верно:
# вещи и носители брались из общих АНГЛИЙСКИХ списков `ITEMS` и `ANIMATE`, и русская сторона
# требовала своего списка СО СЧЁТНЫМИ ФОРМАМИ, а не перевода рамки.
#
#     ДОЛГ, У КОТОРОГО НАЗВАНА ПРИЧИНА, ОТЛИЧИМ ОТ НЕБРЕЖНОСТИ — и тем вернее берётся.
#
# Список взят не отсюда, а из ПАКЕТА РУССКОГО: всякое имя ниже объявлено в `rugram.СЧЁТНЫЕ`
# тремя формами, и дом не пишет своей таблицы. Рамка же выбрана та, где ВСЕ имена стоя́т в
# счётной форме: «17 яблок на 5 детей: каждому по 3 яблока, лишних 2».
#
#     РАМКА ВЫБИРАЕТСЯ ПОД ОБЪЯВЛЕННЫЕ ФОРМЫ, А НЕ ФОРМЫ ПОД КРАСИВУЮ РАМКУ. «Разделить
#     между 5 детьми» требует творительного множественного, какого пакет не объявляет вовсе,
#     — и дом, написавший его от руки, завёл бы вторую таблицу форм в обход пакета.
ВЕЩИ_RU = ("яблоко", "книга", "монета", "марка", "шарик", "орех", "конфета",
           "карандаш", "ручка", "билет", "открытка", "груша", "слива", "печенье")
НОСИТЕЛИ_RU = ("ребёнок", "гость", "ученик", "мальчик", "девочка", "житель", "человек")


def pass_shows(pass_i):
    out = Сбор()
    for i, (a, b) in enumerate(PAIRS):
        q, r = divmod(a, b)
        assert r and a == b * q + r, (a, b)
        thing = THINGS[(pass_i * 5 + i * 3) % len(THINGS)]
        who = SHARERS[(pass_i * 3 + i) % len(SHARERS)]
        out.род = ТОЖДЕСТВО
        out.язык = "—"
        out.append(f"{a} = {b} × {q} + {r}.")
        # THE LEDGER OF THE DIVISION (holon 03.09, ONE-CARRIER: an answer that
        # is computed shows its steps): «5 × 3 = 15, 17 − 15 = 2»
        леджер = f"{b} × {q} = {b * q}, {a} − {b * q} = {r}"
        out.род = ДЕЛЕНИЕ
        out.язык = "en"
        out.append(f"{a} divided by {b} is {q} remainder {r}: {леджер}.")
        out.род = РАЗДАЧА
        out.язык = "en"
        out.append(
            f"{a} {by_count(a, thing)} shared among {b} "
            f"{by_count(b, who)} leaves {r} left over."
        )
        вещь_ru = ВЕЩИ_RU[(pass_i * 5 + i * 3) % len(ВЕЩИ_RU)]
        кто_ru = НОСИТЕЛИ_RU[(pass_i * 3 + i) % len(НОСИТЕЛИ_RU)]
        out.язык = "ru"
        out.append(
            f"{a} {rugram.форма(вещь_ru, a)} на {b} {rugram.форма(кто_ru, b)}: "
            f"каждому по {q} {rugram.форма(вещь_ru, q)}, лишних {r}."
        )
        out.род = ДЕЛЕНИЕ
        out.язык = "ru"
        out.append(
            f"{a} разделить на {b} будет {q}, остаток {r}: {леджер}."
        )
        # ВОПРОСНАЯ ПОВЕРХНОСТЬ БЫЛА ТОЛЬКО ОПРЕДЕЛИТЕЛЬНОЙ («что такое
        # остаток?») — вычислительного вопроса не знал ни один язык.
        out.язык = "ru"
        out.append(
            f"сколько будет {a} разделить на {b}? "
            f"{a} разделить на {b} будет {q}, остаток {r}: {леджер}."
        )
        out.язык = "en"
        out.append(
            f"what is {a} divided by {b}? {a} divided by {b} is {q} remainder {r}: {леджер}."
        )
    out.род = ДЕЛЕНИЕ
    for tpl, яз in BARE:
        out.язык = яз
        out.append(tpl)
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = (ТОЖДЕСТВО, ДЕЛЕНИЕ, РАЗДАЧА)

ЗАЧЕМ_РОДА = {
    ТОЖДЕСТВО: "«17 = 5 × 3 + 2» — равенство, из которого остаток и берётся",
    ДЕЛЕНИЕ: "«17 разделить на 5 будет 3, остаток 2» с леджером — и «что такое остаток» "
             "здесь же",
    РАЗДАЧА: "«17 яблок на 5 друзей — 2 лишних»: тот же счёт в мире вещей",
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


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
