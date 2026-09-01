#!/usr/bin/env python3
"""GENESIS layer: RUSSIAN VERB FRAMES — the missing link of ru-anaphora.

Asked by omega-e9 with the reason MEASURED, not guessed: the pronoun
market bought «he/she» on the English side (held 60/60, ref 0) and the
Russian side stayed outside it — «он/она» could not be bought because
the Russian VERBS of the story frames were never bought either. A form
is bought by MASS IN ITS FRAME, and the Russian frames had no mass.

SAME MASS AS THE ENGLISH `verbal` WORLD: ten verbs, four frames, five
passes. Same frames, so the two sides are comparable surface by surface
— that is what lets a market see them as one relation rather than two.

THREE AGREEMENTS AT ONCE, AND ALL THREE DECLARED, NOT DERIVED:
  · the ACCUSATIVE of the object («написала 1 книгу», not «1 книга») —
    the very defect omega-e9 found by eye in my speech layer;
  · the COUNT form of the noun (1 / 2-4 / 5+), read from the pack;
  · the GENDER of the past tense («вера написала», «пётр написал») —
    Russian marks the actor's gender in the verb itself, and no other
    language of the corpus does.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402

# (имя, родительный, местоимение, «у него/неё», род прошедшего)
ЛИЦА = (("вера", "веры", "она", "неё", "а"),
        ("анна", "анны", "она", "неё", "а"),
        ("мария", "марии", "она", "неё", "а"),
        ("пётр", "петра", "он", "него", ""),
        ("иван", "ивана", "он", "него", ""),
        ("юрий", "юрия", "он", "него", ""))

# (настоящее 3л., прошедшее БЕЗ родового окончания, ключ вещи)
ГЛАГОЛЫ = (("пишет", "написал", "книга"),
           ("читает", "прочитал", "страница"),
           ("продаёт", "продал", "книга"),
           ("берёт", "взял", "монета"),
           ("даёт", "дал", "ручка"),
           ("ест", "съел", "яблоко"),
           ("покупает", "купил", "карта"),
           ("делает", "сделал", "игрушка"),
           ("растит", "вырастил", "цветок"),
           ("пьёт", "выпил", "чашка"))

# ВИНИТЕЛЬНЫЙ ЕДИНСТВЕННОГО НАЗВАН, А НЕ ОТСЕЧЁН: женский род меняет
# окончание, средний и мужской неодушевлённый — нет.
ВИНИТЕЛЬНЫЙ = {"книга": "книгу", "страница": "страницу",
               "монета": "монету", "ручка": "ручку", "яблоко": "яблоко",
               "карта": "карту", "игрушка": "игрушку",
               "цветок": "цветок", "чашка": "чашку"}
# родительный множественного для вопроса «сколько ЧЕГО»
РОДИТЕЛЬНЫЙ = {к: rugram.форма(к, 5) for к in ВИНИТЕЛЬНЫЙ}


def _вещь(ключ, n):
    """Форма вещи при счёте, с винительным при единице."""
    return ВИНИТЕЛЬНЫЙ[ключ] if n == 1 else rugram.форма(ключ, n)


def настоящее(шаг):
    """Голый факт настоящего времени — та же рамка, что в `verbal`."""
    вон = []
    for i, (наст, _, вещь) in enumerate(ГЛАГОЛЫ):
        имя, _, _, _, _ = ЛИЦА[(i + шаг) % len(ЛИЦА)]
        n = 3 + (i + шаг) % 9
        вон.append(f"{имя} {наст} {n} {rugram.форма(вещь, n)}.")
    return вон


def прошедшее(шаг):
    """Прошедшее время с РОДОМ действующего лица."""
    вон = []
    for i, (_, прош, вещь) in enumerate(ГЛАГОЛЫ):
        имя, _, _, _, род = ЛИЦА[(i + шаг) % len(ЛИЦА)]
        n = 3 + (i + шаг) % 9
        вон.append(f"{имя} {прош}{род} {n} {rugram.форма(вещь, n)}.")
    return вон


def вопрос(шаг):
    """Вопрос, повторяющий факт: ответ обязан сойтись числом и вещью."""
    вон = []
    for i, (_, прош, вещь) in enumerate(ГЛАГОЛЫ):
        имя, _, _, _, род = ЛИЦА[(i + шаг) % len(ЛИЦА)]
        n = 3 + (i + шаг) % 9
        вон.append(f"{имя} {прош}{род} {n} {rugram.форма(вещь, n)}. "
                   f"сколько {РОДИТЕЛЬНЫЙ[вещь]} {прош}{род} {имя}? "
                   f"{имя} {прош}{род} {n} {rugram.форма(вещь, n)}.")
    return вон


def прибавка(шаг):
    """Прибыло и итог — рамка, на которой куплена английская анафора."""
    вон = []
    for i, (_, прош, вещь) in enumerate(ГЛАГОЛЫ):
        имя, _, _, _, род = ЛИЦА[(i + шаг) % len(ЛИЦА)]
        n = 3 + (i + шаг) % 7
        m = 1 + (i + шаг) % 3
        вон.append(f"{имя} {прош}{род} {n} {rugram.форма(вещь, n)}. "
                   f"{имя} {прош}{род} ещё {m} {_вещь(вещь, m)}. "
                   f"сколько {РОДИТЕЛЬНЫЙ[вещь]} {прош}{род} {имя} "
                   f"всего? {имя} {прош}{род} {n + m} "
                   f"{rugram.форма(вещь, n + m)}.")
    return вон


def анафора(шаг):
    """МЕСТОИМЕНИЕ ВМЕСТО ИМЕНИ — то, ради чего слой и кладётся."""
    вон = []
    for i, (_, прош, вещь) in enumerate(ГЛАГОЛЫ):
        имя, род_имени, он_она, него_неё, род = ЛИЦА[(i + шаг) % len(ЛИЦА)]
        было = 4 + (i + шаг) % 7
        ушло = 1 + (i + шаг) % 3
        стало = было - ушло
        вон.append(f"у {род_имени} было {было} "
                   f"{rugram.форма(вещь, было)}. "
                   f"{он_она} отдал{род} {ушло} {_вещь(вещь, ушло)}. "
                   f"у {него_неё} осталось {стало} "
                   f"{rugram.форма(вещь, стало)}.")
    return вон


ГРУППЫ = (настоящее, прошедшее, вопрос, прибавка, анафора)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_ruverbs.txt", pass_groups)


if __name__ == "__main__":
    main()
