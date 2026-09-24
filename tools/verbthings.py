"""A VERB TAKES ITS OWN KIND OF THINGS (03.09).

The lexical worlds paired any verb with any countable thing, and the frame
wore nonsense: «sara wrote 8 pencils», «ann bought 21 books and ate 12 books»,
«hugo reads 5 apples», «ann walks 2 pounds every day». A verb of eating takes
food, a verb of writing takes what is written, a verb of walking takes a
distance or a time — and the corpus that teaches speech must not teach the
contrary. One house declares what each verb takes; the generators draw their
things from it, and the episode court refuses a known verb with a thing of
the wrong kind (an unknown verb or an unknown thing is not judged here).
"""
from animacy import ANIMATE  # одушевлённость: свой дом (23.09, решение ведущего)
from plural import singular

# ПАСПОРТ КОРНЯ (07.09): кто читает род глагола. Правка ГЛАГОЛ_БЕРЁТ или ANIMATE есть правка
# всех этих домов и судов — шрам 06.09, когда семь глаголов моста, внесённых сюда, уронили
# суд эпизода 986 ложными строками в одиннадцати мирах. Список сверяется прибором
# `scripts/root_passport.py`, а не памятью.
# ДВА ИМЕНИ ПЕРЕЕХАЛИ, ПАСПОРТ НЕ ПОШЁЛ ЗА НИМИ (16.09): чтение рода глагола ушло из
# кузниц `gen_genesis_everyday` и `gen_genesis_story_chain` в дома `everydayforms` и
# `story_chainforms`. Паспорт звал призраков и молчал о живых читателях — то есть лгал
# ОБЕИМИ половинами разом, и всякий, кто судил по нему о цене правки корня, судил по
# выдумке ровно там, где цена и выросла.
# ДВА НОВЫХ ЧИТАТЕЛЯ (23.09, перепись словаря вещей): словарь `gsm_items` берёт вещи из школьных
# классов этой двери, а перепись полос `gsm_census` мерит ими покрытие. Прибор паспорта назвал их
# на вершине вагона 24.09 — дописаны сюда, а не выведены.
ЧИТАЮТ = ("gen_genesis_gsmlex", "everydayforms", "gen_genesis_realverbs",
          "gen_genesis_gsmwide", "story_chainforms", "gen_genesis_items",
          "gen_genesis_pronouns", "episode_court", "verbthings_court",
          "gsm_items", "gsm_census")

ЕДА = {"apples", "cookies", "cakes", "pastries", "nuts", "eggs", "slices", "bananas", "oranges", "pears", "sweets",
       "candies", "sandwiches", "grapes", "plums", "buns", "pies", "loaves", "pancakes", "cherries", "carrots", "calories"}
# ПИТЬЁ ПОСУДОЙ И ПИТЬЁ МЕРОЙ (24.09, дверь актов): чашку и бутылку держат и считают, галлоном и
# литром меряют выпитое. «drank» берёт оба, словарь держимого (`gsm_items.ВЕЩИ`) — лишь посуду.
ПИТЬЁ_МЕРОЙ = {"gallons", "litres", "liters"}
ПИТЬЁ = {"cups", "glasses", "bottles", "mugs"} | ПИТЬЁ_МЕРОЙ
ВЫПЕЧКА = {"cookies", "cakes", "pies", "buns", "loaves", "pastries", "pancakes"}
ПИСЬМЕННОЕ = {"letters", "pages", "cards", "notes", "words", "lines", "poems", "essays", "stories", "chapters", "books"}
ЧТЕНИЕ = {"books", "pages", "letters", "cards", "stories", "poems", "chapters", "notes", "words", "lines"}
# ДЮЙМ И САНТИМЕТР — ТОЖЕ РАССТОЯНИЕ (03.09, дом историй с мерой): прыжок
# их держал, а ходьба и бег — нет, и «the dog walked 92 inches» звалось
# ложью о языке при верной мере. Мелкая мера не перестаёт быть мерой
# оттого, что ею редко меряют шаг.
РАССТОЯНИЕ_ВРЕМЯ = {"miles", "kilometres", "kilometers", "metres", "meters", "feet", "inches",
                    "centimetres", "centimeters", "steps", "laps", "minutes", "hours", "seconds"}
