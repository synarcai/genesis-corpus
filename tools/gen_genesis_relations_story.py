#!/usr/bin/env python3
"""GENESIS layer: A MULTIPLE, A DIFFERENCE AND A SUM — school pages in three languages.

e9's order (03.09, G1-ATTACK, genus 1 «multiplicative relation + sum», 21
tasks of the g1 band): «there are twice as many worker bees as baby bees.
there are 750 bees in all. how many baby bees are there? 1 + 2 = 3, 750 ÷ 3
= 250. so the answer is 250.», «bobby has 5 fewer than three times as many
games as brian. brian has 20 games. how many games does bobby have? 3 × 20
= 60, 60 − 5 = 55. so the answer is 55.», the same relation backwards
(«janey has 3 more than twice the number of books sally has. janey has 21
books. how many books does sally have? 21 − 3 = 18, 18 ÷ 2 = 9.»), and the
ages («ruby is three times as old as sam …», «together they are 32 years
old …», the g1 idiom «three times older than») — in en/ru/de, whole
answers, the words of multiplicity declared (twice, three times, four
times, half as many, a third as many; вдвое/втрое/вчетверо, удвоенное/
утроенное/учетверённое; doppelt/dreimal/viermal, halb/ein Drittel). The
house of relation pages (tools/relstory.py) holds the templates; the court
reads them back and regenerates the page.

MASS FROM THE RULE (М-148): every (form, sign, multiplicity, language) cell gets ≥ 9 pages
over the five passes on different numbers; names, things and pairs walk
with strides coprime with their tables.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import relstory as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_relations_story.txt"


def язык_группа(шаг, язык):
    я = F.ЯЗЫКИ[язык]
    лица = F.ЛИЦА[язык]
    вон = []
    j = шаг * 31
    # the sum of a multiple: k = 2, 3, 4 × the two questions, twice (plain and «half as many»)
    # 24 per pass: k walks 2, 3, 4; the question alternates by threes; the
    # «half as many» surface takes the second and fourth sixes (k = 2, 3 only)
    for i in range(24):
        k = 2 + (i + шаг) % 3
        долей = (i // 6) % 2 == 1 and k in я["доля"]
        вон.append(F.страница(язык, "сумма", пара=(шаг * 5 + i * 7) % 6, k=k, долей=долей, спрос=("м", "б")[(i // 3 + шаг) % 2], x=5 + (шаг * 11 + i * 13 + j) % 56))
        j += 1
    # the whole asked from the small part (e9: «the same relation, another hole»): 12 per pass
    for i in range(12):
        k = 2 + (i + шаг) % 3
        вон.append(F.страница(язык, "сумма_обр", пара=(шаг * 7 + i * 5 + 2) % 6, k=k, x=6 + (шаг * 13 + i * 11 + j) % 60))
        j += 1
    # three bearers — one multiple, one difference, one sum (g1 37/46/56): 36 per
    # pass over the cells (k, sign, who is asked); the base a keeps every answer whole
    for i in range(36):
        k = 2 + i % 3
        знак = ("−", "+")[(i // 3) % 2]
        спрос = ("X", "Y", "Z")[(i // 6 + шаг) % 3]
        a = (шаг * 3 + i * 5 + j) % len(лица); b = (a + 1 + (i + шаг) % (len(лица) - 2)) % len(лица); c = (b + 1 + (i * 2 + шаг) % (len(лица) - 3)) % len(лица)
        if c == a:
            c = (c + 1) % len(лица)
        d = 2 + (шаг * 5 + i * 7 + j) % 9
        база = 4 + (шаг * 7 + i * 3 + j) % 24
        if знак == "+" and база - d < 2:
            база += d
        вон.append(F.страница(язык, "трое", X=лица[a][0], Y=лица[b][0], Z=лица[c][0], k=k, знак=знак, d=d, вещь=(i + шаг * 3) % 6, a=база, спрос=спрос))
        j += 1
    # a difference over a multiple, both signs, and the relation backwards
    for форма in ("больше", "обратно"):
        for i in range(12):
            k = 2 + (i + шаг + (форма == "обратно")) % 3
            знак = ("−", "+")[(i + шаг) % 2]
            a = (шаг * 3 + i * 5 + j) % len(лица); b = (a + 1 + (i + шаг) % (len(лица) - 1)) % len(лица)
            d = 2 + (шаг * 7 + i * 3 + j) % 8
            if форма == "больше":
                n = 5 + (шаг * 5 + i * 11 + j) % 30
                if знак == "−" and k * n - d < 2:
                    n += d
                вон.append(F.страница(язык, "больше", X=лица[a][0], Y=лица[b][0], k=k, знак=знак, d=d, вещь=(i + шаг * 2) % 6, n=n))
            else:
                r = 3 + (шаг * 5 + i * 7 + j) % 28
                if знак == "−" and k * r - d < 2:
                    r += d
                вон.append(F.страница(язык, "обратно", X=лица[a][0], Y=лица[b][0], k=k, знак=знак, d=d, вещь=(i + шаг * 2 + 3) % 6, r=r))
            j += 1
    # ages: the multiple asked, the sum asked, the idiom «older than» (en)
    # 24 per pass: the multiple asked / the sum asked in turn; in English every
    # second page says the g1 idiom «k times older than»
    for i in range(24):
        k = 2 + (i + шаг) % 3
        a = (шаг * 7 + i * 3 + j) % len(лица); b = (a + 2 + (i + шаг) % (len(лица) - 2)) % len(лица)
        идиома = язык == "en" and (i // 2) % 2 == 1
        if i % 2 == 0:
            вон.append(F.страница(язык, "возраст", X=лица[a][0], Y=лица[b][0], k=k, спрос="x", n=3 + (шаг * 3 + i * 5 + j) % 10, идиома=идиома))
        else:
            вон.append(F.страница(язык, "возраст", X=лица[a][0], Y=лица[b][0], k=k, спрос="сум", x=4 + (шаг * 5 + i * 3 + j) % 12, идиома=идиома))
        j += 1
    # THE AGE AFTER k YEARS (e9's profile of muteness, genus 4): forward,
    # backward and over a multiple — seven pages each per pass
    for i in range(7):
        X = лица[(шаг * 5 + i * 3 + 4) % len(лица)][0]
        n = 4 + (шаг * 7 + i * 5 + j) % 40
        k = 2 + (шаг * 3 + i * 7 + j) % 12
        вон.append(F.страница(язык, "через", X=X, n=n, k=k))
        j += 1
    for i in range(7):
        X = лица[(шаг * 7 + i * 5 + 1) % len(лица)][0]
        k = 2 + (шаг * 5 + i * 3 + j) % 12
        m = k + 3 + (шаг * 3 + i * 11 + j) % 40
        вон.append(F.страница(язык, "через_обратно", X=X, m=m, k=k))
        j += 1
    for i in range(7):
        a = (шаг * 3 + i * 7 + 5) % len(лица); b = (a + 2 + (шаг + i) % (len(лица) - 2)) % len(лица)
        n = 3 + (шаг * 5 + i * 3 + j) % 20
        лет = 2 + (шаг * 7 + i * 5 + j) % 10
        вон.append(F.страница(язык, "кратное_через", X=лица[a][0], Y=лица[b][0],
                              k=2 + (шаг + i) % 3, n=n, лет=лет))
        j += 1
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
