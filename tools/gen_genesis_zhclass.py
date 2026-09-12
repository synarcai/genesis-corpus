#!/usr/bin/env python3
"""GENESIS layer: КИТАЙСКОЕ СЧЁТНОЕ СЛОВО — see tools/zhclassforms.py for the law.

ГРУППЫ СЛОЖЕНЫ ПО ТОМУ, ЧТО ИМЕННО ОНИ ОТНИМАЮТ.

«Счётное обязательно» и «счётное выбирает имя» идут вместе: первое говорит, что слово нужно,
второе — что выбирает его не говорящий.

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«Общее не значит любое» и «сосед обходится без счётного» — второй группой: одна о ГРАНИЦЕ
внутри языка (个 частое, но не всеобщее), другая о границе наружу.

«Спрошено и отвечено» — третьей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import zhclassforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_zhclass.txt"
ГРУППЫ = (("счётное обязательно", "счётное выбирает имя"),
          ("общее не значит любое", "сосед обходится без счётного"),
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
