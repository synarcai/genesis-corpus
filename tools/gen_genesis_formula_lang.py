#!/usr/bin/env python3
"""GENESIS layer: FORMULA ↔ SPEECH — conversion at any complexity.

The owner's requirement, in his words: the organism must be able to
convert formulas of ANY complexity by itself. That is not a list of
formulas; it is a GRAMMAR, and a grammar is learned from a form shown on
many depths, not from many forms shown once.

WHAT A LIST CANNOT BUY. The corpus already carried formula shows: «the
sum of the first n numbers is n × ( n + 1 ) / 2» stood beside its worded
twin. That teaches THAT formula. It cannot teach the NEXT one, because
the pairing was written by hand and nothing in it says how a formula is
read in general.

WHAT IS SHOWN HERE. One tree, four surfaces, and the CONVERSION between
them as the show itself:
    «$ \\frac{a + b}{2} $ in words is the fraction with numerator ( a
     plus b ) and denominator 2.»
    «дробь с числителем ( сумма a и b ) и знаменателем 2 в записи есть
     $ \\frac{a + b}{2} $.»
Both directions, both languages, and the trees behind them are BUILT to
depth: depth one, two, three, four. Depth is the teacher — a reader who
has seen a fraction whose numerator is itself a sum has seen the rule,
not the case.

BRACKETS IN SPEECH ARE GRAMMAR, NOT ORNAMENT. A compound argument is
always spoken inside brackets, an atomic one never; this is what a
mathematician reading aloud actually does, and it is what makes speech
parsable at any depth.

THE ORACLE IS EIGHT WALKS. Four surfaces are written by four renderers
and read back by four parsers, written apart; a tree that does not
return through all of them never becomes a show. Four thousand trees to
depth four pass without a single divergence — that is the proof carried
in `tools/formula_lang.py`, and this layer refuses to build without it.
"""

import pathlib
import random
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import formula_lang as фл  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ДОМ ОТДЕЛЁН ОТ КУЗНИЦЫ (13.09): деревья, глубины, квадратные и словарь показов живут в
# `tools/formulaforms.py`, а кузница берёт у него готовые группы.
#
#     МИР, ЧЬИ СТРАНИЦЫ НЕ НАЗВАНЫ РОДОМ, ЧИТАЕТСЯ ТОЛЬКО ТЕМ, КТО ЧИТАЕТ КУЗНИЦУ.
import formulaforms as F  # noqa: E402

ЦЕЛЬ = "datasets/genesis_formula_lang.txt"
фл = F.фл


def pass_groups(шаг):
    # ГЛУБИНА — СВОЯ ГРУППА: показы одной глубины не перемешиваются с
    # чужими, ибо глубина здесь и есть предмет урока. Сборка — в доме.
    return F.группы_страниц(шаг)


def main():
    беды = фл.оракул() if hasattr(фл, "оракул") else []
    if беды:
        print(f"ФОРМУЛЫ ОТКАЗ: {len(беды)} деревьев не обратимы")
        return 2
    emit_grouped(ЦЕЛЬ, pass_groups)
    return 0


if __name__ == "__main__":
    sys.exit(main())
