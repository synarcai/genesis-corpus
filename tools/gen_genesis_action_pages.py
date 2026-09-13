#!/usr/bin/env python3
"""GENESIS layer: A LEDGER FOR EVERY COUNTABLE ACT — new pages, old worlds untouched.

The collegium of a hundred per cent (owner, 03.09): every computable genus
must show its chain. The reader's worlds of e9 (heads, aggregate, gsmwide,
gsmlex, compare, depletion, verbs, realverbs, verbal) are computable by
nature but answer with a value — «peter keeps 4 coins» — and their form may
not change: his markets buy skeletons from those very lines. So the ledger
comes as NEW PAGES of the same genera, in en/ru/de:

  «peter had 8 coins. peter gave 4 coins away. how many coins are left?
   8 − 4 = 4. so the answer is 4.»
  «у Анны было 70 книг. половина книг ушла. сколько книг осталось?
   70 ÷ 2 = 35, 70 − 35 = 35. значит ответ: 35.»
  «Anna hat 2 Eier. Jonas hat dreimal so viele Eier wie Anna. wie viele
   Eier hat Jonas? 3 × 2 = 6. also ist die Antwort 6.»

The house of action pages (tools/actionpages.py) holds the templates; the
court reads them back and regenerates the page letter by letter.

MASS FROM THE RULE (М-148, and the measured price of mass 03.09: depth-2
chains are bought from mass 9, depth-3 from 20): forty pages per
language per pass — five per genus, eight genera — on numbers that walk with strides coprime with the tables, so every
genus has ≥ 20 pages per language over the five passes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_action_pages.txt"


# ПЕРЕБОР ЖИВЁТ В ДОМЕ, А НЕ ЗДЕСЬ (13.09): дом обязан знать свои страницы, чтобы назвать
# их род. ДВА ПЕРЕБОРА ОДНОГО ПРОСТРАНСТВА РАЗОЙДУТСЯ НА ПЕРВОЙ ЖЕ ПРАВКЕ.
def язык_группа(шаг, язык):
    return [с for с, _род in F.перебор(шаг, язык)]


def pass_groups(шаг):
    # ЯЗЫК, ОБЪЯВИВШИЙ ЛИШЬ СЛОВАРЬ, СТРАНИЦ ДЕЙСТВИЯ НЕ ПИШЕТ (04.09):
    # голландский пришёл в дом за вещами для домов сочленений и связок, а
    # рамок действия у него нет — и генератор не спрашивает того, чего язык
    # не объявил.
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ if "ответ" in F.ЯЗЫКИ[язык]]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
