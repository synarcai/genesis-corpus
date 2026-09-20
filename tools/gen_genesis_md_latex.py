#!/usr/bin/env python3
"""GENESIS layer: MARKDOWN and LaTeX as NOTATION WITH MEANING.

The largest world of the corpus (≈5.7k lines) had NO generator: it was
produced once by a script that lived outside the repository and was
never committed. A world that cannot be re-derived cannot be checked
for reproducibility, cannot get its vocabulary read by a court, and
freezes every defect it happens to contain. `markup_court` even reads
`gen_genesis_md_latex.py` for the layer's vocabulary — a file that did
not exist, so the whole world stood unjudged at 56%.

EVERY MARKUP LINE CARRIES ITS DECLARATION. A heading `### поле.` is
emitted together with `заголовок уровня три: поле.`; a table row with
the sentence naming its columns and values; a fence with the sentence
naming what the block holds. Neither line depends on the other's
POSITION — the pass shuffle separates them on purpose — but the layer
as a whole always contains both, and the court checks BOTH directions:
markup without a declaration is drift, a declaration without markup is
a lie.

ALL ARITHMETIC IS TRUE AND ALL OF IT IS COMPUTED HERE, never written
by hand: sums, differences, powers, exact roots, exact fractions and
index sums. A layer that states a number it did not compute teaches
the organism to trust a number nobody checked.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import markupforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет
# МИР ДОМА по этой самой строке и по ввозу кузницы. Путь, отданный литералом
# внутрь `emit_grouped`, оставляет дом БЕЗ МИРА, и указатель честно пишет None.
#
#     ВВОЗ ЕСТЬ СВЯЗЬ, НО НАЙТИ ЕЁ УКАЗАТЕЛЬ МОЖЕТ ЛИШЬ ТАМ, ГДЕ ОБЪЯВЛЕНА ЦЕЛЬ.
ЦЕЛЬ = "datasets/genesis_md_latex.txt"

# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). Все девять строителей и сборка пар переехали в
# `tools/markupforms.py`: ПЕРЕЕЗД, ПОВТОРИВШИЙ ФУНКЦИЮ И НЕ ПОВТОРИВШИЙ СБОРКУ, ПЕРЕВЁЗ
# ПОЛОВИНУ ДЕЛА.


# ПРОХОД ОБЪЯВЛЕН ИМЕНЕМ ДОГОВОРА, А НЕ ПЕРЕДАН ВНУТРЬ ВЫЗОВА (16.09). Перепись копий
# (`scripts/copies_census.py`) выводит строчность мира, спрашивая у ПОРОЖДАЮЩЕГО его
# проходы — `pass_shows` либо `pass_groups`, — и, не найдя ни того ни другого, честно
# отвечала «НЕ ЗНАЮ». Перебор переехал в дом 13.09, а имя договора не переехало никуда:
# оно осталось литералом внутри одного вызова.
#
#     ФУНКЦИЯ, ПЕРЕДАННАЯ ДОВОДОМ, ДЕЛАЕТ ДЕЛО И НЕ ОТВЕЧАЕТ НА ВОПРОС. Договор читается
#     ПО ИМЕНИ, и переезд, сохранивший дело и потерявший имя, гасит не мир, а ЗНАНИЕ О НЁМ.
#
# Тот же шрам, что у паспортов корней и у прибора следа определений, — третий за два дня.
pass_groups = F.группы


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
