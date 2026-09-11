#!/usr/bin/env python3
"""КОВКА ДОМА ДЕЛЕНИЯ НА ДОЛЮ.

РОСТ И УБЫЛЬ ИДУТ В ОДНОМ ПРОХОДЕ: «3 ÷ 1/2» и «6/7 ÷ 3» суть минимальная пара по направлению,
и разница между ними — в одном месте: делят ли на ДОЛЮ или на ЧИСЛО. Порознь первое внушало бы,
что деление всегда увеличивает, а второе — что всегда уменьшает.

ВОПРОС И ЕГО ПРОВЕРКА идут своей группой: «сколько половин в трёх» и обратный ход, которым это
проверяется. Утверждение о росте, разлучённое со своей проверкой, читателю нечем поверить.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import divshareforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_divshare.txt"
ГРУППЫ = (("целое на долю", "проверка"), ("доля на долю", "доля на число"))


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
