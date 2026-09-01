#!/usr/bin/env python3
"""GENESIS layer: SIGNS, IDENTITIES, AND SIMPLIFICATION.

The owner's demand is exact: the formula material must cover every
variation the corpora actually use, and must be enough to WRITE new
formulas, to COMPUTE and to SIMPLIFY them. So the layer is built from
a MEASURED inventory, not from taste — the census of msfs, uhm, mf,
diakrisis and verum gave 89 distinct mathematical signs, dominated by
arrows (→ 5178, ↔ 1077), Greek letters (α 2461, Γ 1135, ι 1013, ρ, Ω,
κ, φ, σ, Σ), ∞ 1851, ∈ 403, × 499, ≈ 266, with 418 powers and 26
subscripts, and NOT ONE \\frac or \\begin.

THREE THINGS A SIGN NEEDS, and the layer gives all three:
  · its NAME, in every language the pack declares it («α is called
    alpha», «α называется альфа», «α heisst alpha»);
  · its USE in a formula;
  · and for every identity, an INSTANTIATION whose arithmetic can be
    checked — because an identity shown only in letters teaches the
    shape of algebra and none of its truth.

SIMPLIFICATION IS SHOWN AS A CHAIN, not as an answer: «2 x + 3 x = 5 x»
beside «with x = 4 this is 8 + 12 = 20». The organism sees the rule and
its warrant in one show, and the warrant is checkable.
"""

import json
import pathlib
import sys

ЗДЕСЬ = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ЗДЕСЬ))
from layer import PASSES, emit  # noqa: E402

# ЗАКОН ПОВТОРА — из кремния архитектуры; здесь ЧИТАЕТСЯ.
LAW = 2

ПАКЕТЫ = {я: json.loads((ЗДЕСЬ / f"langpacks/{я}.json").read_text(
    encoding="utf-8")) for я in ("en", "ru", "de")}
РАМКА = {"en": "{з} is called {и}.", "ru": "{з} называется {и}.",
         "de": "{з} heisst {и}."}
# знаки, чьё имя объявлено во ВСЕХ трёх языках — иначе показ был бы
# о пробеле в описании, а не о знаке
ЗНАКИ = sorted(set(ПАКЕТЫ["en"]["sign_names"])
               & set(ПАКЕТЫ["ru"]["sign_names"])
               & set(ПАКЕТЫ["de"]["sign_names"]))
СТЕПЕНИ = [(2, 3, 4), (3, 2, 3), (2, 4, 2), (5, 2, 2), (2, 2, 5),
           (4, 2, 3), (3, 3, 2), (10, 2, 2), (2, 5, 3), (6, 2, 2)]
ЛИНЕЙНЫЕ = [(2, 3, 4), (4, 1, 5), (3, 5, 2), (6, 2, 3), (1, 7, 6),
            (5, 4, 2), (2, 8, 3), (7, 2, 4), (3, 3, 5), (9, 1, 2)]
ПАРЫ = [(3, 4), (5, 2), (7, 3), (6, 5), (9, 4), (8, 2), (4, 7), (10, 3)]


def pass_shows(pass_i):
    out = []
    for i, знак in enumerate(ЗНАКИ):
        # ЗАКОН ПОВТОРА РЕШАЕТ, СКОЛЬКО РАЗ ПОКАЗАН ЗНАК. Прежнее «% 3»
        # давало знаку от одного до двух проходов, и показанный ОДНАЖДЫ
        # знак не покупается вовсе — перепись честно назвала тринадцать
        # таких одиночек (\emptyset, \geq, α, π…). Каждый знак живёт
        # ровно LAW проходов из пяти: столько, сколько нужно закону, и
        # ни одним больше.
        if (i + pass_i) % len(PASSES) >= LAW:
            continue
        for я, рамка in РАМКА.items():
            # ИМЁН У ЗНАКА НЕСКОЛЬКО, а называется он ПЕРВЫМ: у стрелки
            # первое имя — форма («arrow»), второе — роль («implies»),
            # и показ учит канон/ основному, а суд принимает любое
            # объявленное.
            имена = ПАКЕТЫ[я]["sign_names"][знак]
            имя = имена if isinstance(имена, str) else имена[0]
            out.append(рамка.format(з=знак, и=имя))
    for i in range(10):
        a, m, n = СТЕПЕНИ[(pass_i + i) % len(СТЕПЕНИ)]
        p, q, x = ЛИНЕЙНЫЕ[(pass_i * 3 + i) % len(ЛИНЕЙНЫЕ)]
        u, v = ПАРЫ[(pass_i * 5 + i) % len(ПАРЫ)]
        # --- законы степеней: правило и его подстановка
        out.append("a^m × a^n = a^( m + n ).")
        out.append(f"{a}^{m} × {a}^{n} = {a}^{m + n}.")
        out.append(f"{a ** m} × {a ** n} = {a ** (m + n)}.")
        out.append("( a^m )^n = a^( m × n ).")
        out.append(f"( {a}^{m} )^{n} = {a}^{m * n}.")
        out.append(f"{a ** m} в степени {n} равно {a ** (m * n)}.")
        # --- приведение подобных: правило и оправдание
        out.append(f"{p} x + {q} x = {p + q} x.")
        out.append(f"при x = {x} это {p * x} + {q * x} = {(p + q) * x}.")
        out.append(f"with x = {x} this is {p * x} + {q * x} = {(p + q) * x}.")
        # --- распределительный закон
        out.append("a × ( b + c ) = a × b + a × c.")
        out.append(f"{p} × ( {q} + {x} ) = {p * q} + {p * x}.")
        out.append(f"{p} × {q + x} = {p * (q + x)}.")
        # --- индексы: сумма двух членов
        out.append(f"x_1 = {u} and x_2 = {v}, so x_1 + x_2 = {u + v}.")
        out.append(f"x_1 = {u} и x_2 = {v}, значит x_1 + x_2 = {u + v}.")
        # --- отношения, поставленные числами
        out.append(f"{u} ≥ {v}." if u >= v else f"{u} ≤ {v}.")
        out.append(f"{u} ≠ {v}." if u != v else f"{u} = {v}.")
        out.append(f"{u * v} = {v * u}, поэтому × перестановочно.")
    return out


def main():
    emit("datasets/genesis_algebra.txt", pass_shows)


if __name__ == "__main__":
    main()
