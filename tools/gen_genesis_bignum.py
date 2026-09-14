#!/usr/bin/env python3
"""GENESIS layer: LARGE NUMBERS (RUNG-1 gap: GSM8K
lives in hundreds and thousands; the positional column
is bought, the shows beyond twenty are scarce).

Kinds (glyph-first — GSM8K asks in digits):
  R  place rulers      "100 + 10 = 110."
  C  hundred chains    "340 + 10 = 350."
  A  column adds       "234 + 152 = 386."
  S  column subs       "574 − 231 = 343."
  M  tens multiplication "30 × 4 = 120."
  D  clean division    "480 ÷ 4 = 120."

Instances vary by pass (32's trail number: repeats buy
weight, not coverage); bare shows; form-feed seams.
"""

import inverting
from layer import Сбор, emit

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_bignum.txt"


# ТРИ РОДА НАЗВАНЫ КОММЕНТАРИЯМИ-БУКВАМИ «R», «A/S», «M/D» И НЕ ВЫШЛИ НАРУЖУ. Вопрос идёт
# в род своего равенства: `inverting.обращения` кладёт его СРАЗУ ЗА ним.
РАЗРЯДНАЯ_ЛИНЕЙКА = "разрядная линейка: сотни и десятки, прибавленные и снятые"
СТОЛБИК = "столбик: сложение и вычитание трёхзначных, с переносом и без"
ДЕСЯТКИ = "десятки: умножение и деление, обратные друг другу"


def kinds_for_pass(pi):
    base = pi * 17
    shows = Сбор(РАЗРЯДНАЯ_ЛИНЕЙКА)
    # R: place rulers around the pass anchor
    for k in range(12):
        h = ((base + k * 7) % 9 + 1) * 100
        t = ((base + k * 5) % 9) * 10
        shows.append(f"{h} + {t} = {h + t}.")
        shows.append(
            f"{h + t} + 10 = {h + t + 10}."
        )
        shows.append(
            f"{h + t + 100} − 100 = {h + t}."
        )
    # A/S: column pairs without/with borrow mix
    shows.род = СТОЛБИК
    for k in range(14):
        a = 111 + ((base + k * 37) % 800)
        b = 101 + ((base + k * 23) % (a - 100))
        shows.append(f"{a} + {b} = {a + b}.")
        shows.append(f"{a + b} − {b} = {a}.")
    # M/D: tens
    shows.род = ДЕСЯТКИ
    for k in range(10):
        m = ((base + k * 3) % 9 + 1) * 10
        f = (base + k) % 8 + 2
        shows.append(f"{m} × {f} = {m * f}.")
        shows.append(f"{m * f} ÷ {f} = {m}.")
    return shows


def with_asks(pi):
    """Every glyph equality gets its question beside it.

    KNOWLEDGE WITHOUT A QUESTION SURFACE DOES NOT ANSWER — IT ONLY
    TELLS. The layer had 424 lines and zero questions; the owner made
    zero silent worlds a law. The question is the same line with the
    predicate lifted out («what is 950 − 100? 950 − 100 = 850.»), so
    the answer is judged by the same court as the statement; a
    corrupted answer is caught — checked before writing.
    """
    out = Сбор()
    for i, (show, род) in enumerate(kinds_for_pass(pi).парами):
        out.род = род
        out.append(show)
        out.extend(inverting.обращения(show, ("глиф",), i))
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

РОДЫ = (РАЗРЯДНАЯ_ЛИНЕЙКА, СТОЛБИК, ДЕСЯТКИ)

ЗАЧЕМ_РОДА = {
    РАЗРЯДНАЯ_ЛИНЕЙКА: "«300 + 40 = 340», «340 + 10 = 350», «440 − 100 = 340»: разряд "
                       "прибавляется и снимается на месте",
    СТОЛБИК: "трёхзначные складываются и вычитаются, и обратный ход показан рядом",
    ДЕСЯТКИ: "круглый десяток умножается и делится обратно тем же множителем",
}


def страницы(pi):
    return with_asks(pi)


def перебор_страниц(pi):
    return with_asks(pi).парами


def группы(pi):
    return [страницы(pi)]


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
    сбор = with_asks(0)
    assert len(сбор) == len(сбор.роды), "показ остался без рода"
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, with_asks)


if __name__ == "__main__":
    main()
