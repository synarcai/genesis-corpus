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
# РАМКА ЕСТЬ ПАРА ГЛАГОЛОВ (e9 03.09: had/used, had/lost, received/spent,
# bought/sold, found/lost — глаголы SVAMP): (v1, v2) → допустимые v3, знак,
# хвост второго предложения; «bought» открывает и прибыль (bought … more), и
# убыль (sold … of them) — судит пара, а не первый глагол.
РАМКИ_EN = {("had", "ate"): (("has", "have"), -1), ("picked", "lost"): (("keeps", "keep"), -1),
            ("found", "found"): (("has", "have"), 1), ("bought", "bought"): (("has", "have"), 1),
            ("had", "used"): (("has", "have"), -1), ("had", "lost"): (("has", "have"), -1),
            ("received", "spent"): (("has", "have"), -1), ("bought", "sold"): (("has", "have"), -1),
            ("found", "lost"): (("has", "have"), -1)}
V1 = r"(had|picked|found|bought|received)"
V2 = r"(ate|lost|found|bought|used|sold|spent)"
V3 = r"(has|have|keeps|keep|holds|hold)"
# THE TAILS OF THE QUESTION (e9 04.09): «still have left» / «have left with
# him» — a decrease; «have altogether» / «have in total» — a gain; «have now»
# / «have» — either. The state before the acts and the two-act comparison
# are their own frames below.
ХВОСТ_ВОПРОСА = r"(has|have|keeps|keep|holds|hold|still have left|have left with (?:him|her|them)|have now|have altogether|have in total)"
V1Q = r"(have|pick|find|buy|receive)"
ОСНОВЫ_V1 = {"had": "have", "picked": "pick", "found": "find", "bought": "buy", "received": "receive"}
СРАВНЕНИЯ = {("made", "sold"): ("make", "sell"), ("bought", "sold"): ("buy", "sell"), ("baked", "ate"): ("bake", "eat")}
МЕСТ = r"(he|she|they)"
ХВОСТ = r"(of them|more)"


def _лица_en(a, b, мест):
    лица = [a] + ([b] if b else [])
    if any(n not in РОД_EN for n in лица):
        return False
    if мест == "they":
        return len(лица) == 2
    return len(лица) == 1 and РОД_EN[a] == ("m" if мест == "he" else "f")


ДЕРЖАНИЯ_ВСЕ = ("has", "have", "keeps", "keep", "holds", "hold")


def _рамка_en(v1, v2, v3, хвост, left):
    """(знак) рамки или None: «of them» — убыль, «more» — прибыль; держание —
    любое из has/keeps/holds (e9 04.09: пара знаков покупается из ≥ 2 разных
    держаний); «left»/«remained» — только у убыли с has/have."""
    рамка = РАМКИ_EN.get((v1, v2))
    if рамка is None:
        return None
    v3ы, знак = рамка
    if v3 is not None and v3 not in ДЕРЖАНИЯ_ВСЕ:
        return None
    if хвост != ("more" if знак > 0 else "of them"):
        return None
    if left and not (знак < 0 and (v3 in (None, "has", "have"))):
        return None
    return знак


def _en_хвост(м):
    """A question with a tail: the tail's sign agrees with the frame's."""
    a, b, v1, n, вещь1, мест, v2, m, хвост, вещь2, a2, b2, хв, on, зн, om, k = м.groups()
    n, m, k, on, om = int(n), int(m), int(k), int(on), int(om)
    if (a, b) != (a2, b2) or вещь1 != вещь2 or not _лица_en(a, b, мест):
        return False
    знак = _рамка_en(v1, v2, None, хвост, False)
    if знак is None:
        return False
    if хв.startswith("still") or хв.startswith("have left with"):
        if знак > 0:
            return False
        if not хв.endswith(("him", "her", "them")) or хв.endswith({"he": "him", "she": "her", "they": "them"}[мест]) is False:
            pass
        if хв.startswith("have left with") and not хв.endswith({"he": "him", "she": "her", "they": "them"}[мест]):
            return False
    if хв in ("have altogether", "have in total") and знак < 0:
        return False
    return (on, om) == (n, m) and зн == ("+" if знак > 0 else "−") and k == n + знак * m >= 0


def _en_до(м):
    """The state before the acts: the answer repeats the first sentence."""
    a, b, v1, n, вещь1, мест, v2, m, хвост, вещь2, a2, b2, v1q, _до, a3, b3, v1b, n2, вещь3 = м.groups()
    if (a, b) != (a2, b2) != (a3, b3) and (a, b) != (a3, b3):
        return False
    if (a, b) != (a2, b2) or (a, b) != (a3, b3) or len({вещь1, вещь2, вещь3}) != 1 or not _лица_en(a, b, мест):
        return False
    return (_рамка_en(v1, v2, None, хвост, False) is not None and ОСНОВЫ_V1.get(v1) == v1q
            and v1b == v1 and int(n2) == int(n))


