#!/usr/bin/env python3
"""ДОМ ИТОГА-ПОДЛЕЖАЩЕГО И ВМЕСТИЛИЩА-ЕДИНИЦЫ (07.09).

ЗАКАЗ КУПЛЕН ПЕРЕПИСЬЮ. Атлас непрочитанных чисел базы p156 (томограф st48, omega-ad)
держит самый большой неразобранный класс — «other», 151 история, — и holon-f9 назвал в нём
две формы поимённо. Перепись по своду `a9e223c334a781cd` (380 610 строк) отвечает на обе:

    «there are a total of N X on the P»   — **0 страниц**. Оборот «a total of» в своде есть
        (16 строк), но ВЕЗДЕ он стои́т ОТВЕТОМ («how many eggs does carlos have? a total of
        32 eggs»), и НИ РАЗУ — подлежащим со сценой.
    «got a box of N X»                    — 8 страниц, и все восемь об ОДНОМ товаре
        (crayons), в одной рамке, у одного дома.

ДВА ЧТЕНИЯ, КОТОРЫХ СВОД НЕ ПОКАЗЫВАЛ:

    ИТОГ, СТОЯЩИЙ ПОДЛЕЖАЩИМ, ЕСТЬ ЧИСЛО ПРЕДМЕТОВ, А НЕ ОТВЕТ. «a total of 10 action
    figures» в голове предложения называет НАЛИЧНОЕ, и с ним дальше что-то делают; тот же
    оборот в хвосте называет ВЫЧИСЛЕННОЕ. Читатель, видевший его только ответом, на первом
    месте его не узнаёт: для него «a total of» есть слово итога, а не слово количества.

    ВМЕСТИЛИЩЕ ЕСТЬ ЕДИНИЦА СЧЁТА, И СЧИТАТЬ МОЖНО ЛИБО ЕГО, ЛИБО ТО, ЧТО В НЁМ. «a box of
    20 crayons and a box of 8 crayons» несёт ТРИ числа: двадцать, восемь и ДВА (коробки), —
    и какое из них спрошено, решает вопрос. Дом, писавший только «how many crayons»,
    показал одно чтение из двух.

ЧТО ПИШЕТ ЭТОТ ДОМ:

    ИТОГ-ПОДЛЕЖАЩЕЕ СО СЦЕНОЙ — прибыль и убыль: «a total of 10 figures are on the shelf.
        4 more figures are put on the shelf. how many figures are on the shelf now?»
    ДВА ВМЕСТИЛИЩА, ДВА РАЗНЫХ ТОВАРА — сумма по вещам: «a box of 457 erasers and a box of
        617 crayons», и вопрос о ВЕЩАХ («how many things»), где стык «and» стои́т между
        двумя числовыми фразами и леджер складывает пару — свидетель списка (М-710).
    ВОПРОС О ВМЕСТИЛИЩАХ, А НЕ О ВЕЩАХ — затвор против ответа по величине: «how many boxes
        did Ava get? 2 boxes». Читатель, берущий большее число, здесь лжёт.

Сцены и товары берутся у пакета `en`; вместилища — те же, что объявлены домом меры
(`measureof.СОСУДЫ`), и это НАРОЧНО: одно слово в двух домах и двух чтениях — мера
(«3 cups of sugar», число при сосуде) и вместилище («a box of 20 crayons», число при
вещах внутри) — есть то самое, что отделяет РОЛЬ МЕСТА от слова.

ЗАКОН ЧИСЛА: не менее LAW³ = 8 страниц на рамку, сцен не менее LAW² = 4, товаров не менее
LAW² = 4.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from layer import emit                                            # noqa: E402
from plural import by_count                                       # noqa: E402
import measureof as _мера                                         # noqa: E402

_ПАКЕТ = json.loads((pathlib.Path(__file__).resolve().parent / "langpacks" / "en.json")
                    .read_text(encoding="utf-8"))
_ИМЕНА_ПАКЕТА = set(_ПАКЕТ["person_names"])
_ПО_СТРОЧНОМУ = {и.lower(): и for и in _ИМЕНА_ПАКЕТА}
ИМЕНА = [_ПО_СТРОЧНОМУ[и] for и in
         ("ann", "ben", "carla", "dan", "elena", "felix", "grace", "hugo", "ava", "carlos")]
assert set(ИМЕНА) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"

# ВМЕСТИЛИЩА — ТЕ ЖЕ СЛОВА, ЧТО У ДОМА МЕРЫ, И ЭТО НАРОЧНО (см. описание).
ВМЕСТИЛИЩА = tuple(с for с in _мера.СОСУДЫ if с in ("box", "bag", "pack", "basket", "crate"))
МНОГО_В = {с: _ПАКЕТ["noun_forms"][с] for с in ВМЕСТИЛИЩА}

ТОВАРЫ = ("crayon", "eraser", "pencil", "card", "sticker", "marble", "button", "coin",
          "stamp", "seed", "ball", "book")
МНОГО_Т = {т: _ПАКЕТ["noun_forms"][т] for т in ТОВАРЫ if т in _ПАКЕТ["noun_forms"]}
ТОВАРЫ = tuple(т for т in ТОВАРЫ if т in МНОГО_Т)
assert len(ТОВАРЫ) >= 4, "товаров меньше LAW²: " + repr(ТОВАРЫ)

# СЦЕНА ИТОГА-ПОДЛЕЖАЩЕГО: место, на котором вещи ЛЕЖАТ, и его предлог — сказаны, а не
# выведены. «on the shelf», но «in the box»: предлог принадлежит месту.
СЦЕНЫ = (("shelf", "on the shelf"), ("table", "on the table"), ("desk", "on the desk"),
         ("box", "in the box"), ("basket", "in the basket"), ("drawer", "in the drawer"),
         ("tray", "on the tray"), ("shelf", "on the shelf"))


def показы(pi):
    основа = pi * 43
    вон = []
    for i in range(len(ТОВАРЫ) * len(СЦЕНЫ) * 4):
        товар = ТОВАРЫ[(основа + i) % len(ТОВАРЫ)]
        второй = ТОВАРЫ[(основа + i + 5) % len(ТОВАРЫ)]
        мн, мн2 = МНОГО_Т[товар], МНОГО_Т[второй]
        _место, где = СЦЕНЫ[(основа + i) % len(СЦЕНЫ)]
        имя = ИМЕНА[(основа + i) % len(ИМЕНА)]
        вмест = ВМЕСТИЛИЩА[(основа + i) % len(ВМЕСТИЛИЩА)]
        мн_в = МНОГО_В[вмест]
        n = (основа + i * 7) % 80 + 5           # 5..84
        m = (основа + i * 11) % 60 + 4          # 4..63
        рамка = ((основа + i) // len(ТОВАРЫ)) % 4
        if рамка == 0:
            # ИТОГ-ПОДЛЕЖАЩЕЕ СО СЦЕНОЙ, ПРИБЫЛЬ
            вон.append(
                f"a total of {n} {by_count(n, мн)} are {где}. "
                f"{m} more {by_count(m, мн)} are put {где}. "
                f"how many {мн} are {где} now? "
                f"{n + m} {by_count(n + m, мн)}: {n} + {m} = {n + m}.")
        elif рамка == 1:
            # ИТОГ-ПОДЛЕЖАЩЕЕ СО СЦЕНОЙ, УБЫЛЬ
            k = m if m < n else n - 1
            вон.append(
                f"a total of {n} {by_count(n, мн)} are {где}. "
                f"{имя} takes {k} {by_count(k, мн)} {'from' if где.startswith('in') else 'off'} the {где.split()[-1]}. "
                f"how many {мн} are {где} now? "
                f"{n - k} {by_count(n - k, мн)}: {n} − {k} = {n - k}.")
        elif рамка == 2:
            # ДВА ВМЕСТИЛИЩА, ДВА РАЗНЫХ ТОВАРА — вопрос о ВЕЩАХ (свидетель стыка «and»)
            вон.append(
                f"{имя} got a {вмест} of {n} {by_count(n, мн)} and "
                f"a {вмест} of {m} {by_count(m, мн2)}. "
                f"how many things did {имя} get? "
                f"{n + m} {by_count(n + m, 'things')}: {n} + {m} = {n + m}.")
        else:
            # ВОПРОС О ВМЕСТИЛИЩАХ, А НЕ О ВЕЩАХ — затвор против ответа по величине
            вон.append(
                f"{имя} got a {вмест} of {n} {by_count(n, мн)} and "
                f"a {вмест} of {m} {by_count(m, мн2)}. "
                f"how many {мн_в} did {имя} get? "
                f"2 {мн_в}.")
    return вон


def main():
    emit("datasets/genesis_totalsubj.txt", показы)


if __name__ == "__main__":
    main()
