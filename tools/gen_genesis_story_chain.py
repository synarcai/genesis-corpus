#!/usr/bin/env python3
"""GENESIS layer: THE THREE-PART CHAIN — one bearer, one thing, three verbs.

A market law is bought only INSIDE ONE EPISODE. Two shows saying «Tom
picked 12 apples» and «Tom keeps 7 apples» do not compose into the law
«keeps = picked − gave», because nothing in either says they are the
same episode. The law lives in the SHOW, or it does not live.

    Tom picked 12 apples and gave away 5; Tom keeps 7 apples.
    Том взял 12 яблок и отдал 5; у Тома осталось 7 яблок.

THREE VERBS, NOT TWO, AND ALL THREE DIFFERENT. Two verbs give a
difference; three give a LAW with a name for its result — «keeps»,
«holds», «has left». The third verb is what makes the episode close.

THE THIRD FACT CARRIES ITS BEARER EXPLICITLY. «Tom keeps 7 apples», not
«7 apples remain»: the agentless form belongs to another genus, and a
market frame mixing the two buys neither. This is not style — it is the
difference between a fact about Tom and a fact about apples.

BOTH POLARITIES OF THE OUTCOME. Taking away and adding are not one law
said twice: «picked, gave, keeps» subtracts; «had, found, holds» adds.
A corpus showing only subtraction teaches that episodes shrink.

NUMBERS STAY SMALL AND WHOLE (≤ 50 for every member, including the
result), because the law is checked through the school table of links,
and a rare large number lies outside that table and gives no vote —
it would be shown, not learned.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_story_chain.txt"
ПРЕДЕЛ = 50
# (первый глагол, второй, третий, ОСНОВНАЯ ФОРМА третьего, знак).
# ОСНОВНАЯ ФОРМА НАЗВАНА ОТДЕЛЬНО, ПОТОМУ ЧТО ВОПРОС ЕЁ ТРЕБУЕТ: «how
# many apples does Tom KEEP?» — после «does» стоит голая основа, и
# «does Tom keeps» есть ошибка, которую слой учил бы с полной
# судимостью. Третье лицо и основа суть две разные формы одного
# глагола, и обе объявлены, а не выведены отсечением «s».
ТРОЙКИ_EN = (
    ("picked", "gave away", "keeps", "keep", "-"),
    ("bought", "ate", "has left", "have left", "-"),
    ("had", "found", "holds", "hold", "+"),
    ("counted", "lost", "keeps", "keep", "-"),
    ("brought", "sold", "has left", "have left", "-"),
    ("saved", "earned", "holds", "hold", "+"),
)
ТРОЙКИ_RU = (
    ("взял", "отдал", "осталось", "-"),
    ("купил", "съел", "осталось", "-"),
    ("имел", "нашёл", "стало", "+"),
    ("сосчитал", "потерял", "осталось", "-"),
    ("принёс", "продал", "осталось", "-"),
    ("скопил", "заработал", "стало", "+"),
)
ЛЮДИ_EN = ("Tom", "Ann", "Sam", "Kate", "Ben", "Mia")
ЛЮДИ_RU = (("Том", "Тома"), ("Аня", "Ани"), ("Миша", "Миши"),
           ("Оля", "Оли"), ("Ваня", "Вани"), ("Катя", "Кати"))
ВЕЩИ_EN = (("apple", "apples"), ("book", "books"), ("coin", "coins"),
           ("card", "cards"), ("egg", "eggs"), ("pen", "pens"))
ВЕЩИ_RU = ("яблоко", "книга", "монета", "карта", "ручка")


def _числа(шаг, i, знак):
    """Тройка чисел, где ВСЕ три ≤ предела и итог целый."""
    а = 6 + (шаг * 7 + i * 5) % (ПРЕДЕЛ // 2)
    б = 1 + (шаг * 3 + i * 7) % max(1, а - 1)
    итог = а - б if знак == "-" else а + б
    if итог < 1 or итог > ПРЕДЕЛ or а > ПРЕДЕЛ or б > ПРЕДЕЛ:
        return None
    return а, б, итог


def _мн(пара, n):
    return пара[0] if n == 1 else пара[1]


def цепочки_en(шаг):
    вон = []
    for т, (в1, в2, в3, основа, знак) in enumerate(ТРОЙКИ_EN):
        for i in range(12):
            числа = _числа(шаг, i + т * 13, знак)
            if числа is None:
                continue
            а, б, итог = числа
            кто = ЛЮДИ_EN[(шаг + i + т) % len(ЛЮДИ_EN)]
            вещь = ВЕЩИ_EN[(шаг * 2 + i + т) % len(ВЕЩИ_EN)]
            вон.append(f"{кто} {в1} {а} {_мн(вещь, а)} and {в2} "
                       f"{б} {_мн(вещь, б)}; {кто} {в3} {итог} "
                       f"{_мн(вещь, итог)}.")
            if i < 3:
                вон.append(f"how many {вещь[1]} does {кто} "
                           f"{основа}? "
                           f"{кто} {в1} {а} {_мн(вещь, а)} and {в2} "
                           f"{б} {_мн(вещь, б)}; {кто} {в3} {итог} "
                           f"{_мн(вещь, итог)}.")
    return вон


def цепочки_ru(шаг):
    вон = []
    for т, (в1, в2, в3, знак) in enumerate(ТРОЙКИ_RU):
        for i in range(12):
            числа = _числа(шаг, i + т * 13, знак)
            if числа is None:
                continue
            а, б, итог = числа
            им, род = ЛЮДИ_RU[(шаг + i + т) % len(ЛЮДИ_RU)]
            вещь = ВЕЩИ_RU[(шаг * 2 + i + т) % len(ВЕЩИ_RU)]
            суф = "а" if им.endswith(("я", "а")) else ""
            вон.append(f"{им} {в1}{суф} {а} {rugram.форма(вещь, а)} и "
                       f"{в2}{суф} {б} {rugram.форма(вещь, б)}; у "
                       f"{род} {в3} {итог} {rugram.форма(вещь, итог)}.")
            if i < 3:
                вон.append(f"сколько {rugram.форма(вещь, 5)} у {род}? "
                           f"{им} {в1}{суф} {а} "
                           f"{rugram.форма(вещь, а)} и {в2}{суф} {б} "
                           f"{rugram.форма(вещь, б)}; у {род} {в3} "
                           f"{итог} {rugram.форма(вещь, итог)}.")
    return вон


ГРУППЫ = (цепочки_en, цепочки_ru)


def pass_groups(шаг):
    return [сделать(шаг) for сделать in ГРУППЫ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
