#!/usr/bin/env python3
"""GENESIS layer: COUNTING, CHANCE AND THE MIDDLE OF A SET.

    the mean of 2 4 6 is 4.          среднее 2 4 6 равно 4.
    the median of 1 3 7 is 3.        размах 2 9 4 равен 7.
    choosing 2 from 5 gives 10 ways.
    arranging 4 items gives 24 orders.
    a die has 6 outcomes; an even number happens in 3 of them.
    two coins give 4 outcomes.

A scientist is made by two habits before any theory: counting the ways
a thing can happen, and asking where the middle of a set is. Both are
exactly checkable, and both are absent from a corpus that teaches only
arithmetic.

WHAT IS SHOWN AND WHY:
  · MEAN, only where the sum divides by the count — a mean of 3.5 would
    need a notation for halves this layer does not own, and rounding it
    would teach a rounding as a truth;
  · MEDIAN and RANGE, which need no division at all and therefore never
    lie;
  · CHOOSING (combinations) and ARRANGING (permutations) — the two ways
    a set gives rise to number, and the difference between them is the
    first thing a counter must not confuse;
  · CHANCE AS A COUNT OF OUTCOMES, never as a decimal: «an even number
    happens in 3 of 6» is a fact about counting; «the probability is
    0.5» is a fact about a notation this corpus has not yet earned.
"""

import math
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

# наборы, чья сумма делится на длину — среднее целое
# СРЕДНЕЕ НЕ ЕСТЬ СРЕДНИЙ ЧЛЕН (аудит покупок holon 03.09): на одних
# прогрессиях организм видел «ответ = второе число» и не мог отличить
# закон от совпадения; тройки с целым средним вне середины — рядом.
НАБОРЫ = [[2, 4, 6], [1, 3, 5], [4, 8], [2, 2, 8], [5, 7, 9],
          [10, 20, 30], [3, 9], [6, 6, 6], [1, 5, 9], [4, 4, 10],
          [2, 3, 7], [1, 4, 10], [3, 5, 10], [1, 2, 9], [2, 5, 5],
          [1, 1, 7], [3, 3, 12], [6, 1, 8],
          # ПАРЫ — МАССОЙ (holon 03.09: «mean of # #» шёл двумя строками,
          # ниже LAW 4, и рынок его не покупал).
          [2, 6], [5, 9], [1, 7], [3, 11], [4, 10], [6, 12], [7, 9], [2, 12]]
# наборы нечётной длины — медиана есть средний по порядку
НЕЧЁТНЫЕ = [[1, 3, 7], [5, 2, 9], [4, 4, 8], [10, 1, 6], [7, 3, 3],
            [2, 8, 5], [9, 9, 1], [6, 2, 4], [3, 7, 5], [8, 1, 2]]
ВЫБОР = [(5, 2), (6, 3), (4, 2), (7, 2), (6, 2), (5, 3), (8, 2), (7, 3)]
ПЕРЕСТАНОВКИ = [3, 4, 5, 3, 4, 6, 5, 4]
# (число исходов, число благоприятных, чему благоприятны)
ИСХОДЫ = [(6, 3, "an even number"), (6, 2, "a number above four"),
          (6, 1, "a six"), (2, 1, "heads"), (4, 1, "one chosen side"),
          (6, 4, "a number below five"), (8, 4, "an even number"),
          (10, 5, "an even number")]
МОНЕТЫ = [2, 3, 4, 2, 3, 4, 5, 3]


# ИСКОМОЕ ОБЪЯВЛЯЕТ СВОЙ ВОПРОС ОДИН РАЗ, и вопрос берёт ТУ ЖЕ фразу
# предмета, какую берёт ответ. Замер вопросной поверхности назвал этот
# мир немым: 600 строк, вопросов ноль.
СПРОСИТЬ = {
    "mean": "what is the mean of {предмет}?",
    "median": "what is the median of {предмет}?",
    "range": "what is the range of {предмет}?",
    "ways": "how many ways does choosing {предмет} give?",
    "orders": "how many orders does arranging {предмет} give?",
    "среднее": "чему равно среднее {предмет}?",
    "медиана": "чему равна медиана {предмет}?",
    "размах": "чему равен размах {предмет}?",
    "способы": "сколько способов даёт выбор {предмет}?",
    "порядки": "сколько порядков даёт расстановка {предмет}?",
}


