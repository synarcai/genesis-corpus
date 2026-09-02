#!/usr/bin/env python3
"""GENESIS layer: QUANTITIES, UNITS, FRACTIONS (М-4 of
the GSM8K collegium).

What GSM8K needs and the corpus lacks: unit conversions
as facts plus applied mass, fractions ("half of"),
division with remainder, money-rate shows. School shape
laws: bare shows, three surfaces (glyph / RU / EN),
deterministic coprime shuffles, form-feed seams.
"""

import units
from layer import emit_grouped


# ПОРЯДОК СВОЙ, ОТНОШЕНИЯ ОБЩИЕ. Здесь жила ВТОРАЯ
# таблица переводов (два факта повторяли соседний
# слой) и ТРЕТЬЯ копия русского согласования — та
# самая, от которой сосед прямо предостерегал в
# своей же шапке. Слой называет, ЧТО показывает и
# КАКИМ письмом; отношения и формы читаются из
# `tools/units.py`. Русские падежные формы нужны
# по-прежнему: организм живёт точными формами, и
# бесподежный показ не отвечает прожитому вопросу
# («2 часа равно», не «2 час равно»).
ПОРЯДОК = ("hour", "minute", "metre", "kilometre",
           "kilogram", "week", "dozen")
ПИСЬМО = "amer"
# Родительный множественного части → её тройка форм. Ключ есть та самая
# форма, какой слой звал часть прежде: перевод не выводится, он назван.
ЧАСТИ = {
    "минут": ("минута", "минуты", "минут"),
    "секунд": ("секунда", "секунды", "секунд"),
    "сантиметров": ("сантиметр", "сантиметра", "сантиметров"),
    "метров": ("метр", "метра", "метров"),
    "граммов": ("грамм", "грамма", "граммов"),
    "дней": ("день", "дня", "дней"),
    "штук": ("штука", "штуки", "штук"),
}


# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 1030 строк, вопросов ноль.
СПРОСИТЬ = {
    "equal": "how many {мелкие} do {предмет} equal?",
    "равно": "чему равно {предмет}?",
}

# ФОРМУЛЫ РОДОВ — ЗАКОН ОТВЕТА ОТ ВЕЛИЧИН ВОПРОСА, объявлен при каждом вопросе
# (таблица родов declarations/GENERA.json — эталон суда охвата, holon 03.09).
ФОРМУЛЫ = {
    "equal": "мелких = крупных × отношение (граф единиц)",
    "равно": "мелких = крупных × отношение (граф единиц)",
}
assert set(ФОРМУЛЫ) == set(СПРОСИТЬ), "формула у каждого вопроса"


def спросить(искомое, ответ, **части):
    """Вопрос и ответ одной строкой; величины у них одни и те же."""
    return f"{СПРОСИТЬ[искомое].format(**части)} {ответ}"


def несоизмеримые():
    """Пара единиц РАЗНЫХ родов — отношения между ними нет.

    Отношение ПРОХОДИТСЯ по объявленному графу единиц, и его отсутствие
    есть такой же факт дома, как его наличие: час не переводится в
    метры не потому, что мы не сочли, а потому, что это меры разных
    родов. Пара выбирается перебором объявленных, а не пишется рукой.
    """
    имена = sorted(units.ФОРМЫ_ВСЕХ)
    for a in имена:
        for b in имена:
            if a != b and units.отношение(a, b) is None:
                return a, b
    return None


def conversions():
    """(формы ру, ед. англ, мн. англ, ру мн. части,
    англ мн. части, во сколько раз)."""
    for имя in ПОРЯДОК:
        часть = next(б for (а, б) in units.РЁБРА
                     if а == имя)
        yield (units.ФОРМЫ_ВСЕХ[имя][1],
               units.англ(имя, False, ПИСЬМО),
               units.англ(имя, True, ПИСЬМО),
               units.рус(часть, 5),
               units.англ(часть, True, ПИСЬМО),
               int(units.отношение(имя, часть)))


RU_NUM = ["ноль", "один", "два", "три", "четыре",
          "пять", "шесть", "семь", "восемь",
          "девять", "десять"]
EN_NUM = ["zero", "one", "two", "three", "four",
          "five", "six", "seven", "eight", "nine",
          "ten"]