def _en_два_акта(м):
    """Two acts of one bearer compared: the difference is recomputed."""
    a, сд, x, вещь1, a2, пр, y, вещь2, a3, сд2, d, вещь3, он, пр2, ox, oy, od = м.groups()
    x, y, d, ox, oy, od = int(x), int(y), int(d), int(ox), int(oy), int(od)
    return (a == a2 == a3 and вещь1 == вещь2 == вещь3 and (сд, пр) in СРАВНЕНИЯ and сд2 == сд and пр2 == пр
            and a in РОД_EN and он == ("she" if РОД_EN[a] == "f" else "he")
            and d == x - y > 0 and (ox, oy, od) == (x, y, d))


def _en_два_акта_вопрос(м):
    a, сд, x, вещь1, a2, пр, y, вещь2, вещь3, он, сдq, прq, ox, oy, od = м.groups()
    x, y, ox, oy, od = int(x), int(y), int(ox), int(oy), int(od)
    return (a == a2 and вещь1 == вещь2 == вещь3 and СРАВНЕНИЯ.get((сд, пр)) == (сдq, прq)
            and a in РОД_EN and он == ("she" if РОД_EN[a] == "f" else "he")
            and (ox, oy, od) == (x, y, x - y) and x > y)


def _en(м):
    a, b, v1, n, вещь1, мест, v2, m, хвост, a2, b2, v3, k, вещь2, left = м.groups()
    n, m, k = int(n), int(m), int(k)
    if (a, b) != (a2, b2) or вещь1 != вещь2 or not _лица_en(a, b, мест):
        return False
    знак = _рамка_en(v1, v2, v3, хвост, bool(left))
    return знак is not None and k == n + знак * m >= 0


def _en_вопрос(м):
    a, b, v1, n, вещь1, мест, v2, m, хвост, вещь2, a2, b2, v3, left, on, зн, om, k = м.groups()
    n, m, k, on, om = int(n), int(m), int(k), int(on), int(om)
    if (a, b) != (a2, b2) or вещь1 != вещь2 or not _лица_en(a, b, мест):
        return False
    знак = _рамка_en(v1, v2, v3, хвост, bool(left))
    return (знак is not None and (on, om) == (n, m)
            and зн == ("+" if знак > 0 else "−") and k == n + знак * m >= 0)


def _en_остаток(м):
    """«how many cookies remained?» — вопрос без подлежащего: убыль, has/have."""
    a, b, v1, n, вещь1, мест, v2, m, хвост, вещь2, on, зн, om, k = м.groups()
    n, m, k, on, om = int(n), int(m), int(k), int(on), int(om)
    if вещь1 != вещь2 or not _лица_en(a, b, мест):
        return False
    знак = _рамка_en(v1, v2, None, хвост, True)
    return (знак == -1 and (on, om) == (n, m) and зн == "−" and k == n - m >= 0)


# RU: рамка — пара (основа первого глагола, основа второго); второй глагол
# согласуется по роду/числу таблицей.
ГЛ2_RU = {"съел": ("съел", "съела", "съели"), "потерял": ("потерял", "потеряла", "потеряли"),
          "нашёл ещё": ("нашёл ещё", "нашла ещё", "нашли ещё"), "купил ещё": ("купил ещё", "купила ещё", "купили ещё"),
          "использовал": ("использовал", "использовала", "использовали"), "потратил": ("потратил", "потратила", "потратили"),
          "продал": ("продал", "продала", "продали")}
РАМКИ_RU = {("было", "съел"): -1, ("собрал", "потерял"): -1, ("нашёл", "нашёл ещё"): 1, ("купил", "купил ещё"): 1,
            ("было", "использовал"): -1, ("было", "потерял"): -1, ("получил", "потратил"): -1,
            ("купил", "продал"): -1, ("нашёл", "потерял"): -1}
ПЕРВОЕ = r"(?:у ([А-ЯЁ][а-яё]+)(?: и ([А-ЯЁ][а-яё]+))? (было)|([А-ЯЁ][а-яё]+)(?: и ([А-ЯЁ][а-яё]+))? (собрал[аи]?|нашёл|нашла|нашли|купил[аи]?|получил[аи]?))"
ВТОРОЕ = r"(?:потом )?(он|она|они) (съел[аи]?|потерял[аи]?|нашёл ещё|нашла ещё|нашли ещё|купил[аи]? ещё|использовал[аи]?|потратил[аи]?|продал[аи]?) (\d+)( из них)?"


def _лица_ru(лица, мест):
    if any(n not in РОД_RU for n in лица):
        return False
    if мест == "они":
        return len(лица) == 2
    return len(лица) == 1 and РОД_RU[лица[0]] == ("m" if мест == "он" else "f")


