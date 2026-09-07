#!/usr/bin/env python3
"""ЧЕКАНКА СВОБОДНЫХ ТАКТОВ для t9_reasoning: числа даёт ЗАМЕР, а не рука.

Условие omega: числа и ответы даёт генератор, не рука, и проверяются течью у самого
генератора. Здесь чеканятся замены для четырёх родов, чьи такты стоя́т в своде:
root 48/48, prime 24/48, median 15/24, mean 11/24.

    ЧИСЛО СВОБОДНО, ЕСЛИ ЕГО ВОПРОС НЕ СТОИТ В СВОДЕ НИ В ОДНОМ ПОКАЗЕ.
"""
import json, pathlib, re
К = pathlib.Path("/Users/taaliman/projects/oldman/synarcai/genesis-corpus")
свод = (К / "datasets" / "GENESIS-FULL.txt").read_text(encoding="utf-8", errors="replace").lower()
срез = pathlib.Path("/tmp/full27.txt").read_text(encoding="utf-8", errors="replace").lower()


def свободен(вопрос):
    н = вопрос.lower().strip()
    return н not in свод and н not in срез


def простое(n):
    return n >= 2 and all(n % d for d in range(2, int(n ** 0.5) + 1))


вон = []
# ПРОСТОТА: пары «да/нет» на числах, чьих вопросов свод не писал
кандидаты = [n for n in range(100, 400)
             if свободен(f"является ли {n} простым числом?") and свободен(f"is {n} a prime number?")]
пр = [n for n in кандидаты if простое(n)]
со = [n for n in кандидаты if not простое(n)]
for i in range(12):
    for n, ждём_ru, ждём_en in ((пр[i], "да", "yes"), (со[i], "нет", "no")):
        вон.append(("prime", f"is {n} a prime number?", ждём_en))
        вон.append(("prime", f"является ли {n} простым числом?", ждём_ru))
# КОРЕНЬ: уравнения x² − s·x + p = 0 с корнями (a, b), которых свод не писал
корни = []
for a in range(2, 30):
    for b in range(a + 1, 40):
        s, p = a + b, a * b
        воп = f"is {a} a root of x^2 - {s} x + {p} = 0?"
        if свободен(воп) and свободен(f"является ли {a} корнем x^2 - {s} x + {p} = 0?"):
            корни.append((a, b, s, p))
        if len(корни) >= 24:
            break
    if len(корни) >= 24:
        break
for a, b, s, p in корни[:12]:
    вон.append(("root", f"is {a} a root of x^2 - {s} x + {p} = 0?", "yes"))
    вон.append(("root", f"является ли {a} корнем x^2 - {s} x + {p} = 0?", "да"))
    не = a + b + 1
    вон.append(("root", f"is {не} a root of x^2 - {s} x + {p} = 0?", "no"))
    вон.append(("root", f"является ли {не} корнем x^2 - {s} x + {p} = 0?", "нет"))
печ = {}
for род, воп, ждём in вон:
    печ.setdefault(род, []).append((воп, ждём))
for род, сп in печ.items():
    print(f"\n=== {род}: {len(сп)} свободных тактов ===")
    for воп, ждём in сп[:6]:
        print(f"    «{воп}»  → {ждём}")
pathlib.Path("/private/tmp/claude-501/-Users-taaliman-projects-oldman-synarcai-genesis-corpus/"
             "c35edaf0-c202-4765-b1df-32c3d0f7d540/scratchpad/free_tacts.json").write_text(
    json.dumps(вон, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\nвсего свободных тактов: {len(вон)} — записаны в free_tacts.json")
