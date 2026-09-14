#!/usr/bin/env python3
"""КУЗНИЦА МИРА ЦЕЛИ: страницы дома `goalturn` — цель, сказанная РЕЧЬЮ.

Просьба omega-ad (14.09): орган цели у организма есть, а речи о цели корпус не показывал ни
разу — цель подавалась командой «/goal wire angle = 30». Дом строит страницы, где цель
сказана словами девяти языков, и каждая несёт наблюдение числом, какое суд пересчитывает.

    ГРУППА — ЯЗЫК, КАК У ДОМА АКТА: шов мира кладётся между языками, а не между родами, ибо
    читатель учится ОДНОМУ языку за раз, а роду — на всех девяти сразу.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import goalturn as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_goal.txt"


def язык_группа(шаг, язык):
    свои = [с for с, (л, _р) in F.ПОКАЗЫ.items() if л == язык]
    return свои[шаг::len(PASSES)]


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
