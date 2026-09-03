#!/usr/bin/env python3
"""THE HOUSE OF ACTION PAGES — a ledger for every countable act, in three languages.

The collegium of a hundred per cent (owner, 03.09; holon's first task):
12 537 lines of the svod answer with a VALUE and no ledger. The reader's
worlds of e9 (heads, aggregate, gsmwide, gsmlex, compare, depletion, verbs,
realverbs, verbal) are computable by nature — «peter had 8 coins. peter
gave 4 coins away. how many coins are left? peter keeps 4 coins.» — but
their form must not change: his markets buy skeletons from those very
lines, and a changed answer would move the canon numbers of every svod. So
the ledger comes as NEW PAGES of the same genera (his own word: «add new
pages, do not rewrite old ones»), the way the world of forms does it.

Five genera, each a chain of primitives, each ≥ 9 pages per language:

  · THE REMAINDER — «peter had 8 coins. peter gave 4 coins away. how many
    coins are left? 8 − 4 = 4. so the answer is 4.»;
  · THE INCREASE — «nick had 9 balls. nick got 2 balls more. how many balls
    does nick have now? 9 + 2 = 11. so the answer is 11.»;
  · THE SHARE THAT WENT — «ida had 70 books. half of the books went. how
    many books are left? 70 ÷ 2 = 35. so the answer is 35.» (the words of
    the fractions come from the house of shares, tools/fracforms.py);
  · THE TWO BEARERS — «elena has 2 children. ava has 3 children. how many
    children do they have together? 2 + 3 = 5. so the answer is 5.»;
  · THE MULTIPLE — «elena has 2 eggs. ben has three times as many eggs as
    elena. how many eggs does ben have? 3 × 2 = 6. so the answer is 6.»

The court reads the page back through the same templates, REGENERATES it
and compares letter by letter.
"""
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import fracforms  # noqa: E402
import phrases  # noqa: E402
import rugram  # noqa: E402

КОРЕНЬ = pathlib.Path(__file__).resolve().parents[1]
ПАКЕТЫ = КОРЕНЬ / "tools" / "langpacks"


def _лица(язык):
    п = json.loads((ПАКЕТЫ / f"{язык}.json").read_text(encoding="utf-8"))
    формы = п.get("person_forms") or {}
    вон = []
    for имя in п.get("person_names", ()):
        ф = формы.get(имя) or формы.get(имя.capitalize())
        if not ф or ф.get("gender") not in ("m", "f"):
            continue
        показ = имя.capitalize() if язык == "ru" else имя
        род = (ф.get("gen") or "").capitalize() if язык == "ru" else показ
        вон.append((показ, ф["gender"], род))
        if len(вон) == 14:
            break
    return tuple(вон)


