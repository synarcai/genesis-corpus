#!/usr/bin/env python3
"""GENESIS layer: НЕМЕЦКОЕ МНОЖЕСТВЕННОЕ — see tools/deplurforms.py for the law.

«Шесть способов» и «брат рода» идут вместе: первое показывает, что способов много, второе
называет вывод — способ заучивается со словом, как и род.

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«По слову не угадать» и «по роду не угадать» — второй группой: обе отнимают догадку, и обе
нужны, ибо читатель, лишённый первой, хватается за вторую.

«Слово без перемены» стои́т ОСОБО: это край закона — случай, где множественное не слышно вовсе
и число несёт артикль.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import deplurforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_deplur.txt"
ГРУППЫ = (("шесть способов", "брат рода"),
          ("по слову не угадать", "по роду не угадать"),
          ("слово без перемены",))


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