def conversion_shows():
    out = []
    for (ruf, en, enp, rus, ens, f) in conversions():
        # ЧАСТЬ СОГЛАСУЕТСЯ СО СВОИМ ЧИСЛОМ, а не берётся одной
        # формой на все счёты: «3 недели равно 21 дней» стояло в
        # корпусе непойманным, ибо суд согласования знал лишь латиницу.
        части = ЧАСТИ[rus]
        out.append(
            f"один {ruf[0]} равно {f} {units.ру_форма(части, f)}."
        )
        out.append(f"one {en} equals {f} {ens}.")
        for k in (2, 3, 5):
            # ЗВЕНО ЦЕПИ (compose, e9): отношение единиц — число леджера
            # («one hour equals 60 minutes» стоит рядом), k × f — звено.
            утв_ru = (f"{k} {units.ру_форма(ruf, k)} равно "
                      f"{k * f} {units.ру_форма(части, k * f)}: {k} × {f} = {k * f}.")
            утв_en = f"{k} {enp} equal {k * f} {ens}: {k} × {f} = {k * f}."
            out.append(утв_ru)
            out.append(утв_en)
            out.append(спросить("равно", утв_ru,
                                предмет=f"{k} {units.ру_форма(ruf, k)}"))
            out.append(спросить("equal", утв_en, мелкие=ens,
                                предмет=f"{k} {enp}"))
    # ОТКАЗ С ОСНОВАНИЕМ: меры разных родов друг в друга не переводятся,
    # и это факт ОБЪЯВЛЕННОГО ГРАФА, а не наша неспособность счесть.
    пара = несоизмеримые()
    if пара is not None:
        a, b = пара
        for k in (2, 3, 5):
            # ОТВЕТ ПОВТОРЯЕТ ВЕЛИЧИНУ ВОПРОСА, И ЭТО НЕ УКРАШЕНИЕ:
            # связь половин пары держится числами (общий дом
            # `tools/asking.py`), и отказ без числа не связать с
            # вопросом ничем. Число стои́т в именительном при своей
            # счётной форме, а не после предлога.
            # ИМЯ ЕДИНИЦЫ СТОИТ В ЕДИНСТВЕННОМ КАК ТЕРМИН, А СЧЁТ —
            # при своей счётной форме: счётная тройка даёт родительный
            # множественного («сантиграммов»), а рядом с «и» нужен
            # именительный, и мир учил бы неверной форме.
            out.append(f"how many {units.англ(b, True)} are in {k} "
                       f"{units.англ(a, True)}? no answer: {k} "
                       f"{units.англ(a, True)}, and a "
                       f"{units.англ(a)} and a {units.англ(b)} "
                       f"measure different kinds.")
            out.append(f"сколько {units.рус(b, 5)} в {k} "
                       f"{units.рус(a, k)}? ответа нет: {k} "
                       f"{units.рус(a, k)}, а {units.рус(a, 1)} и "
                       f"{units.рус(b, 1)} — меры разных родов.")
    return out


def fraction_shows():
    out = []
    for n in range(2, 11):
        d = 2 * n
        out.append(
            f"половина от {d} равно {n}."
        )
        out.append(f"half of {d} equals {n}.")
        out.append(f"{d} ÷ 2 = {n}.")
    for n in range(1, 7):
        d = 3 * n
        out.append(f"треть от {d} равно {n}.")
        out.append(
            f"a third of {d} equals {n}."
        )
        out.append(f"{d} ÷ 3 = {n}.")
    for n in range(1, 6):
        d = 4 * n
        out.append(
            f"четверть от {d} равно {n}."
        )
        out.append(
            f"a quarter of {d} equals {n}."
        )
        out.append(f"{d} ÷ 4 = {n}.")
    return out


def remainder_shows():
    out = []
    for a in range(5, 20):
        for b in (2, 3, 4):
            q, r = divmod(a, b)
            if r == 0:
                continue
            out.append(
                f"{a} делить {b} равно {q} "
                f"остаток {r}."
            )
            out.append(
                f"{a} divided by {b} equals {q} "
                f"remainder {r}."
            )
    return out


def rate_shows():
    out = []
    # ФОРМЫ РУБЛЯ ЧИТАЮТСЯ ИЗ ДОМА ЕДИНИЦ, а не пишутся здесь
    # вторым списком: рубль объявлен там вместе с копейкой.
    rub = units.ФОРМЫ_ВСЕХ["rouble"][1]
    for k in range(2, 7):
        for p in (2, 3, 5):
            out.append(
                f"{k} по {p} {units.ру_форма(rub, p)} "
                f"равно {k * p} "
                f"{units.ру_форма(rub, k * p)}."
            )
            out.append(
                f"{k} items at {p} dollars "
                f"equal {k * p} dollars."
            )
    return out


def main():
    kinds = [
        conversion_shows(), fraction_shows(),
        remainder_shows(), rate_shows(),
    ]
    emit_grouped("datasets/genesis_units.txt", lambda _pi: kinds)


if __name__ == "__main__":
    main()
