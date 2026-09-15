#!/usr/bin/env python3
"""GENESIS layer: NUMBER THEORY — primes, factorisation, congruence.

The syllabus court named three subjects absent from the whole corpus:
factorisation into primes, congruence modulo n, and the notion of a
prime itself. They are not decoration: unique factorisation is the
first structural theorem a mathematician meets, and congruence is the
first equivalence relation that is not equality.

EVERY LINE IS COMPUTED, NEVER WRITTEN. The divisor list, the
factorisation, the residue — all derived here and re-derived by
`courts/number_court.py`, which factorises again rather than trusting
the text. A layer that states a factorisation it did not compute
teaches the organism to trust a number nobody checked.

THREE SURFACES, TWO LANGUAGES: the glyph form («17 mod 5 = 2»), the
Russian sentence and the English sentence say ONE fact, and the court
judges all three by the same computation.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import numtheoryforms as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЦЕЛЬ ОБЪЯВЛЯЕТСЯ СТРОКОЙ, А НЕ ВПИСЫВАЕТСЯ В ВЫЗОВ: указатель родов ищет
# МИР ДОМА по этой самой строке и по ввозу кузницы. Путь, отданный литералом
# внутрь `emit_grouped`, оставляет дом БЕЗ МИРА, и указатель честно пишет None.
#
#     ВВОЗ ЕСТЬ СВЯЗЬ, НО НАЙТИ ЕЁ УКАЗАТЕЛЬ МОЖЕТ ЛИШЬ ТАМ, ГДЕ ОБЪЯВЛЕНА ЦЕЛЬ.
ЦЕЛЬ = "datasets/genesis_numbers.txt"

# ПЕРЕБОР ЖИВЁТ В ДОМЕ (13.09). Таблицы вопросов и формул, помощники и все семь строителей
# переехали в `tools/numtheoryforms.py` ЗАМЫКАНИЕМ ЦЕЛИКОМ.
#
#     ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ НА ПЕРВОЙ ЖЕ ПРАВКЕ.


def main():
    emit_grouped(ЦЕЛЬ, F.группы_страниц)


if __name__ == "__main__":
    main()
