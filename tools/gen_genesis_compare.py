#!/usr/bin/env python3
"""GENESIS layer: THE COMPARATIVE GENUS.

The widest g1 gate (times-as 21 + more-than 8 of
65 asks): value(A) = opf(value(B), n) spoken as a
SURFACE between the number-item pair and the
second bearer («dan has 2 apples more than ben»,
«dan has 2 more apples than ben», «dan has 2
times as many apples as ben»). The market buys
each surface (the word tail between the number
and the second agent, item excluded) with its
operator judged by the shows' own arithmetic —
no word list anywhere.

Discipline: base fact for B, comparative fact
for A, ask, answer by an ANSWER verb (holds/
owns/keeps/saves — never the fact verb: a
repeated (verb, agent, item) key cuts the
episode). Both number positions shown; small
numbers (the school table must hold the pair);
i//8 decoupling against modular resonance.
"""

from layer import emit


from plural import by_count


NAMES = ["ava", "ben", "carla", "dan",
         "elena", "felix", "grace", "hugo"]
ITEMS = ["apples", "cookies", "coins", "books",
         "eggs", "pages", "points", "cards"]
# (tail-before-item?, surface builder)
# A-side sentence surfaces; {n}=delta, {it}=item,
# {b}=second bearer
ADD_SURF = [
    "{a} has {n} {it} more than {b}.",
    "{a} has {n} more {it} than {b}.",
]
SUB_SURF = [
    "{a} has {n} {it} fewer than {b}.",
    "{a} has {n} fewer {it} than {b}.",
    # «less than» — та же связь иной поверхностью. Бенчмарк пишет обе
    # (g1.46 говорит less там, где мы показывали только fewer), и рынок
    # не может купить непоказанного.
    "{a} has {n} {it} less than {b}.",
    "{a} has {n} less {it} than {b}.",
]
MUL_SURF = [
    "{a} has {n} times as many {it} as {b}.",
    # ХВОСТ ПОСЛЕ НОСИТЕЛЯ (g1.37): «Smendrick has 3 times the amount of
    # cards that PJ has» — носитель стоит В СЕРЕДИНЕ, а не в конце, и
    # рынок e9 покупает сигнатуру между числом и носителем. Показов
    # такой поверхности не было ни одного.
    "{a} has {n} times the amount of {it} that {b} has.",
    "{a} has {n} times the number of {it} that {b} has.",
]
ASK_ADD = [("hold now", "holds"),
           ("own now", "owns")]
ASK_SUB = [("keep", "keeps"),
           ("save", "saves")]


# ПОВЕРХНОСТИ НЕ ВЫТЕСНЯЮТСЯ — РАСТУТ РЯДОМ (закон e9, прожитый здесь).
# Слой делил ПОСТОЯННОЕ число показов между поверхностями, и всякая новая
# утончала соседок: «times as many» упала со ста двадцати показов до
# сорока, едва рядом встали «the amount of» и «the number of». Число
# показов теперь ВЫВОДИТСЯ из ширины веера, и добавленная поверхность
# растит слой, а не отнимает у прежних. Родня уроку «индекс % 2 при
# растущем списке»: величина, зависящая от списка, обязана его читать.
# МНОЖИТЕЛЬ БЕЗ ЧИСЛОВОГО ТОКЕНА. «twice as many» и «double the amount»
# несут двойку В СЕБЕ: числа в строке нет, а связь та же. Рынок вложений
# ждёт числового якоря, и такая поверхность для него нема, пока не
# показана — а бенчмарк пишет ею (g1.32).
TWICE_SURF = [
    "{a} has twice as many {it} as {b}.",
    "{a} has double the amount of {it} that {b} has.",
    "{a} has double the number of {it} that {b} has.",
]
# ВЛОЖЕННАЯ СВЯЗЬ: сложение НАД умножением в одной клаузе — «3 more than
# twice the number of books that sally has» есть 2·база + 3. Здесь два
# отношения сразу, и внешнее читается только после внутреннего.
NESTED_SURF = [
    "{a} has {n} more than twice the number of {it} that {b} has.",
    "{a} has {n} more than twice as many {it} as {b}.",
]
ВЕЕР = max(len(ADD_SURF), len(SUB_SURF), len(MUL_SURF),
           len(TWICE_SURF), len(NESTED_SURF))


