#!/usr/bin/env python3
"""[ДОСЯГАЕМОСТЬ СУДА] — a court that grew re-judges EVERY world before it lands (М-404).

THE GATE JUDGES A WORLD WHEN IT IS WRITTEN, WITH THE COURTS OF THAT HOUR. A court
that grows heads or patterns afterwards (compute / find / найди; «/» and «*»;
a topic's definition) reaches worlds written before it — and nobody asks it
about them until the neighbour is rebuilt. Four captures slept that way on
05.09 (the task court over the big-number world, the haste court over long
division, notation and equations, the topics house over units and physics,
the script court over «ilu»), and the sieve of the definitions world threw
away 35 honest lines of Dahl and Webster on the topics house's word.

THIS INSTRUMENT IS THE LAW'S HAND: every world of shows is put to the palata
again, whole. Two modes, both named in the verdict:
  · --суд ИМЯ …  — only the named courts judge (the court that grew, before it
    lands): fast; a line one of them calls a lie is a CAPTURE unless the
    world is its own — blindness is not measured, the other courts would
    have judged;
  · no --суд      — the whole palata: a lie by any court, or a line no court
    judges, is the debt; this is the point's gate and it costs what the gates
    of all worlds cost together.

Rubric: 0 lies (both modes), 0 blind lines (whole palata). The examples name
the world, the line and the courts, so the border is taken from the subject
(М-180-f2) and not from the count.

usage: court_reach.py [--суд ИМЯ …] [--мир ФАЙЛ …] [--пример N]
"""
import collections
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import genesis  # noqa: E402
from panel import палата  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛЖЕЙ_РУБЕЖ = 0
ЛЖЕЙ_РУБЕЖ = 0
# РУБЕЖ-ДОЛГА: СЛЕПЫХ_РУБЕЖ = 0
СЛЕПЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: --суд no-such-court


def _аргументы(argv):
    суды, миры, пример = [], [], 3
    i = 0
    while i < len(argv):
        а = argv[i]
        if а == "--суд":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                суды.append(argv[i]); i += 1
            continue
        if а == "--мир":
            i += 1
            while i < len(argv) and not argv[i].startswith("--"):
                миры.append(pathlib.Path(argv[i])); i += 1
            continue
        if а == "--пример":
            пример = int(argv[i + 1]); i += 2
            continue
        i += 1
    return суды, миры, пример


def main(argv):
    названные, миры, пример = _аргументы(argv)
    п = палата()
    if названные:
        нет = [с for с in названные if с not in п.суды]
        if нет:
            print(f"ДОСЯГАЕМОСТЬ СУДА ОТКАЗ: таких судов в палате нет: {нет} "
                  f"(живых {п.живых}: {', '.join(sorted(п.суды))})")
            return 2
        п.суды = {имя: суд for имя, суд in п.суды.items() if имя in названные}
    if not миры:
        миры = list(genesis.worlds(kind="shows"))
    миры = [м for м in миры if m_file(м)]
    if not миры:
        print("ДОСЯГАЕМОСТЬ СУДА ОТКАЗ: миров нет — судить нечего")
        return 2
    целиком = not названные
    лжей = слепых = строк = 0
    по_миру = collections.Counter(); примеры = []
    for мир in миры:
        for строка, судимо, истинно, кем in п.судить_файл(мир):
            if строка.startswith("\x0c"):
                continue
            строк += 1
            if судимо and not истинно:
                лжей += 1; по_миру[(мир.name, "ложь", ",".join(кем))] += 1
                if len(примеры) < пример:
                    примеры.append(f"ЛОЖЬ [{','.join(кем)}] {мир.name}: {строка[:90]}")
            elif целиком and not судимо:
                слепых += 1; по_миру[(мир.name, "слепа", "")] += 1
                if len(примеры) < пример:
                    примеры.append(f"СЛЕПА {мир.name}: {строка[:90]}")
    for п_ in примеры:
        print(f"  {п_}")
    for (мир, род, кем), к in по_миру.most_common(12):
        print(f"  {мир}: {род} {к}" + (f" [{кем}]" if кем else ""))
    поза = "PASS" if лжей <= ЛЖЕЙ_РУБЕЖ and (not целиком or слепых <= СЛЕПЫХ_РУБЕЖ) else "FAIL"
    режим = "вся палата" if целиком else "суды " + ", ".join(названные)
    print(f"ДОСЯГАЕМОСТЬ СУДА {поза} ({режим}; судов {п.живых}): миров {len(миры)}, строк {строк}, "
          f"ЛЖЕЙ {лжей} (рубеж {ЛЖЕЙ_РУБЕЖ})" +
          (f", слепых {слепых} (рубеж {СЛЕПЫХ_РУБЕЖ})" if целиком else ", слепота не судится"))
    return 0 if поза == "PASS" else 1


def m_file(п):
    return pathlib.Path(п).is_file()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