ЯЗЫКИ = {
    "en": dict(
        # THE THING AGREES WITH ITS COUNT: «1 coin» / «4 coins» (the pack's own
        # law of number; Russian takes it from the house of forms)
        вещи=(("coin", "coins"), ("ball", "balls"), ("book", "books"), ("card", "cards"),
              ("flower", "flowers"), ("egg", "eggs"), ("pen", "pens"), ("apple", "apples")),
        имел="{X} had {n} {Тn}.", имеет="{X} has {n} {Тn}.",
        отдал="{X} gave {k} {Тk} away.", получил="{X} got {k} {Тk} more.",
        ушло="{Ч} of the {Т} {У}.", ушли=("went", "went"), второй="{Y} has {m} {Т}.",
        кратно="{Y} has {K} as many {Т} as {X}.", кратные={2: "twice", 3: "three times", 4: "four times"},
        воп_ост="how many {Т} are left?", воп_теперь="how many {Т} does {X} have now?",
        воп_вместе="how many {Т} do they have together?", воп_второй="how many {Т} does {Y} have?",
        # e9's profile of muteness (03.09): the whole of a good named by its
        # PLACE and without «in all»; a rate «every day»; a sum said by «they»
        # ПРЕДЛОГ ЖИВЁТ ПРИ МЕСТЕ, А НЕ ПРИ РАМКЕ (заказ e9 03.09, обобщение
        # читателя мест: место есть дыра формы «зачин … РОЛЬ □», и роль эту
        # несёт предлог). «on the fence» и «in the pond» суть одно место с
        # разными предлогами; рамка со своим «in» не дала бы забору стоять.
        место="there are {n} {Тn} {П}.",
        места=("in the box", "in the garden", "in the park", "in the room", "on the shelf",
               "in the yard", "in the vase", "on the fence", "in the pond", "in the cage"),
        часть_их="{k} of them are {С}.", свойства=("red", "blue", "green", "new", "old"),
        воп_не="how many are not {С}?", воп_часть="how many of them are {С}?",
        # e9's order (03.09): the same forms in the PAST, and the part named by
        # the GOOD itself rather than «of them» («5 students are good at math»)
        место_п="there were {n} {Тn} {П}.", часть_их_п="{k} of them were {С}.", воп_не_п="how many were not {С}?",
        # ТОВАР УБЫЛ, И ВОПРОС СПРАШИВАЕТ ОБ ОСТАТКЕ (томограф дня 32, 03.09:
        # свод держал утверждение «ben had 6 cookies. he ate 2 of them. ben has
        # 4 cookies.» и вопрос только «сколько было сначала» — вопроса «сколько
        # осталось» после ate/lost/sold не было ни одного)
        убыль="{X} {Гу} {k} {Тk}.", убыли=("ate", "lost", "sold"), съедобные=(5, 7),
        воп_осталось="how many {Т} does {X} have left?",
        # МЕСТО ОПУСТЕЛО: «there were 12 balls in the yard. 5 balls were taken
        # away. how many balls are there now?» — рынок мест требует держания
        # с местом в конце, и держание это идёт с новыми местами
        убрали="{k} {Тk} were taken away.", воп_теперь_место="how many {Т} are there now?",
        # УХОДИТЬ УМЕЕТ ТОЛЬКО ЖИВОЕ (атлас немоты holon 04.09, строка #117
        # «there were 12 kids in the yard. 4 kids left.»): держание с уходом
        # требует одушевлённых, и они объявлены своим списком со своими
        # формами счёта — считаются как вещи, но уходит только живое.
        живые=(("kid", "kids"), ("child", "children"), ("bird", "birds"),
               ("cat", "cats"), ("duck", "ducks"), ("guest", "guests")),
        место_п_живые="there were {n} {Жn} {П}.",
        ушло_живое="{k} {Жk} left.", ушло_живое_один="{k} {Жk} left.",
        воп_живые_теперь="how many {Ж} are there now?",
        # СПИСОК СО СЧЁТОМ, СПРОШЕННЫЙ В ТОЙ ЖЕ СТРОКЕ (holon 03.09): без пары
        # вопрос→ответ рынок не покупает СЧЁТ как исполнителя — утверждение
        # читает только читатель по списку величин
        список_воп="{X} has {n1} {Т1}, {n2} {Т2} and {n3} {Т3}. how many {ВЕЩ2} does {X} have in all? {r} {ВЕЩ}: {л}",
        # СОЧЛЕНЕНИЕ ДВУХ КОЛИЧЕСТВ ОДНОГО АКТА (заказ 32 04.09: «and» не
        # куплено на своде, и это держит 71,8 % немоты SVAMP — рынок
        # агрегатов покупает слово-список только со страниц, где сумма ПАРЫ
        # показана): «X has 149 apples and 91 eggs. how many things does X
        # have in all? 240 things: 149 + 91 = 240.»
        список_воп2="{X} has {n1} {Т1} and {n2} {Т2}. how many {ВЕЩ2} does {X} have in all? {r} {ВЕЩ}: {л}",
        список_воп_дом="{П1} holds {О1}, {О2} and {О3}. how many {ВЕЩ2} does {П1} hold? {Чс} {ВЕЩ}: 1, 2, 3.",
        # ДВА ТОВАРА В ОДНОМ МЕСТЕ (заказ 32 03.09, SVAMP: «3 birds and 4 storks
        # were sitting on the fence. 2 more birds came to join them»): спрошены
        # оба конца — разность двух товаров и их сумма
        # ЕДИНИЦА ГОВОРИТ СВОЕЙ ФОРМОЙ: «1 weitere Bälle kamen dazu» было ложью
        # о языке при верном счёте — немецкое прилагательное согласуется в РОДЕ
        # («ein weiterer Ball», «eine weitere Blume»), испанский глагол — в
        # ЧИСЛЕ («llegó una manzana», «llegaron dos»). Приход объявлен ДВУМЯ
        # формами, и страница берёт ту, какую велит счёт.
        двое="there were {n1} {Т1n} and {n2} {Т2n} {П}.",
        пришло_один="{k} more {Т1k} came.", пришло_многие="{k} more {Т1k} came.",
        воп_двое_разность="how many more {Т1} than {Т2} are there {П}?",
        воп_двое_сумма="how many {Т1} and {Т2} are there {П}?",
        # ДВА СОСТОЯНИЯ ДВУХ ТОВАРОВ (заказ 32): «there were 15 roses and 62
        # orchids in the vase … there are now 17 roses and 96 orchids»
        состояния="there were {n1} {Т1n} and {n2} {Т2n} {П}. now there are {m1} {Т1m} and {m2} {Т2m} {П}.",
        воп_добавили="how many {Т1} were added?",
        воп_теперь_разность="how many more {Т2} than {Т1} are there now?",
        две_части_п="{k} of them were {С}, {k2} were {С2}, and the rest were {С3}.", воп_остаток_п="how many were {С3}?",
        часть_товар="{k} {Тk} are {С}.", воп_не_товар="how many {Т} are not {С}?",
        часть_товар_п="{k} {Тk} were {С}.", воп_не_товар_п="how many {Т} were not {С}?",
        две_части="{k} of them are {С}, {k2} are {С2}, and the rest are {С3}.", воп_остаток="how many are {С3}?",
        ставка="{X} {Г} {n} {Тn} every day.", ставки=("collects", "sells", "packs", "counts", "sorts"),
        воп_за="how many {Т} in {k} {Д}?", воп_дней="how many days for {m} {Т}?", дни=("day", "days"),
        вместе_они="{X} has {n} {Тn}. {Y} has {m} {Тm}. together they have {r} {Тr}: {л}",
        # e9's profile, genus 7 (the rate of exchange): a good priced in ANOTHER
        # good — every form declared, no case guessed
        # THE LIST WITH ITS COUNT SHOWN (holon's word 03.09: «a, b and c» without
        # the count is only a surface; the executors of lists — count, nth,
        # member — buy the form by falsification only when the count is there)
        список_числом="{П1} holds {Чс} {ВЕЩ}: {О1}, {О2} and {О3} — 1, 2, 3.",
        список_итогом="in {П1} there are {О1}, {О2} and {О3} — {Чс} {ВЕЩ}.",
        список_чисел="{X} has {n1} {Т1}, {n2} {Т2} and {n3} {Т3} — {r} {ВЕЩ} in all: {л}",
        вместилища=("the box", "the bag", "the shelf", "the basket", "the drawer"),
        предметы=("thing", "things"), счётом={3: "three", 4: "four"},
        курс="{О1} costs {k} {Т2k}.", один=("one coin", "one ball", "one book", "one card", "one flower", "one egg", "one pen", "one apple"),
        воп_курс="how many {Т2} do {n} {Тn} cost?", воп_курс_обр="how many {Т2} does one {Т1} cost?",
        курс_обр="{n} {Тn} cost {m} {Т2m}.",
        ответ="so the answer is {r}.",
    ),
    "ru": dict(
        вещи=("монета", "шар", "книга", "карта", "цветок", "яблоко", "ручка", "чашка"),
        имел="у {Xр} было {n} {Тn}.", имеет="у {Xр} {n} {Тn}.",
        отдал="{X} отдал{а} {k} {Твk}.", получил="{X} получил{а} ещё {k} {Твk}.",
        ушло="{Ч} {Тм} {У}.", ушли=("ушла", "ушли"), второй="у {Yр} {m} {Тm}.",
        кратно="у {Yр} {K} больше {Тм}, чем у {Xр}.", кратные={2: "вдвое", 3: "втрое", 4: "вчетверо"},
        воп_ост="сколько {Тм} осталось?", воп_теперь="сколько {Тм} у {Xр} теперь?",
        воп_вместе="сколько {Тм} у них вместе?", воп_второй="сколько {Тм} у {Yр}?",
        место="{П} {n} {Тn}.",
        места=("в коробке", "в саду", "в парке", "в комнате", "на полке",
               "во дворе", "в вазе", "у забора", "в пруду", "в клетке"),
        часть_их="{k} из них {С}.", свойства=("красные", "синие", "зелёные", "новые", "старые"),
        воп_не="сколько из них не {С}?", воп_часть="сколько из них {С}?",
        место_п="{П} было {n} {Тn}.", часть_их_п="{k} из них были {С}.", воп_не_п="сколько из них не были {Ст}?",
        убыль="{X} {Гу}{а} {k} {Твk}.", убыли=("съел", "потерял", "продал"), съедобные=(5,),
        воп_осталось="сколько {Тм} осталось у {Xр}?",
        убрали="{k} {Твk} убрали.", воп_теперь_место="сколько {Тм} теперь?",
        живые=("ребёнок", "птица", "кот", "утка", "гость"),
        место_п_живые="{П} было {n} {Жn}.",
        # ЕДИНИЦА УХОДИТ СВОИМ ЧИСЛОМ И СВОИМ РОДОМ: «1 ребёнок ушёл», но
        # «1 птица ушла» — род объявлен при каждом живом, глагол берётся им.
        род_живого=("m", "f", "m", "f", "m"),
        ушёл={"m": "ушёл", "f": "ушла"},
        ушло_живое="{k} {Жвk} ушли.", ушло_живое_один="{k} {Жk} {ГЛЖ}.",
        воп_живые_теперь="сколько {Жм} теперь?",
        вместилища_где=("в коробке", "в сумке", "в шкафу", "в корзине", "в ящике"),
        список_воп="у {Xр} {n1} {Т1}, {n2} {Т2} и {n3} {Т3}. сколько всего {ВЕЩ2} у {Xр}? {r} {ВЕЩ}: {л}",
        список_воп2="у {Xр} {n1} {Т1} и {n2} {Т2}. сколько всего {ВЕЩ2} у {Xр}? {r} {ВЕЩ}: {л}",
        список_воп_дом="{П1} {О1}, {О2} и {О3}. сколько {ВЕЩ2} {П1}? {Чс} {ВЕЩ}: 1, 2, 3.",
        двое="{П} было {n1} {Т1n} и {n2} {Т2n}.",
        пришло_один="добавили ещё {k} {Твk1}.", пришло_многие="добавили ещё {k} {Твk1}.",
        воп_двое_разность="на сколько {Т1м} больше, чем {Т2м}?",
        воп_двое_сумма="сколько {Т1м} и {Т2м} стало {П}?",
        состояния="{П} было {n1} {Т1n} и {n2} {Т2n}. теперь {П} {m1} {Т1m} и {m2} {Т2m}.",
        воп_добавили="сколько {Т1м} добавили?",
        воп_теперь_разность="на сколько {Т2м} теперь больше, чем {Т1м}?",
        две_части_п="{k} из них были {С}, {k2} были {С2}, а остальные были {С3}.", воп_остаток_п="сколько было {С3р}?",
        часть_товар="{k} {Тk} {С}.", воп_не_товар="сколько {Тм} не {С}?",
        часть_товар_п="{k} {Тk} были {С}.", воп_не_товар_п="сколько {Тм} не были {Ст}?",
        # «не были красными» — творительный множественного, формы объявлены
        свойства_твор=("красными", "синими", "зелёными", "новыми", "старыми"),
        две_части="{k} из них {С}, {k2} {С2}, а остальные {С3}.", воп_остаток="сколько {С3р}?",
        # «сколько зелёных?» — вопрос о числе просит родительного множественного
        свойства_род=("красных", "синих", "зелёных", "новых", "старых"),
        ставка="{X} {Г} {n} {Тn} каждый день.", ставки=("собирает", "продаёт", "упаковывает", "считает", "сортирует"),
        воп_за="сколько {Тм} за {k} {Д}?", воп_дней="сколько дней нужно на {m} {Тm}?", дни=("день", "дня", "дней"),
        вместе_они="у {Xр} {n} {Тn}. у {Yр} {m} {Тm}. вместе у них {r} {Тr}: {л}",
        список_числом="в {П1} {Чс} {ВЕЩ}: {О1}, {О2} и {О3} — 1, 2, 3.",
        список_итогом="в {П1} {О1}, {О2} и {О3} — {Чс} {ВЕЩ}.",
        список_чисел="у {Xр} {n1} {Т1}, {n2} {Т2} и {n3} {Т3} — всего {r} {ВЕЩ}: {л}",
        вместилища=("коробке", "сумке", "шкафу", "корзине", "ящике"),
        предметы=("предмет", "предмета", "предметов"), счётом={3: "три", 4: "четыре"},
        курс="{О1} стоит {k} {Т2k}.", один=("одна монета", "один шар", "одна книга", "одна карта", "один цветок", "одно яблоко", "одна ручка", "одна чашка"),
        воп_курс="сколько {Т2м} стоят {n} {Тn}?", воп_курс_обр="сколько {Т2м} стоит одна {Т1}?",
        курс_обр="{n} {Тn} стоят {m} {Т2m}.",
        ответ="значит ответ: {r}.",
    ),
    "de": dict(
        вещи=(("Münze", "Münzen"), ("Ball", "Bälle"), ("Buch", "Bücher"), ("Karte", "Karten"),
              ("Blume", "Blumen"), ("Ei", "Eier"), ("Stift", "Stifte"), ("Tasse", "Tassen")),
        имел="{X} hatte {n} {Тn}.", имеет="{X} hat {n} {Тn}.",
        отдал="{X} gab {k} {Тk} weg.", получил="{X} bekam {k} {Тk} mehr.",
        ушло="{Ч} der {Т} {У}.", ушли=("ging weg", "gingen weg"), второй="{Y} hat {m} {Т}.",
        кратно="{Y} hat {K} so viele {Т} wie {X}.", кратные={2: "doppelt", 3: "dreimal", 4: "viermal"},
        воп_ост="wie viele {Т} bleiben übrig?", воп_теперь="wie viele {Т} hat {X} jetzt?",
        воп_вместе="wie viele {Т} haben sie zusammen?", воп_второй="wie viele {Т} hat {Y}?",
        место="es gibt {n} {Тn} {П}.",
        места=("in der Kiste", "im Garten", "im Park", "im Zimmer", "auf dem Regal",
               "im Hof", "in der Vase", "am Zaun", "im Teich", "im Käfig"),
        часть_их="{k} davon sind {С}.", свойства=("rot", "blau", "grün", "neu", "alt"),
        воп_не="wie viele sind nicht {С}?", воп_часть="wie viele davon sind {С}?",
        место_п="es gab {n} {Тn} {П}.", часть_их_п="{k} davon waren {С}.", воп_не_п="wie viele waren nicht {С}?",
        убыль="{X} {Гу} {k} {Тk}.", убыли=("aß", "verlor", "verkaufte"), съедобные=(5,),
        воп_осталось="wie viele {Т} hat {X} noch?",
        убрали="{k} {Тk} wurden weggenommen.", воп_теперь_место="wie viele {Т} sind jetzt da?",
        живые=(("Kind", "Kinder"), ("Vogel", "Vögel"), ("Katze", "Katzen"),
               ("Ente", "Enten"), ("Gast", "Gäste")),
        место_п_живые="es gab {n} {Жn} {П}.",
        ушло_живое="{k} {Жk} gingen weg.", ушло_живое_один="{k} {Жk} ging weg.",
        воп_живые_теперь="wie viele {Ж} sind jetzt da?",
        вместилища_где=("in der Kiste", "in der Tasche", "im Regal", "im Korb", "in der Schublade"),
        список_воп="{X} hat {n1} {Т1}, {n2} {Т2} und {n3} {Т3}. wie viele {ВЕЩ2} hat {X} insgesamt? {r} {ВЕЩ}: {л}",
        список_воп2="{X} hat {n1} {Т1} und {n2} {Т2}. wie viele {ВЕЩ2} hat {X} insgesamt? {r} {ВЕЩ}: {л}",
        список_воп_дом="{П1} sind {О1}, {О2} und {О3}. wie viele {ВЕЩ2} sind {П1}? {Чс} {ВЕЩ}: 1, 2, 3.",
        двое="{П} waren {n1} {Т1n} und {n2} {Т2n}.",
        пришло_один="{k} {ГВ} {Т1k} kam dazu.", пришло_многие="{k} weitere {Т1k} kamen dazu.",
        род_вещи=("f", "m", "n", "f", "f", "n", "m", "f"),
        ещё_один={"m": "weiterer", "f": "weitere", "n": "weiteres"},
        воп_двое_разность="wie viele {Т1} mehr als {Т2} gibt es {П}?",
        воп_двое_сумма="wie viele {Т1} und {Т2} gibt es {П}?",
        состояния="{П} waren {n1} {Т1n} und {n2} {Т2n}. jetzt gibt es {m1} {Т1m} und {m2} {Т2m} {П}.",
        воп_добавили="wie viele {Т1} kamen dazu?",
        воп_теперь_разность="wie viele {Т2} mehr als {Т1} gibt es jetzt?",
        две_части_п="{k} davon waren {С}, {k2} waren {С2}, der Rest war {С3}.", воп_остаток_п="wie viele waren {С3}?",
        часть_товар="{k} {Тk} sind {С}.", воп_не_товар="wie viele {Т} sind nicht {С}?",
        часть_товар_п="{k} {Тk} waren {С}.", воп_не_товар_п="wie viele {Т} waren nicht {С}?",
        две_части="{k} davon sind {С}, {k2} sind {С2}, der Rest ist {С3}.", воп_остаток="wie viele sind {С3}?",
        ставка="{X} {Г} jeden Tag {n} {Тn}.", ставки=("sammelt", "verkauft", "packt", "zählt", "sortiert"),
        воп_за="wie viele {Т} in {k} {Д}?", воп_дней="wie viele Tage für {m} {Т}?", дни=("Tag", "Tagen"),
        вместе_они="{X} hat {n} {Тn}. {Y} hat {m} {Тm}. zusammen haben sie {r} {Тr}: {л}",
        список_числом="{П1} enthält {Чс} {ВЕЩ}: {О1}, {О2} und {О3} — 1, 2, 3.",
        список_итогом="{П1} enthält {О1}, {О2} und {О3} — {Чс} {ВЕЩ}.",
        список_чисел="{X} hat {n1} {Т1}, {n2} {Т2} und {n3} {Т3} — insgesamt {r} {ВЕЩ}: {л}",
        вместилища=("die Kiste", "die Tasche", "das Regal", "der Korb", "die Schublade"),
        предметы=("Ding", "Dinge"), счётом={3: "drei", 4: "vier"},
        курс="{О1} kostet {k} {Т2k}.", один=("eine Münze", "ein Ball", "ein Buch", "eine Karte", "eine Blume", "ein Ei", "ein Stift", "eine Tasse"),
        воп_курс="wie viele {Т2} kosten {n} {Тn}?", воп_курс_обр="wie viele {Т2} kostet ein {Т1}?",
        курс_обр="{n} {Тn} kosten {m} {Т2m}.",
        ответ="also ist die Antwort {r}.",
    ),
    "es": dict(
        # ЧЕТВЁРТЫЙ ЯЗЫК ДОМА (мандат владельца: языки должны быть закреплены с
        # ИЗБЫТКОМ). Испанский требует того, чего не требовали три первых:
        # вопросное слово согласуется В РОДЕ с вещью («¿cuántas monedas
        # quedan?», но «¿cuántos libros quedan?»), и род объявлен при каждой
        # вещи, а не выведен из окончания. Роды, которых язык не объявил
        # (доли, цветные части), он и не пишет — закон объявленной формы.
        вещи=(("moneda", "monedas"), ("balón", "balones"), ("libro", "libros"), ("carta", "cartas"),
              ("flor", "flores"), ("huevo", "huevos"), ("bolígrafo", "bolígrafos"), ("manzana", "manzanas")),
        род_вещи=("f", "m", "m", "f", "f", "m", "m", "f"),
        вопросное={"f": "cuántas", "m": "cuántos"},
        имел="{X} tenía {n} {Тn}.", имеет="{X} tiene {n} {Тn}.",
        отдал="{X} regaló {k} {Тk}.", получил="{X} recibió {k} {Тk} más.",
        второй="{Y} tiene {m} {Т}.",
        кратно="{Y} tiene {K} {Т} que {X}.",
        кратные={2: "el doble de", 3: "el triple de", 4: "cuatro veces más"},
        воп_ост="¿{КВ} {Т} quedan?", воп_теперь="¿{КВ} {Т} tiene {X} ahora?",
        воп_вместе="¿{КВ} {Т} tienen juntos?", воп_второй="¿{КВ} {Т} tiene {Y}?",
        место_п="había {n} {Тn} {П}.",
        места=("en la caja", "en el jardín", "en el parque", "en la habitación", "en el estante",
               "en el patio", "en el jarrón", "en la valla", "en el estanque", "en la jaula"),
        убыль="{X} {Гу} {k} {Тk}.", убыли=("comió", "perdió", "vendió"), съедобные=(5, 7),
        воп_осталось="¿{КВ} {Т} le quedan a {X}?",
        убрали="quitaron {k} {Тk}.", воп_теперь_место="¿{КВ} {Т} hay ahora?",
        ставка="{X} {Г} {n} {Тn} cada día.", ставки=("recoge", "vende", "empaqueta", "cuenta", "ordena"),
        воп_за="¿{КВ} {Т} en {k} {Д}?", воп_дней="¿cuántos días para {m} {Тm}?", дни=("día", "días"),
        вместе_они="{X} tiene {n} {Тn}. {Y} tiene {m} {Тm}. juntos tienen {r} {Тr}: {л}",
        список_чисел="{X} tiene {n1} {Т1}, {n2} {Т2} y {n3} {Т3} — {r} {ВЕЩ} en total: {л}",
        список_воп="{X} tiene {n1} {Т1}, {n2} {Т2} y {n3} {Т3}. ¿cuántas {ВЕЩ2} tiene {X} en total? {r} {ВЕЩ}: {л}",
        список_воп2="{X} tiene {n1} {Т1} y {n2} {Т2}. ¿cuántas {ВЕЩ2} tiene {X} en total? {r} {ВЕЩ}: {л}",
        список_воп_дом="{П1} hay {О1}, {О2} y {О3}. ¿cuántas {ВЕЩ2} hay {П1}? {Чс} {ВЕЩ}: 1, 2, 3.",
        вместилища_где=("en la caja", "en la bolsa", "en el estante", "en la cesta", "en el cajón"),
        предметы=("cosa", "cosas"), счётом={3: "tres", 4: "cuatro"},
        один=("una moneda", "un balón", "un libro", "una carta", "una flor", "un huevo", "un bolígrafo", "una manzana"),
        курс="{О1} cuesta {k} {Т2k}.", курс_обр="{n} {Тn} cuestan {m} {Т2m}.",
        воп_курс="¿{КВ2} {Т2} cuestan {n} {Тn}?", воп_курс_обр="¿{КВ2} {Т2} cuesta {О1}?",
        двое="{П} había {n1} {Т1n} y {n2} {Т2n}.",
        пришло_один="llegó {k} {Т1k} más.", пришло_многие="llegaron {k} {Т1k} más.",
        воп_двое_разность="¿{КВ1} {Т1} más que {Т2} hay {П}?",
        воп_двое_сумма="¿{КВ1} {Т1} y {Т2} hay {П}?",
        состояния="{П} había {n1} {Т1n} y {n2} {Т2n}. ahora hay {m1} {Т1m} y {m2} {Т2m} {П}.",
        воп_добавили="¿{КВ1} {Т1} se añadieron?",
        воп_теперь_разность="¿{КВ2} {Т2} más que {Т1} hay ahora?",
        ответ="así que la respuesta es {r}.",
    ),
    "fr": dict(
        # ПЯТЫЙ ЯЗЫК ДОМА. Французский спрашивает о числе неизменяемым «combien
        # de» и потому не требует согласования вопросного слова, зато требует
        # своего пробела перед знаком вопроса и перед двоеточием — и это тоже
        # объявление, а не догадка: так пишут французские миры свода.
        вещи=(("pièce", "pièces"), ("ballon", "ballons"), ("livre", "livres"), ("carte", "cartes"),
              ("fleur", "fleurs"), ("œuf", "œufs"), ("stylo", "stylos"), ("pomme", "pommes")),
        имел="{X} avait {n} {Тn}.", имеет="{X} a {n} {Тn}.",
        отдал="{X} a donné {k} {Тk}.", получил="{X} a reçu {k} {Тk} de plus.",
        второй="{Y} a {m} {Т}.",
        кратно="{Y} a {K} {Т} que {X}.",
        кратные={2: "deux fois plus de", 3: "trois fois plus de", 4: "quatre fois plus de"},
        воп_ост="combien {ДЕ}{Т} restent ?", воп_теперь="combien {ДЕ}{Т} a {X} maintenant ?",
        воп_вместе="combien {ДЕ}{Т} ont-ils ensemble ?", воп_второй="combien {ДЕ}{Т} a {Y} ?",
        место_п="{П} il y avait {n} {Тn}.",
        места=("dans la boîte", "dans le jardin", "dans le parc", "dans la chambre", "sur l'étagère",
               "dans la cour", "dans le vase", "sur la clôture", "dans l'étang", "dans la cage"),
        убыль="{X} a {Гу} {k} {Тk}.", убыли=("mangé", "perdu", "vendu"), съедобные=(5, 7),
        воп_осталось="combien {ДЕ}{Т} reste-t-il à {X} ?",
        убрали="on a enlevé {k} {Тk}.", воп_теперь_место="combien {ДЕ}{Т} y a-t-il maintenant ?",
        ставка="{X} {Г} {n} {Тn} chaque jour.", ставки=("ramasse", "vend", "emballe", "compte", "trie"),
        воп_за="combien {ДЕ}{Т} en {k} {Д} ?", воп_дней="combien de jours pour {m} {Тm} ?",
        дни=("jour", "jours"),
        вместе_они="{X} a {n} {Тn}. {Y} a {m} {Тm}. ensemble ils ont {r} {Тr} : {л}",
        список_чисел="{X} a {n1} {Т1}, {n2} {Т2} et {n3} {Т3} — {r} {ВЕЩ} en tout : {л}",
        список_воп="{X} a {n1} {Т1}, {n2} {Т2} et {n3} {Т3}. combien de {ВЕЩ2} a {X} en tout ? {r} {ВЕЩ} : {л}",
        список_воп2="{X} a {n1} {Т1} et {n2} {Т2}. combien de {ВЕЩ2} a {X} en tout ? {r} {ВЕЩ} : {л}",
        элизия=(False, False, False, False, False, True, False, False),
        список_воп_дом="{П1} il y a {О1}, {О2} et {О3}. combien de {ВЕЩ2} y a-t-il {П1} ? {Чс} {ВЕЩ} : 1, 2, 3.",
        вместилища_где=("dans la boîte", "dans le sac", "sur l'étagère", "dans le panier", "dans le tiroir"),
        предметы=("chose", "choses"), счётом={3: "trois", 4: "quatre"},
        один=("une pièce", "un ballon", "un livre", "une carte", "une fleur", "un œuf", "un stylo", "une pomme"),
        курс="{О1} coûte {k} {Т2k}.", курс_обр="{n} {Тn} coûtent {m} {Т2m}.",
        воп_курс="combien {ДЕ2}{Т2} coûtent {n} {Тn} ?", воп_курс_обр="combien {ДЕ2}{Т2} coûte {О1} ?",
        двое="{П} il y avait {n1} {Т1n} et {n2} {Т2n}.",
        пришло_один="on a ajouté {k} {Т1k}.", пришло_многие="on a ajouté {k} {Т1k}.",
        воп_двое_разность="combien {ДЕ1}{Т1} de plus que {ДЕ2}{Т2} y a-t-il {П} ?",
        воп_двое_сумма="combien {ДЕ1}{Т1} et {ДЕ2}{Т2} y a-t-il {П} ?",
        состояния="{П} il y avait {n1} {Т1n} et {n2} {Т2n}. maintenant il y a {m1} {Т1m} et {m2} {Т2m} {П}.",
        воп_добавили="combien {ДЕ1}{Т1} a-t-on ajouté ?",
        воп_теперь_разность="combien {ДЕ2}{Т2} de plus que {ДЕ1}{Т1} y a-t-il maintenant ?",
        ответ="donc la réponse est {r}.",
    ),
    "it": dict(
        # ШЕСТОЙ ЯЗЫК. Итальянский, как испанский, согласует вопросное слово в
        # роде («quante monete» / «quanti libri»); род объявлен при вещи, и
        # неправильная пара «uovo — uova» стоит в таблице формой, а не правилом.
        вещи=(("moneta", "monete"), ("pallone", "palloni"), ("libro", "libri"), ("carta", "carte"),
              ("fiore", "fiori"), ("uovo", "uova"), ("penna", "penne"), ("mela", "mele")),
        род_вещи=("f", "m", "m", "f", "m", "f", "f", "f"),
        вопросное={"f": "quante", "m": "quanti"},
        имел="{X} aveva {n} {Тn}.", имеет="{X} ha {n} {Тn}.",
        отдал="{X} ha dato via {k} {Тk}.", получил="{X} ha ricevuto {k} {Тk} in più.",
        второй="{Y} ha {m} {Т}.",
        воп_ост="{КВ} {Т} restano?", воп_теперь="{КВ} {Т} ha {X} adesso?",
        воп_вместе="{КВ} {Т} hanno insieme?", воп_второй="{КВ} {Т} ha {Y}?",
        место_п="{П} c'erano {n} {Тn}.",
        места=("nella scatola", "nel giardino", "nel parco", "nella stanza", "sullo scaffale",
               "nel cortile", "nel vaso", "sulla staccionata", "nello stagno", "nella gabbia"),
        убыль="{X} ha {Гу} {k} {Тk}.", убыли=("mangiato", "perso", "venduto"), съедобные=(5, 7),
        # ЭВФОНИЧЕСКОЕ «D» ЕСТЬ ПРАВИЛО ЗВУКА, И ПОТОМУ ОБЪЯВЛЕНО ПРАВИЛОМ, А НЕ
        # СПИСКОМ: итальянский говорит «ad Anna», но «a Chiara» — предлог берёт
        # «d» перед гласной. Гласные объявлены буквами, исключений нет (в
        # отличие от французского «h», где буква лжёт о звуке).
        воп_осталось="{КВ} {Т} restano {КО} {X}?",
        гласные_имени="AEIOUaeiou",
        убрали="hanno tolto {k} {Тk}.", воп_теперь_место="{КВ} {Т} ci sono adesso?",
        ставка="{X} {Г} {n} {Тn} ogni giorno.", ставки=("raccoglie", "vende", "impacchetta", "conta", "ordina"),
        воп_за="{КВ} {Т} in {k} {Д}?", воп_дней="quanti giorni per {m} {Тm}?", дни=("giorno", "giorni"),
        вместе_они="{X} ha {n} {Тn}. {Y} ha {m} {Тm}. insieme hanno {r} {Тr}: {л}",
        список_чисел="{X} ha {n1} {Т1}, {n2} {Т2} e {n3} {Т3} — {r} {ВЕЩ} in tutto: {л}",
        список_воп="{X} ha {n1} {Т1}, {n2} {Т2} e {n3} {Т3}. quante {ВЕЩ2} ha {X} in tutto? {r} {ВЕЩ}: {л}",
        список_воп2="{X} ha {n1} {Т1} e {n2} {Т2}. quante {ВЕЩ2} ha {X} in tutto? {r} {ВЕЩ}: {л}",
        список_воп_дом="{П1} ci sono {О1}, {О2} e {О3}. quante {ВЕЩ2} ci sono {П1}? {Чс} {ВЕЩ}: 1, 2, 3.",
        вместилища_где=("nella scatola", "nella borsa", "sullo scaffale", "nel cesto", "nel cassetto"),
        предметы=("cosa", "cose"), счётом={3: "tre", 4: "quattro"},
        один=("una moneta", "un pallone", "un libro", "una carta", "un fiore", "un uovo", "una penna", "una mela"),
        курс="{О1} costa {k} {Т2k}.", курс_обр="{n} {Тn} costano {m} {Т2m}.",
        воп_курс="{КВ2} {Т2} costano {n} {Тn}?", воп_курс_обр="{КВ2} {Т2} costa {О1}?",
        двое="{П} c'erano {n1} {Т1n} e {n2} {Т2n}.",
        пришло_один="hanno aggiunto {k} {Т1k}.", пришло_многие="hanno aggiunto {k} {Т1k}.",
        воп_двое_разность="{КВ1} {Т1} in più di {Т2} ci sono {П}?",
        воп_двое_сумма="{КВ1} {Т1} e {Т2} ci sono {П}?",
        состояния="{П} c'erano {n1} {Т1n} e {n2} {Т2n}. adesso ci sono {m1} {Т1m} e {m2} {Т2m} {П}.",
        воп_добавили="{КВ1} {Т1} hanno aggiunto?",
        воп_теперь_разность="{КВ2} {Т2} in più di {Т1} ci sono adesso?",
        ответ="quindi la risposta è {r}.",
    ),
    "pt": dict(
        # СЕДЬМОЙ ЯЗЫК. Португальский согласует вопросное слово в роде
        # («quantas moedas» / «quantos livros») и ставит носителя перед
        # глаголом в вопросе («quantas moedas Ana tem agora?»).
        вещи=(("moeda", "moedas"), ("bola", "bolas"), ("livro", "livros"), ("carta", "cartas"),
              ("flor", "flores"), ("ovo", "ovos"), ("caneta", "canetas"), ("maçã", "maçãs")),
        род_вещи=("f", "f", "m", "f", "f", "m", "f", "f"),
        вопросное={"f": "quantas", "m": "quantos"},
        имел="{X} tinha {n} {Тn}.", имеет="{X} tem {n} {Тn}.",
        отдал="{X} deu {k} {Тk}.", получил="{X} recebeu mais {k} {Тk}.",
        второй="{Y} tem {m} {Т}.",
        воп_ост="{КВ} {Т} restam?", воп_теперь="{КВ} {Т} {X} tem agora?",
        воп_вместе="{КВ} {Т} têm juntos?", воп_второй="{КВ} {Т} {Y} tem?",
        место_п="{П} havia {n} {Тn}.",
        места=("na caixa", "no jardim", "no parque", "no quarto", "na prateleira",
               "no pátio", "no vaso", "na cerca", "no lago", "na gaiola"),
        убыль="{X} {Гу} {k} {Тk}.", убыли=("comeu", "perdeu", "vendeu"), съедобные=(5, 7),
        воп_осталось="{КВ} {Т} restam para {X}?",
        убрали="tiraram {k} {Тk}.", воп_теперь_место="{КВ} {Т} há agora?",
        ставка="{X} {Г} {n} {Тn} todos os dias.", ставки=("recolhe", "vende", "embala", "conta", "organiza"),
        воп_за="{КВ} {Т} em {k} {Д}?", воп_дней="quantos dias para {m} {Тm}?", дни=("dia", "dias"),
        вместе_они="{X} tem {n} {Тn}. {Y} tem {m} {Тm}. juntos têm {r} {Тr}: {л}",
        список_чисел="{X} tem {n1} {Т1}, {n2} {Т2} e {n3} {Т3} — {r} {ВЕЩ} no total: {л}",
        список_воп="{X} tem {n1} {Т1}, {n2} {Т2} e {n3} {Т3}. quantas {ВЕЩ2} {X} tem no total? {r} {ВЕЩ}: {л}",
        список_воп2="{X} tem {n1} {Т1} e {n2} {Т2}. quantas {ВЕЩ2} {X} tem no total? {r} {ВЕЩ}: {л}",
        список_воп_дом="{П1} há {О1}, {О2} e {О3}. quantas {ВЕЩ2} há {П1}? {Чс} {ВЕЩ}: 1, 2, 3.",
        вместилища_где=("na caixa", "na bolsa", "na prateleira", "no cesto", "na gaveta"),
        предметы=("coisa", "coisas"), счётом={3: "três", 4: "quatro"},
        один=("uma moeda", "uma bola", "um livro", "uma carta", "uma flor", "um ovo", "uma caneta", "uma maçã"),
        курс="{О1} custa {k} {Т2k}.", курс_обр="{n} {Тn} custam {m} {Т2m}.",
        воп_курс="{КВ2} {Т2} custam {n} {Тn}?", воп_курс_обр="{КВ2} {Т2} custa {О1}?",
        двое="{П} havia {n1} {Т1n} e {n2} {Т2n}.",
        пришло_один="acrescentaram {k} {Т1k}.", пришло_многие="acrescentaram {k} {Т1k}.",
        воп_двое_разность="{КВ1} {Т1} a mais que {Т2} há {П}?",
        воп_двое_сумма="{КВ1} {Т1} e {Т2} há {П}?",
        состояния="{П} havia {n1} {Т1n} e {n2} {Т2n}. agora há {m1} {Т1m} e {m2} {Т2m} {П}.",
        воп_добавили="{КВ1} {Т1} acrescentaram?",
        воп_теперь_разность="{КВ2} {Т2} a mais que {Т1} há agora?",
        ответ="portanto a resposta é {r}.",
    ),
}
ЛИЦА = {л: _лица(л) for л in ЯЗЫКИ}
# ЖИВОЕ СТОИТ НЕ ВСЯКОМ МЕСТЕ. «на полке было 23 гостя» есть безупречный
# счёт о ложном мире — тот же род мусора, что «tom ate 5 coins»: ни один
# счётный прибор его не видит. Места живых названы номерами объявленного
# списка (сад, парк, комната, двор) — те, где живое стоит на любом языке.
МЕСТА_ЖИВЫХ = (1, 2, 3, 5)

