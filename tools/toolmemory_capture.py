#!/usr/bin/env python3
"""ПРИБОР СЪЁМКИ МИРА ПАМЯТИ дома `toolmemory`: ответы сервера memory, снятые один раз (29.09, М-2100).

Ход мира на странице — НАСТОЯЩИЙ ответ сервера MCP за мостом ядра `ozar_mcp_world`, не наша модель графа. Всякий акт
страницы (`memoryworld.акты_страниц`) снимается своей сессией на свежем файле графа (`MEMORY_FILE_PATH` в новой папке):
сначала сервер сам строит объявленный граф голоса актами моста (`memoryworld.акты_графа` — всякий обязан быть
наблюдением без ошибки), затем идёт акт страницы; в семя `tools/seeds/toolmemory_world.json` ложатся ответ провода и
байты файла графа после акта целиком, под отпечатком объявленных графов и актов, с именем и версией сервера. Смена
сервера — новое семя, не правка старого (слово ведущего).

    ОРУДИЕ, ПЕРЕПИСЫВАЮЩЕЕ ДЕРЕВО, НЕ ПИШЕТ БЕЗ ДОВОДА. Без доводов прибор только читает: семя верно, пока отпечаток
    тот же, что при съёмке, и всякий объявленный акт снят без отказа моста.

    python3 tools/toolmemory_capture.py                    # самопроверка без процессов
    python3 tools/toolmemory_capture.py --снять [пути]     # снять заново всё и записать
    пути: --мост <ozar_mcp_world> --память <mcp-server-memory> (по умолчанию — из окружения: OZAR_MCP_WORLD,
    OZAR_MCP_MEMORY); --коммит <коммит моста> (OZAR_BRIDGE_COMMIT) — ложится в семя рядом с версией сервера: семя
    объявляет, каким мостом снято
"""
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import memoryworld as П  # noqa: E402 — объявление мира памяти: графы голосов, акты, отпечаток, семя

# ОТКАЗЫ МОСТА, А НЕ ПРАВДА МИРА: сервер, замолчавший сверх терпения, и сбой провода; семя с ними самопроверка не берёт
_БЕДЫ_МОСТА = ("io", "out-of-time")


def _довод(имя, окружение):
    if имя in sys.argv:
        return sys.argv[sys.argv.index(имя) + 1]
    return os.environ.get(окружение)


def _сессия(мост, память, акты):
    """Одна сессия моста на свежем файле графа: ответы на акты по порядку и байты файла графа после сессии."""
    корень = pathlib.Path(tempfile.mkdtemp(prefix="toolmemory-"))
    try:
        граф = корень / "memory.jsonl"
        ввод = "".join(П.ключ(*акт) + "\n" for акт in акты)
        вывод = subprocess.run([мост, память], input=ввод, capture_output=True, text=True, timeout=600, check=True,
                               cwd=корень, env={**os.environ, "MEMORY_FILE_PATH": str(граф)}).stdout.splitlines()
        assert len(вывод) == len(акты), (len(вывод), len(акты))
        return [json.loads(с) for с in вывод], (граф.read_text(encoding="utf-8") if граф.exists() else "")
    finally:
        shutil.rmtree(корень, ignore_errors=True)


def _версия(память):
    """Имя и версия пакета сервера — из его package.json рядом с исполняемым файлом."""
    for пакет in pathlib.Path(память).resolve().parents:
        манифест = пакет / "package.json"
        if манифест.exists():
            м = json.loads(манифест.read_text(encoding="utf-8"))
            return {"name": м.get("name"), "version": м.get("version")}
    return {"name": "?", "version": "?"}


def снять():
    мост = _довод("--мост", "OZAR_MCP_WORLD")
    память = _довод("--память", "OZAR_MCP_MEMORY")
    assert мост and память, "нужны пути моста и сервера: --мост, --память"
    (объявление,), _граф = _сессия(мост, память, [("declare", "", ())])
    вон = {"source": П.отпечаток(), "server": _версия(память), "bridge": _довод("--коммит", "OZAR_BRIDGE_COMMIT") or "?",
           "declare": bytes(объявление.get("bytes") or []).decode("utf-8"), "scenes": {}}
    for язык in П.ЯЗЫКИ:
        граф_ = П.акты_графа(язык)
        сцены = вон["scenes"][язык] = {}
        for акт in П.акты_страниц(язык):
            for _раз in range(3):
                ответы, файл = _сессия(мост, память, граф_ + [акт])
                if ответы[-1].get("why") not in _БЕДЫ_МОСТА:
                    break
            for а, о in zip(граф_, ответы):
                меры = {м["ledger"]: м["value"] for м in о.get("measures", [])}
                assert о.get("reply") == "observed" and меры.get("error") == 0, (язык, а, о)
            сцены[П.ключ(*акт)] = {"reply": ответы[-1], "graph": файл}
        print(f"{язык}: снято актов {len(сцены)} (граф голоса — {len(граф_)} актов)")
    П.СЕМЯ.parent.mkdir(parents=True, exist_ok=True)
    П.СЕМЯ.write_text(json.dumps(вон, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"СНЯТО: голосов {len(вон['scenes'])}, сервер {вон['server']['name']} {вон['server']['version']}, мост "
          f"{вон['bridge']}, отпечаток {вон['source']}")
    return 0


def _самопроверка():
    """Без процессов: семя снято с объявленных графов и актов (отпечаток тот же), всякий акт страницы снят, отказа
    моста нет; объявление сервера называет всякий род, какой акты зовут."""
    с, беды = П.семя(), []
    if not с:
        беды.append("семени нет — снять: --снять")
    else:
        if с.get("source") != П.отпечаток():
            беды.append(f"семя снято под отпечатком {с.get('source')}, а графы и акты — {П.отпечаток()}")
        роды = П.объявление()["роды"]
        for язык in П.ЯЗЫКИ:
            for акт in П.акты_графа(язык) + П.акты_страниц(язык):
                if акт[0] not in роды:
                    беды.append(f"{язык}: род {акт[0]} сервер не объявил")
            for акт in П.акты_страниц(язык):
                снятое = с.get("scenes", {}).get(язык, {}).get(П.ключ(*акт))
                if снятое is None:
                    беды.append(f"{язык}: акт {акт} не снят")
                elif снятое["reply"].get("why") in _БЕДЫ_МОСТА:
                    беды.append(f"{язык}: акт {акт} — отказ моста {снятое['reply'].get('why')} — снять заново")
    for беда in беды[:20]:
        print("  БЕДА", беда)
    print(f"СЪЁМКА МИРА ПАМЯТИ {'FAIL' if беды else 'PASS'}: голосов {len(П.ЯЗЫКИ)}, актов страниц "
          f"{sum(len(П.акты_страниц(я)) for я in П.ЯЗЫКИ)}, бед {len(беды)}")
    return 1 if беды else 0


def main():
    if "--снять" in sys.argv:
        return снять()
    return _самопроверка()


if __name__ == "__main__":
    sys.exit(main())
