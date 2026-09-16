#!/usr/bin/env python3
"""[ЗАКОН АРТИКЛЯ ПО ЗВУКУ] — согласие страницы с законом дома английского, пересчитанное судом.

ИМЯ ВЗЯТО НЕ ТО, ЧТО ПРОСИЛОСЬ: голос «АРТИКЛЬ ПО ЗВУКУ» носит прибор
`scripts/article_sound.py`, ЛОВЯЩИЙ «a hour» в своде. Этот суд сверяет страницу, которая
тот же закон ПОКАЗЫВАЕТ, — и два голоса под одним именем читались бы как один.

Суд не знает английского. Он берёт всякую пару «артикль + слово» в кавычках и спрашивает у
дома английского (`plural.article`), какой артикль полагается этому слову ПО ЗВУКУ. Списки
звуков объявлены там же, и суд не заводит своего.

    СУД, СВЕРЯЮЩИЙ ФОРМУ С ЗАКОНОМ ДОМА ЯЗЫКА, СИЛЁН РОВНО ТЕМ, ЧТО САМ ЯЗЫКА НЕ ЗНАЕТ.

КАВЫЧКИ СУТЬ ГРАНИЦА ПОКАЗЫВАЕМОГО. Страница говорит по-русски и по-английски О английском;
судится лишь то, что она показывает как ОБРАЗЕЦ, а не всякое английское слово в её прозе.

    python3 courts/soundarticle_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира лишь тому, кто ввёз Слой
import soundarticleforms  # noqa: E402 — дом, показывающий закон артикля по звуку

ИМЯ_СУДА = "soundarticle"
ЗАМКНУТЫЕ_МИРЫ = frozenset({"soundarticle"})


def _судить(строка):
    return soundarticleforms.судить(строка)


судить = closedworld.замкнуть(_судить, ЗАМКНУТЫЕ_МИРЫ)


def main():
    import genesis
    судимо = ложных = 0
    примеры = []
    for путь in genesis.worlds(kind="shows"):
        for строка in путь.read_text(encoding="utf-8", errors="replace").split("\n"):
            если, верно = судить(строка)[:2]
            if not если:
                continue
            судимо += 1
            if not верно:
                ложных += 1
                if len(примеры) < 5:
                    примеры.append(f"{путь.stem}: {строка.strip()[:90]}")
    for п in примеры:
        print(f"  {п}")
    поза = "PASS" if ложных == 0 else "FAIL"
    print(f"ЗАКОН АРТИКЛЯ ПО ЗВУКУ {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"родов объявлено {len(soundarticleforms.РОДЫ)}, "
          f"страниц {len(soundarticleforms.ПОКАЗЫ)}")
    return 0 if ложных == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
