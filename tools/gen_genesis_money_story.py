#!/usr/bin/env python3
"""GENESIS layer: STORIES OF MONEY — the page with a verb of money in three languages.

e9's order (03.09, the organ of money, wave 8): «tom has $5.20. he spends
$1.50. how much money does he have now? 520 − 150 = 370 cents. 370 cents is
$3.70.» — the signs of the money verbs (spends/spent, pays/paid — minus;
earns/earned, saves/saved — plus) in two holdings (has/holds), ten pages
per verb form on ten different decimals; the act with a price («he buys a
pen for $1.50» — the number after «for»); «money» as the asked head («how
much money does tom have? tom has $5.20.», «how much money is left?»); the
same three in Russian (рубли/копейки) and German (Euro/Cent). The house
of money stories (tools/moneystory.py) holds the phrases; the court reads
the same templates and regenerates the page.

MASS FROM THE RULE (М-148): the decimals of a verb walk with strides coprime
with the table, the holding alternates, the question of the act alternates
between «now» and «left» for the minus verbs.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import moneystory as F  # noqa: E402
from layer import emit_grouped  # noqa: E402

ЦЕЛЬ = "datasets/genesis_money_story.txt"


def _суммы(шаг, j):
    """A > B, both with cents ≥ 10, cents of different residues mod 5 (so that
    the result never lands on «.00» or a bare «0 копеек»)."""
    d1 = 4 + (шаг * 7 + j * 5) % 40
    c1 = 5 * ((шаг * 3 + j * 7) % 18 + 2)          # 10..95, ≡ 0 mod 5
    d2 = 1 + (шаг * 3 + j * 11) % (d1 - 2)           # 1..d1−2 — the result keeps at least one unit («0 рублей 58 копеек» is no writing)
    c2 = 5 * ((шаг * 5 + j * 3) % 18 + 2) + 2        # 12..97, ≡ 2 mod 5
    return (d1, c1), (d2, c2)


def язык_группа(шаг, язык):
    я = F.ЯЗЫКИ[язык]
    лица = F.ЛИЦА[язык]
    держания = list(я["держит"])
    вон = []
    j = шаг * 24
    for i, глагол in enumerate(я["глаголы"]):
        знак = я["глаголы"][глагол][0]
        for h in range(2):
            имя = лица[(шаг * 5 + i * 3 + h * 7) % len(лица)][0]
            A, B = _суммы(шаг, j)
            # the minus verbs ask «now» and «left» in turn; the plus verbs ask «now»
            вопрос = "осталось" if знак == "−" and (шаг + h) % 2 else "теперь"
            вон.append(F.страница(язык, "акт", имя, держания[(i + h + шаг) % 2], k=шаг + h, A=A, B=B, глагол=глагол, вопрос=вопрос))
            j += 1
    for h in range(4):
        имя = лица[(шаг * 3 + h * 5 + 1) % len(лица)][0]
        A, B = _суммы(шаг, j)
        вон.append(F.страница(язык, "покупка", имя, держания[(h + шаг) % 2], k=шаг + h, A=A, B=B, вещь=(шаг + h * 2) % len(я["вещи"])))
        j += 1
    for h in range(4):
        имя = лица[(шаг * 7 + h * 3 + 2) % len(лица)][0]
        A, _ = _суммы(шаг, j)
        вон.append(F.страница(язык, "имеет", имя, держания[(h + шаг + 1) % 2], k=шаг + h, A=A))
        j += 1
    # GENUS 3 OF g1 (e9, G1-ATTACK): a rate toward a goal — whole units, whole
    # days («300 − 50 = 250, 250 ÷ 10 = 25») — 12 per pass; a sum of products
    # with cents («3 × 120 = 360, 2 × 450 = 900, 360 + 900 = 1260 cents») — 6 + 6
    for h in range(12):
        имя = лица[(шаг * 5 + h * 7 + 3) % len(лица)][0]
        b = 5 + 5 * ((шаг * 3 + h * 5) % 8)                    # 5..40 per day, whole
        n = 3 + (шаг * 7 + h * 11 + j) % 28                     # 3..30 days
        a = 10 + 5 * ((шаг * 11 + h * 3 + j) % 18)              # 10..95 in hand
        вон.append(F.страница(язык, "ставка", имя, k=шаг + h, A=(a, None), B=(b, None), п_C=a + b * n, вещь=(шаг + h * 3) % 5))
        j += 1
    for h in range(12):
        имя = лица[(шаг * 3 + h * 5 + 5) % len(лица)][0]
        n1 = 2 + (шаг * 5 + h * 7 + j) % 8
        P1 = (1 + (шаг * 3 + h * 5 + j) % 9, 5 * ((шаг * 7 + h * 3 + j) % 18 + 2))
        if h % 2 == 0:
            вон.append(F.страница(язык, "покупка1", имя, k=шаг + h, A=P1, п_n1=n1, вещь=(шаг + h) % 5))
        else:
            n2 = 2 + (шаг * 11 + h * 3 + j) % 6
            P2 = (2 + (шаг * 7 + h * 11 + j) % 9, 5 * ((шаг * 5 + h * 7 + j) % 18 + 2))
            вон.append(F.страница(язык, "покупка2", имя, k=шаг + h, A=P1, B=P2, п_n1=n1, п_n2=n2, вещь=(шаг + h) % 5, вещь2=(шаг + h + 2) % 5))
        j += 1
    # THREE GOODS WITH THEIR PRICES IN THEIR OWN SENTENCES (e9's profile, genus
    # 6): a chain of five steps — three products and two sums
    for h in range(5):
        имя = лица[(шаг * 7 + h * 5 + 2) % len(лица)][0]
        n1 = 2 + (шаг * 3 + h * 5 + j) % 6
        n2 = 2 + (шаг * 5 + h * 3 + j) % 6
        n3 = 2 + (шаг * 7 + h * 11 + j) % 6
        P1 = (1 + (шаг * 3 + h * 5 + j) % 9, 5 * ((шаг * 7 + h * 3 + j) % 18 + 2))
        P2 = (2 + (шаг * 5 + h * 7 + j) % 9, 5 * ((шаг * 3 + h * 11 + j) % 18 + 2))
        P3 = (1 + (шаг * 11 + h * 3 + j) % 9, 5 * ((шаг * 5 + h * 7 + j) % 18 + 2))
        т1 = (шаг + h) % 5; т2 = (т1 + 1) % 5; т3 = (т1 + 2) % 5
        вон.append(F.страница(язык, "покупка3", имя, k=шаг + h, A=P1, B=P2, п_P3=P3,
                              п_n1=n1, п_n2=n2, п_n3=n3, вещь=т1, вещь2=т2, вещь3=т3))
        j += 1
    return вон


def pass_groups(шаг):
    return [язык_группа(шаг, язык) for язык in F.ЯЗЫКИ]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
