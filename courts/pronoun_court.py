#!/usr/bin/env python3
"""[МЕСТОИМЕНИЯ] — местоимение читается родом и числом названного лица, итог
пересчитывается, ответ идёт по имени.

Мир местоимений (tools/gen_genesis_pronouns.py) показывает страницы из трёх
предложений: лицо названо в первом, местоимение стоит во втором, в третьем
снова имя и итог (или вопрос по имени с уравнением в ответе). Суд сверяет:
местоимение с родом имени из пакета (he/она — по объявленному роду, they/они
— при двух лицах), имя третьего предложения с первым (по-русски — через
родительный из пакета), глагольную тройку (убыль с «of them»/«из них»,
прибыль с «more»/«ещё») и итог K = N ± M. Счётные формы при числах читает
суд согласования — хозяин своего рода.
"""
import json
import pathlib
import re
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import asking  # noqa: E402
import families  # noqa: E402

_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
РОД_EN = {n: ф["gender"] for n, ф in _EN["person_forms"].items()}
РОД_RU = {n.capitalize(): ф["gender"] for n, ф in _RU["person_forms"].items()}
РОД_П = {n.capitalize(): ф["gen"].capitalize() for n, ф in _RU["person_forms"].items()}

Ч = r"(\d+)"
С = r"([a-z]+)"
ИМЯ = r"([А-ЯЁ][а-яё]+)"
СЛ = r"([а-яё]+)"
УБЫЛЬ_EN = {"had": ("ate", ("has", "have")), "picked": ("lost", ("keeps", "keep"))}
ПРИБЫЛЬ_EN = {"found": ("found", ("has", "have")), "bought": ("bought", ("has", "have"))}
V1 = r"(had|picked|found|bought)"
V2 = r"(ate|lost|found|bought)"
V3 = r"(has|have|keeps|keep)"
МЕСТ = r"(he|she|they)"
ХВОСТ = r"(of them|more)"


def _лица_en(a, b, мест):
    лица = [a] + ([b] if b else [])
    if any(n not in РОД_EN for n in лица):
        return False
    if мест == "they":
        return len(лица) == 2
    return len(лица) == 1 and РОД_EN[a] == ("m" if мест == "he" else "f")


def _тройка_en(v1, v2, v3, хвост, знак):
    if v1 in УБЫЛЬ_EN:
        v2_, v3_ = УБЫЛЬ_EN[v1]
        return v2 == v2_ and v3 in v3_ and хвост == "of them" and знак == -1
    v2_, v3_ = ПРИБЫЛЬ_EN[v1]
    return v2 == v2_ and v3 in v3_ and хвост == "more" and знак == 1


def _en(м):
    a, b, v1, n, вещь1, мест, v2, m, хвост, a2, b2, v3, k, вещь2 = м.groups()
    n, m, k = int(n), int(m), int(k)
    if (a, b) != (a2, b2) or вещь1 != вещь2 or not _лица_en(a, b, мест):
        return False
    знак = 1 if хвост == "more" else -1
    return _тройка_en(v1, v2, v3, хвост, знак) and k == n + знак * m >= 0


def _en_вопрос(м):
    a, b, v1, n, вещь1, мест, v2, m, хвост, вещь2, a2, b2, v3, on, зн, om, k = м.groups()
    n, m, k, on, om = int(n), int(m), int(k), int(on), int(om)
    if (a, b) != (a2, b2) or вещь1 != вещь2 or not _лица_en(a, b, мест):
        return False
    знак = 1 if хвост == "more" else -1
    return (_тройка_en(v1, v2, v3, хвост, знак) and (on, om) == (n, m)
            and зн == ("+" if знак > 0 else "−") and k == n + знак * m >= 0)


УБЫЛЬ_RU = {"было": ("съел", "съела", "съели"), "собрал": ("потерял", "потеряла", "потеряли")}
ПРИБЫЛЬ_RU = {"нашёл": ("нашёл ещё", "нашла ещё", "нашли ещё"), "купил": ("купил ещё", "купила ещё", "купили ещё")}
ПЕРВОЕ = r"(?:у ([А-ЯЁ][а-яё]+)(?: и ([А-ЯЁ][а-яё]+))? (было)|([А-ЯЁ][а-яё]+)(?: и ([А-ЯЁ][а-яё]+))? (собрал[аи]?|нашёл|нашла|нашли|купил[аи]?))"
ВТОРОЕ = r"(?:потом )?(он|она|они) (съел[аи]?|потерял[аи]?|нашёл ещё|нашла ещё|нашли ещё|купил[аи]? ещё) (\d+)( из них)?"


def _лица_ru(лица, мест):
    if any(n not in РОД_RU for n in лица):
        return False
    if мест == "они":
        return len(лица) == 2
    return len(лица) == 1 and РОД_RU[лица[0]] == ("m" if мест == "он" else "f")