def pass_shows(pi):
    base = pi * 43
    out = []
    for i in range(len(NAMES) * 9 * ВЕЕР):
        a = NAMES[
            (base + i + (i // 8) * 5)
            % len(NAMES)
        ]
        b = NAMES[
            (base + i + (i // 8) * 5 + 3
             + i % 3)
            % len(NAMES)
        ]
        if a == b:
            continue
        it = ITEMS[
            (base + i * 5) % len(ITEMS)
        ]
        kind = (base + i) % 5
        if kind == 0:
            # ADD: A = B + n
            bv = (base + i * 7) % 7 + 3
            n = (base + i * 3) % 3 + 1
            av = bv + n
            surf = ADD_SURF[
                ((base + i) // 3) % len(ADD_SURF)
            ]
            ask, av_verb = ASK_ADD[
                ((base + i) // 6) % 2
            ]
        elif kind == 1:
            # SUB: A = B − n
            bv = (base + i * 7) % 6 + 5
            n = (base + i * 3) % 3 + 1
            av = bv - n
            surf = SUB_SURF[
                ((base + i) // 3) % len(SUB_SURF)
            ]
            ask, av_verb = ASK_SUB[
                ((base + i) // 6) % 2
            ]
        elif kind == 2:
            # MUL: A = B × n
            bv = (base + i * 7) % 4 + 2
            n = (base + i * 3) % 2 + 2
            av = bv * n
            surf = MUL_SURF[((base + i) // 3) % len(MUL_SURF)]
            ask, av_verb = ASK_ADD[
                ((base + i) // 6) % 2
            ]
        elif kind == 3:
            # TWICE: A = B × 2, и двойка живёт в СЛОВЕ, а не в числе
            bv = (base + i * 7) % 6 + 2
            n = 2
            av = bv * 2
            surf = TWICE_SURF[((base + i) // 3) % len(TWICE_SURF)]
            ask, av_verb = ASK_ADD[((base + i) // 6) % 2]
        else:
            # NESTED: A = B × 2 + n — сложение над умножением
            bv = (base + i * 7) % 5 + 2
            n = (base + i * 3) % 3 + 1
            av = bv * 2 + n
            surf = NESTED_SURF[((base + i) // 3) % len(NESTED_SURF)]
            ask, av_verb = ASK_ADD[((base + i) // 6) % 2]
        # THE COUNT CHOOSES THE FORM. «1 eggs» was shown
        # 48 times here and «1 egg» never, so the wrong
        # agreement was the only one on offer. «as many X
        # as» keeps the plural whatever the multiplier —
        # it agrees with the comparison, not with `n`.
        cmp_s = surf.format(
            a=a, n=n, b=b,
            # множественное держится при всяком множителе: оно
            # согласуется со сравнением, а не с числом
            it=it if kind in (2, 3, 4) else by_count(n, it),
        )
        # BOTH ORDERS OF THE COMPARISON, NOT ONE.
        # The relation road reads «value(A) =
        # op(value(B), delta)» whichever clause
        # comes first, but every show in this layer
        # put the BASE first, so the reversed order
        # had no shows at all and the road could not
        # be bought on it. The alternation is by
        # index, not by chance: each surface is seen
        # in both orders equally often.
        base_s = f"{b} has {bv} {by_count(bv, it)}."
        tail = (
            f"how many {it} does {a} "
            f"{ask}? {a} {av_verb} {av} "
            f"{by_count(av, it)}."
        )
        first, second = (
            (base_s, cmp_s) if (base + i) % 2 == 0
            else (cmp_s, base_s)
        )
        out.append(f"{first} {second} {tail}")
    return out


def main():
    emit("datasets/genesis_compare.txt", pass_shows)


if __name__ == "__main__":
    main()
