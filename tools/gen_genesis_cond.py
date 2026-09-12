#!/usr/bin/env python3
"""GENESIS layer: УСЛОВНАЯ ВЕРОЯТНОСТЬ — see tools/condforms.py for the law.

ДВЕ ОДЕЖДЫ ИДУТ РАЗНЫМИ ГРУППАМИ, И ЭТО НЕ РАЗЛУЧЕНИЕ, А ПОКАЗ САМОГО ЗАКОНА: ящик с
шарами и игральная кость говорят одно и то же, и читатель обязан встретить обе, чтобы
узнать закон, а не одежду.

    ЗАКОН, ПОКАЗАННЫЙ В ОДНОЙ ОДЕЖДЕ, ЕСТЬ ЗНАНИЕ ОБ ЭТОЙ ОДЕЖДЕ.

ОБЕ СТОРОНЫ ЛОВУШКИ — «знание сужает» и «знание не меняет» — одной группой: показанная
порознь, первая научила бы пересчитывать всегда. ВОПРОС отдельно.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import condforms as C  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_cond.txt"
ГРУППЫ = (("знание сужает", "знание не меняет"),
          ("обратное не то же", "доли складываются", "условие пустое"),
          ("кость сужает", "кость обратное"),
          ("спрошенное",))


def pass_groups(шаг):
    вон = []
    for язык in C.ЯЗЫКИ:
        for роды in ГРУППЫ:
            свои = [с for с, (л, р) in C.ПОКАЗЫ.items() if л == язык and р in роды]
            вон.append(свои[шаг::len(PASSES)])
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
