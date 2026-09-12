#!/usr/bin/env python3
"""GENESIS layer: ПРЯМАЯ РЕЧЬ — see tools/directforms.py for the law.

ПРАВИЛО И ЕГО ИСКЛЮЧЕНИЕ ИДУТ ОДНОЙ ГРУППОЙ: «точка снята, на её место запятая» и «вопрос
остаётся, а запятой нет вовсе».

    ПРАВИЛО, СКАЗАННОЕ БЕЗ СВОЕГО ИСКЛЮЧЕНИЯ, ПРИМЕНЯЕТСЯ И ТАМ, ГДЕ ИСКЛЮЧЕНИЕ; А
    ИСКЛЮЧЕНИЕ БЕЗ ПРАВИЛА СТАНОВИТСЯ ПРАВИЛОМ.

ТРИ ПОЛОЖЕНИЯ СЛОВ АВТОРА — впереди, позади, внутри — одной группой: они суть одно правило,
взятое при трёх положениях. ПИСЬМО КАВЫЧЕК отдельно: это объявление свода, а не случай.
ВОПРОС отдельно.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import directforms as F  # noqa: E402
from layer import emit_grouped, PASSES  # noqa: E402

ЦЕЛЬ = "datasets/genesis_direct.txt"
ГРУППЫ = (("речь впереди", "знак вопроса остаётся"),
          ("автор впереди", "речь разорвана"),
          ("кавычки ёлочкой", "знак выводится"),
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
