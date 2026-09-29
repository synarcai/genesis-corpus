#!/usr/bin/env python3
"""ПРИБОР СЪЁМКИ МИРА КОДА дома `toolcode`: ответы языковых серверов, снятые один раз (28.09, М-2099).

Ведущий: ход мира кода на странице — НАСТОЯЩИЙ ответ сервера языка, не наша модель языка. Сервер идёт не при каждой
сборке свода (индексация занимает десятки секунд, и сборка перестала бы быть лёгкой), а однажды, этим прибором:
объявленный проект кладётся в папку, мост ядра `ozar_lsp_world` поднимает серверы (rust-analyzer, pyright), акты
чтения (`codeworld.акты_чтения`) идут одной сессией, всякое переименование — своей сессией на свежей копии проекта
(правка меняет мир), и снятое — ответ и файлы после правки — ложится семенем `tools/seeds/toolcode_world.json` под
отпечатком проекта (`codeworld.отпечаток`). Дом читает семя; суд сверяет с ним ход мира байт в байт.

    ОРУДИЕ, ПЕРЕПИСЫВАЮЩЕЕ ДЕРЕВО, НЕ ПИШЕТ БЕЗ ДОВОДА. Без доводов прибор только читает: семя верно, пока отпечаток
    проекта и объявленных актов тот же, что при съёмке, и всякий объявленный акт снят.

ПРОГОНЫ ПОСЛЕ ПРАВКИ (план двух миров): после всякого переименования прогоны, чей код правка тронула
(`codeworld.прогоны_затронутые`), снимаются на проекте в оставленном правкой состоянии — прибором съёмки прогонов дома
актов (`toolrepo_capture.снять`), с доводом `--процесс` — через сервер мира процесса ядра (пути отчёта от дома мира).

    python3 tools/toolcode_capture.py                    # самопроверка без процессов
    python3 tools/toolcode_capture.py --снять [пути]     # снять заново всё и записать
    пути: --мост <ozar_lsp_world> --rust <rust-analyzer> --python <pyright-langserver> --процесс <ozar_process>
    (по умолчанию — из окружения: OZAR_LSP_WORLD, OZAR_RUST_ANALYZER, OZAR_PYRIGHT, OZAR_PROCESS)
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import codeworld as К  # noqa: E402 — объявление мира кода: основы, поля, отпечаток, семя
import repoworld as Р  # noqa: E402 — прогоны мира процесса и отпечаток их состояния
import toolrepo_capture as П  # noqa: E402 — съёмка прогонов на состоянии проекта


def _довод(имя, окружение):
    if имя in sys.argv:
        return sys.argv[sys.argv.index(имя) + 1]
    return os.environ.get(окружение)


def _проект_в(корень, файлы):
    for путь, строки in файлы.items():
        файл = корень / путь
        файл.parent.mkdir(parents=True, exist_ok=True)
        файл.write_text("".join(с + "\n" for с in строки), encoding="utf-8")


def _сессия(мост, серверы, файлы, акты):
    """Одна сессия моста на копии проекта: ответы на акты по порядку и файлы проекта после сессии."""
    корень = pathlib.Path(tempfile.mkdtemp(prefix="toolcode-"))
    try:
        _проект_в(корень, файлы)
        ввод = "".join(К.ключ(*акт) + "\n" for акт in акты)
        вывод = subprocess.run([мост, str(корень), *серверы], input=ввод, capture_output=True, text=True,
                               timeout=900, check=True).stdout.splitlines()
        assert len(вывод) == len(акты), (len(вывод), len(акты))
        после = {путь: (корень / путь).read_text(encoding="utf-8").split("\n")[:-1] for путь in файлы}
        return [json.loads(с) for с in вывод], после
    finally:
        shutil.rmtree(корень, ignore_errors=True)


def _версия(команда):
    try:
        return subprocess.run(команда, capture_output=True, text=True, timeout=60).stdout.strip().splitlines()[0]
    except (OSError, IndexError, subprocess.SubprocessError):
        return "?"


def снять():
    мост = _довод("--мост", "OZAR_LSP_WORLD")
    rust = _довод("--rust", "OZAR_RUST_ANALYZER")
    python = _довод("--python", "OZAR_PYRIGHT")
    процесс = _довод("--процесс", "OZAR_PROCESS")
    assert мост and rust and python, "нужны пути моста и серверов: --мост, --rust, --python"
    серверы = [rust, "--", python, "--stdio"]
    проект = {путь: list(строки) for путь, строки in К.ПРОЕКТ.items()}
    акты = К.акты_чтения()
    ответы, после = _сессия(мост, серверы, проект, акты)
    assert после == проект, "акт чтения изменил проект"
    # ОТКАЗ «io» — БЕДА МОСТА, А НЕ ПРАВДА МИРА: сервер, не кончивший индексацию, отвечает ContentModified; такой акт
    # повторяется новой сессией (до трёх раз), и семя с отказом «io» самопроверка не принимает
    for _раз in range(3):
        сбои = [i for i, ответ in enumerate(ответы) if ответ.get("why") == "io"]
        if not сбои:
            break
        повтор, _после = _сессия(мост, серверы, проект, [акты[i] for i in сбои])
        for i, ответ in zip(сбои, повтор):
            ответы[i] = ответ
    вон = {"source": К.отпечаток(), "servers": {"rust-analyzer": _версия([rust, "--version"]),
                                                   "pyright": _версия([python.replace("pyright-langserver", "pyright"),
                                                                       "--version"])},
           "reads": {К.ключ(*акт): ответ for акт, ответ in zip(акты, ответы)}, "renames": {}}
    for x, y in К.ПЕРЕИМЕНОВАНИЯ:
        for _раз in range(3):
            (ответ,), после = _сессия(мост, серверы, проект, [("rename", x, y)])
            if ответ.get("why") != "io":
                break
        изменены = {путь: строки for путь, строки in после.items() if строки != проект[путь]}
        прогоны = {}
        for имя, снятое in П.снять(после, К.прогоны_затронутые(изменены), процесс).items():
            прогоны[имя] = {**снятое, "source": Р.отпечаток(имя, после)}
        вон["renames"][К.ключ("rename", x, y)] = {"reply": ответ, "files": изменены, "runs": прогоны}
        print(f"rename {x} → {y}: {ответ.get('reply')} {[м['value'] for м in ответ.get('measures', [])]} "
              f"файлов изменено {len(изменены)}; прогоны "
              + ", ".join(f"{имя} exit {с['exit']} lines {с['lines']}" for имя, с in прогоны.items()))
    К.СЕМЯ.parent.mkdir(parents=True, exist_ok=True)
    К.СЕМЯ.write_text(json.dumps(вон, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"СНЯТО: актов чтения {len(акты)}, переименований {len(К.ПЕРЕИМЕНОВАНИЯ)}, отпечаток {вон['source']}")
    return 0


def _самопроверка():
    """Без процессов: семя снято с объявленного проекта (отпечаток тот же), всякий объявленный акт снят, всякое
    переименование держит ответ и файлы, какие ответ назвал изменёнными."""
    с, беды = К.семя(), []
    if not с:
        беды.append("семени нет — снять: --снять")
    else:
        if с.get("source") != К.отпечаток():
            беды.append(f"семя снято под отпечатком {с.get('source')}, а проект и акты — {К.отпечаток()}")
        for акт in К.акты_чтения():
            if К.ключ(*акт) not in с["reads"]:
                беды.append(f"акт {акт} не снят")
            elif с["reads"][К.ключ(*акт)].get("why") == "io":
                беды.append(f"акт {акт}: отказ моста io ({с['reads'][К.ключ(*акт)].get('what')}) — снять заново")
        for x, y in К.ПЕРЕИМЕНОВАНИЯ:
            снятое = с["renames"].get(К.ключ("rename", x, y))
            if снятое is None:
                беды.append(f"переименование {x} → {y} не снято")
                continue
            ход_ = К.из_ответа(снятое["reply"])[0]
            if ход_ is None:
                беды.append(f"{x} → {y}: мир отказал ({снятое['reply'].get('why')}), а переименование объявлено исполнимым")
                continue
            названы = set(К.поле(ход_, "path"))
            if названы != set(снятое["files"]):
                беды.append(f"{x} → {y}: ответ назвал {sorted(названы)}, изменены {sorted(снятое['files'])}")
            нужны = К.прогоны_затронутые(снятое["files"])
            if list(снятое.get("runs", {})) != нужны:
                беды.append(f"{x} → {y}: сняты прогоны {list(снятое.get('runs', {}))}, правка тронула код {нужны}")
            for имя, прогон in снятое.get("runs", {}).items():
                if прогон.get("source") != Р.отпечаток(имя, К.после(x, y)):
                    беды.append(f"{x} → {y}: прогон {имя} снят под {прогон.get('source')}, а состояние после правки — "
                                f"{Р.отпечаток(имя, К.после(x, y))}")
    for беда in беды:
        print("  БЕДА", беда)
    print(f"СЪЁМКА МИРА КОДА {'FAIL' if беды else 'PASS'}: актов чтения {len(К.акты_чтения())}, переименований "
          f"{len(К.ПЕРЕИМЕНОВАНИЯ)}, бед {len(беды)}")
    return 1 if беды else 0


def main():
    if "--снять" in sys.argv:
        return снять()
    return _самопроверка()


if __name__ == "__main__":
    sys.exit(main())
