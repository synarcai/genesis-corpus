#!/usr/bin/env python3
"""[ПОРОЖДЕНИЕ ПЛАСТА С ЧИСЛОМ] — строка судима тем, ПОРОЖДАЕТСЯ ЛИ ОНА из пакета.

Остаток долга судимости (03.09): 767 строк свода зачитывались СЛОВАРЁМ
пакета — «всякое ли слово объявлено», — а не истиной. Разведка назвала их:
счёт с классификатором (ja 187, am 145, ko 135, th 125, ta 125) и счётные
цепи (uk 30, fr 20). Суд формы пласта (`courts/langform_court.py`) до них не
дотянулся, ибо читает лексические дыры «{lex:класс:клетка}», а эти строки
стоят в шаблонах С ЧИСЛОМ: «{num:prod}冊の本があります。», «እዚህ {num:prod}
መጽሐፍ አለ።».

Форма суда — слово holon (03.09): судим не словарь, а СПОСОБНОСТЬ ПОРОДИТЬ
строку из объявленной формы и объявленных слов. Пакет объявляет шаблоны
рода в `show_kinds`; суд обращает шаблон в образец, где «{num:…}» есть
объявленное числительное этого языка, а «{lex:класс:клетка}» — объявленная
форма ИМЕННО ЭТОЙ клетки. Строка, ставшая подстановкой такого шаблона, —
порождается пакетом и потому судима содержанием: чужое слово, форма из
соседней клетки или неизвестное числительное образца не пройдут.

СЧЁТНАЯ ЦЕПЬ судится своим законом: «один два три чотири…» есть ряд
объявленных числительных, идущих ПОДРЯД; разрыв ряда — ложь.
"""
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))

ПАКЕТЫ = КОРЕНЬ / "tools" / "langpacks"
_ЛЕКС = re.compile(r"\{lex:([^:}]+):([^}]+)\}")
_ЧИСЛ = re.compile(r"\{num:([^}]+)\}")
_ЦЕПЬ = re.compile(r"\{chain\}")


def _пакеты():
    вон = {}
    for путь in sorted(ПАКЕТЫ.glob("*.json")):
        try:
            вон[путь.stem] = json.loads(путь.read_text(encoding="utf-8"))
        except ValueError:
            continue
    return вон


ПАКЕТЫ_ВСЕ = _пакеты()


def _числительные(пакет):
    вон = {}
    for ключ, слово in (пакет.get("numerals") or {}).items():
        к = str(ключ)
        if к.lstrip("-").isdigit():
            вон[int(к)] = str(слово)
    return вон


def _формы_клетки(пакет, класс, клетка):
    """The declared forms of ONE cell of a class — «one», «many», «by_n» …"""
    кл = (пакет.get("morph_classes") or {}).get(класс) or {}
    формы = кл.get("forms") or []
    лексемы = кл.get("lexemes") or {}
    вон = set()
    if клетка in формы:
        i = формы.index(клетка)
        for ряд in лексемы.values():
            if isinstance(ряд, list) and len(ряд) > i:
                вон.add(str(ряд[i]))
    else:
        # «by_n», «by_sum» — the cell is chosen by a count; every form may stand
        for ряд in лексемы.values():
            if isinstance(ряд, list):
                вон.update(str(ф) for ф in ряд)
    return вон


def _образцы():
    """[(язык, pattern)] — every declared template that carries a NUMBER."""
    вон = []
    for язык, пакет in ПАКЕТЫ_ВСЕ.items():
        числа = _числительные(пакет)
        if not числа:
            continue
        альт_чисел = "(?:" + "|".join(re.escape(с) for с in sorted(set(числа.values()), key=len, reverse=True)) + ")"
        for род in (пакет.get("show_kinds") or {}).values():
            for ш in род.get("templates") or ():
                if not _ЧИСЛ.search(ш) or _ЦЕПЬ.search(ш):
                    continue
                куски, конец, годно = [], 0, True
                for м in re.finditer(r"\{[^}]+\}", ш):
                    куски.append(re.escape(ш[конец:м.start()]))
                    дыра = м.group()
                    лекс = _ЛЕКС.fullmatch(дыра)
                    if лекс:
                        формы = _формы_клетки(пакет, лекс.group(1), лекс.group(2))
                        if not формы:
                            годно = False
                            break
                        куски.append("(?:" + "|".join(re.escape(ф) for ф in sorted(формы, key=len, reverse=True)) + ")")
                    elif _ЧИСЛ.fullmatch(дыра):
                        куски.append(альт_чисел)
                    else:
                        годно = False
                        break
                    конец = м.end()
                if not годно:
                    continue
                куски.append(re.escape(ш[конец:]))
                вон.append((язык, re.compile("^" + "".join(куски) + "$")))
    return вон


ОБРАЗЦЫ = _образцы()
_ПО_СЛОВУ = {язык: {с: з for з, с in _числительные(п).items()} for язык, п in ПАКЕТЫ_ВСЕ.items()}


_ПОРЯДОК = {язык: sorted(по_слову, key=len, reverse=True) for язык, по_слову in
            ((язык, {с: з for з, с in _числительные(п).items()}) for язык, п in ПАКЕТЫ_ВСЕ.items())}


def _раскусить(текст, язык):
    """Числа цепи, откушенные ЖАДНО: составное числительное есть ОДНО число
    («on bir» = 11, «двадцать один» = 21), и ряд по словам его бы разорвал."""
    по_слову = _ПО_СЛОВУ[язык]
    вон, i = [], 0
    while i < len(текст):
        if текст[i] == " ":
            i += 1
            continue
        for слово in _ПОРЯДОК[язык]:
            if текст.startswith(слово, i) and (i + len(слово) == len(текст) or текст[i + len(слово)] == " "):
                вон.append(по_слову[слово])
                i += len(слово)
                break
        else:
            return None
    return вон


def _цепь_счёта(строка):
    """(судимо, истинно) о счётной цепи: ряд объявленных числительных подряд."""
    текст = строка.strip().rstrip(".。")
    if len(текст.split()) < 3:
        return False, False
    for язык in _ПО_СЛОВУ:
        значения = _раскусить(текст, язык)
        if значения is None or len(значения) < 3:
            continue
        подряд = all(b - a == 1 for a, b in zip(значения, значения[1:]))
        return True, подряд
    return False, False


def судить(строка):
    с = строка.strip()
    if not с:
        return False, False
    for язык, образец in ОБРАЗЦЫ:
        if образец.match(с):
            return True, True
    return _цепь_счёта(с)


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip() or с.startswith("\x0c"):
                continue
            судимо, истинно = судить(с)
            if not судимо:
                continue
            итог["судимых"] += 1
            if not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(f"{путь.name}: {с}")
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:120]}")
    поза = "PASS" if итог["ложных"] == 0 else "FAIL"
    print(f"ПОРОЖДЕНИЕ ПЛАСТА {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
