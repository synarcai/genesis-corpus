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
    # THREE GENERA FROM e9's PROFILE OF MUTENESS (03.09): the whole named by its
    # PLACE and a part of it, a rate «every day» without money, and the sum said
    # by «they» after the bearers are named — five pages each per pass
    вещей_мест = len(F.ЯЗЫКИ[язык]["места"])
    for i in range(5):
        n = 40 * (3 + (шаг * 5 + i * 7 + j) % 20)
        k = 5 * (1 + (шаг * 3 + i * 11 + j) % 15)
        if k >= n:
            k = n // 2
        _добавить(вон, язык, "место", X=лица[0][0], Т=(шаг + i) % вещей, n=n, k=k,
                  место=(шаг + i) % вещей_мест, свойство=(шаг * 2 + i) % len(F.ЯЗЫКИ[язык]["свойства"]))
        j += 1
    # the ECHO of a part (e9 03.09: so the market of heads buys «of them»), and
    # TWO PARTS WITH A REST (g1.39)
    for i in range(5):
        n = 40 * (2 + (шаг * 7 + i * 5 + j) % 20)
        k = 5 * (1 + (шаг * 5 + i * 3 + j) % 12)
        if k >= n:
            k = n // 4
        _добавить(вон, язык, "место_эхо", X=лица[0][0], Т=(шаг + i + 1) % вещей, n=n, k=k,
                  место=(шаг + i + 1) % вещей_мест, свойство=(шаг + i) % len(F.ЯЗЫКИ[язык]["свойства"]))
        j += 1
    for i in range(5):
        n = 10 * (3 + (шаг * 3 + i * 7 + j) % 12)
        k = 2 + (шаг * 5 + i * 3 + j) % max(2, n // 4)
        k2 = 2 + (шаг * 7 + i * 5 + j) % max(2, n // 4)
        свойств = len(F.ЯЗЫКИ[язык]["свойства"])
        с1 = (шаг + i) % свойств; с2 = (с1 + 1) % свойств; с3 = (с1 + 2) % свойств
        _добавить(вон, язык, "место_две", X=лица[0][0], Т=(шаг + i + 2) % вещей, n=n, k=k, k2=k2,
                  место=(шаг + i + 2) % вещей_мест, свойство=с1, свойство2=с2, свойство3=с3)
        j += 1
    # A GOOD PRICED IN ANOTHER GOOD (e9's profile, genus 7 — the rate of
    # exchange), asked both ways: eight per pass
    for i in range(8):
        т1 = (шаг + i) % вещей; т2 = (т1 + 1 + (шаг + i) % (вещей - 1)) % вещей
        n = 3 + (шаг * 5 + i * 7 + j) % 12
        k = 2 + (шаг * 3 + i * 5 + j) % 9
        if i % 2 == 0:
            _добавить(вон, язык, "курс", X=лица[0][0], Т=т1, Т2=т2, n=n, k=k)
        else:
            _добавить(вон, язык, "курс_обр", X=лица[0][0], Т=т1, Т2=т2, n=n, m=n * k)
        j += 1
    # the rate is asked BOTH ways, so each way keeps its own mass of twenty
    for i in range(8):
        X = лица[(шаг * 5 + i * 7 + 6) % len(лица)][0]
        n = 5 * (2 + (шаг * 7 + i * 3 + j) % 30)
        k = 2 + (шаг * 3 + i * 5 + j) % 12
        за = i % 2 == 0
        _добавить(вон, язык, "ставка", X=X, Т=(шаг + i + 5) % вещей, n=n, k=k, m=n * k,
                  глагол_ставки=(шаг + i) % len(F.ЯЗЫКИ[язык]["ставки"]), дней=за)
        j += 1
    for i in range(5):
        a = (шаг * 7 + i * 5 + 2) % len(лица); b = (a + 1 + (шаг + i) % (len(лица) - 1)) % len(лица)
        n = 3 + (шаг * 11 + i * 7 + j) % 60
        m = 3 + (шаг * 5 + i * 13 + j) % 60
        _добавить(вон, язык, "вместе_они", X=лица[a][0], Y=лица[b][0], Т=(шаг + i + 6) % вещей, n=n, m=m)
        j += 1
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