def _основа(глагол):
    for ключ in ("было", "собрал", "нашёл", "купил"):
        if глагол.startswith(ключ[:4]):
            return ключ
    return None


def _ru_разбор(м):
    г = м.groups()
    if г[2]:  # «у X было»
        лица_р = [x for x in (г[0], г[1]) if x]
        лица = [n for n in РОД_П if РОД_П[n] in лица_р]
        лица = [next((n for n in РОД_П if РОД_П[n] == р), None) for р in лица_р]
        v1 = "было"
    else:
        лица = [x for x in (г[3], г[4]) if x]
        v1 = _основа(г[5])
    return лица, v1, г[6:]


def _ru(м):
    лица, v1, хвост = _ru_разбор(м)
    n, вещь1, мест, v2, m, из_них, a2, b2, итог, k, вещь2 = хвост
    n, m, k = int(n), int(m), int(k)
    if None in лица or not _лица_ru(лица, мест):
        return False
    if [РОД_П[x] for x in лица] != [x for x in (a2, b2) if x]:
        return False
    return _тройка_ru(v1, v2, из_них, итог, len(лица), мест) and k == n + (1 if v1 in ПРИБЫЛЬ_RU else -1) * m >= 0


def _тройка_ru(v1, v2, из_них, итог, лиц, мест):
    род = 2 if лиц == 2 else (0 if мест == "он" else 1)
    if v1 in УБЫЛЬ_RU:
        return v2 == УБЫЛЬ_RU[v1][род] and bool(из_них) and итог == "осталось"
    if v1 in ПРИБЫЛЬ_RU:
        return v2 == ПРИБЫЛЬ_RU[v1][род] and not из_них and итог == "стало"
    return False


def _ru_вопрос(м):
    лица, v1, хвост = _ru_разбор(м)
    n, вещь1, мест, v2, m, из_них, вещь2, a2, b2, on, зн, om, k = хвост
    n, m, k, on, om = int(n), int(m), int(k), int(on), int(om)
    if None in лица or not _лица_ru(лица, мест):
        return False
    if [РОД_П[x] for x in лица] != [x for x in (a2, b2) if x]:
        return False
    знак = 1 if v1 in ПРИБЫЛЬ_RU else -1
    итог = "стало" if знак > 0 else "осталось"
    return (_тройка_ru(v1, v2, из_них, итог, len(лица), мест) and (on, om) == (n, m)
            and зн == ("+" if знак > 0 else "−") and k == n + знак * m >= 0)


ОБРАЗЦЫ = (
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. {С}(?: and {С})? {V3} {Ч} {С}\.$", _en),
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. how many {С} (?:does|do) {С}(?: and {С})? {V3}\? {Ч} ([+−]) {Ч} = {Ч}\.$", _en_вопрос),
    (rf"^{ПЕРВОЕ} {Ч} {СЛ}\. {ВТОРОЕ}\. у {ИМЯ}(?: и {ИМЯ})? (осталось|стало) {Ч} {СЛ}\.$", _ru),
    (rf"^{ПЕРВОЕ} {Ч} {СЛ}\. {ВТОРОЕ}\. сколько {СЛ} у {ИМЯ}(?: и {ИМЯ})?\? {Ч} ([+−]) {Ч} = {Ч}\.$", _ru_вопрос),
)
СЕМЕЙСТВА_СУДА = (("страница", list(ОБРАЗЦЫ)),)
ПРАВИЛА = families.правила(СЕМЕЙСТВА_СУДА)


def судить(строка):
    """(судимо, истинно) для одной строки."""
    с = строка.strip()
    if not re.search(r"\b(he|she|they|он|она|они)\b", с):
        return False, False
    for образец, проверить in ПРАВИЛА:
        м = образец.match(с)
        if м:
            try:
                return True, bool(проверить(м))
            except (ValueError, TypeError, KeyError):
                return True, False
    return False, False


def main():
    import collections
    from genesis import worlds
    итог = collections.Counter(); примеры = []
    for путь in worlds(kind="shows"):
        if путь.name != "genesis_pronouns.txt":
            continue
        for с in путь.read_text(encoding="utf-8").splitlines():
            if not с.strip() or с.startswith("\x0c"):
                continue
            судимо, истинно = судить(с)
            итог["судимых" if судимо else "несудимых"] += 1
            if судимо and not истинно:
                итог["ложных"] += 1
                if len(примеры) < 5:
                    примеры.append(с)
    for п in примеры:
        print(f"  ЛОЖЬ: {п[:110]}")
    поза = "PASS" if итог["ложных"] == 0 and итог["несудимых"] == 0 else "FAIL"
    print(f"МЕСТОИМЕНИЯ {поза}: {итог['ложных']} ложных из {итог['судимых']} судимых, несудимых {итог['несудимых']}")
    return 0 if поза == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
