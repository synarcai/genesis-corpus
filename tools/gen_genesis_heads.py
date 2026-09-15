#!/usr/bin/env python3
"""GENESIS layer: THE TWO QUESTION HEADS of GSM8K
(32's census: 'how many X' 51.8% + 'how much X' 26.3%
= 78% of question clauses; the clause asks, the story
narrates — the clause law of measurement).

Shows are OUR instances (never benchmark strings):
micro-story (1-2 facts) + head clause + answer —
PURE prose (glyph pairs poisoned the phase in-layer;
digits inside the stories are already glyphs, the
number canon bridges them). Units ride as
lexicon (hours/miles/days/pounds — 32: units are
lexicon, not construction). Instances vary by pass.
"""

from layer import Сбор, emit


from plural import by_count

# ПУТЬ, СКАЗАННЫЙ ТОЛЬКО В ЗОВЕ, ЕСТЬ ПУТЬ, О КОТОРОМ НЕ ОБЪЯВЛЕНО (14.09): указатель
# читает объявление СТРОКОЙ ВЕРХНЕГО УРОВНЯ, и мир, названный лишь внутри `emit`,
# остаётся не связанным ни с одним домом.
ЦЕЛЬ = "datasets/genesis_heads.txt"


NAMES_HOUSE = ["mary", "peter", "vera", "nick", "ann",
         "dima", "lena", "yuri"]
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
ITEMS = ["apples", "balls", "books", "coins",
         "nuts", "stamps", "cookies", "pieces"]
UNITS = ["hours", "miles", "days", "pounds",
         "minutes"]
# a rate's verb and the unit it takes: hours are slept, minutes run, miles
# walked, pounds lifted; «days every day» is no rate — pages are read instead
СТАВКА_ГЛАГОЛ = {"hours": ("sleeps", "hours"), "minutes": ("runs", "minutes"), "miles": ("walks", "miles"),
                 "pounds": ("lifts", "pounds"), "days": ("reads", "pages")}


# ЧЕТЫРЕ ГОЛОВЫ НАЗВАНЫ КОММЕНТАРИЯМИ «HEAD-1/HEAD-2» И НЕ ВЫШЛИ НАРУЖУ. Голова здесь —
# ВОПРОСНОЕ СЛОВО («how many» против «how much»), а род — ДЕЛО под ним: прибавка, убыль,
# цена за штуку, ставка за день. Две головы, четыре дела.
ПРИБАВКА = "прибавка: было столько, получено ещё"
УБЫЛЬ = "убыль: было столько, отдано столько, и больше своего не отдают"
ЦЕНА_ЗА_ШТУКУ = "цена за штуку: сколько заплачено за k штук по p"
СТАВКА_ЗА_ДЕНЬ = "ставка за день: сколько за k дней, и глагол идёт за единицей"


