#!/usr/bin/env python3
"""КОВКА ДОМА ВЫБОРА ДЕЙСТВИЯ.

ПАРА ИДЁТ В ОДНОМ ПРОХОДЕ, А НЕ ВРАЗБИВКУ. Довод здешнего дома есть МИНИМАЛЬНАЯ ПАРА: две
страницы с одними числами, разнящиеся решающим словом. Читатель, увидевший их порознь, увидит
два примера; увидевший рядом — увидит ЗАКОН. Оттого группы прохода режутся по РОДАМ развилки,
и обе половины пары попадают в один блок.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import opchoiceforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_opchoice.txt"


def pass_groups(шаг):
    вон = []
    for язык in F.ЯЗЫКИ:
        for первый, второй in F.ПАРЫ:
            свои = [с for с, (л, р) in F.ПОКАЗЫ.items()
                    if л == язык and р in (первый, второй)]
            вон.append(свои[шаг::len(PASSES)])
    return вон


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
