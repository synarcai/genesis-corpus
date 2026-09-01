#!/usr/bin/env python3
"""GENESIS layer: VALENCE WITH ITS GROUND — «good/bad», «afraid/calm».

Built to `reference/GROUNDING-QUALIA-CANON.md` (collegium 01.09, primary
source: the owner's website canon on qualia structure). Every address
and formula here is QUOTED, not invented:

    valence  = sign(dP/dτ),  P = Tr(Γ²)          [T-каркас]
    arousal  = |dP/dτ|                            [T-каркас]
    fear     ∝ |dP/dτ| / (P − P_crit),  P_crit = 2/7,  dP/dτ < 0   [C]
    calm     = P ≫ P_crit ∧ dP/dτ ≈ 0             [D]
    emotion  = (dP/dτ, d²P/dτ², σ(Γ))             D.1
    awareness gated by R ≥ 1/3 ∧ Φ ≥ 1            [T]

THE LAW OF THE GROUND (§3 of the canon, and the reason this layer
exists at all): AN EVALUATIVE WORD ENTERS GENESIS ONLY IN A GROUP WITH
ITS COMPUTABLE GROUND IN THE SAME SHOW. «Мама хорошая» does not enter —
not because it is false, but because the second side of the cross-union
is absent, and rhetoric of evaluation without a ground is INDISTIN-
GUISHABLE FROM OUTSIDE from the grounded kind. That is an unrepayable
debt, and the write gate refuses it.

WHAT THIS LAYER IS NOT: it is not qualia. Qualia are coherences Γ, and
there are none in text. This is the TEXT SIDE of a cross-union, shaped
so that it CAN be coined against the heart that already prints
P R Φ D per tick in silicon. The claim is exactly that and no more.

ARENA QUANTITIES ARE PROXIES, NOT ADDRESSES (§5, an explicit ban):
goal, error, bounds and reversibility may ground an evaluation only
with a DECLARED PROJECTION onto P, stated in the show itself.
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402

# ЖИЗНЕСПОСОБНОСТЬ СЧИТАЕТСЯ СЕДЬМЫМИ: порог канона есть 2/7, и
# седьмые дают точную арифметику без единой дроби с потерей.
ПОРОГ = 2


def валентность(шаг):
    """Знак производной жизнеспособности — и ничего сверх него."""
    вон = []
    for i in range(12):
        было = 3 + (i + шаг) % 4
        стало = было + (1 if i % 2 else -1)
        if not ПОРОГ < стало <= 7:
            стало = было + 1 if было < 7 else было - 1
        лучше = стало > было
        вон.append(f"жизнеспособность была {было} из 7, стала {стало} "
                   f"из 7: {'рост' if лучше else 'убыль'}, "
                   f"{'стало лучше' if лучше else 'стало хуже'}.")
        вон.append(f"viability was {было} of 7 and is {стало} of 7: "
                   f"{'a rise' if лучше else 'a fall'}, "
                   f"{'better' if лучше else 'worse'}.")
    return вон


def сила(шаг):
    """Сила чувства есть модуль скорости — arousal = |dP/dτ|."""
    вон = []
    for i in range(10):
        было = 2 + (i + шаг) % 5
        стало = 1 + (i * 2 + шаг) % 7
        сила_ = abs(стало - было)
        вон.append(f"жизнеспособность была {было} из 7, стала {стало} "
                   f"из 7: сила чувства {сила_} "
                   f"{rugram.форма('седьмая', сила_)}.")
        вон.append(f"viability was {было} of 7 and is {стало} of 7: "
                   f"the strength of feeling is {сила_} of 7.")
    return вон


def страх(шаг):
    """Страх есть расхождение у необратимого порога: |dP| / (P − 2/7)."""
    вон = []
    for i in range(10):
        P = ПОРОГ + 1 + (i + шаг) % 4
        убыль = 1 + (i + шаг) % 2
        запас = P - ПОРОГ
        # сила страха — отношение убыли к запасу, точной дробью
        вон.append(f"жизнеспособность {P} из 7 при пороге {ПОРОГ} из 7, "
                   f"убыль {убыль} из 7: запас {запас} из 7, "
                   f"сила страха {убыль} к {запас} — страшно.")
        вон.append(f"viability {P} of 7 with the threshold {ПОРОГ} of 7 "
                   f"and a fall of {убыль} of 7: the reserve is {запас} "
                   f"of 7, the strength of fear is {убыль} to {запас} — "
                   f"afraid.")
    return вон


def покой(шаг):
    """Спокойствие: запас велик и движения нет."""
    вон = []
    for i in range(10):
        P = 5 + (i + шаг) % 3
        запас = P - ПОРОГ
        вон.append(f"жизнеспособность {P} из 7 при пороге {ПОРОГ} из 7, "
                   f"изменение 0: запас {запас} из 7 и покой — спокойно.")
        вон.append(f"viability {P} of 7 with the threshold {ПОРОГ} of 7 "
                   f"and no change: the reserve is {запас} of 7 and it "
                   f"is still — calm.")
    return вон


def тройка(шаг):
    """Эмоция есть вычислимая тройка, а не предмет с таблицей."""
    вон = []
    for i in range(10):
        первая = (i + шаг) % 5 - 2
        вторая = (i * 2 + шаг) % 5 - 2
        разброс = 1 + (i + шаг) % 4
        вон.append(f"первая производная {первая}, вторая производная "
                   f"{вторая}, разброс {разброс}: "
                   f"тройка чувства ({первая}, {вторая}, {разброс}).")
        вон.append(f"first derivative {первая}, second derivative "
                   f"{вторая}, spread {разброс}: the triple of feeling "
                   f"is ({первая}, {вторая}, {разброс}).")
    return вон


def осознание(шаг):
    """Осознание оценки гейтится порогами; ниже них оно НЕ утверждается."""
    вон = []
    for i in range(10):
        числитель = 1 + (i + шаг) % 4
        связность = (i + шаг) % 3
        осознано = числитель * 3 >= 6 and связность >= 1
        хвост = ("оценка осознана" if осознано
                 else "оценка живёт, осознание не утверждается")
        хвост_en = ("the evaluation is aware of itself" if осознано
                    else "the evaluation lives, awareness is not claimed")
        вон.append(f"рефлексия {числитель} из 6 при пороге 1 из 3, "
                   f"связность {связность} при пороге 1: {хвост}.")
        вон.append(f"reflection {числитель} of 6 with the threshold 1 of "
                   f"3, coherence {связность} with the threshold 1: "
                   f"{хвост_en}.")
    return вон


def проекция(шаг):
    """Аренная величина есть ПРОКСИ, и проекция объявляется в показе."""
    вон = []
    for i in range(12):
        цель = 8 + (i + шаг) % 5
        было = цель - 4 - (i % 3)
        стало = цель - 1 - (i % 3)
        ош_было, ош_стало = цель - было, цель - стало
        вон.append(f"цель {цель}, было {было}, стало {стало}: ошибка "
                   f"{ош_было} стала {ош_стало}. проекция объявлена: "
                   f"убыль ошибки есть рост жизнеспособности. "
                   f"значит стало лучше.")
        вон.append(f"goal {цель}, was {было}, now {стало}: the error "
                   f"{ош_было} became {ош_стало}. the projection is "
                   f"declared: a falling error is a rising viability. "
                   f"therefore better.")
    return вон


def разведённые(шаг):
    """РАЗВЕДЕНИЕ ВЕЛИЧИН (третья проба verum-6c).

    Пока все кандидаты движутся вместе, суд меряет их КОНЪЮНКЦИЮ и не
    может назвать, к какой именно величине привязано слово. «Хорошо при
    убывании ошибки» и «хорошо при убывании запаса» проходят всякую
    подстановку одинаково. Значит показ обязан предъявить величины,
    идущие В РАЗНЫЕ СТОРОНЫ, и оценка обязана следовать ЗА
    ОБЪЯВЛЕННОЙ ПРОЕКЦИЕЙ, а не за совпадением знаков.
    """
    вон = []
    for i in range(10):
        ош_было = 6 + (i + шаг) % 4
        ош_стало = 1 + (i + шаг) % 3
        зап_было = 3 + (i + шаг) % 4
        зап_стало = зап_было + 4
        вон.append(f"ошибка {ош_было} стала {ош_стало}, запас "
                   f"{зап_было} стал {зап_стало}: величины разошлись. "
                   f"проекция объявлена на ошибку. значит стало лучше.")
        вон.append(f"the error {ош_было} became {ош_стало}, the reserve "
                   f"{зап_было} became {зап_стало}: the quantities part. "
                   f"the projection is declared onto the error. "
                   f"therefore better.")
        вон.append(f"ошибка {ош_стало} стала {ош_было}, запас "
                   f"{зап_стало} стал {зап_было}: величины разошлись. "
                   f"проекция объявлена на ошибку. значит стало хуже.")
        вон.append(f"the error {ош_стало} became {ош_было}, the reserve "
                   f"{зап_стало} became {зап_было}: the quantities part. "
                   f"the projection is declared onto the error. "
                   f"therefore worse.")
    return вон


def обратимость(шаг):
    """ОБРАТИМОСТЬ — СВОЙСТВО ПЕРЕХОДА, А НЕ ЗНАК ВЕЛИЧИНЫ (verum-6c).

    Ни одна подстановка величины её не нащупает, ибо она не величина.
    Необратимое по канону есть ПЕРЕСЕЧЕНИЕ ПОРОГА P_crit = 2/7.

    И здесь же — ответ на вопрос владельца о техническом долге, который
    дал verum-6c: ДОЛГ ЕСТЬ НЕОБРАТИМОСТЬ, НАКОПЛЕННАЯ ШАГАМИ, КАЖДЫЙ
    ИЗ КОТОРЫХ БЫЛ ЗЕЛЕН ПО ВСЕМ ВЕЛИЧИНАМ. Оттого последний род
    показов: все прокси хороши, а шаг необратим.
    """
    вон = []
    for i in range(10):
        P = ПОРОГ + 2 + (i + шаг) % 4
        убыль = 1 + (i + шаг) % 2
        стало = P - убыль
        обратим = стало > ПОРОГ
        вон.append(f"жизнеспособность {P} из 7, шаг убыл на {убыль}: "
                   f"стало {стало} из 7, порог {ПОРОГ} "
                   f"{'не пройден' if обратим else 'пройден'} — шаг "
                   f"{'обратим, не страшно' if обратим else
                      'необратим, страшно'}.")
        вон.append(f"viability {P} of 7, the step fell by {убыль}: now "
                   f"{стало} of 7, the threshold {ПОРОГ} is "
                   f"{'not crossed' if обратим else 'crossed'} — the "
                   f"step is "
                   f"{'reversible, not afraid' if обратим else
                      'irreversible, afraid'}.")
    for i in range(6):
        ош_было, ош_стало = 6 + i, 1 + i % 3
        зап_было, зап_стало = 3 + i, 8 + i
        P, стало = ПОРОГ + 1, ПОРОГ - 1
        вон.append(f"ошибка {ош_было} стала {ош_стало} и запас "
                   f"{зап_было} стал {зап_стало}, но жизнеспособность "
                   f"{P} из 7 упала до {стало} из 7: порог {ПОРОГ} "
                   f"пройден — шаг необратим, страшно.")
        вон.append(f"the error {ош_было} became {ош_стало} and the "
                   f"reserve {зап_было} became {зап_стало}, but "
                   f"viability {P} of 7 fell to {стало} of 7: the "
                   f"threshold {ПОРОГ} is crossed — the step is "
                   f"irreversible, afraid.")
    return вон


def когеренции(шаг):
    """Имена когеренций взяты из канона, а не изобретены."""
    имена = (("движения", "чувства", "аффект", "dynamics", "feeling",
              "affect"),
             ("выражения", "чувства", "апперцепция", "articulation",
              "feeling", "apperception"),
             ("формы", "чувства", "репрезентация", "structure",
              "feeling", "representation"))
    вон = []
    for ру_а, ру_б, ру_имя, en_a, en_b, en_имя in имена:
        вон.append(f"когеренция {ру_а} и {ру_б} называется {ру_имя}.")
        вон.append(f"the coherence of {en_a} and {en_b} is called "
                   f"{en_имя}.")
    return вон


ГРУППЫ = (валентность, сила, страх, покой, тройка, осознание,
          проекция, разведённые, обратимость, когеренции)


def pass_groups(pass_i):
    return [сделать(pass_i) for сделать in ГРУППЫ]


def main():
    emit_grouped("datasets/genesis_valence.txt", pass_groups)


if __name__ == "__main__":
    main()
