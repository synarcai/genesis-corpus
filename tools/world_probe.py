#!/usr/bin/env python3
"""ЗАМЕР МИРА — всё, что нужно знать о мире, чтобы написать ему честное объявление.

Указатель миров назвал долг: миры с объявлением короче двухсот знаков. Платится он ковкой
объявлений, а объявление пишется ПО ЗАМЕРУ, а не по памяти. Замер этот рука сделала пять раз
подряд одинаково — строки, языки, знаки, доля вопроса, признаки границы, читающие суды.

    ТО, ЧТО РУКА ДЕЛАЛА ПЯТЬ РАЗ ОДИНАКОВО, ОБЯЗАНО СТАТЬ ПРИБОРОМ.

ЭТО НЕ СУД, А ОРУДИЕ РУКИ: у него нет рубежа и нет вердикта, и метки пустого обхода он не несёт —
стало быть, в набор не зовётся и падать ему нечем. Он отвечает на вопрос «что в этом мире?» и
молчит о том, хорош мир или плох.

    ОРУДИЕ, ОБЪЯВИВШЕЕ СЕБЯ ПРИБОРОМ, ОБЯЗАНО ЧТО-ТО ЗАЩИЩАТЬ; ОРУДИЕ, НЕ ОБЪЯВИВШЕЕ СЕБЯ ИМ,
    ОБЯЗАНО ЛИШЬ НЕ ЛГАТЬ.

ЧТО ОН МЕРИТ:
  · строки, байты, языки (кириллица против латиницы построчно);
  · знаки счёта и вопроса — сколько строк несёт «=», «?», «+», «−», «×», «÷»;
  · признаки манифеста: дробная запись, отрицательное значение, отказ с основанием, метка «¬»;
  · частые зачины и частые слова — чем мир говорит;
  · ЧИТАЮЩИЕ СУДЫ: палата, спрошенная о пробе строк, называет их поимённо с числом.

    python3 tools/world_probe.py genesis_units
    python3 tools/world_probe.py --бедные        # все миры с объявлением короче 200 знаков
"""
import collections
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(КОРЕНЬ / "tools"))
sys.path.insert(0, str(КОРЕНЬ / "courts"))
МАНИФЕСТ = КОРЕНЬ / "datasets" / "GENESIS-MANIFEST.json"
БЕДНОЕ = 200
КИРИЛЛИЦА = re.compile(r"[а-яё]", re.I)
ЛАТИНИЦА = re.compile(r"[a-z]", re.I)
ЗАЧИН = re.compile(r"^[^\s.?!]+(?:\s+[^\s.?!]+)?")


def _миры():
    return json.loads(МАНИФЕСТ.read_text(encoding="utf-8"))["worlds"]


def замерить(з, проба=50):
    import manifest_kinds as mk
    п = КОРЕНЬ / з["file"]
    if not п.is_file():
        try:
            import genesis
            п = genesis._resolve(з["file"])
        except Exception:                                  # noqa: BLE001
            pass
    if not п.is_file():
        print(f"{з['name']}: файла нет — {з['file']}")
        return
    текст = п.read_text(encoding="utf-8", errors="replace")
    строки = [с.strip() for с in текст.split("\n") if с.strip()]
    кир = sum(1 for с in строки if КИРИЛЛИЦА.search(с))
    лат = sum(1 for с in строки if ЛАТИНИЦА.search(с) and not КИРИЛЛИЦА.search(с))
    print(f"=== {з['name']}  ({з['file']})")
    print(f"  объявление: {len(з.get('genre') or '')} знаков"
          f"{'  ← БЕДНОЕ' if len(з.get('genre') or '') < БЕДНОЕ else ''}")
    print(f"  акт {з.get('act')} | оракул {з.get('oracle')} | граница {з.get('boundary')}")
    print(f"  строк {len(строки)}, байт {п.stat().st_size}; "
          f"кириллицей {кир}, латиницей {лат}, прочих {len(строки) - кир - лат}")
    знаки = {з_: sum(1 for с in строки if з_ in с) for з_ in ("=", "?", "+", "−", "×", "÷", "%")}
    print("  знаки: " + ", ".join(f"{к} {v}" for к, v in знаки.items() if v))
    print(f"  признаки манифеста: дробных {mk.дробных(текст)}, "
          f"знаковых {mk.знаковых(текст)}, отказов {mk.отказов(текст)}, "
          f"меткой «¬» {sum(1 for с in строки if с.startswith('¬'))}")
    зачины = collections.Counter(m.group(0).lower() for с in строки
                                 if (m := ЗАЧИН.match(с)))
    print("  частые зачины: " + ", ".join(f"«{к}» {v}" for к, v in зачины.most_common(6)))
    слова = collections.Counter(w.lower() for с in строки
                                for w in re.findall(r"[а-яёa-z]{4,}", с, re.I))
    print("  частые слова: " + ", ".join(f"{к} {v}" for к, v in слова.most_common(8)))
    try:
        from panel import палата
        суд = палата()
        слои = суд.слои(п)
        шаг = max(1, len(строки) // проба)
        кто = collections.Counter()
        судимо = 0
        for с in строки[::шаг][:проба]:
            вон = суд.судить(с, слои)
            if вон[0]:
                судимо += 1
                for и in (вон[2] if len(вон) > 2 else ()):
                    кто[и] += 1
        print(f"  читают (проба {min(проба, len(строки))}, судимо {судимо}): "
              + (", ".join(f"{и}×{n}" for и, n in кто.most_common(5)) or "НИКТО"))
    except Exception as беда:                              # noqa: BLE001
        print(f"  читают: палата не спрошена — {type(беда).__name__}")
    for с in строки[:3]:
        print(f"    | {с[:96]}")


def main():
    миры = _миры()
    if "--бедные" in sys.argv:
        for з in миры:
            if з.get("text") == "shows" and len(з.get("genre") or "") < БЕДНОЕ:
                print(f"{len(з.get('genre') or ''):4}  {з['name']}")
        return 0
    имена = [а for а in sys.argv[1:] if not а.startswith("-")]
    if not имена:
        print(__doc__.strip().splitlines()[-2].strip())
        return 2
    по = {з["name"]: з for з in миры}
    for и in имена:
        if и not in по:
            print(f"{и}: такого мира манифест не объявляет")
            continue
        замерить(по[и])
    return 0


if __name__ == "__main__":
    sys.exit(main())
