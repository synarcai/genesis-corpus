#!/usr/bin/env python3
"""GENESIS layer: VERBAL EQUALITY AND PAST TENSE — two tails asked by e9.

Requested by omega-e9 from the band side, with the reason measured, not
guessed:

  · «IS» AS THE COPULA OF EQUALITY. The school layer's bought equality
    family is equals / = / равно; «is» was never bought because the
    corpus almost never shows it in that role. «5 plus 3 is 8» is the
    same statement as «5 plus 3 equals 8», and the organism cannot know
    that until both are shown of the SAME facts;
  · THE PAST TENSE IN THE MARKET'S OWN FRAME. Only «writes» was bought;
    «wrote» had sixty lines and did not carry. A form is bought by
    MASS IN ITS FRAME, not by existing somewhere.

BOTH SURFACES OF ONE FACT STAND SIDE BY SIDE. That is the corpus's own
law of bridges: two writings of a single fact, judged by one count, are
what let a market learn that they are one.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from layer import emit_grouped  # noqa: E402
from plural import singular  # noqa: E402

ДЕЙСТВИЯ = (("plus", "+", lambda a, b: a + b),
            ("minus", "-", lambda a, b: a - b),
            ("times", "×", lambda a, b: a * b))

# (настоящее, прошедшее, вещь) — прошедшее объявлено, а не выведено:
# «wrote» из «write» правилом не получить.
ГЛАГОЛЫ = (("writes", "wrote", "novels"), ("bakes", "baked", "cakes"),
           ("sells", "sold", "books"), ("takes", "took", "coins"),
           ("gives", "gave", "pens"), ("reads", "read", "pages"),
           ("grows", "grew", "flowers"), ("eats", "ate", "apples"),
           ("buys", "bought", "cards"), ("makes", "made", "toys"))
ЛИЦА = ("regina", "vera", "peter", "anna", "ivan", "sara",
        "tom", "wanda", "carlos", "lena")


def равенство_словом(шаг):
    """Одно равенство двумя связками: «is» рядом с «equals»."""
    вон = []
    for i in range(24):
        имя, глиф, действие = ДЕЙСТВИЯ[(i + шаг) % 3]
        a = 2 + (i + шаг) % 12
        b = 1 + (i * 2 + шаг) % 9
        if имя == "minus" and b > a:
            a, b = b, a
        итог = действие(a, b)
        вон.append(f"{a} {имя} {b} is {итог}.")
        вон.append(f"{a} {имя} {b} equals {итог}.")
        вон.append(f"{a} {глиф} {b} = {итог}.")
    return вон


def прошедшее(шаг):
    """Прошедшее время в той же рамке, что и настоящее."""
    вон = []
    for i, (наст, прош, вещь) in enumerate(ГЛАГОЛЫ):
        кто = ЛИЦА[(i + шаг) % len(ЛИЦА)]
        n = 3 + (i + шаг) % 9
        вон.append(f"{кто} {наст} {n} {вещь}.")
        вон.append(f"{кто} {прош} {n} {вещь}.")
        вон.append(f"{кто} {прош} {n} {вещь}. how many {вещь} "
                   f"did {кто} {наст.rstrip('s')}? {кто} {прош} "
                   f"{n} {вещь}.")
        m = 1 + (i + шаг) % 4
        # ФОРМА ИДЁТ ЗА ЧИСЛОМ И ЗДЕСЬ: «1 novels more» ложно о языке
        # при верном счёте — тот самый род, что слой речи и учит.
        одна = singular(вещь) if m == 1 else вещь
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166):
        # прочие формы этого мира ПРОЧИТЫВАЮТ число вопроса и выводить в них
        # нечего, а эта — единственная — его ВЫЧИСЛЯЕТ, и шага не было.
        кузн = f": {n} + {m} = {n + m}" if (i + шаг) % 2 == 0 else ""
        вон.append(f"{кто} {прош} {n} {вещь}. {кто} {прош} {m} {одна} "
                   f"more. how many {вещь} did {кто} "
                   f"{наст.rstrip('s')} in all? {кто} {прош} "
                   f"{n + m} {вещь}{кузн}.")
    return вон


ГРУППЫ = (равенство_словом, прошедшее)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_verbal.txt", pass_groups)


if __name__ == "__main__":
    main()
