#!/usr/bin/env python3
"""GENESIS layer: ЗАМКНУТОСТЬ — see tools/closureforms.py for the law.

ДОКАЗАННОЕ И ОПРОВЕРГНУТОЕ ИДУТ РАЗНЫМИ ГРУППАМИ, и это не удобство раздачи, а сам
предмет дома: замкнутость доказывается разбором, а опровергается одним свидетелем, и
поставить их рядом значило бы внушить, что обе покупаются одинаково.

ЛОВУШКА И ВОПРОС — КАЖДЫЙ СВОЕЙ ГРУППОЙ: закон о несимметричности доказательства не
есть третий случай замкнутости, а речь О НЕЙ САМОЙ; вопрос же тем и ценен, что ответ
на него надо искать, и ответ рядом отнимает у него цену.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import closureforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_closure.txt"
ГРУППЫ = (("замкнуто",), ("не замкнуто",), ("один свидетель",), ("спрошенное",))


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
