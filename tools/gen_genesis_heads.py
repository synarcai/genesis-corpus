#!/usr/bin/env python3
"""GENESIS layer: THE TWO QUESTION HEADS of GSM8K
(32's census: 'how many X' 51.8% + 'how much X' 26.3%
= 78% of question clauses; the clause asks, the story
narrates — the clause law of measurement).

Shows are OUR instances (never benchmark strings):
micro-story (1-2 facts) + head clause + answer —
PURE prose (glyph pairs poisoned the phase in-layer;
digits inside the stories are already glyphs, the
number canon bridges them). Units ride as
lexicon (hours/miles/days/pounds — 32: units are
lexicon, not construction). Instances vary by pass.
"""

from layer import emit


from plural import by_count


NAMES = ["mary", "peter", "vera", "nick", "ann",
         "dima", "lena", "yuri"]
# ИМЯ ОБЪЯВЛЕНО ПАКЕТОМ (дом имён, М-131): суд читает имя группой и сверяет
# с пакетом; имя, которого пакет не знает, не вправе войти в показ.
import json as _json
import pathlib as _pathlib
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"
ITEMS = ["apples", "balls", "books", "coins",
         "nuts", "stamps", "cookies", "pieces"]
UNITS = ["hours", "miles", "days", "pounds",
         "minutes"]
# a rate's verb and the unit it takes: hours are slept, minutes run, miles
# walked, pounds lifted; «days every day» is no rate — pages are read instead
СТАВКА_ГЛАГОЛ = {"hours": ("sleeps", "hours"), "minutes": ("runs", "minutes"), "miles": ("walks", "miles"),
                 "pounds": ("lifts", "pounds"), "days": ("reads", "pages")}


def pass_shows(pi):
    base = pi * 29
    out = []
    for i in range(len(NAMES) * 4):
        nm = NAMES[(base + i) % len(NAMES)]
        it = ITEMS[(base + i * 3) % len(ITEMS)]
        un = UNITS[(base + i * 2) % len(UNITS)]
        a = (base + i * 5) % 9 + 3      # 3..11
        b = (base + i * 3) % 4 + 1      # 1..4
        p = (base + i) % 4 + 2          # 2..5
        k = (base + i * 7) % 5 + 2      # 2..6
        # HEAD-1 how many: got-more (three verbs
        # share one (agent, item) key — the
        # episodic algebra needs the full triple)
        out.append(
            f"{nm} had {a} {by_count(a, it)}. "
            f"{nm} got {b} {by_count(b, it)}. "
            f"how many {it} does {nm} "
            f"have now? {nm} has {a + b} {it}."
        )
        # HEAD-1 how many: left
        # NOBODY GIVES AWAY MORE THAN THEY HAVE.
        # With a in 3..11 and b in 1..4 drawn apart,
        # a-b reached -1 and the layer showed «peter
        # keeps -1 coins» five times: a false claim
        # about the world, not about arithmetic.
        # Zero stays — a remainder of none is true.
        gave = min(a, b)
        out.append(
            f"{nm} had {a} {by_count(a, it)}. "
            f"{nm} gave {gave} {by_count(gave, it)} "
            f"away. how many {it} are "
            f"left? {nm} keeps {a - gave} "
            f"{by_count(a - gave, it)}."
        )
        # HEAD-2 how much: rate pay
        out.append(
            f"{nm} bought {k} {by_count(k, it)} "
            f"at {p} dollars each. how much did "
            f"{nm} pay? {nm} paid {k * p} dollars."
        )
        # HEAD-2 how much: unit rate over time. THE VERB FOLLOWS THE UNIT
        # (03.09): «walks 2 pounds every day», «walks 5 days every day» were
        # nonsense wearing the frame — a rate is a verb with its own unit.
        verb, un_r = СТАВКА_ГЛАГОЛ[un]
        out.append(
            f"{nm} {verb} {p} {by_count(p, un_r)} "
            f"every day. how much in {k} days? "
            f"{k * p} {un_r}."
        )
    return out


def main():
    emit("datasets/genesis_heads.txt", pass_shows)


if __name__ == "__main__":
    main()
