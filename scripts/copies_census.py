#!/usr/bin/env python3
"""[ПЕРЕПИСЬ КОПИЙ] — how often a show repeats inside its world; the ceiling LAW is the rubric.

THE CEILING IS A LAW OF THE LAYER, AND A LAW MUST BE READ BACK. layer.emit keeps
at most LAW copies of a show per world (М-402: a copy beyond LAW is not a show —
the skeleton of a line without holes is the line itself). This instrument reads
every world that a generator writes through the layer and counts: lines,
distinct shows, copies (lines − distinct), the largest number of copies of one
show. A world through the layer with a show above LAW is a FAIL — the layer was
bypassed or the world is stale.

THE SIDECAR IS FOR THE QUORUM COURT (holon, 05.09): the reader's market courts
buy a head on DISTINCT shows, not on copies; datasets/COPIES.tsv names, per
world, how many lines are copies, so a quorum can be read against distinct
shows without re-counting the corpus.

A LINE IS NOT ALWAYS A SHOW. Five worlds carry MULTI-LINE shows (a fact line
under several questions, a table with its rows, a fenced block with its
«```»), and a line of such a show repeats as often as the show is worn —
«```» stands 420 times in the LaTeX world with no show above LAW. Whether a
world's shows span lines is READ FROM ITS GENERATOR, not guessed from the file:
the generator's pass_shows / pass_groups of pass 0 are asked, and a world whose
shows carry a newline is counted as a witness (lines, copies) but judged by
the ceiling only through its generator's law. A generator that does not expose
its passes at module level is named, and its world is judged by lines — the
strict side, so the debt shows rather than hides.

WHAT IS NOT GATED, NAMED: worlds written by their own hand (the full canon, the
school and prose assemblies, genesis_l4) are counted and printed, never judged
by the ceiling — the layer never touched them.
"""
import importlib.util
import os
import collections
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
from langpack import LAW  # noqa: E402

# РУБЕЖ-ДОЛГА: СВЕРХ_LAW_РУБЕЖ = 0
СВЕРХ_LAW_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: --корень no-such-root
ПУТЬ = re.compile(r'(?:emit(?:_grouped)?\(\s*|ЦЕЛЬ = )"(datasets/[-\w.]+\.txt)"')
САЙДКАР = "datasets/COPIES.tsv"


def миры(корень):
    """world file → (generator, through the layer?)"""
    вон = {}
    for ген in sorted((корень / "tools").glob("gen_genesis_*.py")):
        т = ген.read_text(encoding="utf-8")
        через_слой = "from layer import" in т and bool(re.search(r"\bemit(?:_grouped)?\(", т))
        for ц in ПУТЬ.findall(т):
            вон[ц] = (ген.name, через_слой)
    return вон


def многострочный(корень, ген):
    """True / False by the generator's own shows of pass 0; None when it does not tell."""
    os.environ.setdefault("GENESIS_NO_GATE", "1")
    путь = корень / "tools" / ген
    try:
        spec = importlib.util.spec_from_file_location("census_" + путь.stem, путь)
        м = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(м)
        f, fg = getattr(м, "pass_shows", None), getattr(м, "pass_groups", None)
        показы = f(0) if f else ([с for г in fg(0) for с in г] if fg else None)
    except Exception:
        return None
    if показы is None:
        return None
    return any("\n" in с for с in показы)


def перепись(путь):
    счёт = collections.Counter()
    for л in путь.read_text(encoding="utf-8").splitlines():
        к = л.strip()
        if k := (к and not к.startswith("\x0c")):
            счёт[к] += 1
    строк = sum(счёт.values())
    return строк, len(счёт), строк - len(счёт), (max(счёт.values()) if счёт else 0)


def main(argv):
    корень = КОРЕНЬ
    if "--корень" in argv:
        корень = pathlib.Path(argv[argv.index("--корень") + 1])
    if not (корень / "tools").is_dir():
        print(f"ПЕРЕПИСЬ КОПИЙ ОТКАЗ: нет дерева в {корень}")
        return 2
    все = миры(корень)
    if not все:
        print("ПЕРЕПИСЬ КОПИЙ ОТКАЗ: генераторов нет — считать нечего")
        return 2
    ряд = []; сверх = []; многострочных = []; немых = []
    sys.path.insert(0, str(корень / "tools"))
    for ц, (ген, через_слой) in sorted(все.items()):
        п = корень / ц
        if not p_file(п):
            continue
        строк, различных, копий, макс = перепись(п)
        ряд.append((ц, ген, через_слой, строк, различных, копий, макс))
        if через_слой and макс > LAW:
            форма = многострочный(корень, ген)
            if форма is True:
                многострочных.append(f"{ц}: до {макс} копий строки, показы многострочны")
                continue
            if форма is None:
                немых.append(ген)
            сверх.append(f"{ц}: до {макс} копий одного показа ({копий} копий из {строк})")
    сайдкар = корень / САЙДКАР
    сайдкар.write_text("мир\tгенератор\tчерез_слой\tстрок\tразличных\tкопий\tмакс_копий\n" +
                       "".join(f"{ц}\t{ген}\t{int(с)}\t{стр}\t{р}\t{к}\t{м}\n" for ц, ген, с, стр, р, к, м in ряд),
                       encoding="utf-8")
    слой = [р for р in ряд if р[2]]
    for с in сверх[:6]:
        print(f"  СВЕРХ LAW {с}")
    for с in многострочных:
        print(f"  МНОГОСТРОЧНЫЙ {с}")
    if немых:
        print(f"  СТРОЧНОСТЬ НЕ ВЫВЕДЕНА (генератор не открывает проходов): {немых}")
    поза = "FAIL" if len(сверх) > СВЕРХ_LAW_РУБЕЖ else "PASS"
    print(f"ПЕРЕПИСЬ КОПИЙ {поза}: миров через слой {len(слой)}, сверх LAW={LAW} {len(сверх)} "
          f"(рубеж {СВЕРХ_LAW_РУБЕЖ}); строк {sum(р[3] for р in слой)}, различных {sum(р[4] for р in слой)}, "
          f"копий {sum(р[5] for р in слой)}, многострочных {len(многострочных)}; вне слоя миров {len(ряд) - len(слой)} "
          f"(копий {sum(р[5] for р in ряд if not р[2])}) — не судятся; сайдкар {САЙДКАР}")
    return 0 if поза == "PASS" else 1


def p_file(п):
    return п.is_file()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
