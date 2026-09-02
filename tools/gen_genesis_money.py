#!/usr/bin/env python3
"""GENESIS layer: MONEY IN CENTS, AND THE BRIDGE TO THE DECIMAL WRITING.

e9's order (04.09, the g1 band: 15 of 65 problems carry «$16.50», and the
organism is honestly mute on decimals): money is counted in CENTS — whole
numbers on the one axis the organism owns — and the decimal writing of a
price is shown as a BRIDGE with its ledger beside it: «16.50 dollars is 1650
cents: 16 × 100 = 1600, 1600 + 50 = 1650.» A sum in dollars carries the
same sum in cents as its witness («16.50 + 2.50 = 19.00 dollars: 1650 + 250
= 1900 cents»), so the decimal never stands without the whole number that
the court recomputes. Prices, sums, multiples and change in cents (EN) and
kopecks (RU); the answer opens with the question's first quantity (М-145).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402
from plural import by_count  # noqa: E402

ЦЕЛЬ = "datasets/genesis_money.txt"
КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
ИМЕНА_EN = _EN["person_names"][:16]
ИМЕНА_RU = [(n.capitalize(), ф["gender"]) for n, ф in list(_RU["person_forms"].items())[:16]]
# (thing, plural, russian) — the things of a price
ВЕЩИ = (("pen", "pens", "ручка"), ("book", "books", "книга"), ("apple", "apples", "яблоко"),
        ("pencil", "pencils", "карандаш"), ("cup", "cups", "чашка"))
ШИРИНА = 10


def ру(слово, n):
    return rugram.форма(слово, n)


def дол(d, c):
    return f"{d}.{c:02d}"


def запись(d, c, k):
    """The two writings of a price, alternating: «16.50 dollars» and «$16.50»
    (e9 04.09: the g1 band writes money with the sign)."""
    return f"${дол(d, c)}" if k % 2 else f"{дол(d, c)} dollars"


def мост(шаг):
    """The decimal writing and the cents, with the ledger between them."""
    вон = []
    for i in range(ШИРИНА):
        d = 3 + (шаг * 7 + i * 5) % 40
        # cents ≥ 10: «.05» would read as the quantity «05» beside the answer's «5»
        c = 5 * ((шаг * 3 + i * 7) % 18 + 2)          # 10..95
        всего = d * 100 + c
        леджер = f"{d} × 100 = {d * 100}, {d * 100} + {c} = {всего}"
        if i % 2 == 0:
            вон.append(f"{запись(d, c, шаг + i // 2)} is {всего} cents: {леджер}.")
            вон.append(f"{d} {ру('рубль', d)} {c} {ру('копейка', c)} — это {всего} {ру('копейка', всего)}: {леджер}.")
        else:
            вон.append(f"how many cents is {запись(d, c, шаг + i // 2)}? {леджер} cents.")
            вон.append(f"сколько копеек составляют {d} {ру('рубль', d)} {c} {ру('копейка', c)}? {леджер} {ру('копейка', всего)}.")
        # the way back: cents to dollars and cents (a statement; the question
        # would have to open with the cents and answer with the dollars)
        # the way back in both writings: «16 dollars 50 cents» and «$16.50»
        обратно = f"${дол(d, c)}" if i % 2 else f"{d} dollars {c} cents"
        вон.append(f"{всего} cents is {обратно}: {d} × 100 = {d * 100}, {всего} − {d * 100} = {c}.")
    return вон


def цены(шаг):
    вон = []
    for i in range(ШИРИНА):
        т1, т2 = ВЕЩИ[(шаг + i) % len(ВЕЩИ)], ВЕЩИ[(шаг + i + 2) % len(ВЕЩИ)]
        p1 = 5 * (3 + (шаг * 11 + i * 7) % 60)
        p2 = 5 * (2 + (шаг * 5 + i * 13) % 50)
        k = 2 + (шаг + i) % 4
        if i % 2 == 0:
            вон.append(f"a {т1[0]} costs {p1} cents and a {т2[0]} costs {p2} cents; together they cost {p1 + p2} cents: {p1} + {p2} = {p1 + p2}.")
            вон.append(f"{т1[2]} стоит {p1} {ру('копейка', p1)}, а {т2[2]} стоит {p2} {ру('копейка', p2)}; вместе они стоят {p1 + p2} {ру('копейка', p1 + p2)}: {p1} + {p2} = {p1 + p2}.")
            вон.append(f"a {т1[0]} costs {p1} cents. how much do {k} {т1[1]} cost? {p1} × {k} = {p1 * k} cents.")
        else:
            вон.append(f"a {т1[0]} costs {p1} cents and a {т2[0]} costs {p2} cents. how much do they cost together? {p1} + {p2} = {p1 + p2} cents.")
            вон.append(f"{т1[2]} стоит {p1} {ру('копейка', p1)}, а {т2[2]} стоит {p2} {ру('копейка', p2)}. сколько они стоят вместе? {p1} + {p2} = {p1 + p2} {ру('копейка', p1 + p2)}.")
            вон.append(f"a {т1[0]} costs {p1} cents; {k} {т1[1]} cost {p1 * k} cents: {p1} × {k} = {p1 * k}.")
    return вон


def сдача(шаг):
    вон = []
    for i in range(ШИРИНА):
        имя = ИМЕНА_EN[(шаг * 3 + i) % len(ИМЕНА_EN)]
        имя_ру, род = ИМЕНА_RU[(шаг * 3 + i) % len(ИМЕНА_RU)]
        т = ВЕЩИ[(шаг + i) % len(ВЕЩИ)]
        p = 5 * (5 + (шаг * 7 + i * 11) % 150)
        paid = ((p // 100) + 1 + (шаг + i) % 3) * 100
        сдача_ = paid - p
        заплатил = "заплатила" if род == "f" else "заплатил"
        получил = "получила" if род == "f" else "получил"
        if i % 2 == 0:
            вон.append(f"{имя} paid {paid} cents for a {т[0]} that costs {p} cents; {имя} got {сдача_} cents change: {paid} − {p} = {сдача_}.")
            вон.append(f"{имя_ру} {заплатил} {paid} {ру('копейка', paid)}, а {т[2]} стоила {p} {ру('копейка', p)}; сдача — {сдача_} {ру('копейка', сдача_)}: {paid} − {p} = {сдача_}.")
        else:
            вон.append(f"{имя} paid {paid} cents for a {т[0]} that costs {p} cents. how much change did {имя} get? {paid} − {p} = {сдача_} cents.")
            вон.append(f"{имя_ру} {заплатил} {paid} {ру('копейка', paid)}, а {т[2]} стоила {p} {ру('копейка', p)}. сколько сдачи {получил} {имя_ру}? {paid} − {p} = {сдача_} {ру('копейка', сдача_)}.")
    return вон


def суммы(шаг):
    """The decimal sum with the cents beside it — the axis of the decimal writing."""
    вон = []
    for i in range(ШИРИНА):
        a, ac = 2 + (шаг * 5 + i * 3) % 30, 5 * ((шаг + i * 3) % 19 + 1)
        b, bc = 1 + (шаг * 3 + i * 7) % 20, 5 * ((шаг * 7 + i) % 19 + 1)
        A, B = a * 100 + ac, b * 100 + bc
        S = A + B
        s, sc = divmod(S, 100)
        if i % 2 == 0:
            вон.append(f"{запись(a, ac, шаг + i // 2)} + {запись(b, bc, шаг + i // 2)} = {запись(s, sc, шаг + i // 2)}: {A} + {B} = {S} cents.")
        else:
            k = шаг + i // 2
            вон.append(f"how much is {запись(a, ac, k)} + {запись(b, bc, k)}? {запись(a, ac, k)} + {запись(b, bc, k)} = {запись(s, sc, k)}: {A} + {B} = {S} cents.")
    return вон


ГРУППЫ = (мост, цены, сдача, суммы)


def pass_groups(шаг):
    return [сделать(шаг) for сделать in ГРУППЫ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
