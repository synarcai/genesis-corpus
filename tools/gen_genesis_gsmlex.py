#!/usr/bin/env python3
"""GENESIS layer: THE FOUR-PLACE LEXICON — one step of counting said by MANY VERBS (rewritten 23.09).

Discipline: [agent verb NUMBER thing], both polarities, instances vary by pass, no glyph pairs
in-layer. Where `gsmwide` multiplies the THINGS, this world multiplies the VERBS over a few
things: the same step said with has / buys, had / got, collects / finds, picks / picks, and taken
away with gives away, lost, sold, ate — the count does not depend on the verb that tells it.

REWRITTEN 23.09 BY THE OWNER'S WORD (a band is an instrument, never a source). The world was «the
bill of materials measured from the real GSM8K questions' own four-places» — the band's top verbs
and items, paired so loosely that the pages said «Ben had 6 miles. Ben bought 1 mile more» and
«Felix uses 1 point away». Now the things are OUR lexicon, a pair of verbs takes only what BOTH
of its verbs take (`tools/verbthings.py` for the verbs it judges, the class of hand-held things
for the rest), «away» follows only the verb that gives, and the equation stands on EVERY page.
"""

from layer import Сбор, emit
import verbthings  # noqa: E402
from gsm_items import ITEMS, PACKAGEABLE, ТОВАРЫ  # noqa: E402


from plural import by_count

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_gsmlex.txt"


NAMES_HOUSE = ["ava", "ben", "carla", "dan",
         "elena", "felix", "grace", "hugo"]
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
# НЕМНОГИЕ ВЕЩИ — ИЗ СЛОВАРЯ, И ВСЕ ТАКИЕ, ЧТО ИХ ДЕРЖАТ В РУКЕ ИЛИ СОБИРАЮТ: мир о глаголах
ВЕЩИ = sorted(PACKAGEABLE & (verbthings.В_РУКЕ | verbthings.СБОР | verbthings.ЕДА))
assert set(ВЕЩИ) <= set(ITEMS)
ADD_PAIRS = [
    ("has", "buys"),
    ("had", "got"),
    ("collects", "finds"),
    ("picks", "picks"),
]
# (глагол своего, глагол убыли, хвост): «away» — у того, кто отдаёт, и только у него
SUB_PAIRS = [
    ("has", "gives", " away"),
    ("had", "lost", ""),
    ("has", "sells", ""),
    ("had", "ate", ""),
]
ASK_ADD = [("have now", "has"),
           ("own now", "owns")]
ASK_SUB = [("keep", "keeps"),
           ("have left", "has")]


def _годные(глаголы):
    """Вещи, какие берут ОБА глагола пары: судимый глагол — по двери; несудимый (has, buys, got,
    gives, lost, sells) — лишь товары: находимое и отломанное не покупают и не продают."""
    return [w for w in ВЕЩИ if all(verbthings.берёт(г, w) if г in verbthings.ГЛАГОЛ_БЕРЁТ else w in ТОВАРЫ
                                   for г in глаголы)]


assert all(_годные(п) for п in ADD_PAIRS) and all(_годные(п[:2]) for п in SUB_PAIRS)


# ДВА РОДА — ДВЕ ВЕТВИ `if add`: прибавка и убыль берут РАЗНЫЕ пары глаголов и разные
# вопросы. Лексика здесь и есть предмет мира: один и тот же счёт сказан четырьмя парами
# глаголов на сторону.
ПРИБАВКА = "прибавка: своя пара глаголов на каждый оборот"
УБЫЛЬ = "убыль: своя пара глаголов и свой вопрос"


def pass_shows(pi):
    base = pi * 37
    out = Сбор()
    for i in range(len(NAMES) * 10):
        # name index coprime-decoupled from the pair/polarity systematics
        nm = NAMES[
            (base + i + (i // 8) * 5)
            % len(NAMES)
        ]
        a = (base + i * 7) % 9 + 4   # 4..12
        b = (base + i * 3) % 3 + 1   # 1..3
        add = (base + i) % 2 == 0
        pick = ((base + i) // 2) % 4
        if add:
            out.род = ПРИБАВКА
            (v1, v2) = ADD_PAIRS[pick]
            годные = _годные((v1, v2))
            it = годные[(base + i * 5) % len(годные)]
            (ask, av) = ASK_ADD[((base + i) // 2) % 2]
            c = a + b
            out.append(
                f"{nm} {v1} {a} {by_count(a, it)}. "
                f"{nm} {v2} {b} {by_count(b, it)} "
                f"more. how many {it} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, it)}: {a} + {b} = {c}."
            )
        else:
            out.род = УБЫЛЬ
            (v1, v2, хвост) = SUB_PAIRS[pick]
            годные = _годные((v1, v2))
            it = годные[(base + i * 5) % len(годные)]
            (ask, av) = ASK_SUB[((base + i) // 2) % 2]
            c = a - b
            out.append(
                f"{nm} {v1} {a} {by_count(a, it)}. "
                f"{nm} {v2} {b} {by_count(b, it)}{хвост}. "
                f"how many {it} does {nm} "
                f"{ask}? {nm} {av} {c} "
                f"{by_count(c, it)}: {a} − {b} = {c}."
            )
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

# ЯЗЫК ДОМА ОБЪЯВЛЕН (15.09). Показы здесь несут одно имя рода, и для меры щербатости
# (`scripts/form_matrix.py`) дом был НЕЧИТАЕМ — молчание её было неотличимо от долга.
#
#     ДОМ, ПИШУЩИЙ НА ОДНОМ ЯЗЫКЕ, НЕ ДОЛЖЕН ВТОРОГО, И СКАЗАТЬ ОБ ЭТОМ ДЕШЕВЛЕ, ЧЕМ
#     ПЕРЕПИСЫВАТЬ ПОРОЖДЕНИЕ РАДИ ТОГО, ЧТО И ТАК ИЗВЕСТНО.
#
# Проверено счётом по ВСЕМУ словарю показов: 400 страниц, кириллицы 0, диакритики 0
ЯЗЫК = "en"

РОДЫ = (ПРИБАВКА, УБЫЛЬ)

ЗАЧЕМ_РОДА = {
    ПРИБАВКА: "a + b четырьмя парами глаголов и двумя вопросами — счёт один, слова разные",
    УБЫЛЬ: "a − b теми же средствами: лексика есть предмет этого мира",
}


def страницы(pi):
    return pass_shows(pi)


def перебор_страниц(pi):
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
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
