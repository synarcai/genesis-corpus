#!/usr/bin/env python3
"""GENESIS layer: THE HOLE MARKET — one fact, every role of it asked, six languages.

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
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import holes  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_holes.txt"
ЧИСЛА = (5, 3, 8, 2, 7, 4, 9, 6, 12, 10, 11)   # counts ≥ 2: the frame's thing is plural
ШИРИНА = 12   # 5 passes × 12 instances → 12 shows per (verb, hole, language): above the knee of 9


def _роли(шаг, i, язык):
    k = (шаг + i) % len(holes.РАМКИ[язык])
    р = holes.РАМКИ[язык][k]
    место = р["места"][(шаг * 2 + i) % len(р["места"])]
    вещь = р["вещи"][(шаг * 3 + i) % len(р["вещи"])]
    n = ЧИСЛА[(шаг * 7 + i) % len(ЧИСЛА)]
    день = holes.ДНИ[язык][(шаг * 3 + i) % 7]
    имена = holes.ИМЕНА[язык]
    имя, род = имена[(шаг * 5 + i * 3) % len(имена)]
    return день, имя, род, k, n, вещь, место


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


ШИРИНА_ЗАПРОСОВ = 10   # 5 passes × 10 instances × 5 roles → 10 per (verb, role, language)


def запросы_группа(шаг, язык):
    """THE ORGANISM ASKS: a fact with one role unfilled — its placeholder in
    place — and the question of that role after it, produced, not answered."""
    вон = []
    for i in range(ШИРИНА_ЗАПРОСОВ):
        роли = _роли(шаг * 3 + 1, i + 5, язык)
        for факт, вопрос in holes.запросы(язык, *роли):
            вон.append(f"{факт} {вопрос}")
    return вон


def pass_groups(шаг):
    return ([язык_группа(шаг, язык) for язык in holes.ЯЗЫКИ]
            + [запросы_группа(шаг, язык) for язык in holes.ЯЗЫКИ])


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
