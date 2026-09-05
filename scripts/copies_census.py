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

WHAT IS NOT GATED, NAMED: worlds written by their own hand (the full canon, the
school and prose assemblies, genesis_l4) are counted and printed, never judged
by the ceiling — the layer never touched them.
"""
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
    ряд = []; сверх = []
    for ц, (ген, через_слой) in sorted(все.items()):
        п = корень / ц
        if not p_file(п):
            continue
        строк, различных, копий, макс = перепись(п)
        ряд.append((ц, ген, через_слой, строк, различных, копий, макс))
        if через_слой and макс > LAW:
            сверх.append(f"{ц}: до {макс} копий одного показа ({копий} копий из {строк})")
    сайдкар = корень / САЙДКАР
    сайдкар.write_text("мир\tгенератор\tчерез_слой\tстрок\tразличных\tкопий\tмакс_копий\n" +
                       "".join(f"{ц}\t{ген}\t{int(с)}\t{стр}\t{р}\t{к}\t{м}\n" for ц, ген, с, стр, р, к, м in ряд),
                       encoding="utf-8")
    слой = [р for р in ряд if р[2]]
    for с in сверх[:6]:
        print(f"  СВЕРХ LAW {с}")
    поза = "FAIL" if len(сверх) > СВЕРХ_LAW_РУБЕЖ else "PASS"
    print(f"ПЕРЕПИСЬ КОПИЙ {поза}: миров через слой {len(слой)}, сверх LAW={LAW} {len(сверх)} "
          f"(рубеж {СВЕРХ_LAW_РУБЕЖ}); строк {sum(р[3] for р in слой)}, различных {sum(р[4] for р in слой)}, "
          f"копий {sum(р[5] for р in слой)}; вне слоя миров {len(ряд) - len(слой)} "
          f"(копий {sum(р[5] for р in ряд if not р[2])}) — не судятся; сайдкар {САЙДКАР}")
    return 0 if поза == "PASS" else 1


def p_file(п):
    return п.is_file()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
