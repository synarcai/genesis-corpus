#!/usr/bin/env python3
"""КУЗНИЦА МИРА СКОБОК: страницы дома `dyckforms` — ряд, который надо закрыть.

Вторая ступень лестницы (BBH, род `dyck_languages`), просьба holon-f9 14.09. Отдельный мир,
а не род в чужом: рынкам нужны РАЗДЕЛЬНЫЕ ШВЫ, и шов между языками кладётся здесь.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import dyckforms as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dyck.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
