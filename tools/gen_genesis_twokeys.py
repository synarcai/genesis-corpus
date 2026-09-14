#!/usr/bin/env python3
"""КУЗНИЦА МИРА ДВУХ ПРИЗНАКОВ: страницы дома `twokeys`.

Куплен НУЛЁМ 14.09: «по двум признакам» — 0 строк. Корпус ставит в порядок числа, буквы
и даты, и всякий раз ключ ОДИН; что ключей бывает ДВА и второй ПОДЧИНЁН первому — нигде.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import twokeys as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_twokeys.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
