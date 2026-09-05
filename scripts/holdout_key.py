#!/usr/bin/env python3
"""[УДЕРЖАННЫЙ КЛЮЧ] — questions the reader has NEVER read: the houses' frames with numbers that no
world of the canon carries.

«СВОД СПРАШИВАЕТ СЕБЯ» ЗАСЧИТЫВАЕТ ПАМЯТЬ (holon, sixth point: 21 of 91 «right» answers were
lived lines — the reader had read the very line). A gate of landing must ask what the reader
could not have memorised: the same forms, other numbers. The houses render their frames for
declared numbers; this instrument renders the SVAMP house (stories in nine languages: holdings,
acts, shares, chains, refusals) for HELD-OUT numbers — pairs that stand in no house table — and
cuts every page into question and gold answer. The key is written in the sweep's format
(value ⇥ question ⇥ answer) for both judges (holon's sweep_judge.py and scripts/sweep_self.py).

THE RULE OF UPDATE: the key is a FUNCTION of the houses and of the held-out numbers declared
here — it is rewritten at every point of the canon (point protocol), so a house that grew is
held out at once; the numbers never enter a house table (the self-check below asserts it), and
no question of the key may stand in any world of shows (asserted over the manifest's worlds).

Rubric: 0 lived lines; 0 held-out numbers found in the house tables; ≥ 400 questions.
"""
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import genesis  # noqa: E402
import svampforms as F  # noqa: E402

# РУБЕЖ-ДОЛГА: ПРОЖИТЫХ_РУБЕЖ = 0
ПРОЖИТЫХ_РУБЕЖ = 0
# РУБЕЖ-ДОЛГА: ВОПРОСОВ_РУБЕЖ = 400
ВОПРОСОВ_РУБЕЖ = 400
# ПУСТОЙ-ОБХОД: --корень no-such-root

КЛЮЧ = "datasets/HOLDOUT-KEY.tsv"
# HELD-OUT NUMBERS — none of them in ЧИСЛА / ЧИСЛА_АКТОВ / ЦЕНЫ of the house (asserted); shares
# need n divisible by 2, 3 or 4 — 16, 28, 44 (by 4), 27, 33 (by 3), the rest by 2
ЧИСЛА = ((14, 9), (22, 13), (26, 17), (34, 19), (16, 9), (28, 13), (38, 17), (44, 19), (27, 13), (33, 17))
ЧИСЛА_АКТОВ = ((14, 9, 8), (22, 13, 11), (26, 17, 13), (34, 19, 14), (16, 9, 8), (28, 13, 11), (38, 17, 13), (44, 19, 14))
# prices of the «unit» form come from the house's own table, not from n and k — held out here
ЦЕНЫ = ((7, 6), (9, 8), (11, 7), (13, 9))
ВОПРОС = re.compile(r"[?？] ")
ЧИСЛО = re.compile(r"\d+")


def _разрезать(страница):
    """(question, answer) at the LAST question mark; None for a page without one."""
    м = list(ВОПРОС.finditer(страница))
    if not м:
        return None
    return страница[:м[-1].end()].strip(), страница[м[-1].end():].strip()


def _значение(ответ):
    числа = ЧИСЛО.findall(ответ)
    return числа[-1] if числа else ответ.rstrip(".")


def страницы():
    """Every form and act of the house for the held-out numbers, two pages per (language, form)."""
    вон = []
    цены_дома, F.ЦЕНЫ = F.ЦЕНЫ, ЦЕНЫ           # the unit form reads prices from the house table
    try:
        return _страницы(вон)
    finally:
        F.ЦЕНЫ = цены_дома


