#!/usr/bin/env python3
"""[ЖИВАЯ ЗАДАЧА] — условие живой задачи и её выкладка суть задача источника и её программа; ПЕРЕСЧИТАНО.

Строка мира `livemath` (tools/livemath.py) есть задача обучающей части GSM8K либо её вариант,
хранящий строй, с ответом и выкладкой. Суд читает строку НАЗАД тем же законом, каким дом её
пишет (tools/livemath_law.py): условие обязано быть условием задачи источника (скелет с числами
«#» тот же), числа условия — годным вариантом, а выкладка и ответ — ровно тем, что даёт программа
задачи на этих числах. Мир ЗАМКНУТ: молчание суда о его строке есть ложь.
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "tools"))
import livemath_law as З  # noqa: E402 — закон живой задачи
import closedworld  # noqa: E402
from closedworld import Слой  # noqa: E402 — палата подаёт имя мира

ЗАМКНУТЫЕ_МИРЫ = frozenset({"livemath"})
# Род текста, за который суд берётся: живой (см. `panel._спросить`). Строк иного рода он не судит.
РОД_ТЕКСТА = "live"


def судить(строка, слой=None):
    """Лишь строки своего мира: закон дома на чужой строке того же вида («…? 21: 48 − 27 = 21.»)
    сказал бы «ложь», ибо её скелета нет в источнике, — а это захват чужой рамки, не суд.
    Мир замкнут: молчание закона о своей строке есть ложь."""
    if not closedworld.замкнут(слой, ЗАМКНУТЫЕ_МИРЫ):
        return False, False
    судимо, истинно = З.судить(строка)
    return (True, False) if not судимо else (судимо, истинно)


def main():
    путь = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else (
        pathlib.Path(__file__).resolve().parents[1] / "datasets" / "genesis_livemath.txt")
    if not путь.is_file():
        print(f"ЖИВАЯ ЗАДАЧА ОТКАЗ: мира «{путь}» нет — судить нечего")
        return 2
    # ПРЕДСТАВЛЕННОЕ «НЕТ»: итог выкладки неверен; число условия не вход программы; слово порчено
    подсадки = (
        "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. "
        "How many clips did Natalia sell altogether in April and May? 72: 48 ÷ 2 = 24, 48 + 24 = 73.",
        "Natalia sold clips to 49 of her friends in April, and then she sold half as many clips in May. "
        "How many clips did Natalia sell altogether in April and May? 72: 48 ÷ 2 = 24, 48 + 24 = 72.",
        "Natalia sold clip to 48 of her friends in April, and then she sold half as many clips in May. "
        "How many clips did Natalia sell altogether in April and May? 72: 48 ÷ 2 = 24, 48 + 24 = 72.",
    )
    пойманы = sum(1 for с in подсадки if З.судить(с) == (True, False))
    судимо = ложных = 0
    примеры = []
    for строка in путь.read_text(encoding="utf-8", errors="replace").splitlines():
        if not строка.strip():
            continue
        с, и = З.судить(строка)
        судимо += 1
        if not (с and и):
            ложных += 1
            if len(примеры) < 5:
                примеры.append(строка[:120])
    for п in примеры:
        print("  ЛОЖЬ:", п)
    поза = "PASS" if ложных == 0 and пойманы == len(подсадки) else "FAIL"
    print(f"ЖИВАЯ ЗАДАЧА {поза}: {ложных} ложных из {судимо} судимых (рубеж 0); "
          f"подсадок поймано {пойманы} из {len(подсадки)}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