def спросить(искомое, предмет, ответ):
    """Вопрос о предмете и ответ о нём же — одной строкой."""
    return f"{СПРОСИТЬ[искомое].format(предмет=предмет)} {ответ}"


# ЗАКОНЫ РОДОВ — ОТДЕЛЬНЫМИ СТРОКАМИ И ЗАКОНОМ РАССУЖДЕНИЯ (дом речи, 03.09):
# общее утверждение без чисел вопроса, живущее в мире своей строкой.
ЗАКОН_СРЕДНЕЕ = {"en": "the mean of a list is the sum of its numbers divided by their count.",
                 "ru": "среднее списка — это сумма его чисел, делённая на их количество."}
ЗАКОН_МЕДИАНА = {"en": "the median of a list of odd length is the middle number when the list is sorted.",
                 "ru": "медиана списка нечётной длины — это среднее по порядку число, когда список упорядочен."}
import discourse  # noqa: E402


def рассуждения(pass_i, i, набор, среднее, нечёт, медиана):
    """Среднее и медиана рассуждением: счёт-свидетель, связка, вывод той же
    формы, что утверждение мира, закон рода; «почему» — вторым зачином."""
    вон = []
    п = spaced(набор); s_ = sum(набор); n = len(набор)
    св_en = f"{' + '.join(str(x) for x in набор)} = {s_} and {s_} ÷ {n} = {среднее}"
    св_ru = f"{' + '.join(str(x) for x in набор)} = {s_} и {s_} ÷ {n} = {среднее}"
    выв_en, выв_ru = f"the mean of {п} is {среднее}", f"среднее {п} равно {среднее}"
    if (pass_i + i) % 2 == 0:
        вон.append(discourse.рассуждение_величины("en", f"what is the mean of {п}", св_en, выв_en, ЗАКОН_СРЕДНЕЕ["en"], k=pass_i + i))
        вон.append(discourse.рассуждение_величины("ru", f"чему равно среднее {п}", св_ru, выв_ru, ЗАКОН_СРЕДНЕЕ["ru"], k=pass_i + i))
    else:
        вон.append(discourse.почему("en", f"why is the mean of {п} equal to {среднее}", св_en, выв_en, ЗАКОН_СРЕДНЕЕ["en"], k=pass_i + i))
        вон.append(discourse.почему("ru", f"почему среднее {п} равно {среднее}", св_ru, выв_ru, ЗАКОН_СРЕДНЕЕ["ru"], k=pass_i + i))
    п2 = spaced(нечёт); упор = spaced(sorted(нечёт))
    св_en = f"sorted it is {упор} and the middle is {медиана}"
    св_ru = f"по порядку это {упор}, и середина — {медиана}"
    выв_en, выв_ru = f"the median of {п2} is {медиана}", f"медиана {п2} равна {медиана}"
    if (pass_i + i) % 2 == 1:
        вон.append(discourse.рассуждение_величины("en", f"what is the median of {п2}", св_en, выв_en, ЗАКОН_МЕДИАНА["en"], k=pass_i + i))
        вон.append(discourse.рассуждение_величины("ru", f"чему равна медиана {п2}", св_ru, выв_ru, ЗАКОН_МЕДИАНА["ru"], k=pass_i + i))
    else:
        вон.append(discourse.почему("en", f"why is the median of {п2} equal to {медиана}", св_en, выв_en, ЗАКОН_МЕДИАНА["en"], k=pass_i + i))
        вон.append(discourse.почему("ru", f"почему медиана {п2} равна {медиана}", св_ru, выв_ru, ЗАКОН_МЕДИАНА["ru"], k=pass_i + i))
    return вон


def spaced(xs):
    return " ".join(str(x) for x in xs)


