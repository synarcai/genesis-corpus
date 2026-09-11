#!/usr/bin/env python3
"""КОВКА ДОМА ПРОПОРЦИИ.

ВОПРОС И ЕГО ДВОЙНИК ИДУТ В ОДНОМ ПРОХОДЕ: «оба отношения равны 2» и «отношение сохранилось, а
разность нет» суть два вопроса об одной паре — во сколько раз и на сколько. Порознь первый
внушал бы, что пропорция сохраняет всякую связь между числами.

ОРАКУЛ И ОРУДИЕ идут своей группой: произведения крест-накрест ПРОВЕРЯЮТ пропорцию, и они же
НАХОДЯТ неизвестный член. Одно правило, взятое в две стороны.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import propforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_prop.txt"
ГРУППЫ = (("отношения", "разность"), ("крест-накрест", "неизвестный"))


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
