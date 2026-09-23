#!/usr/bin/env python3
"""GENESIS layer: THE WIDE LEXICON WAVE — one step of counting said over MANY THINGS (rewritten 23.09).

Where `gsmlex` multiplies the VERBS over few things, this world multiplies the THINGS: the same
add-one or take-away step said of books and coins, of cakes and pages, of miles walked and
dollars spent — and every time the answer is recomputed. Plus the possessive genus: «Ava's hens
lay 7 eggs» — the acting noun (hens) agents the episode and the verb agrees with IT; the owner
rides as colour.

REWRITTEN 23.09 BY THE OWNER'S WORD (a band is an instrument, never a source). The world was
«the census-ranked verbs and items of the real GSM8K questions» and its possessive genus was the
band's very first problem («janet s ducks lay 16 eggs»), name and all. Now the things are OUR
lexicon (`tools/gsm_items.py`), each verb pair is tied to the class of things it truly takes
(`tools/verbthings.py`: one earns and spends MONEY, bakes and sells BAKED GOODS, walks a
DISTANCE, reads what is WRITTEN), the question verb is the verb of the act («how many miles does
Ava walk in all?», not «does Ava hold»), «away» follows only the verb that gives, and the
equation of the answer stands on EVERY page — the core door learns by deriving the answer.
"""

from layer import Сбор, emit
import verbthings  # noqa: E402
from gsm_items import ITEMS, PACKAGEABLE, ТОВАРЫ  # noqa: E402


from plural import by_count

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_gsmwide.txt"


NAMES_HOUSE = ["ava", "ben", "carla", "dan", "elena",
         "felix", "grace", "hugo", "iris",
         "mia", "nina", "lena"]
# ИМЯ ОБЪЯВЛЕНО ПАКЕТОМ (дом имён, М-131): суд читает имя группой и сверяет
# с пакетом; имя, которого пакет не знает, не вправе войти в показ.
import json as _json
import pathlib as _pathlib
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
# РЕГИСТР ИМЕНИ ЧИТАЕТСЯ ИЗ ПАКЕТА (05.09): список дома выбирает лица, пакет
# объявляет их письмо; «ann» дома есть «Ann» пакета, и в показ входит пакетное.
_ПО_СТРОЧНОМУ = {и.lower(): и for и in _ИМЕНА_ПАКЕТА}
NAMES = [_ПО_СТРОЧНОМУ.get(и.lower(), и) for и in NAMES_HOUSE]
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"

_СЛОВАРЬ = set(ITEMS)


def _берёт(глагол):
    """Вещи словаря, какие глагол ПО ПРАВДЕ берёт, — у двери `verbthings`, а не здесь."""
    return sorted(w for w in _СЛОВАРЬ if verbthings.берёт(глагол, w))


# ПАРА ГЛАГОЛОВ ВЯЗАНА С КЛАССОМ ВЕЩЕЙ, А ВОПРОС — С ДЕЛОМ ПАРЫ: (глагол, глагол ещё, вопрос,
# глагол ответа, вещи). Класс берётся у двери: у судимого глагола — его собственный ряд, у
# глагола, которого дверь не судит («buys», «gets», «has»), — класс вещей, какие покупают.
ПРИБАВКА_РЯД = (
    ("buys", "gets", "have now", "has", sorted(ТОВАРЫ & verbthings.В_РУКЕ)),
    ("collects", "finds", "have now", "has", sorted(_СЛОВАРЬ & verbthings.СБОР)),
    ("bakes", "bakes", "have now", "has", _берёт("bakes")),
    ("earns", "earns", "have now", "has", _берёт("earns")),
    ("walks", "walks", "walk in all", "walks", sorted(set(_берёт("walks")) - verbthings.ВРЕМЯ)),
    ("reads", "reads", "read in all", "reads", _берёт("reads")),
)
# (глагол своего, глагол убыли, хвост, вопрос, глагол ответа, вещи): «away» — у того, кто отдаёт
УБЫЛЬ_РЯД = (
    ("has", "gives", " away", "keep", "keeps", sorted(ТОВАРЫ & verbthings.В_РУКЕ)),
    ("has", "eats", "", "have left", "has", sorted(set(_берёт("eats")) & PACKAGEABLE)),
    ("has", "spends", "", "have left", "has", sorted(_СЛОВАРЬ & verbthings.ДЕНЬГИ)),
    ("bakes", "sells", "", "keep", "keeps", _берёт("bakes")),
)
assert all(ряд[-1] for ряд in ПРИБАВКА_РЯД + УБЫЛЬ_РЯД), "пара глаголов без единой вещи"
# ПРИТЯЖАТЕЛЬНЫЙ НОСИТЕЛЬ: (носитель, глагол при нём, основа для вопроса, вещь, do/does)
ПИТОМЦЫ = (("hens", "lay", "lay", "eggs", "do"), ("garden", "grows", "grow", "flowers", "does"))


