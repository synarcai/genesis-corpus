#!/usr/bin/env python3
"""ПРИБОР СЪЁМКИ ПРОГОНОВ дома `toolrepo`: настоящий вывод бегунов тестов, снятый один раз (25.09).

Ведущий: ход мира на странице прогона — НАСТОЯЩИЙ вывод бегуна, не объявленные строки. Бегун идёт не при каждой
сборке свода (время бегуна и имя сборки плавают — свод перестал бы быть воспроизводимым), а однажды, этим прибором:
репозиторий дома кладётся в папку, мир-процесс держит свои прогоны в `.ozar/acts/<имя>` (как мир ядра `process.rs`:
отчёт — stdout и stderr одним файлом в порядке записи, `lines` — число переводов строки, `millis` — стенное время,
`exit` — код), каждый прогон исполняется, и снятое ложится семенем в `tools/seeds/toolrepo_runs.json`. Дом читает его и
печатает отчёт строками хода мира; самопроверка дома сверяет снятое с объявленным кодом.

    ОРУДИЕ, ПЕРЕПИСЫВАЮЩЕЕ ДЕРЕВО, НЕ ПИШЕТ БЕЗ ДОВОДА. Самопроверка домов зовёт всякий файл парка без доводов;
    прибор, который при этом снимал бы прогоны заново, переписывал бы время бегуна посреди суда. Без доводов он
    только читает: снятое верно, пока отпечаток объявленного (код проекта и команды прогонов) тот же, что при съёмке.

    python3 tools/toolrepo_capture.py            # самопроверка без процессов: отпечаток и строки снятого
    python3 tools/toolrepo_capture.py --сверить  # снять заново и сравнить: слова обязаны совпасть, числа плавают
    python3 tools/toolrepo_capture.py --снять    # снять и записать
"""
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import repoworld as R  # noqa: E402 — объявление мира: код проекта и прогоны

ЦЕЛЬ = R.СЕМЯ_ПРОГОНОВ


def снять():
    корень = pathlib.Path(tempfile.mkdtemp(prefix="toolrepo-"))
    try:
        for путь, строки in R.ПРОЕКТ.items():
            файл = корень / путь
            файл.parent.mkdir(parents=True, exist_ok=True)
            файл.write_text("".join(с + "\n" for с in строки), encoding="utf-8")
        мир = корень / ".ozar"
        (мир / "acts").mkdir(parents=True)
        (мир / "reports").mkdir()
        вон = {}
        for имя, команда in R.ПРОГОНЫ.items():
            act = мир / "acts" / имя
            act.write_text(f"#!/bin/sh\ncd .. && {команда}\n", encoding="utf-8")
            act.chmod(0o755)
            лог = мир / "reports" / f"{имя}.log"
            with open(лог, "wb") as out:
                начало = time.monotonic()
                код = subprocess.run([str(act)], cwd=мир, stdin=subprocess.DEVNULL, stdout=out, stderr=out,
                                     env={**os.environ}).returncode
                millis = int((time.monotonic() - начало) * 1000)
            отчёт = лог.read_bytes()
            вон[имя] = {"exit": код, "millis": millis, "lines": отчёт.count(b"\n"),
                        "report": отчёт.decode("utf-8").split("\n")[:-1] if отчёт.endswith(b"\n")
                        else отчёт.decode("utf-8").split("\n")}
        return вон
    finally:
        shutil.rmtree(корень, ignore_errors=True)


def отпечаток():
    """Отпечаток объявленного: код проекта и команды прогонов. Снятое верно, пока отпечаток тот же."""
    return hashlib.sha256(json.dumps([sorted(R.ПРОЕКТ.items()), sorted(R.ПРОГОНЫ.items())],
                                     ensure_ascii=False).encode("utf-8")).hexdigest()[:16]


def _снятое():
    return json.loads(ЦЕЛЬ.read_text(encoding="utf-8")) if ЦЕЛЬ.exists() else {}


def _самопроверка():
    """Без процессов: снятые прогоны — ровно объявленные, сняты с этого проекта, lines сходится с отчётом."""
    было, знак, беды = _снятое(), отпечаток(), []
    if sorted(было) != sorted(R.ПРОГОНЫ):
        беды.append(f"сняты прогоны {sorted(было)}, объявлены {sorted(R.ПРОГОНЫ)}")
    for имя, снятое in было.items():
        if снятое.get("source") != знак:
            беды.append(f"{имя}: снято с другого проекта (отпечаток {снятое.get('source')}, объявленный {знак}) — "
                        f"снять заново: --снять")
        if not снятое["lines"] <= len(снятое["report"]) <= снятое["lines"] + 1:
            беды.append(f"{имя}: lines {снятое['lines']}, а строк отчёта {len(снятое['report'])}")
    for беда in беды:
        print("  БЕДА", беда)
    print(f"СЪЁМКА ПРОГОНОВ {'FAIL' if беды else 'PASS'}: прогонов {len(было)}, отпечаток {знак}, бед {len(беды)}")
    return 1 if беды else 0


ЧИСЛО = re.compile(r"\d+")


def сверить():
    """Снять заново и сравнить со снятым: exit, lines и слова каждой строки обязаны совпасть; числа (время бегуна,
    номер нити) плавают и печатаются, чтобы их видел глаз."""
    было, вон, беды = _снятое(), снять(), []
    for имя, b in вон.items():
        a = было.get(имя)
        if a is None:
            беды.append(f"{имя}: не снят")
            continue
        if (a["exit"], a["lines"]) != (b["exit"], b["lines"]):
            беды.append(f"{имя}: exit {a['exit']} → {b['exit']}, lines {a['lines']} → {b['lines']}")
        for i, (x, y) in enumerate(zip(a["report"], b["report"]), 1):
            if x != y and ЧИСЛО.sub("#", x) != ЧИСЛО.sub("#", y):
                беды.append(f"{имя}: строка {i} разнится словами: {x!r} → {y!r}")
            elif x != y:
                print(f"  {имя}: строка {i} — плавают числа: {x!r} → {y!r}")
    for беда in беды:
        print("  БЕДА", беда)
    print(f"СВЕРКА ПРОГОНОВ {'FAIL' if беды else 'PASS'}: прогонов {len(вон)}, бед {len(беды)}")
    return 1 if беды else 0


def main():
    if "--сверить" in sys.argv:
        return сверить()
    if "--снять" not in sys.argv:
        return _самопроверка()
    вон, знак = снять(), отпечаток()
    for снятое in вон.values():
        снятое["source"] = знак
    ЦЕЛЬ.write_text(json.dumps(вон, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for имя, снятое in вон.items():
        print(f"{имя}: exit {снятое['exit']} · millis {снятое['millis']} · lines {снятое['lines']}")
        for строка in снятое["report"]:
            print("    |", строка)
    return 0


if __name__ == "__main__":
    sys.exit(main())
