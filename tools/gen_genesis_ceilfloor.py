#!/usr/bin/env python3
"""КОВКА ДОМА ДВУХ ОТВЕТОВ ОДНОГО ДЕЛЕНИЯ.

ВОПРОС И ЕГО БЛИЗНЕЦ ИДУТ В ОДНОМ ПРОХОДЕ: «сколько нужно» и «сколько наполнится» суть
минимальная пара ПО ВОПРОСУ — то же деление, те же числа, и разница в одном месте: о чём спросили.
Порознь читатель взял бы первый попавшийся ответ за единственный.

ЗАКОН И ЕГО ИСКЛЮЧЕНИЕ ИДУТ СВОЕЙ ГРУППОЙ: страница «два ответа» говорит, что ответы расходятся
на единицу, страница «без остатка» — что при остатке 0 они сходятся. Порознь первая стала бы
новым суеверием.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import ceilfloorforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_ceilfloor.txt"
ГРУППЫ = (("вверх", "вниз"), ("два ответа", "без остатка"))


def pass_groups(шаг):
    вон = []
    for язык in F.ЯЗЫКИ:
        for роды in ГРУППЫ:
            свои = [с for с, (л, р) in F.ПОКАЗЫ.items() if л == язык and р in роды]
            вон.append(свои[шаг::len(PASSES)])
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
