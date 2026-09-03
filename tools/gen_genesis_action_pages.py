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
    of the declared form: no case is ever guessed).

    ДВА РОДА НЕОБЪЯВЛЕННОГО, И ОБА МОЛЧАТ ОДИНАКОВО: форма ВЕЩИ, которой нет
    в парадигме (ValueError дома), и целый РОД, слов которого язык не назвал
    (KeyError таблицы) — испанский не объявил долей и цветных частей, и эти
    страницы он просто не пишет.
    """
    try:
        вон.append(F.страница(*арг, **кв))
    except (ValueError, KeyError):
        pass


def язык_группа(шаг, язык):
    лица = F.ЛИЦА[язык]
    вещей = len(F.ЯЗЫКИ[язык]["вещи"])
    кратности = sorted(F.ЯЗЫКИ[язык].get("кратные") or (2,))
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
    вещей_мест = len(F.ЯЗЫКИ[язык].get("места") or (0,))
    for i in range(5):
        n = 40 * (3 + (шаг * 5 + i * 7 + j) % 20)
        k = 5 * (1 + (шаг * 3 + i * 11 + j) % 15)
        if k >= n:
            k = n // 2
        _добавить(вон, язык, "место", X=лица[0][0], Т=(шаг + i) % вещей, n=n, k=k,
                  место=(шаг + i) % вещей_мест, свойство=(шаг * 2 + i) % len(F.ЯЗЫКИ[язык].get("свойства") or (0,)))
        j += 1
    # the ECHO of a part (e9 03.09: so the market of heads buys «of them»), and
    # TWO PARTS WITH A REST (g1.39)
    for i in range(5):
        n = 40 * (2 + (шаг * 7 + i * 5 + j) % 20)
        k = 5 * (1 + (шаг * 5 + i * 3 + j) % 12)
        if k >= n:
            k = n // 4
        _добавить(вон, язык, "место_эхо", X=лица[0][0], Т=(шаг + i + 1) % вещей, n=n, k=k,
                  место=(шаг + i + 1) % вещей_мест, свойство=(шаг + i) % len(F.ЯЗЫКИ[язык].get("свойства") or (0,)))
        j += 1
    for i in range(5):
        n = 10 * (3 + (шаг * 3 + i * 7 + j) % 12)
        k = 2 + (шаг * 5 + i * 3 + j) % max(2, n // 4)
        k2 = 2 + (шаг * 7 + i * 5 + j) % max(2, n // 4)
        свойств = len(F.ЯЗЫКИ[язык].get("свойства") or (0,))
        с1 = (шаг + i) % свойств; с2 = (с1 + 1) % свойств; с3 = (с1 + 2) % свойств
        _добавить(вон, язык, "место_две", X=лица[0][0], Т=(шаг + i + 2) % вещей, n=n, k=k, k2=k2,
                  место=(шаг + i + 2) % вещей_мест, свойство=с1, свойство2=с2, свойство3=с3)
        j += 1
    # THE SAME PARTS IN THE PAST, and the part named by the GOOD itself
    # (e9's order 03.09: g1 says «80 were Japanese», «5 of them were red»,
    # «5 students are good at math») — five each per pass
    for i in range(5):
        n = 40 * (2 + (шаг * 3 + i * 7 + j) % 20)
        k = 5 * (1 + (шаг * 7 + i * 5 + j) % 12)
        if k >= n:
            k = n // 4
        _добавить(вон, язык, "место_п", X=лица[0][0], Т=(шаг + i + 3) % вещей, n=n, k=k,
                  место=(шаг + i + 3) % вещей_мест, свойство=(шаг + i + 1) % len(F.ЯЗЫКИ[язык].get("свойства") or (0,)))
        j += 1
    for i in range(5):
        n = 10 * (3 + (шаг * 7 + i * 3 + j) % 12)
        k = 2 + (шаг * 3 + i * 5 + j) % max(2, n // 4)
        k2 = 2 + (шаг * 5 + i * 7 + j) % max(2, n // 4)
        свойств = len(F.ЯЗЫКИ[язык].get("свойства") or (0,))
        с1 = (шаг + i + 1) % свойств; с2 = (с1 + 1) % свойств; с3 = (с1 + 2) % свойств
        _добавить(вон, язык, "место_две_п", X=лица[0][0], Т=(шаг + i + 4) % вещей, n=n, k=k, k2=k2,
                  место=(шаг + i + 4) % вещей_мест, свойство=с1, свойство2=с2, свойство3=с3)
        j += 1
    for i in range(10):
        n = 10 * (2 + (шаг * 5 + i * 3 + j) % 14)
        k = 2 + (шаг * 7 + i * 5 + j) % max(2, n // 3)
        форма = "место_товар" if i % 2 == 0 else "место_товар_п"
        _добавить(вон, язык, форма, X=лица[0][0], Т=(шаг + i + 5) % вещей, n=n, k=k,
                  место=(шаг + i + 5) % вещей_мест, свойство=(шаг + i + 2) % len(F.ЯЗЫКИ[язык].get("свойства") or (0,)))
        j += 1
    # THE LIST WITH ITS COUNT SHOWN (holon 03.09: the executors of lists buy the
    # form only when the count stands beside the enumeration) — seven each
    вещей_мест = len(F.ЯЗЫКИ[язык].get("вместилища") or F.ЯЗЫКИ[язык].get("вместилища_где") or (0,))
    for i in range(7):
        т1 = (шаг + i) % вещей; т2 = (т1 + 1 + i % 3) % вещей; т3 = (т2 + 1 + (шаг + i) % 3) % вещей
        if len({т1, т2, т3}) < 3:
            т3 = (т3 + 1) % вещей
        _добавить(вон, язык, "список_числом", X=лица[0][0], место=(шаг + i) % вещей_мест, Т=т1, Т2=т2, Т3=т3)
        j += 1
    for i in range(7):
        т1 = (шаг * 2 + i + 3) % вещей; т2 = (т1 + 2 + i % 3) % вещей; т3 = (т2 + 1 + (шаг + i) % 4) % вещей
        if len({т1, т2, т3}) < 3:
            т3 = (т3 + 2) % вещей
        _добавить(вон, язык, "список_итогом", X=лица[0][0], место=(шаг + i + 2) % вещей_мест, Т=т1, Т2=т2, Т3=т3)
        j += 1
    for i in range(7):
        т1 = (шаг + i * 2) % вещей; т2 = (т1 + 3) % вещей; т3 = (т2 + 2) % вещей
        n1 = 2 + (шаг * 3 + i * 5 + j) % 12
        n2 = 2 + (шаг * 5 + i * 7 + j) % 12
        n3 = 2 + (шаг * 7 + i * 3 + j) % 12
        _добавить(вон, язык, "список_чисел", X=лица[(шаг + i) % len(лица)][0], Т=т1, Т2=т2, Т3=т3, n=n1, m=n2, k=n3)
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
                  глагол_ставки=(шаг + i) % len(F.ЯЗЫКИ[язык].get("ставки") or (0,)), дней=за)
        j += 1
    # THE GOOD LEAVES AND THE REST IS ASKED (32's tomograph 03.09): «paco had
    # 26 apples. paco ate 9 apples. how many apples does paco have left?» —
    # nine per pass, the three verbs walking, and the eating verb taking only
    # a good the language declares edible
    съедобные = (F.ЯЗЫКИ[язык].get("съедобные") or (0,))
    убылей = len(F.ЯЗЫКИ[язык].get("убыли") or (0,))
    # ЧЕТЫРНАДЦАТЬ, А НЕ ДЕВЯТЬ, И ЭТО СЧИТАНО: русский глагол убыли делится
    # ещё и РОДОМ носителя («съел» и «съела» суть две поверхности рамки), и
    # девять страниц на проход давали ячейке пять–восемь показов — ниже LAW².
    # Перепись после правки назвала эти четыре рамки числом, и число это —
    # цена рода: столько же глаголов, вдвое больше поверхностей.
    for i in range(14):
        X = лица[(шаг * 7 + i * 3 + 2) % len(лица)][0]
        глагол = (шаг + i) % убылей
        Т = съедобные[(шаг + i) % len(съедобные)] if глагол == 0 else (шаг * 3 + i * 5) % вещей
        n = 8 + (шаг * 7 + i * 11 + j) % 60
        k = 1 + (шаг * 5 + i * 7 + j) % (n - 2)
        _добавить(вон, язык, "убыль", X=X, Т=Т, n=n, k=k, глагол_убыли=глагол)
        j += 1
    # ДЕРЖАНИЕ С УХОДОМ ЖИВОГО (атлас немоты holon 04.09, строка #117): живое
    # уходит само, и вопрос спрашивает об оставшихся — по странице на каждое
    # объявленное живое существо за проход
    живых = len(F.ЯЗЫКИ[язык].get("живые") or ())
    for i in range(живых):
        n = 8 + (шаг * 7 + i * 5 + j) % 40
        k = 1 + (шаг * 3 + i * 7 + j) % (n - 2)
        _добавить(вон, язык, "место_ушли", X=лица[0][0], Т=i, n=n, k=k,
                  место=F.МЕСТА_ЖИВЫХ[(шаг * 2 + i) % len(F.МЕСТА_ЖИВЫХ)])
        j += 1
    # A PLACE EMPTIED (32's order 03.09): every declared place gets its own
    # pages — the market of places buys a place only from holdings that name it
    мест = len(F.ЯЗЫКИ[язык].get("места") or (0,))
    for i in range(мест):
        n = 7 + (шаг * 11 + i * 7 + j) % 70
        k = 1 + (шаг * 3 + i * 5 + j) % (n - 2)
        _добавить(вон, язык, "место_убыло", X=лица[0][0], Т=(шаг * 2 + i) % вещей,
                  n=n, k=k, место=i)
        j += 1
    # THE LIST ASKED IN THE SAME LINE (holon 03.09): the count as an executor is
    # bought only from a question→answer pair beside the enumeration
    вместилищ = len(F.ЯЗЫКИ[язык].get("вместилища_где") or F.ЯЗЫКИ[язык].get("вместилища") or (0,))
    for i in range(7):
        т1 = (шаг * 3 + i) % вещей; т2 = (т1 + 2 + i % 3) % вещей; т3 = (т2 + 3) % вещей
        if len({т1, т2, т3}) < 3:
            т3 = (т3 + 1) % вещей
        n1 = 2 + (шаг * 7 + i * 3 + j) % 14
        n2 = 2 + (шаг * 3 + i * 11 + j) % 14
        n3 = 2 + (шаг * 5 + i * 7 + j) % 14
        _добавить(вон, язык, "список_воп", X=лица[(шаг * 3 + i) % len(лица)][0],
                  Т=т1, Т2=т2, Т3=т3, n=n1, m=n2, k=n3)
        j += 1
    for i in range(вместилищ):
        т1 = (шаг + i) % вещей; т2 = (т1 + 1 + (шаг + i) % 3) % вещей; т3 = (т2 + 2) % вещей
        if len({т1, т2, т3}) < 3:
            т3 = (т3 + 1) % вещей
        _добавить(вон, язык, "список_воп_дом", X=лица[0][0], место=i, Т=т1, Т2=т2, Т3=т3)
        j += 1
    # TWO GOODS IN ONE PLACE, and TWO STATES OF TWO GOODS (32's order 03.09):
    # both ends of each fact are asked, so each question keeps its own mass
    for i in range(10):
        т1 = (шаг * 5 + i) % вещей; т2 = (т1 + 1 + (шаг + i) % (вещей - 1)) % вещей
        n1 = 3 + (шаг * 7 + i * 5 + j) % 40
        n2 = 2 + (шаг * 3 + i * 7 + j) % 20
        k = 1 + (шаг * 5 + i * 3 + j) % 12
        _добавить(вон, язык, "двое_разность" if i % 2 == 0 else "двое_сумма",
                  X=лица[0][0], Т=т1, Т2=т2, n=n1, m=n2, k=k, место=(шаг + i) % мест)
        j += 1
    for i in range(10):
        т1 = (шаг * 3 + i + 2) % вещей; т2 = (т1 + 1 + (шаг + i) % (вещей - 1)) % вещей
        n1 = 5 + (шаг * 11 + i * 7 + j) % 30
        n2 = n1 + 5 + (шаг * 5 + i * 13 + j) % 60
        k = 1 + (шаг * 7 + i * 3 + j) % 10
        k2 = k + 1 + (шаг * 3 + i * 5 + j) % 40
        _добавить(вон, язык, "состояния_добавили" if i % 2 == 0 else "состояния_разность",
                  X=лица[0][0], Т=т1, Т2=т2, n=n1, m=n2, k=k, k2=k2, место=(шаг + i + 3) % мест)
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