ФОРМЫ = ("остаток", "прибавка", "доля", "вместе", "кратное", "место", "место_эхо", "место_две", "место_п", "место_две_п", "место_товар", "место_товар_п", "ставка", "вместе_они", "курс", "курс_обр", "список_числом", "список_итогом", "список_чисел", "убыль", "место_убыло", "место_ушли",
          "список_воп", "список_воп2", "список_воп_дом", "двое_разность", "двое_сумма",
          "состояния_добавили", "состояния_разность")
# the shares that may «go»: the house of shares says their words in every language
ДОЛИ = ((1, 2), (1, 3), (1, 4), (2, 3), (3, 4), (1, 5), (2, 5))


def _вещь(язык, i, n):
    в = ЯЗЫКИ[язык]["вещи"][i]
    if язык == "ru":
        return rugram.форма(в, n)
    один, много = в
    return один if n == 1 else много


def _де(язык, i):
    """«de » или «d'» — предлог, съедающий гласную (элизия французского).

    «combien de œufs» есть ложь о языке при верном счёте, и правило это
    объявлено ПРИ ВЕЩИ (какая начинается с гласной), а не выведено из буквы:
    французское «h» бывает немым и придыхательным, и буква о том молчит.
    """
    элизия = ЯЗЫКИ[язык].get("элизия")
    if not элизия:
        return ""
    return "d'" if элизия[i] else "de "