ВЕС = {"pounds", "kilograms", "grams"}
ОЧКИ = {"points", "goals", "runs"}
ДЕНЬГИ = {"dollars", "coins", "cents", "rubles", "euros"}
ПОСЕВ = {"seeds", "flowers", "trees", "bulbs"}
СБОР = {"shells", "stones", "stamps", "coins", "cards", "seeds", "flowers", "mushrooms", "berries", "nuts", "eggs", "apples", "pears", "plums", "cherries"}
ВРЕМЯ = {"minutes", "hours", "seconds", "days", "weeks", "months", "years"}
# what a hand picks: small countable things (not distances, not money, not points)
В_РУКЕ = {"books", "cards", "pens", "pencils", "balls", "marbles", "stamps", "coins", "shells", "stones", "flowers", "toys", "blocks",
          "buttons", "stickers", "balloons", "cups", "boxes", "bottles", "hats", "shirts", "keys", "rings", "pieces", "sticks", "leaves"}

# the verbs of the SVAMP/g1 bands the school lacked (e9 04.09): what they take
ПРЫЖОК = {"inches", "feet", "centimetres", "centimeters", "metres", "meters", "times"}
УПРАЖНЕНИЯ = {"push-ups", "crunches", "laps", "sit-ups", "jumps", "squats"}
ВЫПОЛНЕНИЕ = {"pages", "problems", "laps", "tasks", "exercises", "chapters", "levels"}
ПРОСМОТР = {"movies", "episodes", "films", "shows", "videos", "games"}
ВЫИГРЫШ = {"games", "tickets", "medals", "prizes", "rounds", "matches"}
# ВЫИГРЫВАЮТ И СВОЁ (24.09, дверь актов): класс выше взят у полосы, и ни одной его вещи нет в нашем
# словаре — «won» оставался без страницы. Дети играют на шарики, карточки и наклейки и выигрывают
# их друг у друга; все три — вещи в руке нашего класса.
ИГРОВОЕ = {"marbles", "cards", "stickers"}
ПОСЫЛКА = {"letters", "emails", "cards", "messages", "parcels", "postcards"}
УБОРКА = {"figures", "books", "stones", "boxes", "toys", "stickers", "weeds", "leaves"}
СБОР_ДЕНЕГ = {"dollars", "euros", "rubles", "coins"}
РОСТ = {"inches", "centimetres", "centimeters", "flowers", "plants", "trees", "tomatoes"}
ВЫБРОС = {"caps", "boxes", "cans", "bottles", "papers", "toys", "cards"}