def pass_shows(pi):
    base = pi * 29
    out = Сбор()
    for i in range(len(NAMES) * 4):
        nm = NAMES[(base + i) % len(NAMES)]
        it = ITEMS[(base + i * 3) % len(ITEMS)]
        un = UNITS[(base + i * 2) % len(UNITS)]
        a = (base + i * 5) % 9 + 3      # 3..11
        b = (base + i * 3) % 4 + 1      # 1..4
        p = (base + i) % 4 + 2          # 2..5
        k = (base + i * 7) % 5 + 2      # 2..6
        # ОТВЕТ И ЕГО КУЗНИЦА — ДВЕ ПОВЕРХНОСТИ ОДНОГО ФАКТА (М-166). Все
        # четыре головы вычисляют ответ из чисел вопроса, и ни один из 640
        # показов не нёс шага; кузница встаёт рядом с голым ответом
        # чередованием по номеру, на разряде, свободном от разрядов имени,
        # вещи, единицы и ставки.
        forge = ((base + i) // 4) % 2 == 0
        # HEAD-1 how many: got-more (three verbs
        # share one (agent, item) key — the
        # episodic algebra needs the full triple)
        out.род = ПРИБАВКА
        out.append(
            f"{nm} had {a} {by_count(a, it)}. "
            f"{nm} got {b} {by_count(b, it)}. "
            f"how many {it} does {nm} "
            f"have now? {nm} has {a + b} {it}"
            f"{f': {a} + {b} = {a + b}' if forge else ''}."
        )
        # HEAD-1 how many: left
        # NOBODY GIVES AWAY MORE THAN THEY HAVE.
        # With a in 3..11 and b in 1..4 drawn apart,
        # a-b reached -1 and the layer showed «peter
        # keeps -1 coins» five times: a false claim
        # about the world, not about arithmetic.
        # Zero stays — a remainder of none is true.
        gave = min(a, b)
        out.род = УБЫЛЬ
        out.append(
            f"{nm} had {a} {by_count(a, it)}. "
            f"{nm} gave {gave} {by_count(gave, it)} "
            f"away. how many {it} are "
            f"left? {nm} keeps {a - gave} "
            f"{by_count(a - gave, it)}"
            f"{f': {a} − {gave} = {a - gave}' if forge else ''}."
        )
        # HEAD-2 how much: rate pay
        out.род = ЦЕНА_ЗА_ШТУКУ
        out.append(
            f"{nm} bought {k} {by_count(k, it)} "
            f"at {p} {by_count(p, 'dollars')} each. how much did "
            f"{nm} pay? {nm} paid {k * p} {by_count(k * p, 'dollars')}"
            f"{f': {k} × {p} = {k * p}' if forge else ''}."
        )
        # HEAD-2 how much: unit rate over time. THE VERB FOLLOWS THE UNIT
        # (03.09): «walks 2 pounds every day», «walks 5 days every day» were
        # nonsense wearing the frame — a rate is a verb with its own unit.
        verb, un_r = СТАВКА_ГЛАГОЛ[un]
        out.род = СТАВКА_ЗА_ДЕНЬ
        out.append(
            f"{nm} {verb} {p} {by_count(p, un_r)} "
            f"every day. how much in {k} {by_count(k, 'days')}? "
            f"{k * p} {un_r}"
            f"{f': {p} × {k} = {k * p}' if forge else ''}."
        )
    return out


# --------------------------------------------------------------- ОБЪЯВЛЕНИЕ ДОМА

# ЯЗЫК ДОМА ОБЪЯВЛЕН (15.09). Показы здесь несут одно имя рода, и для меры щербатости
# (`scripts/form_matrix.py`) дом был НЕЧИТАЕМ — молчание её было неотличимо от долга.
#
#     ДОМ, ПИШУЩИЙ НА ОДНОМ ЯЗЫКЕ, НЕ ДОЛЖЕН ВТОРОГО, И СКАЗАТЬ ОБ ЭТОМ ДЕШЕВЛЕ, ЧЕМ
#     ПЕРЕПИСЫВАТЬ ПОРОЖДЕНИЕ РАДИ ТОГО, ЧТО И ТАК ИЗВЕСТНО.
#
# Проверено счётом по ВСЕМУ словарю показов: 472 страницы, кириллицы 0, диакритики 0
ЯЗЫК = "en"

РОДЫ = (ПРИБАВКА, УБЫЛЬ, ЦЕНА_ЗА_ШТУКУ, СТАВКА_ЗА_ДЕНЬ)

ЗАЧЕМ_РОДА = {
    ПРИБАВКА: "a + b под вопросом «how many», и кузница ответа стои́т рядом через раз",
    УБЫЛЬ: "a − b, где отданное НЕ БОЛЬШЕ своего: «keeps −1 coins» есть ложь о мире, "
           "а не об арифметике",
    ЦЕНА_ЗА_ШТУКУ: "k × p под вопросом «how much»: умножение, где оба множителя названы",
    СТАВКА_ЗА_ДЕНЬ: "p за день, сколько за k дней — и сказуемое согласовано с ЕДИНИЦЕЙ, "
                    "а не с вещью",
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
    вне = {р for _с, р in сбор.парами} - set(РОДЫ)
    assert not вне, f"род кован и не объявлен: {sorted(вне)}"
    пустые = set(РОДЫ) - set(ПОКАЗЫ.values())
    assert not пустые, f"род объявлен и не кован: {sorted(пустые)}"


_самопроверка_дома()


def main():
    emit(ЦЕЛЬ, pass_shows)


if __name__ == "__main__":
    main()
