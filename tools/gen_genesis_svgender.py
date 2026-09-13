#!/usr/bin/env python3
"""GENESIS layer: ШВЕДСКИЙ РОД — see tools/svgenderforms.py for the law.

ГРУППЫ СЛОЖЕНЫ ПО ТОМУ, ЧТО ИМЕННО ОНИ ОТНИМАЮТ.

«Род сказан артиклем» и «родов два, а не один» идут вместе: первое говорит, ГДЕ род, второе
отнимает вывод «значит, „ett“ есть описка».

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«Род правит прилагательным» и «сосед делит иначе» — второй группой: обе о том, что род не
кончается артиклем. Первая внутрь языка, вторая наружу.

«Спрошено и отвечено» — третьей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import svgenderforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_svgender.txt"
ГРУППЫ = (("род сказан артиклем", "родов два, а не один"),
          ("род правит прилагательным", "прилагательное спрошено", "сосед делит иначе"),
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
