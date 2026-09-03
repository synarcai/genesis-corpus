#!/usr/bin/env python3
"""МИР МЕСТОИМЕНИЙ — местоимение стоит после названного лица и никогда не
открывает страницу; ответ идёт ПО ИМЕНИ.

Заказ e9 (03.09, полоса SVAMP): рынок местоимений покупает слово как
местоимение по страницам из трёх предложений «X V1 N. <pron> V2 M. X V3 K»
с K = N ± M; на срезе без такого рода он купил «коля» и «петя» — имена
стояли вторыми, а настоящих местоимений было мало. Масса рода (≥ 9 страниц
на местоимение) это выправляет; обе полярности не нужны — нужна масса и
ответ по имени.

СТРАНИЦА — ОДНА СТРОКА ИЗ ТРЁХ ПРЕДЛОЖЕНИЙ (закон читателя e9): лицо названо
в первом, местоимение — во втором (он/она по роду имени из пакета, они — при
двух лицах), в третьем — снова имя и итог. Вопросная поверхность: третье
предложение — вопрос по имени, ответ — уравнение (дом пары: величины вопроса
открывают ответ в его порядке; последнее число ответа — искомое):

    paco had 25 cookies. then he ate 5 of them. paco has 20 cookies.
    paco had 25 cookies. he ate 5 of them. how many cookies does paco have? 25 − 5 = 20.
    у Вани было 25 печений. потом он съел 5 из них. у Вани осталось 20 печений.

Глагольные тройки со знаком: убыль («of them» / «из них») и прибыль
(«more» / «ещё»). Род имени — пакетом (person_forms), русский падеж — тоже.
Суд местоимений (courts/pronoun_court.py) сверяет местоимение с родом и
числом лиц, имя третьего предложения — с первым, и пересчитывает K.
"""
import json
import pathlib
import sys

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(КОРЕНЬ / "tools"))
import rugram  # noqa: E402
from layer import emit_grouped  # noqa: E402
import verbthings  # noqa: E402
from plural import by_count  # noqa: E402

ЦЕЛЬ = "datasets/genesis_pronouns.txt"
_EN = json.loads((КОРЕНЬ / "tools" / "langpacks" / "en.json").read_text(encoding="utf-8"))
_RU = json.loads((КОРЕНЬ / "tools" / "langpacks" / "ru.json").read_text(encoding="utf-8"))
МУЖ_EN = [n for n in _EN["person_names"] if _EN["person_forms"][n]["gender"] == "m"]
ЖЕН_EN = [n for n in _EN["person_names"] if _EN["person_forms"][n]["gender"] == "f"]
МУЖ_RU = [n.capitalize() for n, ф in _RU["person_forms"].items() if ф["gender"] == "m"]
ЖЕН_RU = [n.capitalize() for n, ф in _RU["person_forms"].items() if ф["gender"] == "f"]
РОД_П = {n.capitalize(): ф["gen"].capitalize() for n, ф in _RU["person_forms"].items()}

# ≥ 2 ВЕЩИ НА КАЖДЫЙ ГЛАГОЛ (e9 03.09: суд историй требует ≥ 2 актёров и
# ≥ 2 вещей на глагол): у еды — печенье, яблоки, орехи, конфеты; у денег —
# монеты, доллары; в руке — марки, книги, ручки, карандаши.
ВЕЩИ = (("cookies", "печенье"), ("apples", "яблоко"), ("coins", "монета"), ("stamps", "марка"), ("books", "книга"), ("pens", "ручка"),
        ("nuts", "орех"), ("dollars", "доллар"), ("candies", "конфета"), ("pencils", "карандаш"))
