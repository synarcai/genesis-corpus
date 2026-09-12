#!/usr/bin/env python3
"""GENESIS layer: ОМОГРАФ — see tools/homoforms.py for the law.

ОБЕ СТОРОНЫ ЛОВУШКИ ИДУТ ОДНОЙ ГРУППОЙ: «знак в одно слово тонок» и «единоличное решает
спор». Показанное порознь, первое учит не верить письму вовсе, второе — верить одному слову.

    ЗНАК ЯЗЫКА ЕСТЬ СЧЁТ ОБЪЯВЛЕННЫХ СЛОВ, А НЕ НАХОДКА ОДНОГО.

СЧЁТ ПО ВСЕМУ СВОДУ стои́т отдельно: он есть ЗАМЕР, а не пример, и место ему своё. ВОПРОС
отдельно — ответ рядом с ним отнял бы у него цену.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import homoforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_homo.txt"
ГРУППЫ = (("одно письмо два языка", "четыре языка разом", "форма не есть смысл"),
          ("знак в одно слово тонок", "единоличное решает спор"),
          ("сколько их в своде",),
          ("спрошенное",))


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
