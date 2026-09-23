#!/usr/bin/env python3
"""GENESIS layer: THE LIVING ITEM LEXICON — our doors' things, named and counted (rewritten 23.09).

REWRITTEN 23.09 BY THE OWNER'S WORD (path «a» of the lead). The lexicon below was the census of the
public GSM8K bands, shown so that the reader would buy the band's own items; it is now OUR lexicon
(`tools/gsm_items.py`: the en pack's nouns in the classes of `tools/verbthings.py`). The frames stay;
what they may carry is narrowed to what they can say truly: counting frames and bare forms take
THINGS (the packable) and THE LIVING, never measures («packed 6 hours», «likes the inches»); «away»
stands only after a verb that takes it («gave 4 away», never «used 4 away»); the chain «made — sold
— made more» is written only of baked goods; names are written as the pack writes them.

HISTORY OF THE HOUSE, KEPT:

The g1 band stood at 0 of 65 with the mechanism alive: the real items
of the benchmark (lollipops, crates, sandwiches, vlogs, tablespoons)
were never bought into the ITEM role, because no layer ever showed
them. A market cannot buy what was never shown.

THE VOCABULARY IS CENSUS-DERIVED, NOT INVENTED. A word earns its place
by TWO independent witnesses in bench/suites/t7_gsm8k_g*.jsonl:
  · it stands after a number at least LAW times, and
  · it stands in a NUMBER-FREE question frame («how many/much X»).
That second witness is the law «the question confirms the item»: a
word that only ever follows a digit is a measure, not a thing. The
`plural` organ then certifies it — an item is a word that HAS a
singular; `of`, `in`, `is`, `were`, `more`, `total` have none and fall
away without a stop-list and without a word of English in this file.

TWO DISCIPLINES, BOTH REQUIRED:
  · the FOUR-PLACE frame [agent verb NUMBER item], twice per item, so
    the episodic algebra has raw material sharing one (agent, item)
    key;
  · NUMBER-FREE life — the same item in sentences carrying no digit at
    all, singular and plural. Without it the item is known only as
    «what follows a number», and the question frame cannot confirm it.

ONE CENSUS WORD IS DELIBERATELY ABSENT, AND THE REASON IS A DEBT,
NOT A DODGE: «fish» is invariant — its singular IS its plural — and a
corpus that must certify agreement BY ITS OWN USE cannot tell the two
apart. scripts/agreement_court.py therefore reads «1 fish» as a
disagreement, and it is right to, given what it can see. Weakening
the court for one word would blind it to the 1700 real faults it was
built for. Invariant nouns need their own show discipline and a court
that can see invariance; until both exist, the word waits, named.

No glyph pairs in-layer (worlds must not mix inside one file); the
count chooses the form through the shared `plural` organ.
"""

from layer import Сбор, emit


from gsm_items import ITEMS, PACKAGEABLE, ТОВАРЫ
from animacy import ANIMATE
import verbthings  # noqa: E402
from plural import by_count, singular

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_items.txt"

# ИМЕНА, ЧУЖИЕ БЕНЧМАРКУ: агенты не должны совпадать с носителями
# вопросов, иначе слой начнёт узнаваться по имени, а не по роду.
NAMES_HOUSE = ["ida", "omar", "pia", "rosa", "sven",
               "tara", "umar", "vera"]
# РЕГИСТР ИМЕНИ ЧИТАЕТСЯ ИЗ ПАКЕТА (как у соседей `gsmwide`, `verbs`): дом выбирает лица, пакет
# объявляет их письмо, и «umar counted» без заглавной больше не пишется.
import json as _json  # noqa: E402
import pathlib as _pathlib  # noqa: E402
_ИМЕНА_ПАКЕТА = set(_json.loads((_pathlib.Path(__file__).resolve().parent / "langpacks"
                                  / "en.json").read_text(encoding="utf-8"))["person_names"])
