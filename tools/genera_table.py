#!/usr/bin/env python3
"""ТАБЛИЦА РОДОВ С ФОРМУЛАМИ — эталон суда охвата (заказ holon 03.09).

Для каждой рамки-семейства мира: формула ответа от величин вопроса, языки,
полярности и ЧИСЛО ПОКАЗОВ, ЗАМЕРЕННОЕ ГЕНЕРАТОРОМ (не обещанное): таблица
собирается прогоном тех же функций, что пишут мир, и потому не расходится с
ним. Рамки, которые ДОЛЖНЫ купиться, — те, что здесь с ≥ LAW показами;
купленная рамка с чужой формулой — ложь охвата.

    python3 tools/genera_table.py  → declarations/GENERA.json
"""
import collections
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
ВЫХОД = КОРЕНЬ / "declarations" / "GENERA.json"
ПРОХОДОВ = 5
КИРИЛЛИЦА = re.compile(r"[а-яё]", re.I)


def полярность(строка):
    if "?" in строка:
        return "вопрос"
    if re.search(r"\bnot\b|\bне\b|\bnо\b", строка) and ": " in строка:
        return "отрицание"
    return "утверждение"


def семейства_gsmforms():
    import gen_genesis_gsmforms as G
    вон = []
    for семья in G.СЕМЕЙСТВА:
        имя = семья.__name__
        счёт = collections.Counter()
        for шаг in range(ПРОХОДОВ):
            for i in range(16):
                с = G.с_ответом(семья(шаг, i), шаг, i)
                счёт[("ru" if КИРИЛЛИЦА.search(с) else "en", полярность(с))] += 1
        вон.append({"мир": "gsmforms", "семейство": имя, "формула": G.ФОРМУЛЫ[имя],
                    "величины": sorted(k for k in getattr(G, "п_" + имя)(0, 0) if k != "ответ"),
                    "показов": {f"{яз}/{пол}": n for (яз, пол), n in sorted(счёт.items())},
                    "всего": sum(счёт.values())})
    return вон


def законы_миров():
    import laws
    вон = []
    for мир, з in laws.ЗАКОНЫ.items():
        for в_en, в_ru, з_en, з_ru in з:
            вон.append({"мир": мир, "семейство": в_en.rstrip("?"), "формула": "закон рода (определение фразой)",
                        "вопрос": {"en": в_en, "ru": в_ru}, "закон": {"en": з_en, "ru": з_ru},
                        "показов": {"en/вопрос": ПРОХОДОВ, "ru/вопрос": ПРОХОДОВ, "en/утверждение": ПРОХОДОВ, "ru/утверждение": ПРОХОДОВ},
                        "всего": 4 * ПРОХОДОВ})
    return вон


def рассуждения():
    import gen_genesis_inquiry as I
    import gen_genesis_equation as E
    import gen_genesis_statistics as S
    E._СО_ЗНАКОМ = False
    источники = (("inquiry", "простота", "вердикт = простое(n); свидетель n = d × (n ÷ d) | делители 1 и n", lambda ш: I.рассужд_простота(ш)),
                 ("inquiry", "делимость", "вердикт = a mod b == 0; свидетель a = b × q (+ r)", lambda ш: I.рассужд_делимость(ш)),
                 ("equation", "корень", "вердикт = v² + b·v + c == 0; свидетель подстановка", lambda ш: E.рассужд_корень(ш)),
                 ("statistics", "среднее/медиана", "среднее = сумма ÷ n; медиана = средний по порядку", lambda ш: sum((S.рассуждения(ш, i, S.НАБОРЫ[(ш + i) % len(S.НАБОРЫ)], sum(S.НАБОРЫ[(ш + i) % len(S.НАБОРЫ)]) // len(S.НАБОРЫ[(ш + i) % len(S.НАБОРЫ)]), S.НЕЧЁТНЫЕ[(ш * 3 + i) % len(S.НЕЧЁТНЫЕ)], sorted(S.НЕЧЁТНЫЕ[(ш * 3 + i) % len(S.НЕЧЁТНЫЕ)])[1]) for i in range(10)), [])))
    вон = []
    for мир, имя, формула, сделать in источники:
        счёт = collections.Counter()
        for шаг in range(ПРОХОДОВ):
            for с in сделать(шаг):
                яз = "ru" if КИРИЛЛИЦА.search(с) else "en"
                вид = "почему" if с.startswith(("why", "почему")) else "рассуждение"
                счёт[f"{яз}/{вид}"] += 1
        вон.append({"мир": мир, "семейство": имя + " (рассуждение)", "формула": формула,
                    "форма": "{вопрос}? {вердикт}: {свидетель}. {связка} {вывод}. {закон}.",
                    "показов": dict(sorted(счёт.items())), "всего": sum(счёт.values())})
    return вон


# МИРЫ С ОБЪЯВЛЕННЫМИ ВОПРОСАМИ (СПРОСИТЬ) И ФОРМУЛАМИ (ФОРМУЛЫ): род = вопрос,
# показы считаются совпадением строк мира с образцом вопроса.
МИРЫ_СПРОСИТЬ = ("numbers", "sequences", "geometry", "linalg", "physlaws", "statistics", "machine", "compsci", "physics", "units")
ДЫРКА = re.compile(r"\{[^}]+\}")


def роды_спросить():
    import importlib
    вон = []
    for мир in МИРЫ_СПРОСИТЬ:
        м = importlib.import_module(f"gen_genesis_{мир}")
        # ПОКАЗЫ СЧИТАЮТСЯ В МИРЕ, КАК ОН ЛЕЖИТ (datasets/genesis_<мир>.txt):
        # это и есть замер, а не повторное порождение; входы генераторов
        # различны (pass_groups, pass_shows, kinds), мир — один.
        строки = [с for с in (КОРЕНЬ / "datasets" / f"genesis_{мир}.txt").read_text(encoding="utf-8").splitlines() if с.strip()]
        for ключ, шаблон in м.СПРОСИТЬ.items():
            # ДЫРКА ШАБЛОНА ({n}, {предмет}) — ЛЮБАЯ ВЕЛИЧИНА; остальное — дословно.
            образец = re.compile("^" + re.sub(r"\\\{[^}]+\\\}", "(.+?)", re.escape(шаблон)) + " ")
            n = sum(1 for с in строки if образец.match(с))
            яз = "ru" if КИРИЛЛИЦА.search(шаблон) else "en"
            вон.append({"мир": мир, "семейство": ключ, "вопрос": шаблон, "формула": м.ФОРМУЛЫ[ключ],
                        "показов": {f"{яз}/вопрос": n}, "всего": n})
    return вон


def main():
    таблица = семейства_gsmforms() + законы_миров() + рассуждения() + роды_спросить()
    ВЫХОД.write_text(json.dumps({"comment": "таблица родов с формулами — эталон суда охвата; числа показов замерены генераторами на 5 проходах (tools/genera_table.py)",
                                 "родов": len(таблица), "показов": sum(р["всего"] for р in таблица), "роды": таблица},
                                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"ТАБЛИЦА РОДОВ: {len(таблица)} родов, {sum(р['всего'] for р in таблица)} показов → {ВЫХОД}")


if __name__ == "__main__":
    main()
