#!/usr/bin/env python3
"""[ВОСПРОИЗВОДИМОСТЬ] — отгруженный корпус обязан совпадать с порождённым.

Корпус в репозитории есть ИЗДЕЛИЕ генераторов, лежащих рядом. Если они
разошлись — правкой генератора без пересборки или правкой файла руками,
— то отгружено одно, а порождается другое, и всякий, кто соберёт корпус
заново, получит не то, что судили суды. Это тот же род беды, что
выведенные данные без выводящего: подпись «измерено» на рукописном
списке.

Прибор перезапускает КАЖДЫЙ генератор во временный каталог и сличает
sha256 с отгруженным. Ноль расхождений — рубеж.

ЧЕГО ПРИБОР НЕ ВИДИТ, НАЗВАНО: миры, у которых генератора нет вовсе
(школьные корпуса, прозаические учебники), он не проверяет и считает
отдельно — их воспроизводимость есть дело того конвейера, что их строит.
"""
import hashlib
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent

# РУБЕЖ-ДОЛГА: РАСХОЖДЕНИЙ_РУБЕЖ = 0
РАСХОЖДЕНИЙ_РУБЕЖ = 0

# ПУСТОЙ-ОБХОД: no-such-generator-dir

ПУТЬ = re.compile(r'emit(?:_grouped)?\(\s*"(datasets/[\w.]+\.txt)"')


def хэш(п):
    return hashlib.sha256(п.read_bytes()).hexdigest()


def main():
    генераторы = sorted((КОРЕНЬ / "tools").glob("gen_genesis_*.py"))
    if not генераторы:
        print("ВОСПРОИЗВОДИМОСТЬ ОТКАЗ: генераторов нет, сличать нечего")
        return 2
    расхождений = сличено = без_пути = 0
    имена = []
    with tempfile.TemporaryDirectory() as врем:
        двор = pathlib.Path(врем)
        (двор / "datasets").mkdir()
        for ф in ["layer.py", "plural.py", "segment.py", "genesis.py",
                  "gsm_items.py", "langpack.py"]:
            if (КОРЕНЬ / "tools" / ф).is_file():
                shutil.copy(КОРЕНЬ / "tools" / ф, двор / ф)
        if (КОРЕНЬ / "tools/langpacks").is_dir():
            shutil.copytree(КОРЕНЬ / "tools/langpacks", двор / "langpacks")
        for ген in генераторы:
            текст = ген.read_text(encoding="utf-8")
            м = ПУТЬ.search(текст)
            if not м:
                без_пути += 1
                continue
            цель = КОРЕНЬ / м.group(1)
            if not цель.is_file():
                continue
            shutil.copy(ген, двор / ген.name)
            r = subprocess.run([sys.executable, ген.name],
                               cwd=двор, capture_output=True, text=True)
            свежий = двор / м.group(1)
            if r.returncode or not свежий.is_file():
                расхождений += 1
                имена.append(f"{ген.name}: не собрался (rc={r.returncode})")
                continue
            сличено += 1
            if хэш(свежий) != хэш(цель):
                расхождений += 1
                имена.append(f"{ген.name}: {м.group(1)} разошёлся")
    for и in имена[:6]:
        print(f"  {и}")
    итог = "PASS" if расхождений <= РАСХОЖДЕНИЙ_РУБЕЖ else "FAIL"
    print(f"ВОСПРОИЗВОДИМОСТЬ {итог}: {расхождений} расхождений из "
          f"{сличено} сличённых ({без_пути} генераторов без явной цели)")
    return 0 if расхождений <= РАСХОЖДЕНИЙ_РУБЕЖ else 1


if __name__ == "__main__":
    sys.exit(main())