# THE VERBS OF SVAMP THAT THE SCHOOL LACKED (e9 03.09: «used», «remained»,
# «spent», «received», «lost», «sold»): every triple is a frame (v1, v2) → v3
# with its sign; the decrease frames answer both «how many … does X have
# left?» and «how many … remained?». (V1 past, V2 past, V3 present sg, V3
# present pl, V3 question stem, sign, tail of the second sentence.)
ТРОЙКИ_EN = (("had", "ate", "has", "have", "have", -1, "of them"),
             ("picked", "lost", "keeps", "keep", "keep", -1, "of them"),
             ("found", "found", "has", "have", "have", 1, "more"),
             ("bought", "bought", "has", "have", "have", 1, "more"),
             ("had", "used", "has", "have", "have", -1, "of them"),
             ("had", "lost", "has", "have", "have", -1, "of them"),
             ("received", "spent", "has", "have", "have", -1, "of them"),
             ("bought", "sold", "has", "have", "have", -1, "of them"),
             ("found", "lost", "has", "have", "have", -1, "of them"))
НАРЕЧИЯ_EN = ("", "then ", "later ")
# RU: первое предложение (с падежом), второе (глагол по роду), третье; знак; хвост
ТРОЙКИ_RU = (("у {кого} было", ("съел", "съела", "съели"), "у {кого} осталось", -1, " из них"),
             ("{имя} {собрал}", ("потерял", "потеряла", "потеряли"), "у {кого} осталось", -1, " из них"),
             ("{имя} {нашёл}", ("нашёл ещё", "нашла ещё", "нашли ещё"), "у {кого} стало", 1, ""),
             ("{имя} {купил}", ("купил ещё", "купила ещё", "купили ещё"), "у {кого} стало", 1, ""),
             ("у {кого} было", ("использовал", "использовала", "использовали"), "у {кого} осталось", -1, " из них"),
             ("у {кого} было", ("потерял", "потеряла", "потеряли"), "у {кого} осталось", -1, " из них"),
             ("{имя} {получил}", ("потратил", "потратила", "потратили"), "у {кого} осталось", -1, " из них"),
             ("{имя} {купил}", ("продал", "продала", "продали"), "у {кого} осталось", -1, " из них"),
             ("{имя} {нашёл}", ("потерял", "потеряла", "потеряли"), "у {кого} осталось", -1, " из них"))
ГЛАГОЛЫ_RU = {"собрал": ("собрал", "собрала", "собрали"), "нашёл": ("нашёл", "нашла", "нашли"), "купил": ("купил", "купила", "купили"),
              "получил": ("получил", "получила", "получили")}
НАРЕЧИЯ_RU = ("", "потом ")
assert len(ТРОЙКИ_EN) == len(ТРОЙКИ_RU)


def ру(вещь, n):
    return rugram.форма(вещь, n)


