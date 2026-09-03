#!/usr/bin/env python3
"""[FEW-SHOT PROFILE] — how many shows each question form has, per language.

holon's third order (03.09, ONE-CARRIER): a TSV «question form, language,
shows» — the measure «shows before the purchase»: the organism buys a frame
at LAW² = 9 shows, so a form with fewer shows is a form the corpus offers
but does not sell, and a form with hundreds is weight, not knowledge
(scripts/form_census.py, the minimal-corpus law).

The form of a question is its skeleton on the corpus side (numbers → «#»,
declared names → «@», the declared fillers of the houses of phrases → «※»,
notations → their one hole) cut at the question mark: the question clause
alone, the answer left out — the organism's frame is keyed by the question.
The language is the sign of the language (tools/langsign.py) over the whole
line. A line without a question mark carries no question form and is not
counted here (the statement forms are the census of forms).

Print: a TSV to stdout or to --out, sorted by language and by mass; the
summary line names the forms below the law (shows < 9) per language.
"""
import argparse
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
sys.path.insert(0, str(КОРЕНЬ / "scripts"))
import form_census as C  # noqa: E402
import langsign  # noqa: E402
from genesis import worlds  # noqa: E402

LAW2 = C.LAW2
# the question clause: up to and including the FIRST question mark (fr/es
# put a space before it, es opens with «¿»)
_ВОПРОС = re.compile(r"^(.*?\?)")


def форма_вопроса(строка):
    м = _ВОПРОС.match(строка)
    if not м:
        return None
    return C.род(C.скелет(м.group(1)))


def мир_имя(путь):
    return путь.stem[len("genesis_"):] if путь.stem.startswith("genesis_") else путь.stem


def профиль(пути):
    """(form, language) → shows; (form, language) → worlds."""
    масса = collections.Counter()
    миры = collections.defaultdict(set)
    for путь in пути:
        имя = мир_имя(путь)
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip() or с.startswith("\x0c"):
                continue
            ф = форма_вопроса(с)
            if ф is None:
                continue
            # a line without a sign of any language (notation alone) is «—»
            я = langsign.язык(с) or "—"
            масса[(ф, я)] += 1
            миры[(ф, я)].add(имя)
    return масса, миры


def main():
    ап = argparse.ArgumentParser()
    ап.add_argument("--out", type=pathlib.Path)
    ап.add_argument("--worlds", nargs="*", help="world names (default: every world of shows)")
    а = ап.parse_args()
    пути = [п for п in worlds(kind="shows") if not а.worlds or мир_имя(п) in а.worlds]
    масса, миры = профиль(пути)
    строки = ["форма вопроса\tязык\tпоказов\tмиры"]
    for (ф, я), n in sorted(масса.items(), key=lambda kv: (kv[0][1], -kv[1], kv[0][0])):
        строки.append(f"{ф}\t{я}\t{n}\t{','.join(sorted(миры[(ф, я)]))}")
    текст = "\n".join(строки) + "\n"
    if а.out:
        а.out.write_text(текст, encoding="utf-8")
    else:
        sys.stdout.write(текст)
    по_языку = collections.defaultdict(lambda: [0, 0, 0])
    for (ф, я), n in масса.items():
        з = по_языку[я]; з[0] += 1; з[1] += n
        if n < LAW2:
            з[2] += 1
    сводка = "; ".join(f"{я}: форм {з[0]}, показов {з[1]}, ниже закона {з[2]}" for я, з in sorted(по_языку.items()))
    print(f"FEW-SHOT ПРОФИЛЬ: форм вопроса {len(масса)}, показов {sum(масса.values())} — {сводка}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
