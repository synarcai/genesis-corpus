#!/usr/bin/env python3
"""СИРОТА ПОЛУЧАЕТ ГЕНЕРАТОР: мир «ruler_dense» из семени с вопросной поверхностью.

Мир лежал в datasets/ без генератора и без единого вопроса; владелец
объявил ноль немых законом. Вчерашний файл стал СЕМЕНЕМ в tools/seeds/:
генератор переносит каждую его строку и к обратимым прикладывает вопрос
по ОБЪЯВЛЕННЫМ образцам дома обращения (tools/inverting.py). Ответ
судится тем же судом, что и утверждение; порча ловится — проверено
палатой до записи.
"""
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import inverting  # noqa: E402
from layer import PASSES, emit  # noqa: E402

СЕМЯ = КОРЕНЬ / "tools" / "seeds" / "school_ruler_dense.txt"
ВЫХОД = "datasets/school_ruler_dense.txt"
ОБРАЩЕНИЯ = ('equals', 'равно', 'глиф',)


def показы(шаг):
    строки = СЕМЯ.read_text(encoding="utf-8").splitlines()
    return inverting.с_вопросами(строки, ОБРАЩЕНИЯ, len(PASSES), шаг)


def main():
    if not СЕМЯ.exists():
        print(f"ОТКАЗ: семени {СЕМЯ.name} нет")
        return 2
    emit(ВЫХОД, показы)
    return 0


if __name__ == "__main__":
    sys.exit(main())