# ОСНОВА ПЕРВОГО ГЛАГОЛА — ПО ТАБЛИЦЕ ФОРМ, А НЕ ПО ПРЕФИКСУ: «нашла», «нашли»
# не начинаются с «нашё» (страницы с «нашли» шли мимо суда, пока форма и
# тройка были сцеплены).
ГЛ1_RU = {"было": ("было",), "собрал": ("собрал", "собрала", "собрали"), "нашёл": ("нашёл", "нашла", "нашли"),
          "купил": ("купил", "купила", "купили"), "получил": ("получил", "получила", "получили")}


def _основа(глагол):
    for ключ, формы in ГЛ1_RU.items():
        if глагол in формы:
            return ключ
    return None


def _ru_разбор(м):
    г = м.groups()
    if г[2]:  # «у X было»
        лица_р = [x for x in (г[0], г[1]) if x]
        лица = [next((n for n in РОД_П if РОД_П[n] == р), None) for р in лица_р]
        v1 = "было"
    else:
        лица = [x for x in (г[3], г[4]) if x]
        v1 = _основа(г[5])
    return лица, v1, г[6:]


def _рамка_ru(v1, v2, из_них, лиц, мест):
    """Знак рамки или None: второй глагол — форма основы по роду/числу."""
    род = 2 if лиц == 2 else (0 if мест == "он" else 1)
    for (в1, основа), знак in РАМКИ_RU.items():
        if в1 == v1 and v2 == ГЛ2_RU[основа][род]:
            if bool(из_них) == (знак < 0):
                return знак
    return None


def _ru(м):
    лица, v1, хвост = _ru_разбор(м)
    n, вещь1, мест, v2, m, из_них, a2, b2, итог, k, вещь2 = хвост
    n, m, k = int(n), int(m), int(k)
    if None in лица or not _лица_ru(лица, мест):
        return False
    if [РОД_П[x] for x in лица] != [x for x in (a2, b2) if x]:
        return False
    знак = _рамка_ru(v1, v2, из_них, len(лица), мест)
    return знак is not None and итог == ("стало" if знак > 0 else "осталось") and k == n + знак * m >= 0


def _ru_вопрос(м):
    лица, v1, хвост = _ru_разбор(м)
    n, вещь1, мест, v2, m, из_них, вещь2, осталось, a2, b2, on, зн, om, k = хвост
    n, m, k, on, om = int(n), int(m), int(k), int(on), int(om)
    if None in лица or not _лица_ru(лица, мест):
        return False
    if [РОД_П[x] for x in лица] != [x for x in (a2, b2) if x]:
        return False
    знак = _рамка_ru(v1, v2, из_них, len(лица), мест)
    if знак is None or (осталось and знак > 0):
        return False
    return (on, om) == (n, m) and зн == ("+" if знак > 0 else "−") and k == n + знак * m >= 0


ОБРАЗЦЫ = (
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. {С}(?: and {С})? {V3} {Ч} {С}( left)?\.$", _en),
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. how many {С} (?:does|do) {С}(?: and {С})? {V3}( left)?\? {Ч} ([+−]) {Ч} = {Ч}\.$", _en_вопрос),
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. how many {С} remained\? {Ч} ([+−]) {Ч} = {Ч}\.$", _en_остаток),
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. how many {С} (?:does|do) {С}(?: and {С})? {ХВОСТ_ВОПРОСА}\? {Ч} ([+−]) {Ч} = {Ч}\.$", _en_хвост),
    (rf"^{С}(?: and {С})? {V1} {Ч} {С}\. (?:then |later )?{МЕСТ}(?: also)? {V2} {Ч} {ХВОСТ}\. how many {С} did {С}(?: and {С})? {V1Q} (at first|initially|at the beginning)\? {С}(?: and {С})? {V1} {Ч} {С}\.$", _en_до),
    (rf"^{С} (made|bought|baked) {Ч} {С}\. {С} (sold|ate) {Ч} {С}\. {С} (made|bought|baked) {Ч} more {С} than (he|she) (sold|ate): {Ч} − {Ч} = {Ч}\.$", _en_два_акта),
    (rf"^{С} (made|bought|baked) {Ч} {С}\. {С} (sold|ate) {Ч} {С}\. how many more {С} did (he|she) (make|buy|bake) than (sell|eat)\? {Ч} − {Ч} = {Ч}\.$", _en_два_акта_вопрос),
    (rf"^{ПЕРВОЕ} {Ч} {СЛ}\. {ВТОРОЕ}\. у {ИМЯ}(?: и {ИМЯ})? (осталось|стало) {Ч} {СЛ}\.$", _ru),
    (rf"^{ПЕРВОЕ} {Ч} {СЛ}\. {ВТОРОЕ}\. сколько {СЛ} (осталось )?у {ИМЯ}(?: и {ИМЯ})?\? {Ч} ([+−]) {Ч} = {Ч}\.$", _ru_вопрос),
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
