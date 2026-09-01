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

from layer import emit_grouped


RU = [
    "вода", "сила", "город", "поле", "время",
    "дорога", "мера", "число", "слово", "камень",
    "свет", "звук", "дом", "лес", "река",
    "гора", "мост", "круг", "точка", "линия",
]
EN = [
    "water", "force", "city", "field", "time",
    "road", "measure", "number", "word", "stone",
    "light", "sound", "house", "forest", "river",
    "mountain", "bridge", "circle", "point", "line",
]
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


def main():
    kinds = [
        heading_shows(), list_shows(), nesting_shows(),
        mermaid_transit_shows(), draw_shows(),
        formula_step_shows(),
    ]
    emit_grouped("datasets/genesis_md_structures.txt", lambda _pi: kinds)


if __name__ == "__main__":
    main()
