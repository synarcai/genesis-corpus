#!/usr/bin/env python3
"""GENESIS layer: КОРЕЙСКАЯ ЧАСТИЦА — see tools/koparticleforms.py for the law.

ГРУППЫ СЛОЖЕНЫ ПО ТОМУ, ЧТО ИМЕННО ОНИ ОТНИМАЮТ.

«Три пары, а не шесть частиц» и «решает последний звук» идут вместе: первое говорит, что
формы парны, второе — что выбирает между ними.

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«Выбор не о смысле» и «сосед опирается на иное» — второй группой: обе отнимают ложную опору,
одна изнутри (смысл не решает), другая снаружи (турецкий опирается на гласную основы).

«Спрошено и отвечено» — третьей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import koparticleforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_koparticle.txt"
ГРУППЫ = (("три пары, а не шесть частиц", "решает последний звук"),
          ("выбор не о смысле", "сосед опирается на иное"),
          ("спрошено и отвечено",))


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