def _к_имени(язык, имя):
    """«a» или «ad» перед именем — по звуку его первой буквы (итальянский)."""
    гласные = ЯЗЫКИ[язык].get("гласные_имени")
    if not гласные:
        return ""
    return "ad" if имя and имя[0] in гласные else "a"


def _квопрос(язык, i):
    """«cuántas» или «cuántos» — вопросное слово, согласованное с ВЕЩЬЮ.

    Испанский спрашивает о числе словом, которое согласуется в роде с
    предметом счёта, и род объявлен при каждой вещи (`род_вещи`), а не выведен
    из окончания. Язык, не объявивший вопросного слова, получает пустую
    строку: его шаблоны этой дыры не держат.
    """
    я = ЯЗЫКИ[язык]
    роды, слова = я.get("род_вещи"), я.get("вопросное")
    if not роды or not слова:
        return ""
    return слова.get(роды[i], "")


def _живое(язык, i, n):
    """Форма одушевлённого при счёте — по тем же законам, что вещь."""
    ж = ЯЗЫКИ[язык]["живые"][i]
    if язык == "ru":
        return rugram.форма(ж, n)
    один, много = ж
    return один if n == 1 else много


def _живое_вин(язык, i, n):
    """Винительный одушевлённого: у русского он равен родительному, формы
    объявлены домом грамматики; язык без объявления страницы не пишет."""
    if язык != "ru":
        return _живое(язык, i, n)
    лемма = ЯЗЫКИ[язык]["живые"][i]
    счётная = rugram.форма(лемма, n)
    пар = rugram.ПАРАДИГМЫ.get(лемма)
    if счётная == rugram.форма(лемма, 1):
        return пар[3] if пар else None
    return счётная


