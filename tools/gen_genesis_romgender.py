#!/usr/bin/env python3
"""GENESIS layer: РОМАНСКИЙ РОД — see tools/romgenderforms.py for the law.

ГРУППЫ СЛОЖЕНЫ ПО ТОМУ, ЧТО ИМЕННО ОНИ ОТНИМАЮТ.

«Род сказан артиклем» и оба рода об окончании идут вместе: первое даёт ПРАВИЛО, вторые
отнимают вывод «значит, род читается по слову» — у части имён окончание молчит.

    ПРАВИЛО, ДАННОЕ БЕЗ СВОИХ ЛОЖНЫХ СЛЕДСТВИЙ, УЧИТ ИМ НАРАВНЕ С СОБОЮ.

«Роды языков не совпадают» и «сосед рода не имеет» — второй группой: обе о ГРАНИЦАХ. Первая
между четырьмя родственными языками, вторая — наружу, к языку без рода вовсе.

«Спрошено и отвечено» — третьей.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import romgenderforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_romgender.txt"
ГРУППЫ = (("род сказан артиклем", "окончание подсказывает", "окончание молчит"),
          ("роды языков не совпадают", "сосед рода не имеет"),
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
