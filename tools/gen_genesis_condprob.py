#!/usr/bin/env python3
"""КУЗНИЦА МИРА ДОЛИ И ЕЁ ОСНОВАНИЯ: страницы дома `condprob`.

Куплен НУЛЁМ 14.09: «условная вероятность» — 6 строк на 451 367, и все шесть поминают
слово. Что доля бывает ОТ ЧАСТИ и что основание решает всё, не сказано нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import condprob as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_condprob.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
