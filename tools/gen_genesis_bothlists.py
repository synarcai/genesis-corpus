#!/usr/bin/env python3
"""КУЗНИЦА МИРА ДВУХ СПИСКОВ: страницы дома `bothlists`.

Куплен НУЛЁМ 14.09: «круг в доказательстве» — 0 строк. Мир вывода называет две ФОРМАЛЬНЫЕ
ошибки; что основание бывает НЕГОДНЫМ, НЕ БУДУЧИ ЛОЖНЫМ, не сказано нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import bothlists as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_bothlists.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
