#!/usr/bin/env python3
"""GENESIS layer: THE SURFACES OF AN ACT — one fact, many ways to say it.

The dialogue probe came back mute on «сложение 7 и 6 даёт», «the
addition of 9 and 8 gives» and «сорок два минус пять будет». The corpus
knew the arithmetic — it had said «7 + 6 = 13» and «7 plus 6 is 13»
thousands of times. What it had never said was the act NAMED AS A NOUN.

NOMINALISATION IS NOT DECORATION. It is how a language turns a doing
into a thing that can itself be talked about — the move from «add» to
«addition», from «сложить» to «сложение» — and it is the grammatical
engine of every scientific sentence ever written: «the DECOMPOSITION of
the field», «the CONVERGENCE of the series», «сходимость последовательности».
An organism that has only verbs can execute; an organism that has
nominalisations can REASON ABOUT executions. This is the cheapest
possible purchase of that power, and the corpus had none of it.

FOUR NAMES PER ACT, and they are not synonyms:
    ГЛАГОЛ         — the doing: «умножить на»
    НОМИНАЛИЗАЦИЯ  — the doing as a thing: «умножение»
    ИМЯ РЕЗУЛЬТАТА — the result as a thing: «произведение»
    УПРАВЛЕНИЕ     — which preposition each takes, and it DIFFERS:
                     «сложение A И B», «вычитание B ИЗ A»,
                     «умножение A НА B», «деление A НА B».
Government is the part a table of synonyms cannot carry and a language
model must have: it is where «вычитание 12 из 5» is not a small error
but the opposite claim.

RUSSIAN AGREEMENT COMES FREE AND IS JUDGED. «сумма … равнА» but
«произведение … равнО»: the copula agrees with the GENDER of the result
noun, which the pack declares. The court checks it, so the layer cannot
teach a wrong ending with full judgeability.

NUMBERS SPOKEN, NOT ONLY WRITTEN. «сорок два минус пять будет тридцать
семь» — the numerals come from `tools/numerals.py`, which names a number
by the pack's own declared table and reads it back to prove the name;
a number the language cannot name is not uttered at all.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import surfaceforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет
# МИР ДОМА по этой самой строке и по ввозу кузницы. Путь, отданный литералом
# внутрь `emit_grouped`, оставляет дом БЕЗ МИРА, и указатель честно пишет None.
#
#     ВВОЗ ЕСТЬ СВЯЗЬ, НО НАЙТИ ЕЁ УКАЗАТЕЛЬ МОЖЕТ ЛИШЬ ТАМ, ГДЕ ОБЪЯВЛЕНА ЦЕЛЬ.
ЦЕЛЬ = "datasets/genesis_surfaces.txt"

# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). Таблицы, пары и оба строителя переехали в
# `tools/surfaceforms.py` ЗАМЫКАНИЕМ ЦЕЛИКОМ.
#
#     ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ НА ПЕРВОЙ ЖЕ ПРАВКЕ.
ГРУППЫ = F.ГРУППЫ


def pass_groups(шаг):
    # МЕТКА ЯЗЫКА СНИМАЕТСЯ ЗДЕСЬ, А НЕ ТЕРЯЕТСЯ В ДОМЕ: строитель метит страницу языком с
    # 15.09, кузнице же нужен ряд строк, и порядок их — тот же, что был до разделения.
    return [[с for с, _я in сделать(шаг)] for сделать in ГРУППЫ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
