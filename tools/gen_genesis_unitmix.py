#!/usr/bin/env python3
"""КУЗНИЦА МИРА НЕСВОДИМЫХ МЕР: страницы дома `unitmix`.

Куплен НУЛЁМ 14.09: «нельзя сложить» — 0 строк, «метры и килограммы» — 0. Мир смешанной
меры умеет перенос внутри ОДНОЙ меры; что бывают меры без переноса вовсе — не сказано нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import unitmix as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_unitmix.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