def _вещь_вин(язык, i, n):
    """THE THING AFTER A VERB STANDS IN THE ACCUSATIVE WHERE THE COUNT SAYS
    «ONE»: «отдала 1 монету», while «2 монеты» and «5 монет» are the count
    forms themselves. The paradigm is declared (tools/rugram.py), not guessed."""
    if язык != "ru":
        return _вещь(язык, i, n)
    лемма = ЯЗЫКИ[язык]["вещи"][i]
    счётная = rugram.форма(лемма, n)
    пар = rugram.ПАРАДИГМЫ.get(лемма)
    if счётная == rugram.форма(лемма, 1):
        # the count says «one», so the verb wants the accusative; a thing whose
        # paradigm the house has not declared DOES NOT SAY IT (the law of the
        # declared form: no case is ever guessed) — the page is not written
        return пар[3] if пар else None
    return счётная


def _лицо(язык, имя):
    return next(л for л in ЛИЦА[язык] if л[0] == имя)


def _предмет(язык, n):
    """«three things», «три предмета», «drei Dinge» — счёт объявлен, не выведен."""
    формы = ЯЗЫКИ[язык]["предметы"]
    if язык == "ru":
        сотня, десяток = n % 100, n % 10
        if 11 <= сотня <= 14:
            return формы[2]
        if десяток == 1:
            return формы[0]
        if 2 <= десяток <= 4:
            return формы[1]
        return формы[2]
    return формы[0] if n == 1 else формы[1]


def _день(язык, k):
    """The word «day» agrees with its count: «1 day» / «4 days», «1 день» /
    «4 дня» / «5 дней», «1 Tag» / «4 Tagen» (the Russian form comes from the
    declared house of count, tools/rugram.py)."""
    формы = ЯЗЫКИ[язык]["дни"]
    if язык == "ru":
        return rugram.форма("день", k)
    return формы[0] if k == 1 else формы[1]


def _а(язык, пол):
    """The Russian past tense bends by gender: «отдал» / «отдала»."""
    return "а" if (язык == "ru" and пол == "f") else ""


