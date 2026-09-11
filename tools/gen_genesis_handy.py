#!/usr/bin/env python3
"""КОВКА ДОМА УДОБНОГО СЧЁТА.

ХОД И ЕГО ОСНОВАНИЕ ИДУТ В ОДНОМ ПРОХОДЕ: «дополним 37 до 40 и вернём разницу» и
«перегруппировка законна, ибо скобка сумму не меняет» суть приём и закон, на котором он стои́т.
Порознь приём читался бы фокусом, а закон — украшением.

ДВА НАПРАВЛЕНИЯ ПОПРАВКИ идут своей группой: в сложении разницу ОТНИМАЮТ у второго слагаемого, в
вычитании лишнее ВОЗВРАЩАЮТ. Порознь каждая страница внушала бы, что поправка всегда одна и та же.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import handyforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_handy.txt"
ГРУППЫ = (("сложением", "закон"), ("вычитанием", "дополнение"))


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
