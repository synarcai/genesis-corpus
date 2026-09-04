#!/usr/bin/env python3
"""[ЩЕРБАТОСТЬ ДОМОВ] — форма, написанная не на всех языках своего дома.

Слово holon (04.09), снявшего произведение «голова × запись × действие»:
немота сидит не на голове и не на записи, а на КЛЕТКЕ, и часто на ОДНОМ
действии из четырёх. Дыры ВНУТРИ дома дешевле и важнее новых домов — но
увидеть их можно, лишь померив дом по его собственному произведению.

Прибор берёт у каждого дома форм его ПОКАЗЫ (там при каждой строке стоят язык
и форма) и строит решётку «форма × язык». Щербатая клетка — форма, живущая на
одних языках дома и молчащая на других.

ЩЕРБАТОСТЬ НЕ ЕСТЬ ЛОЖЬ И ЧАСТО НЕ ЕСТЬ ДОЛГ. Дом поведения нарочно не пишет
«кратко» по-немецки и по-голландски: их порядок ставит местоимение перед
именем, и страницы им не даётся по закону, а не по недосмотру. Прибор потому
не судит, а НАЗЫВАЕТ, и решение оставляет дому — как прибор массы на форму
называет цену, а не приговор.

    python3 scripts/form_matrix.py [--сверху 12]
"""
import argparse
import collections
import importlib
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

# СПИСОК ДОМОВ ЕСТЬ ЗНАМЕНАТЕЛЬ ПРИБОРА (М-264, М-269): всякий новый дом форм
# вписывается сюда в тот же день, иначе прибор мерит свою память о корпусе.
ДОМА = ("dialogueforms", "linkforms", "behaviorforms", "topicforms", "natureforms",
        "oppositeforms", "roleforms", "scaleforms", "jointforms", "actionpages",
        "worldfacts", "inferforms", "disjforms", "induforms", "analogforms",
        "replyforms", "rewriteforms", "opinionforms", "objectforms", "jointforms2",
        "crossforms", "hypoforms", "anaphoraforms")


def main():
    ап = argparse.ArgumentParser()
    ап.add_argument("--сверху", type=int, default=12)
    а = ап.parse_args()
    щербатых = целых = 0
    ряды = []
    for имя in ДОМА:
        try:
            м = importlib.import_module(имя)
        except Exception as е:
            print(f"  ДОМ НЕ ПРОЧТЁН {имя}: {е}", file=sys.stderr)
            continue
        показы = getattr(м, "ПОКАЗЫ", None)
        if not isinstance(показы, dict):
            continue
        по_форме = collections.defaultdict(set)
        языки = set()
        for _, значение in показы.items():
            if not (isinstance(значение, tuple) and len(значение) == 2):
                continue
            яз, форма = значение
            по_форме[форма].add(яз)
            языки.add(яз)
        for форма, свои in sorted(по_форме.items()):
            нет = sorted(языки - свои)
            if нет:
                щербатых += 1
                ряды.append((len(нет), имя, форма, нет))
            else:
                целых += 1
    ряды.sort(reverse=True)
    print(f"{'дом':16} {'форма':22} нет на языках")
    for _, имя, форма, нет in ряды[:а.сверху]:
        print(f"{имя[:16]:16} {форма[:22]:22} {', '.join(нет)}")
    всего = щербатых + целых
    print(f"ЩЕРБАТОСТЬ ДОМОВ: {щербатых} щербатых форм из {всего} "
          f"({100 * щербатых // max(1, всего)} %), домов {len(ДОМА)}")
    if всего == 0:
        print("  ВНИМАНИЕ: форм НОЛЬ — прибор ничего не прочёл (М-264)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
