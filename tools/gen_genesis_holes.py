#!/usr/bin/env python3
"""GENESIS layer: THE HOLE MARKET — one fact, every role of it asked.

holon's Д-1 (REVISION 02.09): a question in the organism is a per-genus
surface, not an operation over a bought fact frame, so the organism cannot
ask what it was never shown asked. The census of the svod says the same in
numbers: the number hole («what», «how many», «сколько») carries about
twenty thousand questions, the entity, place and time holes («who», «where»,
«when») a few dozen, some of them mute. This world buys the question as an
OPERATION: one fact frame — «on monday anna put 5 cups on the shelf» — and
every role of it asked in turn, the question word naming the type of the
hole (who → actor, how many → number, what → thing, where → place, when →
time), the answer being exactly the filler the question took out. A line
is fact + question + answer; the frame alone is shown too (the fact with no
hole). The house of holes (tools/holes.py) holds the frame and the
operation; the court recomputes the question from the fact and the answer
from the hole by the same house.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holes  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_holes.txt"
КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
ИМЕНА_EN = tuple(_EN["person_names"][:16])
ИМЕНА_RU = tuple((n.capitalize(), ф["gender"]) for n, ф in list(_RU["person_forms"].items())[:16])
ЧИСЛА = (5, 3, 8, 2, 7, 4, 9, 6, 12, 10, 11)   # counts ≥ 2: the frame's thing is plural
ШИРИНА = 12   # 5 passes × 12 instances → 12 shows per (verb, hole, language): above the knee of 9


def _роли(шаг, i, язык):
    р = holes.РАМКИ[(шаг + i) % len(holes.РАМКИ)]
    место = р[5][(шаг * 2 + i) % len(р[5])]
    вещь = р[6][(шаг * 3 + i) % len(р[6])]
    n = ЧИСЛА[(шаг * 7 + i) % len(ЧИСЛА)]
    день = holes.ДНИ[язык][(шаг * 3 + i) % 7]
    k = шаг * 5 + i * 3
    if язык == "en":
        return день, ИМЕНА_EN[k % len(ИМЕНА_EN)], "m", р, n, вещь, место
    имя, род = ИМЕНА_RU[k % len(ИМЕНА_RU)]
    return день, имя, род, р, n, вещь, место


def язык_группа(шаг, язык):
    """Per frame instance: the fact, then every hole of it."""
    вон = []
    for i in range(ШИРИНА):
        роли = _роли(шаг, i, язык)
        факт = holes.факт(язык, *роли)
        вон.append(факт)
        # the line is an episode: the fact stands beside every question of it
        for вопрос, ответ in holes.дыры(язык, *роли):
            вон.append(f"{факт} {вопрос} {ответ}")
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, "en"), язык_группа(шаг, "ru")]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
