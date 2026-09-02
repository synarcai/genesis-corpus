#!/usr/bin/env python3
"""[ГЛАГОЛ–ВЕЩЬ] — известный глагол с вещью чужого рода ложен о языке.

ЗАКОН: глагол берёт свой род вещей (tools/verbthings.py): еду едят, письменное
пишут, расстояние и время проходят, вес поднимают. Показ «sara wrote 8
pencils», «ann bought 21 books and ate 12 books», «walks 2 pounds every day»
верен арифметикой и ложен речью — а корпус, который учит речи, не вправе
учить обратному. Прибор считает по всем мирам показов тройки «глагол число
вещь», у которых дом сочетаемости отвечает «нет».

ПОВОД (03.09): 138 таких строк в пяти мирах историй нашлись только глазами,
после того как рынок историй e9 купил «walks pounds» как ставку.

ЧЕГО ПРИБОР НЕ ВИДИТ, НАЗВАНО ЧЕСТНО:
  · глагол вне дома и вещь вне всех родов не судятся — дом читает не
    смысл, а ОБЪЯВЛЕННУЮ сочетаемость, и молчит о необъявленном;
  · вещь, отделённая от глагола не числом («ate 5 of them»), здесь не
    читается: её судит суд мира, знающий свою рамку.

РУБЕЖ — 0: бессмыслица не порог, а дефект.

Использование:
  python3 scripts/verbthings_court.py
"""
# ПУСТОЙ-ОБХОД: no-such-corpus-file
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import genesis  # noqa: E402
import verbthings  # noqa: E402

# РУБЕЖ-ДОЛГА: ЧУЖИХ_РУБЕЖ = 0
ЧУЖИХ_РУБЕЖ = 0
ТРОЙКА = re.compile(r"\b([a-z]+) (\d+) ([a-z]+)\b")


def обход():
    return [genesis._resolve(м["file"]) for м in genesis.manifest()["worlds"] if м.get("text") == "shows"]


def main():
    пути = [п for п in обход() if п.is_file()]
    if not пути:
        print("ГЛАГОЛ–ВЕЩЬ ОТКАЗ: обход пуст, судить нечего")
        return 2
    чужих = collections.Counter()
    примеры = {}
    строк = 0
    for путь in пути:
        for строка in путь.read_text(encoding="utf-8", errors="replace").splitlines():
            if not строка.strip():
                continue
            строк += 1
            for глагол, _, вещь in ТРОЙКА.findall(строка):
                if not verbthings.берёт(глагол, вещь):
                    ключ = (путь.stem, глагол, вещь)
                    чужих[ключ] += 1
                    примеры.setdefault(ключ, строка.strip()[:100])
    всего = sum(чужих.values())
    вердикт = "PASS" if всего <= ЧУЖИХ_РУБЕЖ else "FAIL"
    print(f"ГЛАГОЛ–ВЕЩЬ {вердикт}: {всего} чужих пар глагол–вещь в {строк} строках показов ({len(пути)} файлов, рубеж {ЧУЖИХ_РУБЕЖ})")
    for ключ, сколько in чужих.most_common(8):
        мир, глагол, вещь = ключ
        print(f"  {сколько:4d} {мир}: «{глагол} … {вещь}» — {примеры[ключ]}")
    return 0 if вердикт == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
