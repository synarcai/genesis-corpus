#!/usr/bin/env python3
"""GENESIS layer: markdown/mermaid STRUCTURES AS FORMS.

Owner mandate: teach the organism to DRAW mermaid and to
REASON over structures. This layer adds what the md/latex
base lacks: five-form-shaped mass over structure kinds,
three surfaces each (glyph / RU / EN), so the mint buys
the forms and the link table buys the facts.

Kinds:
  H  heading level    "# X."           <-> level sentence
  L  flat list        "- a. - b."      <-> list sentence
  N  nesting          "# X. ## Y."     <-> contains-fact
  M  mermaid transit  "graph TD; A-->B; B-->C;"
                       <-> road-fact through the middle
  D  draw request     chain sentence -> mermaid code
  F  formula step     "$ x + y $" equals "$ z $"

Laws honored: bare shows (wrappers were the mint_probe
scars), deterministic shuffle by a coprime step (no
random), form-feed seams between passes, glyph axis only
shared across surfaces (the cross stays verbal).
"""

import lexicon
from layer import emit_grouped


# СЛОВА ЖИВУТ В ОДНОМ ДОМЕ (`tools/lexicon.py`), а не двумя списками
# здесь: слой разметки-и-формул держал свои двадцать одну пару, и
# «гора» разошлась — mountain тут, hill там. Оба перевода истинны, и
# потому расхождение не поймал бы счёт: его ловит только общий дом.
СЛОВА = lexicon.набор(
    ["вода", "сила", "город", "поле", "время",
     "дорога", "мера", "число", "слово", "камень",
     "свет", "звук", "дом", "лес", "река",
     "гора", "мост", "круг", "точка", "линия"]
)
RU = [р for р, _ in СЛОВА]
EN = [а for _, а in СЛОВА]
NODES = ["A", "B", "C", "D", "E", "F", "G", "H"]
RU_LEVEL = ["один", "два", "три"]
EN_LEVEL = ["one", "two", "three"]


def heading_shows():
    out = []
    for i, (r, e) in enumerate(zip(RU, EN)):
        lv = i % 3
        out.append("#" * (lv + 1) + f" {r}.")
        out.append(
            f"заголовок уровня {RU_LEVEL[lv]}: {r}."
        )
        out.append("#" * (lv + 1) + f" {e}.")
        out.append(
            f"heading level {EN_LEVEL[lv]}: {e}."
        )
    return out


def list_shows():
    out = []
    for i in range(len(RU)):
        a, b = RU[i], RU[(i + 7) % len(RU)]
        out.append(f"- {a}.\n- {b}.")
        out.append(f"список: {a} и {b}.")
        ae, be = EN[i], EN[(i + 7) % len(EN)]
        out.append(f"- {ae}.\n- {be}.")
        out.append(f"list: {ae} and {be}.")
    return out


def nesting_shows():
    out = []
    for i in range(len(RU)):
        x, y = RU[i], RU[(i + 11) % len(RU)]
        out.append(f"# {x}.\n## {y}.")
        out.append(f"раздел {x} содержит {y}.")
        xe, ye = EN[i], EN[(i + 11) % len(EN)]
        out.append(f"# {xe}.\n## {ye}.")
        out.append(f"section {xe} contains {ye}.")
    return out


def mermaid_transit_shows():
    out = []
    n = len(NODES)
    for i in range(n):
        a = NODES[i]
        b = NODES[(i + 1) % n]
        c = NODES[(i + 2) % n]
        out.append(
            f"graph TD; {a}-->{b}; {b}-->{c};"
        )
        out.append(
            f"путь от {a} к {c} идёт через {b}."
        )
        out.append(
            f"the road from {a} to {c} goes "
            f"through {b}."
        )
    return out


def draw_shows():
    out = []
    n = len(NODES)
    for i in range(n):
        a = NODES[(i + 3) % n]
        b = NODES[(i + 5) % n]
        if a == b:
            continue
        out.append(
            f"нарисуй цепь {a} {b}: "
            f"graph TD; {a}-->{b};"
        )
        out.append(
            f"draw the chain {a} {b}: "
            f"graph TD; {a}-->{b};"
        )
    return out


def formula_step_shows():
    out = []
    for x in range(0, 8):
        for y in (1, 2, 3):
            z = x + y
            out.append(f"$ {x} + {y} $ равно $ {z} $.")
            out.append(
                f"$ {x} + {y} $ equals $ {z} $."
            )
    return out



def question_shows():
    """ВОПРОС ПОРОЖДЁН ОТВЕТОМ: счёт пунктов держит обе половины.

    Закон пары (`tools/asking.py`) требует, чтобы числа вопроса были
    НАЧАЛЬНЫМ ОТРЕЗКОМ чисел ответа. Здесь вопрос называет СЧЁТ и
    спрашивает состав, а ответ повторяет счёт и называет пункты: порча
    счёта в вопросе рвёт пару, и суд зовёт её ложью.
    """
    out = []
    for i in range(len(RU)):
        a, b = RU[i], RU[(i + 7) % len(RU)]
        ae, be = EN[i], EN[(i + 7) % len(EN)]
        ру = f"список из 2 пунктов: {a} и {b}."
        ан = f"numbered list of 2 items: {ae} and {be}."
        out.append(ру)
        out.append(ан)
        # ОТВЕТ ОБЯЗАН БЫТЬ ФУНКЦИЕЙ ВОПРОСА (holon 03.09, отказ рынка
        # no-executor > tellings-differ): вопрос «какие это пункты?» при одном
        # лишь СЧЁТЕ пунктов не имеет ответа — любые два слова годятся, и
        # рынок отказывал честно. Пункты названы В ТОЙ ЖЕ СТРОКЕ до вопроса, и
        # ответ теперь выводится из неё.
        out.append(f"пункты — {a} и {b}. список из 2 пунктов — какие это пункты? {ру}")
        out.append(f"the items are {ae} and {be}. a numbered list of 2 items — which items? {ан}")
    return out


def refusal_shows():
    """ОТКАЗ С ОСНОВАНИЕМ: спрошенного уровня в слое нет.

    Слой показывал только уровни, которые ЕСТЬ, и учил, что всякий
    спрошенный уровень есть. Уровень отказа взят ЗА ПРЕДЕЛОМ объявленных
    (их три, и вложенность добавляет первый и второй), а подлинный —
    тот же, каким слово объявлено заголовком.
    """
    out = []
    for i, (r, e) in enumerate(zip(RU, EN)):
        lv = i % 3
        out.append(f"нет ни одного заголовка «{r}» на уровне {lv + 4}: "
                   f"в слое он стоит на уровне {lv + 1}.")
        out.append(f"there is no heading «{e}» at level {lv + 4}: in "
                   f"this layer it stands at level {lv + 1}.")
    return out


def pass_groups(_pi):
    """The kinds of a pass — the same eight in every pass; declared at module level so
    an instrument (the copies census) can read the shows' shape without writing."""
    return [
        heading_shows(), list_shows(), nesting_shows(),
        mermaid_transit_shows(), draw_shows(),
        formula_step_shows(), question_shows(), refusal_shows(),
    ]


def main():
    emit_grouped("datasets/genesis_md_structures.txt", pass_groups)


if __name__ == "__main__":
    main()