ГЛАГОЛ_БЕРЁТ = {
    "jumped": ПРЫЖОК, "jumps": ПРЫЖОК, "jump": ПРЫЖОК,
    # «do/does/did» — лёгкий глагол и вспомогательный разом («how many minutes
    # do 2 hours equal?»): дом о нём молчит; как дело он судится рамкой семейства.
    "completed": ВЫПОЛНЕНИЕ, "completes": ВЫПОЛНЕНИЕ, "complete": ВЫПОЛНЕНИЕ,
    "watched": ПРОСМОТР, "watches": ПРОСМОТР, "watch": ПРОСМОТР,
    "won": ВЫИГРЫШ | ИГРОВОЕ, "wins": ВЫИГРЫШ | ИГРОВОЕ, "win": ВЫИГРЫШ | ИГРОВОЕ,
    "sent": ПОСЫЛКА, "sends": ПОСЫЛКА, "send": ПОСЫЛКА,
    "removed": УБОРКА, "removes": УБОРКА, "remove": УБОРКА,
    "raised": СБОР_ДЕНЕГ | РОСТ, "raises": СБОР_ДЕНЕГ | РОСТ, "raise": СБОР_ДЕНЕГ | РОСТ,
    "grew": РОСТ, "grown": РОСТ, "grows": РОСТ, "grow": РОСТ,
    "threw": ВЫБРОС, "throws": ВЫБРОС, "throw": ВЫБРОС,
    "ate": ЕДА, "eats": ЕДА, "eat": ЕДА, "eaten": ЕДА,
    "drank": ПИТЬЁ, "drinks": ПИТЬЁ, "drink": ПИТЬЁ, "drunk": ПИТЬЁ,
    "baked": ВЫПЕЧКА, "bakes": ВЫПЕЧКА, "bake": ВЫПЕЧКА,
    "wrote": ПИСЬМЕННОЕ, "writes": ПИСЬМЕННОЕ, "write": ПИСЬМЕННОЕ, "written": ПИСЬМЕННОЕ,
    "read": ЧТЕНИЕ, "reads": ЧТЕНИЕ,
    "walks": РАССТОЯНИЕ_ВРЕМЯ, "walked": РАССТОЯНИЕ_ВРЕМЯ, "runs": РАССТОЯНИЕ_ВРЕМЯ | ОЧКИ, "ran": РАССТОЯНИЕ_ВРЕМЯ,
    "drove": РАССТОЯНИЕ_ВРЕМЯ, "drives": РАССТОЯНИЕ_ВРЕМЯ, "swam": РАССТОЯНИЕ_ВРЕМЯ, "swims": РАССТОЯНИЕ_ВРЕМЯ,
    "weighs": ВЕС, "weighed": ВЕС, "lifts": ВЕС, "lifted": ВЕС,
    "scored": ОЧКИ, "scores": ОЧКИ,
    "earns": ДЕНЬГИ, "earned": ДЕНЬГИ, "paid": ДЕНЬГИ, "pays": ДЕНЬГИ,
    # money is spent, and so is time
    "spends": ДЕНЬГИ | ВРЕМЯ, "spent": ДЕНЬГИ | ВРЕМЯ,
    "planted": ПОСЕВ, "plants": ПОСЕВ,
    "collected": СБОР | В_РУКЕ, "collects": СБОР | В_РУКЕ, "picked": СБОР | ЕДА | В_РУКЕ, "picks": СБОР | ЕДА | В_РУКЕ,
}
ВСЕ_ВЕЩИ = set().union(*ГЛАГОЛ_БЕРЁТ.values())

# ЧЕЛОВЕК — НЕ ТОВАР И НЕ МАТЕРИАЛ (04.09). Одушевлённость объявлена в
# gsm_items («a layer that pastes a possession verb onto these words is
# wrong by construction»), но ЭТОТ дом её не читал, и одушевлённое слово
# не лежит ни в одном пуле — а вещь, которой не знает ни один пул, дом
# пропускал как «не моё дело». Оттого 155 показов двух миров говорили
# «felix sold 1 person away», «carla eats 3 students», «hugo weighs 9
# people»: грамматично и ложно о мире — тот же род изъяна, что «peter
# keeps -1 coins».
#
# Отказ ложится ДВУМЯ правилами, и оба выводятся из уже объявленного:
#   · глагол С ПУЛОМ отказывает одушевлённому, ибо ни один пул его не
#     держит (ест еду, пишет письменное, взвешивает вес) — здесь чинится
#     сама дыра «неизвестной вещи»;
#   · глагол БЕЗ ПУЛА отказывает, если он есть глагол ТОРГА ИЛИ РАСХОДА:
#     купить, продать, заплатить, сделать, потратить, заработать —
#     обращение с живым как с товаром. Прочие беспулевые глаголы живое
#     держат и держать должны: «у ани трое детей», «команда потеряла двух
#     игроков», «в проект нужно 3 человека».
ТОРГ_И_РАСХОД = {
    "bought", "buys", "buy", "sold", "sells", "sell", "paid", "pays", "pay",
    "makes", "made", "make", "earns", "earned", "earn",
    "spends", "spent", "spend", "uses", "used", "use",
    # ЗАКАЗ ЕСТЬ ПОКУПКА (24.09, дверь актов ниже): «ordered 3 students» ложно так же, как «bought»
    "ordered", "orders", "order",
}


