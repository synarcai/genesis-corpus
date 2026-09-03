#!/usr/bin/env python3
"""GENESIS layer: COUNTED UNITS — «1 day, 2 days, 5 days» in one frame.

32's tomograph of the rate (03.09): the market of count forms buys the pair
«day / days» only INSIDE ONE FRAME that carries at least three different
numbers. The corpus said «worked on 1 day» in one world and «how much in 8
days» in another — two frames, no pair — and so the rate «cynthia collects 10
eggs every day. how many eggs in 8 days?» stayed mute while «in 8 day»
answered. This world says the unit with five counts in one show, on four
frames of each of en/ru/de and six units:

    the trip takes 1 day. the trip takes 2 days. the trip takes 3 days.
    the trip takes 5 days. the trip takes 10 days.

Every form is declared by the house (tools/countforms.py); Russian names three
forms and chooses by the last digit under the teenage census.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import countforms as F  # noqa: E402
from layer import PASSES, emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_unit_counts.txt"


def показы(язык):
    """Показ-парадигма (одна рамка со всеми счётами) и показ-вопрос (тот же
    факт, спрошенный в той же строке): мир, говорящий одними утверждениями,
    учит отвечать молчанием — это сказал прибор широты вопроса."""
    я = F.ЯЗЫКИ[язык]
    вон = [F.показ(язык, рамка, единица)
           for рамка in range(len(я["рамки"]))
           for единица in range(len(я["единицы"]))]
    вон += [F.показ_вопросом(язык, рамка, единица, n)
            for рамка in range(len(я["рамки"]))
            for единица in range(len(я["единицы"]))
            for n in F.СЧЁТЫ]
    return вон


ВСЕ = {язык: показы(язык) for язык in F.ЯЗЫКИ}


def pass_groups(шаг):
    """Each pass takes its share of the shows: the house is finite, and saying
    it five times over would be weight, not knowledge."""
    return [[с for j, с in enumerate(ВСЕ[язык]) if j % len(PASSES) == шаг]
            for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
