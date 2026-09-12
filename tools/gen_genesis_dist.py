#!/usr/bin/env python3
"""GENESIS layer: ТРИ ЗАКОНА РАССТОЯНИЯ — see tools/distforms.py for the law.

ЗАКОН И ЕГО ЛОВУШКА ИДУТ ОДНОЙ ГРУППОЙ, и это не удобство раздачи, а сам предмет дома:
«через третью точку не короче» и «а когда точка НА пути — равно» суть правило и его
граница, и разлучить их значило бы отдать читателю правило без границы.

    ПРАВИЛО, РАЗЛУЧЁННОЕ СО СВОЕЙ ГРАНИЦЕЙ, БУДЕТ ПРИМЕНЕНО ТАМ, ГДЕ ГРАНИЦА МОЛЧИТ.

СИММЕТРИЯ И НОЛЬ идут своей группой: оба говорят о расстоянии ОДНОЙ пары точек, тогда как
третий закон требует трёх. ВОПРОС стои́т отдельно — ответ рядом с ним отнял бы у него цену.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import distforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_dist.txt"
ГРУППЫ = (("симметрия", "ноль до себя"),
          ("через третью", "через угол", "на пути"),
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
