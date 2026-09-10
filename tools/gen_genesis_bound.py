#!/usr/bin/env python3
"""КОВКА ДОМА ГРАНИЦЫ ВЕЛИЧИНЫ.

ВОЗМОЖНОЕ И ГРАНИЦА ИДУТ В ОДНОМ ПРОХОДЕ: «взять 5 из 12 можно» и «взять 12 из 12 можно» суть
один закон на разных числах, и второе порознь читалось бы особым правилом о равенстве, которого
нет. ОТКАЗ И ЕГО ПРИЧИНА идут своей группой: «нельзя, ибо 15 больше 12» и «в числах −3, но
орехов не бывает −3» суть один и тот же отказ, сказанный с двух сторон, и рядом друг с другом
они читаются законом, а не двумя случаями.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import boundforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_bound.txt"
ГРУППЫ = (("можно", "ровно всё"), ("нельзя", "число", "проверка"))


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