def п_страница(шаг, i):
    """Параметры страницы: лица, местоимение, тройка, числа.

    ТРОЙКА И ФОРМА РАСЦЕПЛЕНЫ (e9 03.09): (шаг + i) % 4 выбирает форму
    страницы, (шаг + i) // 4 — тройку; прежде обе шли одной чётностью, и
    вопрос получали только страницы «found … more»."""
    кто = (шаг + i) % 3  # 0 he/он, 1 she/она, 2 they/они
    k = (шаг * 3 + i) // 3
    if кто == 0:
        en, ru = [МУЖ_EN[k % len(МУЖ_EN)]], [МУЖ_RU[k % len(МУЖ_RU)]]
    elif кто == 1:
        en, ru = [ЖЕН_EN[k % len(ЖЕН_EN)]], [ЖЕН_RU[k % len(ЖЕН_RU)]]
    else:
        en = [ЖЕН_EN[k % len(ЖЕН_EN)], МУЖ_EN[(k + 1) % len(МУЖ_EN)]]
        ru = [ЖЕН_RU[k % len(ЖЕН_RU)], МУЖ_RU[(k + 1) % len(МУЖ_RU)]]
    т = ((шаг + i) // 4 + шаг * 2) % len(ТРОЙКИ_EN)
    n = 6 + (шаг * 7 + i * 3) % 30
    m = 2 + (шаг + i * 5) % (n - 3)
    знак = ТРОЙКИ_EN[т][5]
    # A VERB TAKES ITS OWN KIND OF THINGS (tools/verbthings.py): «ate … of them» — food only
    # ИНДЕКС ВЕЩИ НЕ СЦЕПЛЕН С ЧЁТНОСТЬЮ ФОРМЫ: (шаг + i) % 4 выбирает язык и
    # форму, и вещь по (шаг + i) давала английским страницам одну вещь из двух.
    вещь = verbthings.подобрать(ТРОЙКИ_EN[т][:2], ВЕЩИ, (шаг + i) // 4 + шаг, ключ=lambda в: в[0])
    return dict(кто=кто, en=en, ru=ru, т=т, n=n, m=m, вещь=вещь,
                нареч=(шаг * 3 + i) % 3, тоже=((шаг + i) // 3) % 2 == 1, ответ=n + знак * m,
                вид=((шаг + i) // 4 + шаг) % 3)


def страница(шаг, i):
    п = п_страница(шаг, i)
    кто, n, m, k = п["кто"], п["n"], п["m"], п["ответ"]
    en, вещь_ru = п["вещь"]
    v1, v2, v3, v3мн, v3q, знак, хвост = ТРОЙКИ_EN[п["т"]]
    имена = " and ".join(п["en"])
    мест = ("he", "she", "they")[кто]
    третье = v3мн if кто == 2 else v3
    делает = "do" if кто == 2 else "does"
    нареч = НАРЕЧИЯ_EN[п["нареч"]]
    тоже = " also" if п["тоже"] else ""
    зн = "+" if знак > 0 else "−"
    # УБЫЛЬ ГОВОРИТ И «LEFT», И «REMAINED»: вид 0 — «has k», 1 — «has k left»
    # / «does X have left?», 2 — «how many … remained?»; прибыль — только вид 0.
    вид = п["вид"] if (знак < 0 and v3 == "has") else 0
    ф = (шаг + i) % 4
    if ф == 0:
        left = " left" if вид == 1 else ""
        return f"{имена} {v1} {n} {by_count(n, en)}. {нареч}{мест}{тоже} {v2} {m} {хвост}. {имена} {третье} {k} {by_count(k, en)}{left}."
    if ф == 2:
        if вид == 2:
            вопрос = f"how many {en} remained?"
        else:
            left = " left" if вид == 1 else ""
            вопрос = f"how many {en} {делает} {имена} {v3q}{left}?"
        return f"{имена} {v1} {n} {by_count(n, en)}. {нареч}{мест}{тоже} {v2} {m} {хвост}. {вопрос} {n} {зн} {m} = {k}."
    # русские страницы
    перв, втор, трет, знак_ru, хвост_ru = ТРОЙКИ_RU[п["т"]]
    род = 2 if кто == 2 else кто  # 0 м, 1 ж, 2 мн
    имя = " и ".join(п["ru"])
    кого = " и ".join(РОД_П[x] for x in п["ru"])
    первое = перв.format(кого=кого, имя=имя, **{г: ф_[род] for г, ф_ in ГЛАГОЛЫ_RU.items()})
    мест_ru = ("он", "она", "они")[кто]
    нареч_ru = НАРЕЧИЯ_RU[п["нареч"] % 2]
    if ф == 1:
        return f"{первое} {n} {ру(вещь_ru, n)}. {нареч_ru}{мест_ru} {втор[род]} {m}{хвост_ru}. {трет.format(кого=кого)} {k} {ру(вещь_ru, k)}."
    осталось = "осталось " if (знак < 0 and вид == 1) else ""
    return f"{первое} {n} {ру(вещь_ru, n)}. {нареч_ru}{мест_ru} {втор[род]} {m}{хвост_ru}. сколько {ру(вещь_ru, 5)} {осталось}у {кого}? {n} {зн} {m} = {k}."


# THE TAILS OF HOLDING AND THE HOLDINGS THEMSELVES (e9 04.09, the market of
# story skeletons — a tail of the question is part of the form, only the
# shown one is read): SVAMP asks «still have left», «have left with him»,
# «at first / initially / at the beginning» (the state before the acts: the
# first number), «altogether / in total»; and a pair of signs (ate → has) is
# bought only from ≥ 2 holdings — «has» beside «holds» and «keeps». Each tail
# and each holding gets its pages with different numbers and verbs; a page
# with two acts of one bearer asks «how many more did X make than sell».
ХВОСТЫ_УБЫЛИ = ("still have left", "have left with {мест_к}", "have now", "have")
ХВОСТЫ_ПРИБЫЛИ = ("have altogether", "have in total", "have now", "have")
ДО_АКТОВ = ("at first", "initially", "at the beginning")
ДЕРЖАНИЯ = (("has", "have"), ("holds", "hold"), ("keeps", "keep"))
# (act 1 past, act 2 past, base 1, base 2, things both acts take)
СРАВНЕНИЯ_EN = (("made", "sold", "make", "sell", ("cakes", "pies", "cookies")),
                ("bought", "sold", "buy", "sell", ("books", "pens", "cards")),
                ("baked", "ate", "bake", "eat", ("cookies", "cakes", "pies")))
ОСНОВА_V1 = {"had": "have", "picked": "pick", "found": "find", "bought": "buy", "received": "receive"}


def страница_хвостов(шаг, i):
    """The second block: tails, holdings, the state before the acts, the
    comparison of two acts of one bearer."""
    п = п_страница(шаг, i)
    кто, n, m, k = п["кто"], п["n"], п["m"], п["ответ"]
    en, _ = п["вещь"]
    v1, v2, v3, v3мн, v3q, знак, хвост = ТРОЙКИ_EN[п["т"]]
    имена = " and ".join(п["en"])
    мест = ("he", "she", "they")[кто]
    мест_к = ("him", "her", "them")[кто]
    делает = "do" if кто == 2 else "does"
    нареч = НАРЕЧИЯ_EN[п["нареч"]]
    факты = f"{имена} {v1} {n} {by_count(n, en)}. {нареч}{мест} {v2} {m} {хвост}."
    ф = (шаг * 3 + i) % 7
    if ф == 0:                                   # the state before the acts
        до = ДО_АКТОВ[(шаг + i) % 3]
        return f"{факты} how many {en} did {имена} {ОСНОВА_V1[v1]} {до}? {имена} {v1} {n} {by_count(n, en)}."
    if ф in (1, 2):                              # a tail of the question
        хв = (ХВОСТЫ_УБЫЛИ if знак < 0 else ХВОСТЫ_ПРИБЫЛИ)[(шаг + i) % 4].format(мест_к=мест_к)
        return f"{факты} how many {en} {делает} {имена} {хв}? {n} {'+' if знак > 0 else '−'} {m} = {k}."
    if ф in (3, 4):                              # another holding for the same pair
        д = ДЕРЖАНИЯ[1 + (шаг + i) % 2]
        держит = д[1] if кто == 2 else д[0]
        if ф == 3:
            return f"{факты} {имена} {держит} {k} {by_count(k, en)}."
        return f"{факты} how many {en} {делает} {имена} {д[1]}? {n} {'+' if знак > 0 else '−'} {m} = {k}."
    # two acts of one bearer, compared
    сд, пр, сдq, прq, вещи = СРАВНЕНИЯ_EN[(шаг + i) % 3]
    вещь = вещи[((шаг + i) // 3 + шаг) % len(вещи)]
    a = 8 + (шаг * 5 + i * 3) % 40
    b = 2 + (шаг + i * 7) % (a - 3)
    имя = п["en"][0]
    он = "she" if имя in ЖЕН_EN else "he"
    if ф == 5:
        return f"{имя} {сд} {a} {by_count(a, вещь)}. {имя} {пр} {b} {by_count(b, вещь)}. {имя} {сд} {a - b} more {by_count(a - b, вещь)} than {он} {пр}: {a} − {b} = {a - b}."
    # the question names the bearer by the pronoun — the world's own market
    return f"{имя} {сд} {a} {by_count(a, вещь)}. {имя} {пр} {b} {by_count(b, вещь)}. how many more {вещь} did {он} {сдq} than {прq}? {a} − {b} = {a - b}."


def pass_groups(шаг):
    return [[страница(шаг, i) for i in range(48)], [страница_хвостов(шаг, i) for i in range(48)]]


def main():
    emit_grouped(ЦЕЛЬ, pass_groups)


if __name__ == "__main__":
    main()