# РОД ЗДЕСЬ БЫЛ НАЗВАН КОММЕНТАРИЕМ («possessive genus: the acting noun agents») И НЕ ВЫШЕЛ
# НАРУЖУ. Два прочих — две ветви `if add`, и это ДЕЛО, а не поверхность: прибавка и убыль
# берут разные пары глаголов и разные вопросы.
ПРИБАВКА = "прибавка: к своему прибавлено ещё"
УБЫЛЬ = "убыль: от своего отдано"
ПРИТЯЖАТЕЛЬНЫЙ = "притяжательный носитель: несёт питомец хозяина"


def pass_shows(pi):
    base = pi * 41
    out = Сбор()
    for i in range(len(NAMES) * 12):
        nm = NAMES[
            (base + i + (i // 8) * 5)
            % len(NAMES)
        ]
        a = (base + i * 5) % 9 + 4
        b = (base + i * 3) % 3 + 1
        add = (base + i) % 2 == 0
        if add:
            out.род = ПРИБАВКА
            v1, v2, ask, av, вещи = ПРИБАВКА_РЯД[((base + i) // 2) % len(ПРИБАВКА_РЯД)]
            itm = вещи[(base + i * 7) % len(вещи)]
            c = a + b
            out.append(
                f"{nm} {v1} {a} {by_count(a, itm)}. "
                f"{nm} {v2} {b} {by_count(b, itm)} "
                f"more. how many {itm} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, itm)}: {a} + {b} = {c}."
            )
        else:
            out.род = УБЫЛЬ
            v1, v2, хвост, ask, av, вещи = УБЫЛЬ_РЯД[((base + i) // 2) % len(УБЫЛЬ_РЯД)]
            itm = вещи[(base + i * 7) % len(вещи)]
            c = a - b
            out.append(
                f"{nm} {v1} {a} {by_count(a, itm)}. "
                f"{nm} {v2} {b} {by_count(b, itm)}{хвост}. "
                f"how many {itm} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, itm)}: {a} − {b} = {c}."
            )
        # possessive genus: the acting noun agents; the verb agrees with it, not with the owner
        if i % 4 == 0:
            out.род = ПРИТЯЖАТЕЛЬНЫЙ
            pet, vp, v0, вещь, do = ПИТОМЦЫ[(base + i) % len(ПИТОМЦЫ)]
            a2 = (base + i * 3) % 8 + 3
            b2 = (base + i) % 3 + 1
            out.append(
                f"{nm}'s {pet} {vp} {a2} {by_count(a2, вещь)}. "
                f"{nm}'s {pet} {vp} {b2} {by_count(b2, вещь)} more. "
                f"how many {вещь} {do} the {pet} {v0} in all? "
                f"the {pet} {vp} {a2 + b2} {by_count(a2 + b2, вещь)}: {a2} + {b2} = {a2 + b2}."
            )
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

# ЯЗЫК ДОМА ОБЪЯВЛЕН (15.09). Показы здесь несут одно имя рода, и для меры щербатости
# (`scripts/form_matrix.py`) дом был НЕЧИТАЕМ — молчание её было неотличимо от долга.
#
#     ДОМ, ПИШУЩИЙ НА ОДНОМ ЯЗЫКЕ, НЕ ДОЛЖЕН ВТОРОГО, И СКАЗАТЬ ОБ ЭТОМ ДЕШЕВЛЕ, ЧЕМ
#     ПЕРЕПИСЫВАТЬ ПОРОЖДЕНИЕ РАДИ ТОГО, ЧТО И ТАК ИЗВЕСТНО.
#
# Проверено счётом по ВСЕМУ словарю показов: 840 страниц, кириллицы 0, диакритики 0
ЯЗЫК = "en"

РОДЫ = (ПРИБАВКА, УБЫЛЬ, ПРИТЯЖАТЕЛЬНЫЙ)

ЗАЧЕМ_РОДА = {
    ПРИБАВКА: "a + b, где оба глагола пары суть «взял» и «взял ещё»",
    УБЫЛЬ: "a − b, где второй глагол уносит",
    ПРИТЯЖАТЕЛЬНЫЙ: "подлежащее есть ЧУЖОЙ носитель («{имя}'s {питомец}»), и сказуемое "
                    "согласуется с ним, а не с хозяином",
}


def страницы(pi):
    return pass_shows(pi)


def перебор_страниц(pi):
    """[(строка, род)] — ТОТ ЖЕ ОБХОД, что и у кузницы, прочтённый вторым столбцом."""
    return pass_shows(pi).парами


def группы(pi):
    return [страницы(pi)]


def _показы():
    from layer import PASSES                             # noqa: PLC0415
    вон = {}
    for шаг in range(len(PASSES)):
        for с, род in перебор_страниц(шаг):
            for строка in с.split("\n"):
                if строка.rstrip():
                    вон.setdefault(строка.rstrip(), род)
    return вон


ПОКАЗЫ = _показы()


def _самопроверка_дома():
    assert set(ЗАЧЕМ_РОДА) == set(РОДЫ), "глосса рода разошлась с объявлением"
    сбор = pass_shows(0)
    assert len(сбор) == len(сбор.роды), "показ остался без рода"
    вне = {р for _с, р in сбор.парами} - set(РОДЫ)
    assert not вне, f"род кован и не объявлен: {sorted(вне)}"
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