_ПО_СТРОЧНОМУ = {и.lower(): и for и in _ИМЕНА_ПАКЕТА}
NAMES = [_ПО_СТРОЧНОМУ.get(и, и) for и in NAMES_HOUSE]
assert set(NAMES) <= _ИМЕНА_ПАКЕТА, "имя не объявлено пакетом en"
# ДОМ НАЗЫВАЕТ И СЧИТАЕТ ВЕЩИ И ЖИВЫХ, НЕ МЕРЫ: мера («hours», «miles», «pounds») стоит в словаре
# ради домов мер, а «packed 6 hours» и «likes the inches» ложны о мире при верной грамматике.
# КУПЛЯ И ПРОДАЖА БЕРУТ ТОЛЬКО ТОВАР (`gsm_items.ТОВАРЫ`): «bought 3 leaves» дверь `verbthings`
# не судит (глагол купли ей не объявлен), и граница стоит здесь, у глаголов, которые дом пишет.
КУПЛЯ_ПРОДАЖА = frozenset({"bought", "buys", "sold", "sells"})
# ЦЕПЬ «написал — отослал — написал ещё» — о письмах и открытках: прежняя цепь «made — sold» о
# тортах была сценой самой полосы (SVAMP chal-220), и суд утечки назвал её шинглы. Вещь цепи
# берут оба глагола по двери `verbthings`.
ПИШУТ_И_ОТСЫЛАЮТ = frozenset(it for it in ITEMS
                             if verbthings.берёт("wrote", it) and verbthings.берёт("sent", it))

# Census of bench/suites/t7_gsm8k_g1+g2 (2026-09-01): after a number
# >= LAW times AND inside a number-free «how many/much X» frame, then
# certified by the `plural` organ. 66 items.
# (add-verb pair, ask, answer-verb) — real GSM8K prose verbs
# places of holding without a holder; the question of the decrease in three forms
МЕСТА_ВЕЩЕЙ = ("on the shelf", "in the box", "on the table", "in the basket", "in the bag")
МЕСТА_ЛЮДЕЙ = ("in the yard", "in the room", "at the party", "in the hall")
ВОПРОСЫ_ДЕРЖАНИЯ = ("how many {it} are left?", "how many {it} are there now?", "how many {it} remain?")
ADD_PAIRS = [("bought", "got"), ("found", "collected")]
# (глагол своего, глагол убыли, хвост убыли): «away» — у того, кто отдаёт, и только у него
SUB_PAIRS = [("had", "gave", " away"), ("bought", "lost", ""), ("picked", "ate", "")]
# A THING IS BOUGHT AND PACKED; A PERSON IS NOT. «ida bought 3 friends»
# is grammatical and false about the world, so animate items carry
# their own verbs and their own ask — the animacy itself is declared in
# gsm_items, where no census could have found it.
ADD_ANIM = [("counted", "met"), ("greeted", "met")]
SUB_ANIM = [("counted", "missed"), ("greeted", "missed")]
# (add-ask, add-verb, sub-ask, sub-verb); хвост убыли вещей — у пары глаголов, живых — пустой
ASK_THING = ("have now", "has", "keep", "keeps")
ASK_ANIM = ("know now", "knows", "still know", "knows")
# NUMBER-FREE frames: the item must live where no digit stands
BARE_PLURAL = [
    "{a} likes the {it}.",
    "the {it} are on the table.",
    "what are the {it}?",
]
BARE_SINGULAR = [
    "the {one} is a thing.",
    "{a} looks at the {one}.",
]
# «what are the children?» asks after a thing; «who» asks after a
# person, and a table is not where people are kept.
BARE_PLURAL_ANIM = [
    "{a} likes the {it}.",
    "the {it} are here.",
    "who are the {it}?",
]
BARE_SINGULAR_ANIM = [
    "the {one} is a person.",
    "{a} looks at the {one}.",
]


# ШЕСТЬ РОДОВ НАЗВАНЫ КОММЕНТАРИЯМИ НАД ВЕТВЯМИ И НЕ ВЫШЛИ НАРУЖУ. Одушевлённость вещи —
# не род, а ПРЕДМЕТ: она меняет глаголы и вопрос, но не дело.
ПРИБАВКА = "прибавка: акт и ещё акт того же носителя"
УБЫЛЬ = "убыль: отдано не больше своего"
ЦЕПЬ_АКТОВ = "цепь актов: написал, отослал, написал ещё — на сколько больше написал"
БЕЗ_НОСИТЕЛЯ = "держание без носителя: страница открывается МЕСТОМ, а не лицом"
МНОЖЕСТВЕННОЕ = "голая форма множественного при вещи"
ЕДИНСТВЕННОЕ = "голая форма единственного при вещи"


def _пары(it):
    """(пары прибавки, пары убыли), какие вещь ПО ПРАВДЕ берёт: судимый глагол — по двери,
    глагол купли-продажи — лишь товар, прочие несудимые — всякую вещь и всякого живого."""
    anim = it in ANIMATE
    add = ADD_ANIM if anim else ADD_PAIRS
    sub = [(v1, v2, "") for v1, v2 in SUB_ANIM] if anim else SUB_PAIRS

    def годен(г):
        if г in verbthings.ГЛАГОЛ_БЕРЁТ:
            return verbthings.берёт(г, it)
        return anim or г not in КУПЛЯ_ПРОДАЖА or it in ТОВАРЫ

    return ([п for п in add if all(годен(г) for г in п)],
            [п for п in sub if all(годен(г) for г in п[:2])])