# ОТКУДА И КУДА АКТ ДВИЖЕТ ВЕЩЬ — ОДНА ДВЕРЬ (24.09, наряд ведущего: пробел 4 языка количеств).
# Дверь выше говорит, ЧТО глагол берёт; эта — что акт делает с держанием. Знак акта жил в домах
# местными таблицами: пары прибавки и убыли дома вещей, тройки дома местоимений со своим ±1, пары
# накопления суда эпизодов со своим «away», — и одна правда («отдал — убыль, и отдают away»)
# стояла тремя руками, каждая из которых могла разойтись с другими молча.
#
#     АКТ ДВИЖЕТ ВЕЩЬ ИЗ ОДНОГО ДЕРЖАНИЯ В ДРУГОЕ; ЗНАК ЕСТЬ ТО, ЧЕМ ЭТО ДВИЖЕНИЕ ВЫГЛЯДИТ С
#     МЕСТА СПРОШЕННОГО ДЕРЖАТЕЛЯ.
#
# Держатели: НОСИТЕЛЬ — тот, кто делает (подлежащее страницы); МЕСТО — вместилище, названное
# страницей («on the shelf», «in the basket»); ДРУГОЙ — иной держатель, кому отдают, куда сажают и
# откуда приносят; НИЧТО — откуда берётся сделанное и найденное и куда уходит съеденное,
# потерянное, выброшенное. Потому одно объявление «took» даёт убыль месту и прибыль взявшему, а
# «brought» о носителе молчит: страница принесённого спрашивает место. Посаженное уходит не в
# вместилище, а в землю, доставленное — адресату: оба акта о полке и корзине молчат.
#
# ЧАСТИЦА — ЧАСТЬ АКТА, А НЕ СТРАНИЦЫ: «gave … away» и «threw … away» суть акты отдачи в чужое
# и в никуда; «threw 3 stones» без частицы есть бросок, а не убыль, и дом, писавший частицу
# своей рукой, мог бы её забыть.
#
# ВНЕ ДВЕРИ, С ПРИЧИНОЙ: «caught» — дверь не знает, что он берёт (мир форм глагола пишет «caught 8
# cards» мимо неё), а его естественная вещь, fish, изъята из словаря как неизменяемое имя
# (`gsm_items.WITHHELD`); объявить его здесь значило бы писать «caught 3 cakes». Он ждёт класса.
# «drank» — выпивают питьё, а не чашку: «had 8 cups … drank 7 cups … has 1 cup» говорит, что чашки
# исчезли. Посуда при нём есть мера питья, и страница держания, не назвавшая питья, лжёт о мире;
# он ждёт рамки, где питьё названо («8 cups of juice»).
НОСИТЕЛЬ, МЕСТО, ДРУГОЙ, НИЧТО = "носитель", "место", "другой", "ничто"
АКТЫ = {
    # к носителю: получено от другого, взято из места, сделано или найдено из ничего
    "got": (ДРУГОЙ, НОСИТЕЛЬ, ""),
    "received": (ДРУГОЙ, НОСИТЕЛЬ, ""),
    "bought": (ДРУГОЙ, НОСИТЕЛЬ, ""),
    "ordered": (ДРУГОЙ, НОСИТЕЛЬ, ""),
    "won": (ДРУГОЙ, НОСИТЕЛЬ, ""),
    "took": (МЕСТО, НОСИТЕЛЬ, ""),
    "picked": (МЕСТО, НОСИТЕЛЬ, ""),
    "collected": (МЕСТО, НОСИТЕЛЬ, ""),
    "earned": (ДРУГОЙ, НОСИТЕЛЬ, ""),
    "found": (НИЧТО, НОСИТЕЛЬ, ""),
    "baked": (НИЧТО, НОСИТЕЛЬ, ""),
    "wrote": (НИЧТО, НОСИТЕЛЬ, ""),
    "grew": (НИЧТО, НОСИТЕЛЬ, ""),
    "added": (НИЧТО, НОСИТЕЛЬ, ""),
    # от носителя: отдано другому держателю, ушло в ничто
    "gave": (НОСИТЕЛЬ, ДРУГОЙ, "away"),
    "sold": (НОСИТЕЛЬ, ДРУГОЙ, ""),
    "sent": (НОСИТЕЛЬ, ДРУГОЙ, ""),
    "spent": (НОСИТЕЛЬ, ДРУГОЙ, ""),
    "delivered": (НОСИТЕЛЬ, ДРУГОЙ, ""),
    "planted": (НОСИТЕЛЬ, ДРУГОЙ, ""),
    "lost": (НОСИТЕЛЬ, НИЧТО, ""),
    "threw": (НОСИТЕЛЬ, НИЧТО, "away"),
    "ate": (НОСИТЕЛЬ, НИЧТО, ""),
    "used": (НОСИТЕЛЬ, НИЧТО, ""),
    # место без носителя: принесено из другого держания, убрано в другое
    "brought": (ДРУГОЙ, МЕСТО, ""),
    "removed": (МЕСТО, ДРУГОЙ, ""),
}


