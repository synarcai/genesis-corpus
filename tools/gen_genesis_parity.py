#!/usr/bin/env python3
"""КОВКА ДОМА ЧЁТНОСТИ ДЕЙСТВИЙ.

ТРИ СЛУЧАЯ СЛОЖЕНИЯ ИДУТ ОДНОЙ ГРУППОЙ, ибо закон о классах доказывается полнотой: чёт с чётом,
нечёт с нечётом, чёт с нечётом. Разлучить их значило бы оставить правило с неназванной дырой.

УМНОЖЕНИЕ идёт своей группой: там довольно ОДНОГО чётного множителя, где в сложении нужны оба, —
и порознь читатель перенёс бы закон сложения на умножение.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import parityforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_parity.txt"
ГРУППЫ = (("чёт и чёт", "нечёт и нечёт", "чёт и нечёт"), ("множитель",))


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