# ВЕЩЬ ВХОДИТ В ДОМ, ЕСЛИ БЕРЁТ И ПАРУ ПРИБАВКИ, И ПАРУ УБЫЛИ; иначе закон дома («страница
# вопреки закону не пишется») остановил бы кузницу — и вещь уходит из дома с этим основанием.
ВЕЩИ_ДОМА = [it for it in ITEMS if (it in PACKAGEABLE or it in ANIMATE) and all(_пары(it))]


def pass_shows(pass_i):
    out = Сбор()
    for i, it in enumerate(ВЕЩИ_ДОМА):
        seed = pass_i * 31 + i * 7
        a = NAMES[seed % len(NAMES)]
        b = NAMES[(seed + 3) % len(NAMES)]
        one = singular(it)
        n = seed % 8 + 3          # 3..10
        m = seed % 4 + 1          # 1..4
        anim = it in ANIMATE
        q1, a1, q2, a2 = (
            ASK_ANIM if anim else ASK_THING)
        # A VERB TAKES ITS OWN KIND OF THINGS (tools/verbthings.py): the page
        # is per thing, so the PAIR follows the thing — «picked 4 miles» no more.
        #
        # ЗАПАСНОЙ ХОД «or add» ОТМЕНЁН (07.09, по просьбе holon-f9). Он значил вот
        # что: если закон не оставил дому НИ ОДНОЙ годной пары, дом берёт пару
        # НЕГОДНУЮ и пишет страницу вопреки закону — молча. Закон при этом стои́т в
        # тексте и в имени, и всякий читающий его верит, что он держит.
        #
        #     ЗАКОН С ЗАПАСНЫМ ХОДОМ ЕСТЬ НЕ ЗАКОН, А ПОЖЕЛАНИЕ. Он держит ровно
        #     там, где и без него всё в порядке, и отступает ровно там, где нужен.
        #
        # ЗАМЕРЕНО ПЕРЕД ПРАВКОЙ: ход этот НЫНЕ МЁРТВ — у всех 69 вещей есть годная
        # пара и сложения, и вычитания, и ни разу отступать не приходится. Свод от
        # правки не меняется ни на байт; меняется то, что случится ЗАВТРА, когда
        # заведут вещь без пары: дом ОСТАНОВИТСЯ с именем вещи в руках вместо того,
        # чтобы написать «picked 4 miles» и промолчать.
        add, sub = _пары(it)
        if not add or not sub:
            raise AssertionError(
                "вещь «%s» не берёт ни одной объявленной пары (%s): объяви пару в "
                "tools/verbthings.py или убери вещь — страница вопреки закону не "
                "пишется" % (it, "сложения" if not add else "вычитания"))
        v1, v2 = add[seed % len(add)]
        s1, s2, tail = sub[seed % len(sub)]
        out.род = ПРИБАВКА
        out.append(
            f"{a} {v1} {n} {by_count(n, it)}. "
            f"{a} {v2} {m} {by_count(m, it)} more. "
            f"how many {it} does {a} {q1}? "
            f"{a} {a1} {n + m} {by_count(n + m, it)}: {n} + {m} = {n + m}."
        )
        # NOBODY GIVES AWAY MORE THAN THEY HAVE (the heads layer showed
        # «keeps -1 coins» five times before this law was written down)
        gave = min(n, m)
        out.род = УБЫЛЬ
        out.append(
            f"{b} {s1} {n} {by_count(n, it)}. "
            f"{b} {s2} {gave} {by_count(gave, it)}{tail}. "
            f"how many {it} does {b} {q2}? "
            f"{b} {a2} {n - gave} {by_count(n - gave, it)}: {n} − {gave} = {n - gave}."
        )
        # НАКОПЛЕНИЕ ПОВТОРЁННОГО АКТА (конструкция названа переписью e9 04.09): «wrote … sent … of
        # them. then wrote N more … how many more did X write than send?» — оба звена цепью. Число
        # при «ещё» согласует имя («1 more letter»): прежняя рамка писала «made 1 more keys».
        # HOLDING WITHOUT A HOLDER (e9 04.09, SVAMP: «there are/were N … »
        # opens 44 of 726 problems): the page opens with the place, not with
        # an actor; the three question forms of the decrease alternate.
        if n - m >= 2 and m >= 2:
            out.род = БЕЗ_НОСИТЕЛЯ
            if anim:
                место = МЕСТА_ЛЮДЕЙ[seed % len(МЕСТА_ЛЮДЕЙ)]
                вопрос = ВОПРОСЫ_ДЕРЖАНИЯ[seed % len(ВОПРОСЫ_ДЕРЖАНИЯ)].format(it=it)
                out.append(f"there were {n} {it} {место}. {m} {it} left. {вопрос} {n} − {m} = {n - m}.")
            else:
                место = МЕСТА_ВЕЩЕЙ[seed % len(МЕСТА_ВЕЩЕЙ)]
                вопрос = ВОПРОСЫ_ДЕРЖАНИЯ[seed % len(ВОПРОСЫ_ДЕРЖАНИЯ)].format(it=it)
                out.append(f"there are {n} {it} {место}. {a} took {m} {it}. {вопрос} {n} − {m} = {n - m}.")
        out.род = МНОЖЕСТВЕННОЕ
        for tpl in (BARE_PLURAL_ANIM if anim
                    else BARE_PLURAL):
            out.append(tpl.format(a=a, it=it))
        out.род = ЕДИНСТВЕННОЕ
        for tpl in (BARE_SINGULAR_ANIM if anim
                    else BARE_SINGULAR):
            out.append(tpl.format(a=b, one=one))
    # ЦЕПЬ ИДЁТ СВОИМ ОБХОДОМ: письменное не упаковывают, и в ряд вещей дома письма не входят, а
    # цепь о них есть. Три показа на вещь за проход — род несёт массу (LAW³ = 8), а не одну строку.
    for j, it in enumerate(sorted(ПИШУТ_И_ОТСЫЛАЮТ)):
        for r in range(3):
            seed = pass_i * 31 + j * 11 + r * 17
            a = NAMES[seed % len(NAMES)]
            n = seed % 8 + 3          # 3..10
            m = seed % 4 + 1          # 1..4
            out.род = ЦЕПЬ_АКТОВ
            sold = min(n, m)
            # с «more» и без него поровну (e9): иначе «more» купится как условие суммы
            ещё = " more" if seed % 2 == 0 else ""
            out.append(
                f"{a} wrote {n} {by_count(n, it)}. {a} sent {sold} of them. "
                f"then {a} wrote {m}{ещё} {by_count(m, it)}. "
                f"how many more {it} did {a} write than send? "
                f"{n} + {m} = {n + m}, {n + m} − {sold} = {n + m - sold}."
            )
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

