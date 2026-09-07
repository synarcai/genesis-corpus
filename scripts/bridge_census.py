#!/usr/bin/env python3
"""РАЗНОСТЬ МОСТОВ: FULL против школьного среза — какие стены среза на своде закрыты.

    свод FULL:  datasets/GENESIS-FULL.txt — 32 549 388 байт, 06.09 14:56, 24676660a30336a9
    срез:       /tmp/full27.txt           — 19 504 070 байт, 06.09 03:30

Мост есть страница, где глагол стои́т в ВОПРОСЕ своей вопросной формой, а рядом —
ответ-факт. Глагол берётся из строк (слово перед числом, живущее в двух формах), язык
строки — английский, ибо «did X sind» не существует в природе.
"""
import collections, json, pathlib, re, sys
К = pathlib.Path("/Users/taaliman/projects/oldman/synarcai/genesis-corpus")
sys.path.insert(0, str(К / "tools"))
import langsign  # noqa: E402

_ПЕРЕД_ЧИСЛОМ = re.compile(r"(?<![\w-])([a-z]{3,})\s+\d")
_ВОПРОС = re.compile(r"(?<![\w-])(?:did|does|do)\s+(?:the\s+)?([A-Za-z]+)\s+([a-z]{3,})(?![\w-])")
_СЛУЖЕБНЫЕ = {"and", "the", "for", "with", "has", "have", "had", "was", "were", "are", "his", "her",
              "than", "then", "there", "these", "those", "all", "any", "each", "every", "how", "many",
              "much", "more", "less", "one", "two", "six", "ten", "not", "but", "out", "off", "per",
              "cost", "costs", "into", "onto", "from", "over", "under", "about", "after", "before",
              "left", "now", "still", "also", "only", "just", "que", "des", "les", "una", "uno",
              "worth", "total", "together", "both", "some", "first", "last", "next", "same",
              "other", "another", "such", "very"}
НЕПРАВИЛЬНЫЕ = {"bought": "buy", "sold": "sell", "got": "get", "made": "make", "paid": "pay",
                "found": "find", "lost": "lose", "took": "take", "gave": "give", "put": "put",
                "read": "read", "kept": "keep", "held": "hold", "ate": "eat", "wrote": "write"}


def база(г):
    if г in НЕПРАВИЛЬНЫЕ:
        return НЕПРАВИЛЬНЫЕ[г]
    for х in ("ed", "es", "s"):
        if г.endswith(х) and len(г) - len(х) >= 3:
            return г[:-len(х)]
    return г


def перепись(путь, имя):
    утв, воп = collections.Counter(), collections.Counter()
    нос = collections.defaultdict(set)
    формы = collections.defaultdict(set)
    for с in путь.read_text(encoding="utf-8", errors="replace").splitlines():
        с = с.strip()
        if not с or langsign.язык(с) not in (None, "en"):
            continue
        низ = с.lower()
        for м in _ПЕРЕД_ЧИСЛОМ.finditer(низ):
            г = м.group(1)
            if г in _СЛУЖЕБНЫЕ:
                continue
            утв[г] += 1
            формы[база(г)].add(г)
        for м in _ВОПРОС.finditer(с):
            г = м.group(2).lower()
            if г in _СЛУЖЕБНЫЕ:
                continue
            воп[г] += 1
            нос[г].add(м.group(1).lower())
    свод = collections.Counter()
    for г, n in утв.items():
        свод[база(г)] += n
    свод = {б: n for б, n in свод.items() if len(формы[б]) >= 2}
    мосты = {б for б in свод if воп.get(б, 0) >= 4 and len(нос.get(б, ())) >= 2}
    print(f"  [{имя}] глаголов истории {len(свод)}, с мостом {len(мосты)}")
    return свод, воп, нос, мосты


ф_свод, ф_воп, ф_нос, ф_мосты = перепись(К / "datasets" / "GENESIS-FULL.txt", "FULL")
с_свод, с_воп, с_нос, с_мосты = перепись(pathlib.Path("/tmp/full27.txt"), "срез")
закрыты = sorted(ф_мосты - с_мосты, key=lambda б: -ф_свод.get(б, 0))
открыты = sorted(с_мосты - ф_мосты, key=lambda б: -с_свод.get(б, 0))
общие = ф_мосты & с_мосты
print(f"\nМОСТ ЕСТЬ В FULL И НЕТ В СРЕЗЕ (стена среза, на своде ЗАКРЫТАЯ): {len(закрыты)}")
for б in закрыты[:16]:
    print(f"    {б:<14} FULL: утв {ф_свод.get(б,0):>5}, вопр {ф_воп.get(б,0):>4}, нос {len(ф_нос.get(б,())):>3}"
          f"   срез: утв {с_свод.get(б,0):>5}, вопр {с_воп.get(б,0):>4}")
print(f"\nМОСТ ЕСТЬ В СРЕЗЕ И НЕТ В FULL: {len(открыты)}")
for б in открыты[:8]:
    print(f"    {б:<14} срез вопр {с_воп.get(б,0)}, FULL вопр {ф_воп.get(б,0)}")
print(f"\nМОСТ В ОБОИХ: {len(общие)}")
без = sorted((б for б in ф_свод if б not in ф_мосты and ф_свод[б] >= 150), key=lambda б: -ф_свод[б])
print(f"\nБЕЗ МОСТА В FULL ПРИ 150+ УТВЕРЖДЕНИЙ: {len(без)}")
for б in без[:14]:
    print(f"    {б:<14} утв {ф_свод[б]:>5}, вопросов {ф_воп.get(б,0):>4}, носителей {len(ф_нос.get(б,())):>3}")
