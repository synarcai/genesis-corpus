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
import concurrent.futures
import os
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import genesis  # noqa: E402
import panel  # noqa: E402
from panel import палата  # noqa: E402

# РУБЕЖ-ДОЛГА: ЛЖЕЙ_РУБЕЖ = 0
ЛЖЕЙ_РУБЕЖ = 0
# РУБЕЖ-ДОЛГА: СЛЕПЫХ_РУБЕЖ = 0
СЛЕПЫХ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: --суд no-such-court


_ПАЛАТА_РАБОЧЕГО = None


def _палата_рабочего(названные):
    """Одна палата на процесс, суженная теми же именами, что и у родителя.

    СУЖЕНИЕ ОБЪЯВЛЕНО ЗАДАЧЕЙ, А НЕ УНАСЛЕДОВАНО: рабочий строит палату сам
    (spawn на этой машине), и если бы он не знал о доводе `--суд`, он судил бы
    ПОЛНОЙ палатой и вернул чужие числа.
    """
    global _ПАЛАТА_РАБОЧЕГО
    if _ПАЛАТА_РАБОЧЕГО is None:
        п = палата()
        if названные:
            п.суды = {и: с for и, с in п.суды.items() if и in названные}
        _ПАЛАТА_РАБОЧЕГО = п
    return _ПАЛАТА_РАБОЧЕГО


def _судить_ломоть(задача):
    """Один ЛОМОТЬ мира: (имя, начало, строк, лжей, слепых, по_миру, примеры).

    ЛОМОТЬ, А НЕ МИР. Раздача по мирам не может быть быстрее самого длинного мира.
    Слои и пласт строятся по ЦЕЛОМУ файлу в каждом ломте — иначе эпизодные ставки
    увидели бы обрубок, — а судятся строки [начало, конец).
    """
    путь, начало, конец, названные, целиком, пример = задача
    путь = pathlib.Path(путь)
    п = _палата_рабочего(названные)
    слои = п.слои(путь)
    пласт = п.пласт_файла(путь)
    строки = panel._живые_строки(путь)
    лжей = слепых = строк = 0
    по_миру = collections.Counter(); примеры = []
    for строка in строки[начало:конец]:
        if строка.startswith("\x0c"):
            continue
        _с, судимо, истинно, кем = строка, *п.судить(строка, слои, пласт)
        строк += 1
        if судимо and not истинно:
            лжей += 1; по_миру[(путь.name, "ложь", ",".join(кем))] += 1
            if len(примеры) < пример:
                примеры.append(f"ЛОЖЬ [{','.join(кем)}] {путь.name}: {строка[:90]}")
        elif целиком and not судимо:
            слепых += 1; по_миру[(путь.name, "слепа", "")] += 1
            if len(примеры) < пример:
                примеры.append(f"СЛЕПА {путь.name}: {строка[:90]}")
    return путь.name, начало, строк, лжей, слепых, по_миру, примеры


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
    # ЛОМТИ, ДЛИННЫМИ ВПЕРЁД. Прибор ходил свод МИР ЗА МИРОМ, и внутри мира палата
    # делилась лишь при двух тысячах строк и лишь если машина не занята — то есть
    # почти никогда. Сорок шесть минут на набор, и это второй по цене прибор свода.
    #
    #     САМАЯ ДЛИННАЯ ЗАДАЧА ЕСТЬ ДНО СРОКА.
    #
    # Ныне список задач плоский — (путь, начало, конец), — режется общим законом
    # палаты по замеренной цене и раздаётся длинными вперёд.
    jobs = panel._джобы()
    ломти = panel.ломти(миры, panel.ЦЕЛЬ_ЛОМТЯ if jobs > 1 else 0)
    порядок = {м.name: i for i, м in enumerate(миры)}
    задачи = [(str(пт), a, b, tuple(названные), целиком, пример) for пт, a, b, _ц in ломти]
    if jobs <= 1:
        итоги = [_судить_ломоть(з) for з in задачи]
    else:
        # СТОРОЖ РОДИТЕЛЯ: рабочий, переживший убитый набор, есть память,
        # которую никто не освободит (79 таких сирот на 5.9 ГБ, замер 12.09).
        with concurrent.futures.ProcessPoolExecutor(
                max_workers=jobs, initializer=panel._сторожить_родителя,
                initargs=(os.getpid(),)) as пул:
            итоги = list(пул.map(_судить_ломоть, задачи))
    # СБОРКА В ПОРЯДКЕ МИРОВ И СТРОК: вердикт обязан читаться так же,
    # как читался бы в один поток.
    итоги.sort(key=lambda и: (порядок.get(и[0], 10**9), и[1]))
    for _имя, _нач, свои_строк, свои_лжей, свои_слепых, свои_по_миру, свои_примеры in итоги:
        строк += свои_строк; лжей += свои_лжей; слепых += свои_слепых
        по_миру.update(свои_по_миру)
        for п_ in свои_примеры:
            if len(примеры) < пример:
                примеры.append(п_)
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