# ЯЗЫК ДОМА ОБЪЯВЛЕН (15.09). Показы здесь несут одно имя рода, и для меры щербатости
# (`scripts/form_matrix.py`) дом был НЕЧИТАЕМ — молчание её было неотличимо от долга.
#
#     ДОМ, ПИШУЩИЙ НА ОДНОМ ЯЗЫКЕ, НЕ ДОЛЖЕН ВТОРОГО, И СКАЗАТЬ ОБ ЭТОМ ДЕШЕВЛЕ, ЧЕМ
#     ПЕРЕПИСЫВАТЬ ПОРОЖДЕНИЕ РАДИ ТОГО, ЧТО И ТАК ИЗВЕСТНО.
#
# Проверено счётом по ВСЕМУ словарю показов: 2150 страниц, кириллицы 0, диакритики 0
ЯЗЫК = "en"

РОДЫ = (ПРИБАВКА, УБЫЛЬ, ЦЕПЬ_АКТОВ, БЕЗ_НОСИТЕЛЯ, МНОЖЕСТВЕННОЕ, ЕДИНСТВЕННОЕ)

ЗАЧЕМ_РОДА = {
    ПРИБАВКА: "n + m, и глагол берётся из пар, какие ДАННАЯ вещь принимает",
    УБЫЛЬ: "n − m, где отданное не больше своего: «keeps −1 coins» есть ложь о мире",
    ЦЕПЬ_АКТОВ: "два звена цепью: «написал n, отослал столько-то, написал ещё m — на сколько "
                "больше написал, чем отослал»",
    БЕЗ_НОСИТЕЛЯ: "«there were N … » — страница открывается МЕСТОМ, а не лицом: 44 задачи "
                  "из 726 в SVAMP устроены так",
    МНОЖЕСТВЕННОЕ: "голая форма множественного числа при этой вещи",
    ЕДИНСТВЕННОЕ: "голая форма единственного — та, при которой «1» ведёт себя как один",
}


def страницы(pass_i):
    return pass_shows(pass_i)


def перебор_страниц(pass_i):
    return pass_shows(pass_i).парами


def группы(pass_i):
    return [страницы(pass_i)]


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
