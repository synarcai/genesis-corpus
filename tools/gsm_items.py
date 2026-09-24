#!/usr/bin/env python3
"""THE ITEM LEXICON — one source, read by every layer; OUR lexicon since 23.09.

Two layers needed the same list and would have drifted apart the first time either was touched,
so the list lives here alone.

ЗАМЕНЁН 23.09 ПО СЛОВУ ВЛАДЕЛЬЦА (решение ведущего omega-90, путь «а»). До того здесь стояли 66
слов, выведенных переписью ПУБЛИЧНЫХ полос GSM8K g1/g2 (`tools/gsm_census.py`): «chimichangas»,
«vlogs», «tablespoons» были показаны затем, чтобы читатель купил словарь самих задач меры.

    СЛОВАРЬ, ВЫВЕДЕННЫЙ ИЗ МЕРЫ, ЕСТЬ ТЕЧЬ ПО САМОЙ ДВЕРИ: всякий дом, читающий его, учит
    читателя словам полосы, какими бы своими ни были его рамки и числа.

ОТКУДА СЛОВАРЬ ТЕПЕРЬ. Из двух наших дверей и ни из какой полосы:
  · существительные пакета en (`tools/langpacks/en.json`, `noun_forms` — множественное), и
  · школьные классы двери «глагол берёт свою вещь» (`tools/verbthings.py`): еда, питьё,
    выпечка, письменное, чтение, путь и время, вес, очки, деньги, посев, сбор, вещи в руке.
Вещь входит, если пакет её склоняет И класс её объявляет; одушевлённые (`tools/animacy.py`) —
если их склоняет пакет. Классы полосных глаголов (прыжок, упражнения, просмотр…) сюда не входят:
их вещи были взяты у полосы.

ОДНО ПИСЬМО МЕРЫ В ОДНОМ СЛОВАРЕ: где пакет даёт и британское, и американское письмо единицы,
берётся американское (письмо домов мер — «amer»); чья пара письма — говорит дверь единиц
(`tools/units.py`), а не список здесь.

Перепись полос (`tools/gsm_census.py`) осталась ПРИБОРОМ: она мерит, сколько слов полосы наш
словарь покрывает, и не диктует ему ни слова.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import units  # noqa: E402 — пары письма единиц
import verbthings  # noqa: E402 — классы вещей по глаголу
from animacy import ANIMATE  # noqa: E402 — одушевлённость: свой дом (23.09)

ШКОЛЬНЫЕ_КЛАССЫ = ("ЕДА", "ПИТЬЁ", "ВЫПЕЧКА", "ПИСЬМЕННОЕ", "ЧТЕНИЕ", "РАССТОЯНИЕ_ВРЕМЯ", "ВЕС",
                   "ОЧКИ", "ДЕНЬГИ", "ПОСЕВ", "СБОР", "ВРЕМЯ", "В_РУКЕ")

_ПАКЕТ = json.loads((pathlib.Path(__file__).resolve().parent / "langpacks" / "en.json")
                    .read_text(encoding="utf-8"))
_МНОЖЕСТВЕННЫЕ = frozenset(_ПАКЕТ["noun_forms"].values())
_В_КЛАССАХ = frozenset().union(*(getattr(verbthings, к) for к in ШКОЛЬНЫЕ_КЛАССЫ))
# британское письмо, чья американская пара тоже склоняется пакетом, — лишнее письмо той же меры
_БРИТАНСКИЕ = frozenset(
    en["brit"][1] for en, *_ in units.ФОРМЫ_ВСЕХ.values()
    if isinstance(en, dict) and "brit" in en and "amer" in en and en["brit"] != en["amer"]
    and en["amer"][1] in _МНОЖЕСТВЕННЫЕ)

# СЛОВА, КАКИЕ ДВЕРИ ДАЮТ, НО СЛОВАРЬ НЕ БЕРЁТ, НАЗЫВАЮТСЯ, А НЕ РОНЯЮТСЯ МОЛЧА. Прежде здесь
# стояли три слова переписи полос; ныне — слова наших дверей, выведенные из словаря с причиной.
WITHHELD = {
    "fish": (
        "invariant — its singular IS its plural, and a corpus that certifies agreement by its "
        "own use cannot tell the two apart"
    ),
}
# ОДНО ИМЯ — ОДНО ОПРЕДЕЛЕНИЕ (24.09, прибор [ЗАТЕНЕНИЕ]): словарь писался дважды — сперва целиком,
# потом без изъятых, — и читатель первой строки видел не тот словарь, каким живёт дом.
ITEMS = sorted((((_МНОЖЕСТВЕННЫЕ & _В_КЛАССАХ) - _БРИТАНСКИЕ) | (_МНОЖЕСТВЕННЫЕ & ANIMATE))
               - set(WITHHELD))

# УПАКОВАТЬ МОЖНО ВЕЩЬ, НО НЕ МЕРУ (М-103). «acres come 2 to a pack», «centimeters come 4 to a
# crate» безупречны грамматически и ложны о мире. Упаковываемое есть ВЕЩЬ дверей — в руке,
# выпечка, сбор, еда, — минус всё, что те же двери объявили мерой (путь и время, вес, очки,
# деньги, питьё мерой), и минус живое.
_МЕРЫ = frozenset().union(*(getattr(verbthings, к) for к in ("РАССТОЯНИЕ_ВРЕМЯ", "ВЕС", "ОЧКИ",
                                                              "ДЕНЬГИ", "ВРЕМЯ", "ПИТЬЁ_МЕРОЙ")))
# КАЛОРИЯ СТОИ́Т В КЛАССЕ ЕДЫ («ate 300 calories»), но она мера еды, а не еда, и сказано это ЗДЕСЬ,
# при упаковке, где различие и работает; глагол «съел» её берёт по праву.
_МЕРА_ЕДЫ = frozenset({"calories"})
PACKAGEABLE = frozenset(
    w for w in ITEMS
    if w in (verbthings.В_РУКЕ | verbthings.ВЫПЕЧКА | verbthings.СБОР | verbthings.ЕДА)
    and w not in _МЕРЫ and w not in _МЕРА_ЕДЫ and w not in ANIMATE)

# ТОВАР — ТО, ЧТО ПОКУПАЮТ И ПРОДАЮТ, А НЕ ВСЁ, ЧТО В РУКЕ. Лист, прутик и камень находят,
# кусок отламывают; «bought 3 leaves», «sells 2 pieces» верны грамматикой и ложны о мире. Глагол
# купли-продажи дверь `verbthings` не судит, и дома, пишущие его, берут вещи отсюда.
НАХОДЯТ_А_НЕ_ПОКУПАЮТ = frozenset({"leaves", "sticks", "stones", "pieces"})
ТОВАРЫ = frozenset(PACKAGEABLE - НАХОДЯТ_А_НЕ_ПОКУПАЮТ)

# ВЕЩЬ ДЕРЖАНИЯ — ШИРЕ УПАКОВЫВАЕМОГО (24.09, дверь актов `verbthings.АКТЫ`): письмо не пакуют, но
# его пишут, держат и отсылают; дерево не пакуют, но его сажают и растят. Держимое — всякая вещь
# словаря, кроме меры и живого; упаковываемое есть его часть.
ВЕЩИ = frozenset(w for w in ITEMS if w not in _МЕРЫ and w not in _МЕРА_ЕДЫ and w not in ANIMATE)

# ЧТО ЛИЦО ИМЕЕТ (24.09, строка 35 реестра пробелов): вещи, деньги, очки и живых — «Ava has 5 coins»,
# «Ben has 6 points», «Dan has 2 friends» верны; путь, вес, время, объём и калория лицу не принадлежат —
# «Hugo has 2 inches», «Elena has 2 days» грамматичны и ложны о мире. Деньги и очки суть меры для домов
# мер, но держат их лица, и потому они здесь.
ИМЕЮТ = ВЕЩИ | frozenset(w for w in ITEMS
                         if w in verbthings.ДЕНЬГИ or w in verbthings.ОЧКИ or w in ANIMATE)



def по_кругу(круг, k, годные):
    """k-е слово круга; слово вне «годных» уступает следующему годному (24.09, строка 35 реестра).

    НЕГОДНОЕ УСТУПАЕТ МЕСТО, А НЕ СДВИГАЕТ КРУГ: честные страницы стоят, где стояли, и меняются
    лишь те, где стояла мера при лице («Hugo has 2 inches») или мера, делимая как вещь («23 calories
    shared among 5 players»). Одно правило для всех домов круга, а не копия в каждом."""
    for шаг in range(len(круг)):
        слово = круг[(k + шаг) % len(круг)]
        if слово in годные:
            return слово
    raise AssertionError("в круге нет ни одного годного слова")


# ВСЯКОЕ ОБЪЯВЛЕНИЕ О СЛОВАРЕ ПРОВЕРЯЕТСЯ ИМ ЖЕ.
assert PACKAGEABLE <= ВЕЩИ, sorted(PACKAGEABLE - ВЕЩИ)
assert PACKAGEABLE <= set(ITEMS), sorted(PACKAGEABLE - set(ITEMS))
assert not (PACKAGEABLE & ANIMATE), sorted(PACKAGEABLE & ANIMATE)
assert not (set(ITEMS) & _БРИТАНСКИЕ), sorted(set(ITEMS) & _БРИТАНСКИЕ)