def страница(язык, форма, X, Т=0, n=0, k=0, m=0, Y=None, доля=None, кратность=2,
             место=0, свойство=0, свойство2=1, свойство3=2, k2=0, глагол_ставки=0, дней=True, Т2=1, Т3=2,
             глагол_убыли=0):
    я = ЯЗЫКИ[язык]
    имя, пол, род = _лицо(язык, X)
    з = dict(X=имя, Xр=род, а=_а(язык, пол))
    if Y is not None:
        имяY, полY, родY = _лицо(язык, Y)
        з.update(Y=имяY, Yр=родY)
    def вещь(сколько):
        return _вещь(язык, Т, сколько)
    вин = _вещь_вин(язык, Т, k)
    if форма in ("остаток", "прибавка", "убыль", "место_убыло") and вин is None:
        raise ValueError("форма вещи не объявлена")   # the page is not written
    общ = dict(з, Т=вещь(2), Тn=вещь(n), Тk=вещь(k), Тm=вещь(m), Тм=вещь(5), Твk=вин,
               КВ=_квопрос(язык, Т), ДЕ=_де(язык, Т), КО=_к_имени(язык, имя))
    if форма == "вместе_они" and Y is None:
        raise ValueError("второй носитель не назван")
    if форма == "остаток":
        r = n - k
        факт = я["имел"].format(**общ, n=n) + " " + я["отдал"].format(**общ, k=k)
        воп = я["воп_ост"].format(**общ)
        леджер = f"{n} − {k} = {r}."
    elif форма == "прибавка":
        r = n + k
        факт = я["имел"].format(**общ, n=n) + " " + я["получил"].format(**общ, k=k)
        воп = я["воп_теперь"].format(**общ)
        леджер = f"{n} + {k} = {r}."
    elif форма == "доля":
        чс, зн = доля
        ушло_ = n * чс // зн
        r = n - ушло_
        слово = fracforms.доля_слово(язык, чс, зн)
        факт = я["имел"].format(**общ, n=n) + " " + я["ушло"].format(**общ, Ч=слово, У=я["ушли"][0 if чс == 1 else 1])
        воп = я["воп_ост"].format(**общ)
        леджер = (f"{n} ÷ {зн} = {n // зн}, {n // зн} × {чс} = {ушло_}, {n} − {ушло_} = {r}."
                  if чс > 1 else f"{n} ÷ {зн} = {ушло_}, {n} − {ушло_} = {r}.")
    elif форма == "вместе":
        r = n + m
        факт = я["имеет"].format(**общ, n=n) + " " + я["второй"].format(**общ, m=m)
        воп = я["воп_вместе"].format(**общ)
        леджер = f"{n} + {m} = {r}."
    elif форма == "кратное":
        r = кратность * n
        факт = я["имеет"].format(**общ, n=n) + " " + я["кратно"].format(**общ, K=я["кратные"][кратность])
        воп = я["воп_второй"].format(**общ)
        леджер = f"{кратность} × {n} = {r}."
    elif форма == "место":
        # THE WHOLE NAMED BY ITS PLACE, AND A PART OF IT (e9's profile 03.09:
        # «there are 700 bees in a hive» is the whole without «in all»)
        r = n - k
        С = я["свойства"][свойство]
        факт = я["место"].format(**общ, n=n, П=я["места"][место]) + " " + я["часть_их"].format(**общ, k=k, С=С)
        воп = я["воп_не"].format(С=С)
        леджер = f"{n} − {k} = {r}."
    elif форма == "место_эхо":
        # THE ECHO OF A PART (e9 03.09): not for counting, but so that the market
        # of heads buys «of them» as part-of-the-whole
        С = я["свойства"][свойство]
        факт = я["место"].format(**общ, n=n, П=я["места"][место]) + " " + я["часть_их"].format(**общ, k=k, С=С)
        воп = я["воп_часть"].format(С=С)
        return f"{факт} {воп} {я['часть_их'].format(**общ, k=k, С=С)} {я['ответ'].format(r=k)}"
    elif форма in ("место_п", "место_товар", "место_товар_п"):
        # THE SAME WHOLE AND PART IN THE PAST, and the part named by the GOOD
        # itself (e9's order 03.09: «5 students are good at math»)
        С = я["свойства"][свойство]
        прош = форма.endswith("_п")
        r = n - k
        факт = (я["место_п"] if прош else я["место"]).format(**общ, n=n, П=я["места"][место])
        Ст = (я.get("свойства_твор") or я["свойства"])[свойство]
        if форма.startswith("место_товар"):
            часть = (я["часть_товар_п"] if прош else я["часть_товар"]).format(**общ, k=k, С=С)
            воп = (я["воп_не_товар_п"] if прош else я["воп_не_товар"]).format(**общ, С=С, Ст=Ст)
        else:
            часть = я["часть_их_п"].format(**общ, k=k, С=С)
            воп = я["воп_не_п"].format(С=С, Ст=Ст)
        леджер = f"{n} − {k} = {r}."
        return f"{факт} {часть} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма == "место_две_п":
        С, С2, С3 = (я["свойства"][i] for i in (свойство, свойство2, свойство3))
        r1 = n - k
        r = r1 - k2
        С3р = (я.get("свойства_род") or я["свойства"])[свойство3]
        факт = я["место_п"].format(**общ, n=n, П=я["места"][место]) + " " + я["две_части_п"].format(**общ, k=k, k2=k2, С=С, С2=С2, С3=С3)
        воп = я["воп_остаток_п"].format(С3=С3, С3р=С3р)
        леджер = f"{n} − {k} = {r1}, {r1} − {k2} = {r}."
        return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма == "место_две":
        # TWO PARTS AND A REST (g1.39: «5 good at math only, 8 at English only,
        # the rest at both»): the whole is spent twice
        С, С2, С3 = (я["свойства"][i] for i in (свойство, свойство2, свойство3))
        r1 = n - k
        r = r1 - k2
        факт = я["место"].format(**общ, n=n, П=я["места"][место]) + " " + я["две_части"].format(**общ, k=k, k2=k2, С=С, С2=С2, С3=С3)
        С3р = (я.get("свойства_род") or я["свойства"])[свойство3]
        воп = я["воп_остаток"].format(С3=С3, С3р=С3р)
        леджер = f"{n} − {k} = {r1}, {r1} − {k2} = {r}."
        return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма in ("список_числом", "список_итогом", "список_чисел"):
        # THE LIST WITH ITS COUNT SHOWN (holon's word 03.09): the enumeration and
        # its count in one line — «a, b and c» alone is only a surface
        т1, т2, т3 = Т, Т2, Т3
        з2 = dict(общ, П1=я["вместилища"][место], О1=я["один"][т1], О2=я["один"][т2], О3=я["один"][т3],
                  Чс=я["счётом"][3], ВЕЩ=_предмет(язык, 3))
        if форма == "список_числом":
            return я["список_числом"].format(**з2)
        if форма == "список_итогом":
            return я["список_итогом"].format(**з2)
        n1, n2, n3 = n, m, k
        r = n1 + n2 + n3
        з3 = dict(общ, n1=n1, n2=n2, n3=n3, Т1=_вещь(язык, т1, n1), Т2=_вещь(язык, т2, n2), Т3=_вещь(язык, т3, n3),
                  r=r, ВЕЩ=_предмет(язык, r), л=f"{n1} + {n2} = {n1 + n2}, {n1 + n2} + {n3} = {r}.")
        return я["список_чисел"].format(**з3)
    elif форма == "список_воп2":
        # ДВА КОЛИЧЕСТВА ОДНОГО АКТА, СОЧЛЕНЁННЫЕ СЛОВОМ, И СУММА ПАРЫ РЯДОМ
        # (заказ 32 04.09): рынок агрегатов покупает слово-список только с
        # такой страницы, а без него читатель не знает, что «and» соединяет —
        # и молчит на семи строках из десяти в полосе SVAMP.
        if Т == Т2:
            raise ValueError("два товара должны быть разными")
        r = n + m
        з2 = dict(общ, n1=n, n2=m, Т1=_вещь(язык, Т, n), Т2=_вещь(язык, Т2, m),
                  r=r, ВЕЩ=_предмет(язык, r), ВЕЩ2=_предмет(язык, 5),
                  л=f"{n} + {m} = {r}.")
        return я["список_воп2"].format(**з2)
    elif форма in ("список_воп", "список_воп_дом"):
        # THE LIST ASKED IN THE SAME LINE (holon 03.09): the market buys COUNT
        # as an executor only from a question→answer pair standing beside the
        # enumeration; the statement alone is read by no market of questions
        if форма == "список_воп_дом":
            з2 = dict(общ, П1=(я.get("вместилища_где") or я["вместилища"])[место],
                      О1=я["один"][Т], О2=я["один"][Т2], О3=я["один"][Т3],
                      Чс=я["счётом"][3], ВЕЩ=_предмет(язык, 3), ВЕЩ2=_предмет(язык, 5))
            return я["список_воп_дом"].format(**з2)
        n1, n2, n3 = n, m, k
        r = n1 + n2 + n3
        з3 = dict(общ, n1=n1, n2=n2, n3=n3, Т1=_вещь(язык, Т, n1), Т2=_вещь(язык, Т2, n2),
                  Т3=_вещь(язык, Т3, n3), r=r, ВЕЩ=_предмет(язык, r), ВЕЩ2=_предмет(язык, 5),
                  л=f"{n1} + {n2} = {n1 + n2}, {n1 + n2} + {n3} = {r}.")
        return я["список_воп"].format(**з3)
    elif форма in ("двое_разность", "двое_сумма"):
        # TWO GOODS IN ONE PLACE (32's order 03.09): one of them grows, and the
        # question asks either their difference or their sum — one fact, two ends
        if Т == Т2:
            raise ValueError("два товара должны быть разными")
        вин1 = _вещь_вин(язык, Т, k)
        if вин1 is None:
            raise ValueError("форма вещи не объявлена")
        s = n + k
        общ2 = dict(общ, n1=n, n2=m, k=k, П=я["места"][место],
                    Т1=_вещь(язык, Т, 2), Т2=_вещь(язык, Т2, 2),
                    Т1м=_вещь(язык, Т, 5), Т2м=_вещь(язык, Т2, 5),
                    Т1n=_вещь(язык, Т, n), Т2n=_вещь(язык, Т2, m),
                    Т1k=_вещь(язык, Т, k), Твk1=вин1,
                    КВ1=_квопрос(язык, Т), КВ2=_квопрос(язык, Т2),
                    ДЕ1=_де(язык, Т), ДЕ2=_де(язык, Т2))
        общ2["ГВ"] = (я.get("ещё_один") or {}).get(
            (я.get("род_вещи") or ("",) * len(я["вещи"]))[Т], "")
        приход = я["пришло_один" if k == 1 else "пришло_многие"]
        факт = я["двое"].format(**общ2) + " " + приход.format(**общ2)
        if форма == "двое_разность":
            if s < m:
                raise ValueError("разность ушла бы в минус")
            r = s - m
            воп = я["воп_двое_разность"].format(**общ2)
            леджер = f"{n} + {k} = {s}, {s} − {m} = {r}."
        else:
            r = s + m
            воп = я["воп_двое_сумма"].format(**общ2)
            леджер = f"{n} + {k} = {s}, {s} + {m} = {r}."
        return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма in ("состояния_добавили", "состояния_разность"):
        # TWO STATES OF TWO GOODS (32's order 03.09): the before and the after
        # said in full, and the question reads ONE pair of them
        if Т == Т2:
            raise ValueError("два товара должны быть разными")
        m1, m2 = n + k, m + k2
        общ2 = dict(общ, n1=n, n2=m, m1=m1, m2=m2, П=я["места"][место],
                    Т1=_вещь(язык, Т, 2), Т2=_вещь(язык, Т2, 2),
                    Т1м=_вещь(язык, Т, 5), Т2м=_вещь(язык, Т2, 5),
                    Т1n=_вещь(язык, Т, n), Т2n=_вещь(язык, Т2, m),
                    Т1m=_вещь(язык, Т, m1), Т2m=_вещь(язык, Т2, m2),
                    КВ1=_квопрос(язык, Т), КВ2=_квопрос(язык, Т2),
                    ДЕ1=_де(язык, Т), ДЕ2=_де(язык, Т2))
        факт = я["состояния"].format(**общ2)
        if форма == "состояния_добавили":
            r = k
            воп = я["воп_добавили"].format(**общ2)
            леджер = f"{m1} − {n} = {r}."
        else:
            if m2 < m1:
                raise ValueError("разность ушла бы в минус")
            r = m2 - m1
            воп = я["воп_теперь_разность"].format(**общ2)
            леджер = f"{m2} − {m1} = {r}."
        return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма in ("курс", "курс_обр"):
        # A GOOD PRICED IN ANOTHER GOOD (e9's profile, genus 7): «one book costs
        # 2 coins. how many coins do 7 books cost? 7 × 2 = 14.»
        def вещь2(сколько):
            return _вещь(язык, Т2, сколько)
        общ2 = dict(общ, Т1=вещь(1), Т2=вещь2(2), Т2k=вещь2(k), Т2m=вещь2(m), Т2м=вещь2(5),
                    О1=я["один"][Т], КВ2=_квопрос(язык, Т2), ДЕ2=_де(язык, Т2))
        if форма == "курс":
            r = n * k
            факт = я["курс"].format(**общ2, k=k)
            воп = я["воп_курс"].format(**общ2, n=n)
            леджер = f"{n} × {k} = {r}."
        else:
            r = m // n
            факт = я["курс_обр"].format(**общ2, n=n, m=m)
            воп = я["воп_курс_обр"].format(**общ2)
            леджер = f"{m} ÷ {n} = {r}."
        return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма == "убыль":
        # THE GOOD LEAVES AND THE QUESTION ASKS FOR THE REST (32's tomograph
        # 03.09): «paco had 26 apples. paco ate 9 apples. how many apples does
        # paco have left? 26 − 9 = 17.» The eating verb is allowed ONLY on a
        # good the language declares edible — a page saying «tom ate 5 coins»
        # would be faultless arithmetic about a false world, and that is the
        # worst kind of rubbish, for no counting instrument sees it.
        if глагол_убыли == 0 and Т not in я["съедобные"]:
            raise ValueError("этот товар не съедобен")
        if k > n:
            raise ValueError("убыло больше, чем было")
        r = n - k
        факт = я["имел"].format(**общ, n=n) + " " + я["убыль"].format(**общ, Гу=я["убыли"][глагол_убыли], k=k)
        воп = я["воп_осталось"].format(**общ)
        леджер = f"{n} − {k} = {r}."
    elif форма == "место_ушли":
        # ДЕРЖАНИЕ С УХОДОМ (атлас немоты holon 04.09, строка #117): живое
        # уходит САМО, и вопрос спрашивает об оставшихся — «there were 12 kids
        # in the yard. 4 kids left. how many kids are there now?»
        if k > n:
            raise ValueError("ушло больше, чем было")
        живвин = _живое_вин(язык, Т, k)
        if живвин is None:
            raise ValueError("форма живого не объявлена")
        r = n - k
        род_ж = (я.get("род_живого") or ("",) * len(я["живые"]))[Т]
        общ3 = dict(общ, Ж=_живое(язык, Т, 2), Жn=_живое(язык, Т, n),
                    Жk=_живое(язык, Т, k), Жм=_живое(язык, Т, 5), Жвk=живвин,
                    ГЛЖ=(я.get("ушёл") or {}).get(род_ж, ""))
        уход = я["ушло_живое_один" if k == 1 else "ушло_живое"]
        факт = (я["место_п_живые"].format(**общ3, n=n, П=я["места"][место])
                + " " + уход.format(**общ3, k=k))
        воп = я["воп_живые_теперь"].format(**общ3)
        леджер = f"{n} − {k} = {r}."
        return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"
    elif форма == "место_убыло":
        # A PLACE EMPTIED (32's order 03.09, the places the market of places
        # never bought: yard, vase, fence, pond, cage, garden): the holding is
        # said with the place, then part of it goes, and the question asks what
        # stands there NOW
        if k > n:
            raise ValueError("убыло больше, чем было")
        r = n - k
        факт = я["место_п"].format(**общ, n=n, П=я["места"][место]) + " " + я["убрали"].format(**общ, k=k)
        воп = я["воп_теперь_место"].format(**общ)
        леджер = f"{n} − {k} = {r}."
    elif форма == "ставка":
        # A RATE WITHOUT MONEY: «every day», the days asked or the amount asked
        Г = я["ставки"][глагол_ставки]
        факт = я["ставка"].format(**общ, Г=Г, n=n)
        if дней:
            r = n * k
            воп = я["воп_за"].format(**общ, k=k, Д=_день(язык, k))
            леджер = f"{n} × {k} = {r}."
        else:
            r = m // n
            воп = я["воп_дней"].format(**общ, m=m)
            леджер = f"{m} ÷ {n} = {r}."
    else:
        # THE SUM SAID BY «THEY» after the bearers are named
        r = n + m
        л = f"{n} + {m} = {r}."
        return я["вместе_они"].format(**общ, n=n, m=m, r=r, Тr=вещь(r), л=л) + " " + я["ответ"].format(r=r)
    return f"{факт} {воп} {леджер} {я['ответ'].format(r=r)}"