def _страницы(вон):
    for язык in F.РАМКИ:
        лиц = len(F.A.ЛИЦА[язык]); вещей = len(F.A.ЯЗЫКИ[язык]["вещи"])
        for форма in F.ФОРМЫ:
            if форма not in F.РАМКИ[язык] or язык in F.ОБЪЯВЛЕННЫЕ_ПРОПУСКИ.get(форма, ()):
                continue
            взято = 0
            for q, (n, k) in enumerate(ЧИСЛА):
                for вариант in range(3):
                    с = F.страница(язык, форма, (q + 2) % лиц, (q * 3 + 2) % лиц, (q + 1) % вещей, n, k, вариант)
                    # A PAGE WITHOUT A NUMBER IN ITS QUESTION CANNOT BE HELD OUT: the refusal «how many
                    # coins does Ann have? I do not know …» is the same line for every number
                    if с and _разрезать(с) and ЧИСЛО.search(_разрезать(с)[0]):
                        вон.append((язык, форма, с)); взято += 1
                        break
                if взято >= 2:
                    break
        for форма in F.ФОРМЫ_АКТОВ:
            if форма not in F.РАМКИ_АКТОВ[язык]:
                continue
            взято = 0
            for q, (n, k, m) in enumerate(ЧИСЛА_АКТОВ):
                с = F.страница_акта(язык, форма, (q + 2) % лиц, (q * 3 + 2) % лиц, n, k, m)
                if с and _разрезать(с):
                    вон.append((язык, форма, с)); взято += 1
                if взято >= 2:
                    break
    return вон


def main(argv):
    корень = pathlib.Path(argv[argv.index("--корень") + 1]) if "--корень" in argv else КОРЕНЬ
    if not (корень / "datasets").is_dir():
        print(f"УДЕРЖАННЫЙ КЛЮЧ ОТКАЗ: нет дерева в {корень}")
        return 2
    # THE FIRST NUMBER OF A STORY IS WHAT MEMORY KEYS ON: the held-out n never stands as a house n,
    # and no held-out pair or triple stands in a house table (a small k or m may recur — the
    # line differs by its story)
    свои_n = {n for n, *_ in F.ЧИСЛА} | {n for n, *_ in F.ЧИСЛА_АКТОВ}
    свои_ряды = set(F.ЧИСЛА) | set(F.ЧИСЛА_АКТОВ) | {(n, k) for n, k, _ in F.ЧИСЛА_АКТОВ} | set(F.ЦЕНЫ)
    беда = ({n for n, *_ in ЧИСЛА} | {n for n, *_ in ЧИСЛА_АКТОВ}) & свои_n
    беда |= {р for р in set(ЧИСЛА) | set(ЧИСЛА_АКТОВ) | {(n, k) for n, k, _ in ЧИСЛА_АКТОВ} | set(ЦЕНЫ) if р in свои_ряды}
    if беда:
        print(f"УДЕРЖАННЫЙ КЛЮЧ FAIL: удержанные числа стоят в таблицах дома: {sorted(map(str, беда))}")
        return 1
    ряд = страницы()
    # no question may stand in a world of shows (lived lines)
    прожито = set()
    for путь in genesis.worlds(kind="shows"):
        if путь.is_file():
            прожито.update(л.strip() for л in путь.read_text(encoding="utf-8", errors="replace").splitlines())
    прожитых = sum(1 for _, _, с in ряд if с.strip() in прожито)
    строки = []
    for язык, форма, с in ряд:
        в, о = _разрезать(с)
        строки.append(f"{_значение(о)}\t{в}\t{о}")
    (корень / КЛЮЧ).write_text("\n".join(строки) + "\n", encoding="utf-8")
    по_языку = collections.Counter(я for я, _, _ in ряд)
    глубина = collections.Counter(("2+" if с.count("=") >= 2 else "1" if "=" in с else "0") for _, _, с in ряд)
    поза = "PASS" if прожитых <= ПРОЖИТЫХ_РУБЕЖ and len(ряд) >= ВОПРОСОВ_РУБЕЖ else "FAIL"
    print(f"УДЕРЖАННЫЙ КЛЮЧ {поза}: вопросов {len(ряд)} (рубеж {ВОПРОСОВ_РУБЕЖ}), прожитых {прожитых} "
          f"(рубеж {ПРОЖИТЫХ_РУБЕЖ}); по языкам " + " ".join(f"{я} {к}" for я, к in sorted(по_языку.items()))
          + "; по глубине " + " ".join(f"[{г}] {к}" for г, к in sorted(глубина.items())) + f"; ключ {КЛЮЧ}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