def знак_акта(глагол, держатель):
    """+1 — акт приносит вещь спрошенному держателю, −1 — уносит, None — держателя не касается
    (или глагол не акт двери)."""
    акт = АКТЫ.get(глагол)
    if акт is None:
        return None
    откуда, куда, _ = акт
    return 1 if куда == держатель else -1 if откуда == держатель else None


def частица(глагол):
    """Частица акта («away» у отдачи в чужое и в никуда) или пустая строка."""
    акт = АКТЫ.get(глагол)
    return акт[2] if акт else ""


# ОДНА ВЕЩЬ — ТА ЖЕ ВЕЩЬ (04.09). Пулы объявлены множественным числом, а
# показ при счёте один пишет единственное («felix sold 1 person away», «sara
# wrote 1 pencil»), и дом, сверявший слово буквально, звал единственное
# «вещью, которой не знает ни один пул», то есть не своим делом. Единственное
# число не объявляется заново: дом множественного (tools/plural.py) уже знает
# его для всякого объявленного слова, неправильные формы включая
# («people → person», «children → child»), — и обратное соответствие ВЫВОДИТСЯ
# из объявленных пулов, а не пишется рядом с ними.
_ПО_ЕДИНСТВЕННОМУ = {singular(в): в for в in (ВСЕ_ВЕЩИ | ANIMATE)}


def _множественное(вещь):
    """Слово пула для вещи, названной в любом числе."""
    if вещь in ВСЕ_ВЕЩИ or вещь in ANIMATE:
        return вещь
    return _ПО_ЕДИНСТВЕННОМУ.get(вещь, вещь)


def берёт(глагол, вещь):
    """True — the pair is admissible or not this house's business (an unknown
    verb, or a thing no pool names); False — a known verb with a thing of
    the wrong kind, or a verb of trade and expense with a LIVING thing."""
    вещь = _множественное(вещь)
    род = ГЛАГОЛ_БЕРЁТ.get(глагол)
    if вещь in ANIMATE:
        return род is None and глагол not in ТОРГ_И_РАСХОД
    if род is None or вещь not in ВСЕ_ВЕЩИ:
        return True
    return вещь in род


def годные(глаголы, вещи, ключ=None):
    """The things of a pool that every verb of the frame admits (the pool
    itself when nothing is constrained); `ключ` names the English plural of
    an item that is not a plain string."""
    ключ = ключ or (lambda в: в if isinstance(в, str) else в[-1])
    вон = [в for в in вещи if all(берёт(г, ключ(в)) for г in глаголы)]
    return вон or list(вещи)


def подобрать(глаголы, вещи, k, ключ=None):
    """The k-th admissible thing of the pool for the verbs of a frame."""
    г = годные(глаголы, вещи, ключ)
    return г[k % len(г)]


def индекс(глаголы, вещи, k, ключ=None):
    """The index in the pool of the k-th admissible thing — for a second
    pool that runs parallel to the first (Russian things beside English)."""
    return вещи.index(подобрать(глаголы, вещи, k, ключ))
