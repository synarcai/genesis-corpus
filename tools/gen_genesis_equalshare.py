#!/usr/bin/env python3
"""КУЗНИЦА МИРА РАВНОЙ ДОЛИ: страницы дома `equalshare` — деление БЕЗ носителя.

Просьба holon-f9 (14.09): семья «поровну» ключа нема целиком — восемнадцать строк из
восемнадцати. Во всём своде деление живёт при носителе и при товаре, а ключ спрашивает
голо: «раздели 14 на 2 поровну. что получится?» Мир даёт эту форму на девяти языках.

    ГРУППА — ЯЗЫК: шов мира кладётся между языками, как у домов акта и цели.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import equalshare as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_equalshare.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