# --- the court's side ---
def _альт(слова):
    return "(" + "|".join(re.escape(с) for с in sorted(set(с for с in слова if с), key=len, reverse=True)) + ")"


def _дыры(язык):
    я = ЯЗЫКИ[язык]
    вещи = set()
    for i in range(len(я["вещи"])):
        for n in range(0, 400):
            вещи.add(_вещь(язык, i, n))
            в = _вещь_вин(язык, i, n)
            if в:
                вещи.add(в)
    # ФОРМЫ ЖИВОГО — ТЕМ ЖЕ ХОДОМ, ЧТО ФОРМЫ ВЕЩИ: язык, не объявивший живых,
    # рода ухода не пишет и не судит.
    живые = set()
    for i in range(len(я.get("живые") or ())):
        for n in range(0, 400):
            живые.add(_живое(язык, i, n))
            в = _живое_вин(язык, i, n)
            if в:
                живые.add(в)
    # ЯЗЫК, НЕ ОБЪЯВИВШИЙ ДОЛЕЙ, НЕ ПИШЕТ ИХ И НЕ СУДИТ: дом дробей знает
    # три языка, дом страниц — четыре, и четвёртый просто не имеет рода доли
    try:
        доли = {fracforms.доля_слово(язык, чс, зн) for чс, зн in ДОЛИ}
    except KeyError:
        доли = set()
    лица = ЛИЦА[язык]
    ч = r"(\d+)"
    return {"X": _альт(л[0] for л in лица), "Y": _альт(л[0] for л in лица),
            "Xр": _альт(л[2] for л in лица), "Yр": _альт(л[2] for л in лица),
            "Т": _альт(вещи), "Тn": _альт(вещи), "Тk": _альт(вещи), "Тm": _альт(вещи), "Тм": _альт(вещи), "Твk": _альт(вещи),
            "Ч": _альт(доли), "K": _альт((я.get("кратные") or {}).values()), "а": r"(а?)", "У": _альт(я.get("ушли") or ()),
            "П": _альт(я.get("места") or ()), "С": _альт(я.get("свойства") or ()), "С2": _альт(я.get("свойства") or ()), "С3": _альт(я.get("свойства") or ()),
            "С3р": _альт(я.get("свойства_род") or я.get("свойства") or ()), "Ст": _альт(я.get("свойства_твор") or я.get("свойства") or ()),
            "k2": r"(\d+)", "Г": _альт(я.get("ставки") or ()), "Гу": _альт(я.get("убыли") or ()), "Тr": _альт(вещи),
            "Д": _альт([_день(язык, k) for k in range(1, 60)] if я.get("дни") else ()),
            "Т1": _альт(вещи), "Т2": _альт(вещи), "Т3": _альт(вещи), "Т2k": _альт(вещи), "Т2m": _альт(вещи), "Т2м": _альт(вещи),
            "О1": _альт(я.get("один") or ()), "О2": _альт(я.get("один") or ()), "О3": _альт(я.get("один") or ()),
            "П1": _альт(list(я.get("вместилища") or ()) + list(я.get("вместилища_где") or ())), "n1": r"(\d+)", "n2": r"(\d+)", "n3": r"(\d+)",
            "Чс": _альт((я.get("счётом") or {}).values()), "ВЕЩ": _альт([_предмет(язык, i) for i in range(1, 40)]),
            "ГВ": _альт((я.get("ещё_один") or {}).values()),
            "Ж": _альт(живые), "Жn": _альт(живые), "Жk": _альт(живые),
            "ГЛЖ": _альт((я.get("ушёл") or {}).values()),
            "Жм": _альт(живые), "Жвk": _альт(живые),
            "КО": _альт(("a", "ad") if я.get("гласные_имени") else ()),
            "ДЕ": _альт(("de ", "d'") if я.get("элизия") else ()),
            "ДЕ1": _альт(("de ", "d'") if я.get("элизия") else ()),
            "ДЕ2": _альт(("de ", "d'") if я.get("элизия") else ()),
            "КВ": _альт((я.get("вопросное") or {}).values()),
            "КВ1": _альт((я.get("вопросное") or {}).values()),
            "КВ2": _альт((я.get("вопросное") or {}).values()),
            "ВЕЩ2": _альт([_предмет(язык, i) for i in range(1, 40)]),
            "Т1м": _альт(вещи), "Т2м": _альт(вещи), "Т1k": _альт(вещи), "Твk1": _альт(вещи),
            "Т1m": _альт(вещи), "Т2m": _альт(вещи), "m1": r"(\d+)", "m2": r"(\d+)",
            "Т1n": _альт(вещи), "Т2n": _альт(вещи),
            "n": ч, "k": ч, "m": ч, "r": ч}


def _шаблоны(язык):
    """[(форма, шаблон)] — ТОЛЬКО те роды, которые язык объявил.

    Дом говорит на четырёх языках, и не всякий объявил всё: у испанского нет
    рода доли (дом дробей знает три языка) и нет цветных частей (прилагательное
    согласуется в роде, и объявлять его надо при каждой вещи). Прежде шаблоны
    собирались одним списком и падали на первом же недостающем ключе; теперь
    род, чьих слов язык не объявил, ПРОСТО НЕ ПИШЕТСЯ И НЕ СУДИТСЯ — тот же
    закон объявленной формы, каким живёт страница.
    """
    я = ЯЗЫКИ[язык]
    л = "{л}"
    хвост = "{л} " + я["ответ"]
    состав = (
        ("остаток", ("имел", "отдал", "воп_ост"), True),
        ("прибавка", ("имел", "получил", "воп_теперь"), True),
        ("доля", ("имел", "ушло", "воп_ост"), True),
        ("вместе", ("имеет", "второй", "воп_вместе"), True),
        ("кратное", ("имеет", "кратно", "воп_второй"), True),
        ("место", ("место", "часть_их", "воп_не"), True),
        ("место_две", ("место", "две_части", "воп_остаток"), True),
        ("место_п", ("место_п", "часть_их_п", "воп_не_п"), True),
        ("место_две_п", ("место_п", "две_части_п", "воп_остаток_п"), True),
        ("место_товар", ("место", "часть_товар", "воп_не_товар"), True),
        ("место_товар_п", ("место_п", "часть_товар_п", "воп_не_товар_п"), True),
        ("убыль", ("имел", "убыль", "воп_осталось"), True),
        ("место_убыло", ("место_п", "убрали", "воп_теперь_место"), True),
        ("место_ушли", ("место_п_живые", "ушло_живое", "воп_живые_теперь"), True),
        ("место_ушли", ("место_п_живые", "ушло_живое_один", "воп_живые_теперь"), True),
        ("двое_разность", ("двое", "пришло_один", "воп_двое_разность"), True),
        ("двое_разность", ("двое", "пришло_многие", "воп_двое_разность"), True),
        ("двое_сумма", ("двое", "пришло_один", "воп_двое_сумма"), True),
        ("двое_сумма", ("двое", "пришло_многие", "воп_двое_сумма"), True),
        ("состояния_добавили", ("состояния", "воп_добавили"), True),
        ("состояния_разность", ("состояния", "воп_теперь_разность"), True),
        ("курс", ("курс", "воп_курс"), True),
        ("курс_обр", ("курс_обр", "воп_курс_обр"), True),
        ("ставка_за", ("ставка", "воп_за"), True),
        ("ставка_дней", ("ставка", "воп_дней"), True),
        ("вместе_они", ("вместе_они",), True),
        ("список_числом", ("список_числом",), False),
        ("список_итогом", ("список_итогом",), False),
        ("список_чисел", ("список_чисел",), False),
        ("список_воп", ("список_воп",), False),
        ("список_воп2", ("список_воп2",), False),
        ("список_воп_дом", ("список_воп_дом",), False),
    )
    вон = []
    for форма, ключи, с_хвостом in состав:
        if any(к not in я for к in ключи):
            continue
        куски = [я[к] for к in ключи]
        if форма == "место_эхо":
            continue
        шаблон = " ".join(куски)
        if с_хвостом and форма != "вместе_они":
            шаблон = f"{шаблон} {хвост}"
        elif форма == "вместе_они":
            шаблон = f"{шаблон} {я['ответ']}"
        вон.append((форма, шаблон))
    if all(к in я for к in ("место", "часть_их", "воп_часть")):
        вон.append(("место_эхо",
                    f"{я['место']} {я['часть_их']} {я['воп_часть']} "
                    f"{я['часть_их']} {я['ответ']}"))
    return вон


def образцы(язык):
    дыры = dict(_дыры(язык), л=r"((?:\d+ [+−×÷] \d+ = \d+(?:, )?)+\.)")
    return [(re.compile("^" + phrases.образец(ш, дыры) + "$"), phrases.порядок(ш), форма)
            for форма, ш in _шаблоны(язык)]


ОБРАЗЦЫ = {л: образцы(л) for л in ЯЗЫКИ}


def _имя(з, язык, ключ):
    for к in (ключ, ключ + "р"):
        if з.get(к):
            return next((л[0] for л in ЛИЦА[язык] if з[к] in (л[0], л[2])), None)
    return None


