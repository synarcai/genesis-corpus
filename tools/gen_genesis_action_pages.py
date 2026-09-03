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
chains are bought from mass 9, depth-3 from 20): twenty-five pages per
language per pass — five per genus — on numbers that walk with strides coprime with the tables, so every
genus has ≥ 20 pages per language over the five passes.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import actionpages as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_action_pages.txt"


def _добавить(вон, *арг, **кв):
    """A page whose form the language has not declared is not written (the law
    of the declared form: no case is ever guessed)."""
    try:
        вон.append(F.страница(*арг, **кв))
    except ValueError:
        pass


def язык_группа(шаг, язык):
    лица = F.ЛИЦА[язык]
    вещей = len(F.ЯЗЫКИ[язык]["вещи"])
    кратности = sorted(F.ЯЗЫКИ[язык]["кратные"])
    вон = []
    j = шаг * 17
    for i in range(5):
        X = лица[(шаг * 3 + i * 5) % len(лица)][0]
        n = 6 + (шаг * 7 + i * 11 + j) % 90
        k = 1 + (шаг * 5 + i * 3 + j) % (n - 2)
        _добавить(вон, язык, "остаток", X=X, Т=(шаг + i) % вещей, n=n, k=k)
        j += 1
    for i in range(5):
        X = лица[(шаг * 5 + i * 3 + 1) % len(лица)][0]
        n = 4 + (шаг * 11 + i * 7 + j) % 80
        k = 1 + (шаг * 3 + i * 5 + j) % 20
        _добавить(вон, язык, "прибавка", X=X, Т=(шаг + i + 2) % вещей, n=n, k=k)
        j += 1
    for i in range(5):
        X = лица[(шаг * 7 + i * 5 + 2) % len(лица)][0]
        чс, зн = F.ДОЛИ[(шаг * 3 + i) % len(F.ДОЛИ)]
        # the whole is a multiple of the denominator: every step stays whole
        n = зн * (3 + (шаг * 5 + i * 7 + j) % 24)
        _добавить(вон, язык, "доля", X=X, Т=(шаг + i + 4) % вещей, n=n, доля=(чс, зн))
        j += 1
    for i in range(5):
        a = (шаг * 3 + i * 7 + 3) % len(лица); b = (a + 1 + (шаг + i) % (len(лица) - 1)) % len(лица)
        n = 2 + (шаг * 7 + i * 5 + j) % 40
        m = 2 + (шаг * 5 + i * 11 + j) % 40
        _добавить(вон, язык, "вместе", X=лица[a][0], Y=лица[b][0], Т=(шаг + i + 1) % вещей, n=n, m=m)
        j += 1
    for i in range(5):
        a = (шаг * 5 + i * 3 + 5) % len(лица); b = (a + 2 + (шаг + i) % (len(лица) - 2)) % len(лица)
        n = 2 + (шаг * 11 + i * 7 + j) % 30
        _добавить(вон, язык, "кратное", X=лица[a][0], Y=лица[b][0], Т=(шаг + i + 3) % вещей,
                              n=n, кратность=кратности[(шаг + i) % len(кратности)])
        j += 1
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
