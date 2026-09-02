#!/usr/bin/env python3
"""GENESIS layer: HOW A NUMBER IS WRITTEN.

    20% of 40 is 8.            20% от 40 — это 8.
    20% means 20 out of 100.   half is 50%.
    $12.48 is 12 dollars and 48 cents.
    3 dollars and 40 cents make 340 cents.
    three and a half plus three and a half is seven.
    7 - 2 = 5.                 8 / 2 = 4.

One number wears many clothes, and a corpus that shows only one of them
teaches the clothes instead of the number. Four notations live here,
each requested by holon's markets and each absent from the corpus
before:

  · PER CENT — a part of a hundred, shown as an operation with a
    checkable value and as a BRIDGE to its meaning («20% means 20 out
    of 100»), so the ratio is derivable and not merely asserted;
  · MONEY — the decimal point of a currency, bridged to cents, because
    the band's mute questions are full of «$12.48» and «$0.03»;
  · MIXED NUMBERS — «three and a half», shown only in the sums that
    stay whole, because a corpus with halves in its answers would need
    a notation for halves it does not yet have;
  · ASCII SIGNS — «-» and «/» live in the benchmark and lived nowhere
    in our layers, so an operator court could never buy them.

MONEY IS NEVER PUT AT THE END OF A SENTENCE. The decimal point inside
«$12.48» is a digit's neighbour, not a full stop, and a reader cutting
sentences on the dot would tear the sum in half. The rule costs a word
of care in the template and saves a whole genus from being unreadable.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import units
from layer import emit  # noqa: E402
from plural import by_count  # noqa: E402

# (процент, целое) — произведение кратно сотне, доля целая
ПРОЦЕНТЫ = [(20, 40), (20, 60), (50, 12), (50, 18), (25, 8), (25, 16),
            (10, 70), (10, 90), (75, 8), (75, 16), (40, 25), (40, 35),
            (5, 80), (5, 60), (60, 15), (60, 25)]
# (доллары, центы) — обе формы записи
ДЕНЬГИ = [(12, 48), (5, 0), (0, 3), (3, 40), (7, 25), (0, 99),
          (10, 5), (2, 50), (0, 7), (15, 75), (1, 1), (20, 0)]
# смешанные числа: только пары, дающие целое
ПОЛОВИНЫ = [1, 2, 3, 4, 5, 6, 7, 8]
СЛОВОМ = {1: ("one", "один"), 2: ("two", "два"), 3: ("three", "три"),
          4: ("four", "четыре"), 5: ("five", "пять"), 6: ("six", "шесть"),
          7: ("seven", "семь"), 8: ("eight", "восемь"),
          9: ("nine", "девять"), 10: ("ten", "десять"),
          11: ("eleven", "одиннадцать"), 12: ("twelve", "двенадцать"),
          13: ("thirteen", "тринадцать"), 14: ("fourteen", "четырнадцать"),
          15: ("fifteen", "пятнадцать"), 16: ("sixteen", "шестнадцать"),
          17: ("seventeen", "семнадцать")}
# (a, b) для знаков ASCII: разность и частное целые
МИНУС = [(7, 2), (9, 4), (12, 5), (15, 6), (11, 3), (20, 8)]
ДЕЛЕНИЕ = [(8, 2), (12, 3), (20, 4), (18, 6), (30, 5), (24, 8)]


def pass_shows(pass_i):
    out = []
    for i in range(8):
        p, whole = ПРОЦЕНТЫ[(pass_i * 3 + i) % len(ПРОЦЕНТЫ)]
        d, c = ДЕНЬГИ[(pass_i * 5 + i) % len(ДЕНЬГИ)]
        h = ПОЛОВИНЫ[(pass_i + i) % len(ПОЛОВИНЫ)]
        ma, mb = МИНУС[(pass_i + i) % len(МИНУС)]
        da, db = ДЕЛЕНИЕ[(pass_i * 2 + i) % len(ДЕЛЕНИЕ)]
        # --- проценты: действие и мост к смыслу
        часть = p * whole // 100
        out.append(f"{p}% of {whole} is {часть}.")
        out.append(f"{p}% от {whole} — это {часть}.")
        # ОДНА ФОРМА ОТВЕТА НА РАМКУ (holon 03.09: под «what is #% of #» жили
        # «it is 4» и «25% of 16 is 4», и организм отвечал голым числом):
        # ответ повторяет предмет, как в мире процентов.
        out.append(f"what is {p}% of {whole}? {p}% of {whole} is {часть}.")
        # ВОПРОС ЗАДАЁТСЯ НА ОБОИХ ЯЗЫКАХ, а не только на одном: русская
        # половина слоя знала утверждение и не знала вопроса.
        out.append(f"сколько будет {p}% от {whole}? это {часть}.")
        out.append(f"{p}% means {p} out of 100.")
        out.append(f"{p}% значит {p} из 100.")
        # --- деньги: мост записи к центам, НИКОГДА не в конце фразы
        if d and c:
            out.append(f"${d}.{c:02d} is {d} {by_count(d, 'dollars')} and "
                       f"{c} {by_count(c, 'cents')} in all.")
            out.append(f"${d}.{c:02d} makes {d * 100 + c} "
                       f"{by_count(d * 100 + c, 'cents')} in all.")
            out.append(f"{d} {by_count(d, 'dollars')} and {c} "
                       f"{by_count(c, 'cents')} make {d * 100 + c} "
                       f"{by_count(d * 100 + c, 'cents')} in all.")
            out.append(f"how many cents is ${d}.{c:02d}? it is "
                       f"{d * 100 + c} "
                       f"{by_count(d * 100 + c, 'cents')}.")
        elif c:
            out.append(f"$0.{c:02d} is {c} {by_count(c, 'cents')} in all.")
            out.append(f"how many cents is $0.{c:02d}? it is {c} "
                       f"{by_count(c, 'cents')}.")
        else:
            out.append(f"${d} is {d} {by_count(d, 'dollars')} in all.")
            out.append(f"${d} makes {d * 100} {by_count(d * 100, 'cents')} in all.")
        # --- РУССКИЕ ДЕНЬГИ: тот же род составной величины, что доллар
        # с центом. Формы рубля и копейки читаются из дома единиц —
        # там же, где объявлено и само отношение «в рубле 100 копеек».
        руб, коп = units.рус("rouble", d), units.рус("kopeck", c)
        всего = d * 100 + c
        коп_всего = units.рус("kopeck", всего)
        if d and c:
            out.append(f"{d} {руб} {c} {коп} — это {всего} {коп_всего}.")
            out.append(f"{d} {руб} и {c} {коп} вместе дают {всего} "
                       f"{коп_всего}.")
            out.append(f"сколько копеек в {d} {руб} {c} {коп}? "
                       f"это {всего} {коп_всего}.")
        elif c:
            out.append(f"{c} {коп} — это {c} {коп}.")
            out.append(f"сколько копеек в {c} {коп}? это {c} {коп}.")
        else:
            out.append(f"{d} {руб} — это {d * 100} "
                       f"{units.рус('kopeck', d * 100)}.")
            out.append(f"сколько копеек в {d} {руб}? это {d * 100} "
                       f"{units.рус('kopeck', d * 100)}.")
        # --- смешанные числа: только суммы, остающиеся целыми
        en, ru = СЛОВОМ[h]
        # СУММА ДВУХ ЧИСЕЛ «h с половиной» ЕСТЬ 2h + 1, а не 2h:
        # половины складываются в целое. Первая редакция писала
        # «дважды один с половиной — два», и это ложь, которую видно
        # глазом, но не видно ни одному прибору без своего суда.
        сумма_en, сумма_ru = СЛОВОМ[2 * h + 1]
        out.append(f"{en} and a half plus {en} and a half is {сумма_en}.")
        out.append(f"{ru} с половиной плюс {ru} с половиной — {сумма_ru}.")
        out.append(f"twice {en} and a half is {сумма_en}.")
        out.append(f"дважды {ru} с половиной — {сумма_ru}.")
        # --- знаки ASCII, которых в слоях не было ни одного
        out.append(f"{ma} - {mb} = {ma - mb}.")
        out.append(f"{da} / {db} = {da // db}.")
        out.append(f"{ma} * {mb} = {ma * mb}.")
    return out


def main():
    emit("datasets/genesis_notation.txt", pass_shows)


if __name__ == "__main__":
    main()