def _вещь_по_формам(язык, з):
    """Which declared thing wears ALL the forms the line shows: the plural, the
    count form beside n, k, m, and the accusative after the verb."""
    я = ЯЗЫКИ[язык]
    for i in range(len(я["вещи"])):
        годно = True
        for ключ, форма in (("Т", lambda: _вещь(язык, i, 2)), ("Тм", lambda: _вещь(язык, i, 5)),
                            ("Тn", lambda: _вещь(язык, i, int(з["n"]))), ("Тk", lambda: _вещь(язык, i, int(з["k"]))),
                            ("Тm", lambda: _вещь(язык, i, int(з["m"]))), ("Твk", lambda: _вещь_вин(язык, i, int(з["k"])) or "")):
            if з.get(ключ) is None:
                continue
            try:
                if з[ключ] != форма():
                    годно = False
                    break
            except (KeyError, ValueError):
                годно = False
                break
        if годно:
            return i
    return None


def _вещь_при_числах(язык, пары):
    """Which declared thing wears every named form beside its own number.

    The new genera name a good TWICE with two different counts («there were 15
    flowers … now there are 17 flowers»), and the general reader of forms above
    knows only the holes of the old genera. This one is told the pairs.
    """
    я = ЯЗЫКИ[язык]
    for i in range(len(я["вещи"])):
        if all(форма == _вещь(язык, i, n) for форма, n in пары if форма is not None):
            return i
    return None


def разобрать(язык, строка):
    я = ЯЗЫКИ[язык]
    for образец, имена, форма in ОБРАЗЦЫ[язык]:
        м = образец.match(строка)
        if not м:
            continue
        з = {}
        плохо = False
        for имя, г in zip(имена, м.groups()):
            if имя in з and з[имя] != г:
                плохо = True
                break
            з[имя] = г
        if плохо:
            continue
        X = _имя(з, язык, "X")
        # «место», «курс» и списки, названные вместилищем, обходятся без носителя
        if X is None and not (форма.startswith("место") or форма.startswith("курс")
                              or форма.startswith("двое") or форма.startswith("состояния")
                              or форма in ("список_числом", "список_итогом", "список_воп_дом")):
            continue
        Т = _вещь_по_формам(язык, з)
        if Т is None:
            continue
        п = dict(форма=форма, X=X or ЛИЦА[язык][0][0], Т=Т)
        try:
            if форма in ("остаток", "прибавка"):
                п.update(n=int(з["n"]), k=int(з["k"]))
            elif форма == "доля":
                доля = next(((чс, зн) for чс, зн in ДОЛИ if fracforms.доля_слово(язык, чс, зн) == з["Ч"]), None)
                if доля is None:
                    continue
                п.update(n=int(з["n"]), доля=доля)
            elif форма == "вместе":
                Y = _имя(з, язык, "Y")
                if Y is None:
                    continue
                п.update(n=int(з["n"]), m=int(з["m"]), Y=Y)
            elif форма == "кратное":
                Y = _имя(з, язык, "Y")
                кратность = next((k for k, с in я["кратные"].items() if с == з["K"]), None)
                if Y is None or кратность is None:
                    continue
                п.update(n=int(з["n"]), Y=Y, кратность=кратность)
            elif форма == "убыль":
                глагол = я["убыли"].index(з["Гу"])
                п.update(n=int(з["n"]), k=int(з["k"]), глагол_убыли=глагол)
            elif форма == "список_воп2":
                n1, n2 = int(з["n1"]), int(з["n2"])
                т2 = [_вещь_при_числах(язык, [(з[к], n)])
                      for n, к in ((n1, "Т1"), (n2, "Т2"))]
                if None in т2:
                    return None
                return dict(форма=форма, X=X or ЛИЦА[язык][0][0], n=n1, m=n2,
                            Т=т2[0], Т2=т2[1])
            elif форма == "список_воп":
                n1, n2, n3 = int(з["n1"]), int(з["n2"]), int(з["n3"])
                т3 = [_вещь_при_числах(язык, [(з[к], n)])
                      for n, к in ((n1, "Т1"), (n2, "Т2"), (n3, "Т3"))]
                if None in т3:
                    return None
                return dict(форма=форма, X=X or ЛИЦА[язык][0][0], n=n1, m=n2, k=n3,
                            Т=т3[0], Т2=т3[1], Т3=т3[2])
            elif форма == "список_воп_дом":
                где = (я.get("вместилища_где") or я["вместилища"])
                место_ = next((i for i, в in enumerate(где) if в == з["П1"]), None)
                т3 = [next((i for i, о in enumerate(я["один"]) if о == з[к]), None)
                      for к in ("О1", "О2", "О3")]
                if место_ is None or None in т3:
                    return None
                return dict(форма=форма, X=X or ЛИЦА[язык][0][0], место=место_,
                            Т=т3[0], Т2=т3[1], Т3=т3[2])
            elif форма in ("двое_разность", "двое_сумма"):
                n1, n2, k_ = int(з["n1"]), int(з["n2"]), int(з["k"])
                Т1 = _вещь_при_числах(язык, [(з.get("Т1n"), n1), (з.get("Т1k"), k_),
                                             (з.get("Т1"), 2), (з.get("Т1м"), 5)])
                Т2_ = _вещь_при_числах(язык, [(з.get("Т2n"), n2), (з.get("Т2"), 2), (з.get("Т2м"), 5)])
                if Т1 is None or Т2_ is None:
                    return None
                return dict(форма=форма, X=X or ЛИЦА[язык][0][0], Т=Т1, Т2=Т2_,
                            n=n1, m=n2, k=k_, место=я["места"].index(з["П"]))
            elif форма in ("состояния_добавили", "состояния_разность"):
                n1, n2, m1, m2 = int(з["n1"]), int(з["n2"]), int(з["m1"]), int(з["m2"])
                Т1 = _вещь_при_числах(язык, [(з.get("Т1n"), n1), (з.get("Т1m"), m1),
                                             (з.get("Т1"), 2), (з.get("Т1м"), 5)])
                Т2_ = _вещь_при_числах(язык, [(з.get("Т2n"), n2), (з.get("Т2m"), m2),
                                              (з.get("Т2"), 2), (з.get("Т2м"), 5)])
                if Т1 is None or Т2_ is None or m1 < n1 or m2 < n2:
                    return None
                return dict(форма=форма, X=X or ЛИЦА[язык][0][0], Т=Т1, Т2=Т2_,
                            n=n1, m=n2, k=m1 - n1, k2=m2 - n2,
                            место=я["места"].index(з["П"]))
            elif форма == "место_убыло":
                п.update(n=int(з["n"]), k=int(з["k"]), место=я["места"].index(з["П"]))
            elif форма == "место_ушли":
                # ЖИВОЕ УЗНАЁТСЯ ПО ТЕМ ФОРМАМ, КАКИЕ СТРОКА НАЗВАЛА: языки
                # берут разные (английский — множественное, русский — счётное
                # и родительное), и суд не вправе требовать одной.
                n_, k_ = int(з["n"]), int(з["k"])
                пары = (("Ж", 2), ("Жn", n_), ("Жk", k_), ("Жм", 5))
                живой = next(
                    (i for i in range(len(я.get("живые") or ()))
                     if all(з.get(к) is None or з[к] == _живое(язык, i, n2)
                            for к, n2 in пары)
                     and (з.get("Жвk") is None
                          or з["Жвk"] == _живое_вин(язык, i, k_))), None)
                if живой is None:
                    return None
                п.update(Т=живой, n=n_, k=k_, место=я["места"].index(з["П"]))
            elif форма in ("место", "место_эхо", "место_п", "место_товар", "место_товар_п"):
                п.update(форма=форма, n=int(з["n"]), k=int(з["k"]),
                         место=я["места"].index(з["П"]), свойство=я["свойства"].index(з["С"]))
            elif форма in ("место_две", "место_две_п"):
                п.update(форма=форма, n=int(з["n"]), k=int(з["k"]), k2=int(з["k2"]),
                         место=я["места"].index(з["П"]), свойство=я["свойства"].index(з["С"]),
                         свойство2=я["свойства"].index(з["С2"]), свойство3=я["свойства"].index(з["С3"]))
            elif форма in ("список_числом", "список_итогом", "список_чисел"):
                if форма != "список_чисел":
                    место_ = next((i for i, в in enumerate(я["вместилища"]) if в == з["П1"]), None)
                    т = [next((i for i, о in enumerate(я["один"]) if о == з[к]), None) for к in ("О1", "О2", "О3")]
                    if место_ is None or None in т:
                        return None
                    return dict(форма=форма, X=X or ЛИЦА[язык][0][0], место=место_, Т=т[0], Т2=т[1], Т3=т[2])
                n1, n2, n3 = int(з["n1"]), int(з["n2"]), int(з["n3"])
                т = [next((i for i in range(len(я["вещи"])) if _вещь(язык, i, n) == з[к]), None)
                     for n, к in ((n1, "Т1"), (n2, "Т2"), (n3, "Т3"))]
                if None in т:
                    return None
                return dict(форма=форма, X=X or ЛИЦА[язык][0][0], n=n1, m=n2, k=n3, Т=т[0], Т2=т[1], Т3=т[2])
            elif форма in ("курс", "курс_обр"):
                Т2 = next((i for i in range(len(я["вещи"]))
                           if з.get("Т2") in (None, _вещь(язык, i, 2)) and з.get("Т2м") in (None, _вещь(язык, i, 5))), None)
                if Т2 is None:
                    return None
                Т1 = next((i for i in range(len(я["вещи"])) if я["один"][i] == з["О1"]), None) if "О1" in з else Т
                п.update(форма=форма, Т=Т1 if Т1 is not None else Т, Т2=Т2, n=int(з["n"]))
                п.update(k=int(з["k"])) if форма == "курс" else п.update(m=int(з["m"]))
                return п
            elif форма in ("ставка_за", "ставка_дней"):
                за = форма == "ставка_за"
                п.update(форма="ставка", n=int(з["n"]), глагол_ставки=я["ставки"].index(з["Г"]), дней=за)
                п.update(k=int(з["k"])) if за else п.update(m=int(з["m"]))
            else:
                Y = _имя(з, язык, "Y")
                if Y is None:
                    continue
                п.update(форма="вместе_они", n=int(з["n"]), m=int(з["m"]), Y=Y)
        except (KeyError, ValueError):
            continue
        return п
    return None


def судить(строка):
    с = строка.strip()
    for язык in ЯЗЫКИ:
        п = разобрать(язык, с)
        if п is not None:
            форма = п.pop("форма")
            try:
                return True, страница(язык, форма, **п) == с
            except (StopIteration, KeyError, IndexError, ValueError, ZeroDivisionError):
                return True, False
    return False, False
