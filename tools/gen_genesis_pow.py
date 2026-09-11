#!/usr/bin/env python3
"""КОВКА ДОМА СТЕПЕНИ ЗА НУЛЁМ.

ЛЕСТНИЦА И ЕЁ ПЕРВАЯ СТУПЕНЬ ЗА НУЛЁМ идут в одном проходе: «5^3 = 125, и 125 ÷ 5 = 25» и
«5^0 = 1, а не 0» суть причина и следствие, и разлучить их значило бы оставить ловушку без
вывода.

ДОЛЯ И ЕЁ ОПРАВДАНИЕ идут своей группой: «2^-3 = 1/8, а не −8» и «2^3 × 2^-3 = 8 × 1/8 = 1» —
вторая страница проверяет первую произведением, и порознь доля осталась бы объявлением.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import powforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_pow.txt"
ГРУППЫ = (("лестница", "нулевая"), ("отрицательная", "замок"))


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