def pass_shows(pass_i):
    out = []
    for i in range(8):
        набор = НАБОРЫ[(pass_i + i) % len(НАБОРЫ)]
        нечёт = НЕЧЁТНЫЕ[(pass_i * 3 + i) % len(НЕЧЁТНЫЕ)]
        n, k = ВЫБОР[(pass_i + i * 3) % len(ВЫБОР)]
        p = ПЕРЕСТАНОВКИ[(pass_i * 5 + i) % len(ПЕРЕСТАНОВКИ)]
        всего, благо, чему = ИСХОДЫ[(pass_i * 2 + i) % len(ИСХОДЫ)]
        монет = МОНЕТЫ[(pass_i + i) % len(МОНЕТЫ)]
        среднее = sum(набор) // len(набор)
        медиана = sorted(нечёт)[len(нечёт) // 2]
        размах = max(нечёт) - min(нечёт)
        сочетаний = math.comb(n, k)
        порядков = math.factorial(p)
        # --- середина набора
        for искомое_en, искомое_ru, ряд, значение, есть, равно in (
                ("mean", "среднее", набор, среднее, "the mean of",
                 "среднее"),
                ("median", "медиана", нечёт, медиана, "the median of",
                 "медиана"),
                ("range", "размах", нечёт, размах, "the range of",
                 "размах")):
            предмет = spaced(ряд)
            связка = {"mean": "is", "median": "is", "range": "is"}[искомое_en]
            хвост = {"среднее": "равно", "медиана": "равна",
                     "размах": "равен"}[искомое_ru]
            утв_en = f"{есть} {предмет} {связка} {значение}."
            утв_ru = f"{равно} {предмет} {хвост} {значение}."
            out.append(утв_en)
            out.append(утв_ru)
            out.append(спросить(искомое_en, предмет, утв_en))
            out.append(спросить(искомое_ru, предмет, утв_ru))
        out.extend(рассуждения(pass_i, i, набор, среднее, нечёт, медиана))
        if i == 0:
            out.extend([ЗАКОН_СРЕДНЕЕ["en"], ЗАКОН_СРЕДНЕЕ["ru"], ЗАКОН_МЕДИАНА["en"], ЗАКОН_МЕДИАНА["ru"],
                        f"what is the mean of a list? {ЗАКОН_СРЕДНЕЕ['en']}", f"что такое среднее списка? {ЗАКОН_СРЕДНЕЕ['ru']}",
                        f"what is the median of a list? {ЗАКОН_МЕДИАНА['en']}", f"что такое медиана списка? {ЗАКОН_МЕДИАНА['ru']}"])
        # ОТКАЗ С ОСНОВАНИЕМ: у набора чётной длины ЕДИНСТВЕННОЙ
        # середины нет. Мир пишет медиану только на нечётных наборах —
        # таков его закон, — и отказ называет основание числом:
        # сколько элементов и что это число чётно.
        чётный = spaced(list(нечёт) + [max(нечёт) + 1])
        сколько = len(нечёт) + 1
        out.append(f"what is the median of {чётный}? no single middle "
                   f"for {чётный}: the count {сколько} is even.")
        out.append(f"чему равна медиана {чётный}? единственной середины "
                   f"нет у {чётный}: элементов {сколько}, а это чётное "
                   f"число.")
        # --- счёт способов
        выб_en, выб_ru = f"{k} from {n}", f"{k} из {n}"
        утв_в_en = (f"choosing {выб_en} gives {сочетаний} "
                    f"{by_count(сочетаний, 'ways')}.")
        утв_в_ru = (f"выбор {выб_ru} даёт {сочетаний} "
                    f"{rugram.форма('способ', сочетаний)}.")
        out.append(утв_в_en)
        out.append(утв_в_ru)
        out.append(спросить("ways", выб_en, утв_в_en))
        out.append(спросить("способы", выб_ru, утв_в_ru))
        рас_en = f"{p} items"
        рас_ru = f"{p} {rugram.форма('предмет', p)}"
        утв_р_en = (f"arranging {рас_en} gives {порядков} "
                    f"{by_count(порядков, 'orders')}.")
        утв_р_ru = (f"расстановка {рас_ru} даёт "
                    f"{порядков} {rugram.форма('порядок', порядков)}.")
        out.append(утв_р_en)
        out.append(утв_р_ru)
        out.append(спросить("orders", рас_en, утв_р_en))
        out.append(спросить("порядки", рас_ru, утв_р_ru))
        out.append(f"choosing is not arranging: {k} from {n} gives "
                   f"{сочетаний}, arranging {k} of them gives "
                   f"{сочетаний * math.factorial(k)}.")
        # --- случай как счёт исходов
        out.append(f"a trial has {всего} outcomes; {чему} happens in "
                   f"{благо} of them.")
        out.append(f"испытание имеет {всего} "
                   f"{rugram.форма('исход', всего)}; благоприятных "
                   f"{благо}.")
        out.append(f"{монет} coins give {2 ** монет} outcomes.")
        out.append(f"{монет} {rugram.форма('монета', монет)} дают "
                   f"{2 ** монет} {rugram.форма('исход', 2 ** монет)}.")
    return out


def main():
    emit("datasets/genesis_statistics.txt", pass_shows)


if __name__ == "__main__":
    main()
