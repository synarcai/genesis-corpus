#!/usr/bin/env python3
"""THE MONEY ROAD WITH A DISCOUNT — «each bottle costs $30, the discount is $3» (05.09; scenes 23.09).

The SECOND gate of the silence atlas by d5's measure: 72–76 turns of the grove stop on the
money road. The shape that stops them is not arithmetic — it is a price with a DISCOUNT and a
question that may ask for one of four different things over the same two numbers:

    THE PRICE AFTER THE DISCOUNT.   «how much is paid for one bottle? $27: 30 − 3 = 27.»
    THE BILL FOR SEVERAL.           «how much is paid for 5 bottles? $135: 5 × 27 = 135.»
    HOW MANY FIT INTO A SUM.        «how many bottles can be bought for $150? 5: 150 ÷ 30 = 5.»
    HOW MANY AT THE DISCOUNTED PRICE. «for $135? 5: 135 ÷ 27 = 5.»

A reader that has bought «price × count» and nothing else answers the first question with the
price and the third with a multiplication. The four questions stand over ONE pair of numbers
on purpose: the market must buy the QUESTION, not the arithmetic — the arithmetic it has.

THE SIGN OF MONEY STANDS WHERE THE LANGUAGE PUTS IT: «$51» before, «51 ₽», «51 zł», «51 €»
after; that is a property of the language and is declared, not guessed. The count form of the
goods follows the pack's own counting rule, so «5 пачек», «2 пачки», «1 пачка» are one law and
not three tables.

WHAT IS BORROWED: nine languages and the counting rule of the packs (through the house of the
price). Declared here: two goods that are bought in numbers (a pack and a ticket), the frames
of a price, a discount, a bill and a purchase, and the currency sign with its side.

WHAT IS NOT MEASURED, NAMED: a discount in per cent (the percent house owns it), a discount on
the whole bill rather than on each item, and change from a payment.

REWRITTEN 23.09 (the owner's word: a band is an instrument, never a source). The pages said the
band's own sentence — «each pack costs $76. the discount is $25 on each pack» was SVAMP chal-1,
numbers and all, and the leak court named it. The construction stays (a price, a discount on
each item, four questions over one pair); the goods are the house's own (a bottle and a glass,
whose gender fits the declared frames in all nine languages) and the grid is drawn by a rule.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import asking  # noqa: E402 — the house of the pair declares which openers a question may wear
import priceforms as P  # noqa: E402 — the pack's counting rule (P.форма)

ЯЗЫКИ = ("ru", "en", "de", "fr", "es", "it", "pt", "nl", "pl")
# ПАРЫ (цена, скидка) ВЫВОДЯТСЯ ПРАВИЛОМ, А НЕ ПЕРЕПИСЫВАЮТСЯ (23.09): цена от 30 до 96, скидка
# от 10 до 45 % цены, разность не меньше трёх, цены не повторяются. Прежняя таблица начиналась
# парой (76, 25) — числами самой задачи полосы.
def _сетка():
    вон = []
    for i in range(80):
        ц = 30 + (i * 17) % 67
        с = max(3, ц * (10 + (i * 7) % 36) // 100)
        if ц - с < 3 or any(п[0] == ц for п in вон):
            continue
        вон.append((ц, с))
        if len(вон) == 24:
            break
    return tuple(вон)


ЦЕНЫ = _сетка()
СЧЁТ = (2, 3, 4, 5)
ЗНАК = {"ru": ("₽", "после"), "en": ("$", "до"), "de": ("€", "после"), "fr": ("€", "после"),
        "es": ("€", "после"), "it": ("€", "после"), "pt": ("€", "после"), "nl": ("€", "после"),
        "pl": ("zł", "после")}
# ДВЕ ВЕЩИ, КОТОРЫЕ ПОКУПАЮТ ЧИСЛОМ. Счётная форма — по правилу пакета, а не по трём таблицам.
# РОД ВЕЩИ ПОДОБРАН ПОД ОБЪЯВЛЕННЫЕ РАМКИ, А НЕ РАМКИ ПОД ВЕЩЬ: первая — женского рода там, где
# рамка говорит «каждая / jede / każda», мужского при «un / um», среднего при «elk»; вторая —
# по рамкам `РАМКА2`. Бутылка и стакан ложатся в обе линейки на всех девяти языках.
ТОВАРЫ = {
    "ru": (dict(one="бутылка", few="бутылки", many="бутылок"), dict(one="стакан", few="стакана", many="стаканов")),
    "en": (dict(one="bottle", many="bottles"), dict(one="glass", many="glasses")),
    "de": (dict(one="Flasche", many="Flaschen"), dict(one="Tasse", many="Tassen")),
    "fr": (dict(one="flacon", many="flacons"), dict(one="gobelet", many="gobelets")),
    "es": (dict(one="frasco", many="frascos"), dict(one="vaso", many="vasos")),
    "it": (dict(one="flacone", many="flaconi"), dict(one="bicchiere", many="bicchieri")),
    "pt": (dict(one="frasco", many="frascos"), dict(one="copo", many="copos")),
    "nl": (dict(one="flesje", many="flesjes"), dict(one="kopje", many="kopjes")),
    "pl": (dict(one="butelka", few="butelki", many="butelek"), dict(one="kubek", few="kubki", many="kubków")),
}
# ВИНИТЕЛЬНЫЙ ПАДЕЖ ТАМ, ГДЕ ЯЗЫК ЕГО ГНЁТ: «на каждую пачкУ», «na każdą paczkĘ». Падеж
# пишется, а не выводится из именительного — иначе «на каждую пачка» уходит в свод.
ВИН = {"ru": ("бутылку", "стакан"), "pl": ("butelkę", "kubek")}
# РОД ТОВАРА ТАМ, ГДЕ ВОПРОСНОЕ СЛОВО ЕГО ДЕРЖИТ
РОД = {"es": ("m", "m"), "it": ("m", "m"), "pt": ("m", "m")}
КСК = {"es": {"m": "¿cuántos", "f": "¿cuántas"}, "it": {"m": "quanti", "f": "quante"},
       "pt": {"m": "quantos", "f": "quantas"}}
РЕЧЬ = {
    "ru": dict(цена="каждая {Т1} стоит {Ц}.", скидка="скидка {Цс} на каждую {Т1в}.",
               вопрос_одна="сколько платить за одну {Т1в}?",
               вопрос_много="сколько платить за {k} {Тk}?",
               вопрос_сколько="сколько {МН} можно купить за {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "en": dict(цена="each {Т1} costs {Ц}.", скидка="the discount is {Цс} on each {Т1}.",
               вопрос_одна="how much is paid for one {Т1}?",
               вопрос_много="how much is paid for {k} {Тk}?",
               вопрос_сколько="how many {МН} can be bought for {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "de": dict(цена="jede {Т1} kostet {Ц}.", скидка="der Rabatt beträgt {Цс} auf jede {Т1}.",
               вопрос_одна="wie viel zahlt man für eine {Т1}?",
               вопрос_много="wie viel zahlt man für {k} {Тk}?",
               вопрос_сколько="wie viele {МН} kann man für {Цвсего} kaufen?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "fr": dict(цена="chaque {Т1} coûte {Ц}.", скидка="la remise est de {Цс} sur chaque {Т1}.",
               вопрос_одна="combien paie-t-on pour un {Т1} ?",
               вопрос_много="combien paie-t-on pour {k} {Тk} ?",
               вопрос_сколько="combien de {МН} peut-on acheter pour {Цвсего} ?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=" : "),
    "es": dict(цена="cada {Т1} cuesta {Ц}.", скидка="el descuento es de {Цс} en cada {Т1}.",
               вопрос_одна="¿cuánto se paga por un {Т1}?",
               вопрос_много="¿cuánto se paga por {k} {Тk}?",
               вопрос_сколько="{КСК} {МН} se pueden comprar por {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "it": dict(цена="ogni {Т1} costa {Ц}.", скидка="lo sconto è di {Цс} su ogni {Т1}.",
               вопрос_одна="quanto si paga per un {Т1}?",
               вопрос_много="quanto si paga per {k} {Тk}?",
               вопрос_сколько="{КСК} {МН} si possono comprare con {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "pt": dict(цена="cada {Т1} custa {Ц}.", скидка="o desconto é de {Цс} em cada {Т1}.",
               вопрос_одна="quanto se paga por um {Т1}?",
               вопрос_много="quanto se paga por {k} {Тk}?",
               вопрос_сколько="{КСК} {МН} se podem comprar por {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "nl": dict(цена="elk {Т1} kost {Ц}.", скидка="de korting is {Цс} op elk {Т1}.",
               вопрос_одна="hoeveel betaalt men voor één {Т1}?",
               вопрос_много="hoeveel betaalt men voor {k} {Тk}?",
               вопрос_сколько="hoeveel {МН} kan men kopen voor {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
    "pl": dict(цена="każda {Т1} kosztuje {Ц}.", скидка="rabat wynosi {Цс} na każdą {Т1в}.",
               вопрос_одна="ile płaci się za jedną {Т1в}?",
               вопрос_много="ile płaci się za {k} {Тk}?",
               вопрос_сколько="ile {МН} można kupić za {Цвсего}?",
               ответ_деньги="{Цv}", ответ_счёт="{v} {Тv}", двоеточие=": "),
}
# ВТОРАЯ ВЕЩЬ МУЖСКОГО РОДА ТАМ, ГДЕ ПЕРВАЯ ЖЕНСКОГО: рамка «каждая {Т1}» подошла бы не всем,
# и потому дом объявляет РАМКУ ВТОРОЙ ВЕЩИ отдельно там, где язык её гнёт.
РАМКА2 = {
    "ru": dict(цена="каждый {Т1} стоит {Ц}.", скидка="скидка {Цс} на каждый {Т1в}.",
               вопрос_одна="сколько платить за один {Т1в}?"),
    "de": dict(цена="jede {Т1} kostet {Ц}.", скидка="der Rabatt beträgt {Цс} auf jede {Т1}.",
               вопрос_одна="wie viel zahlt man für eine {Т1}?"),
    "fr": dict(цена="chaque {Т1} coûte {Ц}.", скидка="la remise est de {Цс} sur chaque {Т1}.",
               вопрос_одна="combien paie-t-on pour un {Т1} ?"),
    "nl": dict(цена="elk {Т1} kost {Ц}.", скидка="de korting is {Цс} op elk {Т1}.",
               вопрос_одна="hoeveel betaalt men voor één {Т1}?"),
    "pl": dict(цена="każdy {Т1} kosztuje {Ц}.", скидка="rabat wynosi {Цс} na każdy {Т1в}.",
               вопрос_одна="ile płaci się za jeden {Т1в}?"),
}
ФОРМЫ = ("цена_со_скидкой", "счёт_со_скидкой", "сколько_за_сумму", "сколько_со_скидкой")


def _вещь(язык, i, k):
    return P.форма(язык, ТОВАРЫ[язык][i], k)


def _кс_k(язык, i):
    return КСК[язык][РОД[язык][i]] if язык in КСК else ""


def _цена(язык, n):
    знак, сторона = ЗНАК[язык]
    return f"{знак}{n}" if сторона == "до" else f"{n} {знак}"


def _речь(язык, i, ключ):
    """Вторая вещь берёт свою рамку там, где язык гнёт её род."""
    если = РАМКА2.get(язык, {}) if i == 1 else {}
    return если.get(ключ, РЕЧЬ[язык][ключ])


def _винительный(язык, i):
    """Именительный, если язык винительного не гнёт; иначе объявленная форма."""
    return ВИН[язык][i] if язык in ВИН else _вещь(язык, i, 1)


def рамка(язык, форма, i):
    р = РЕЧЬ[язык]
    одна, вин = _вещь(язык, i, 1), _винительный(язык, i)
    начало = (_речь(язык, i, "цена").replace("{Т1}", одна).replace("{Т1в}", вин) + " "
              + _речь(язык, i, "скидка").replace("{Т1}", одна).replace("{Т1в}", вин))
    мн = _вещь(язык, i, 5)
    if форма == "цена_со_скидкой":
        вопрос = _речь(язык, i, "вопрос_одна").replace("{Т1}", одна).replace("{Т1в}", вин)
        return начало + " " + вопрос + " " + р["ответ_деньги"] + р["двоеточие"] + "{Ц0} − {Цс0} = {v}."
    if форма == "счёт_со_скидкой":
        вопрос = р["вопрос_много"].replace("{Тk}", "{Тk}")
        return начало + " " + вопрос + " " + р["ответ_деньги"] + р["двоеточие"] + "{k} × {ц} = {v}."
    вопрос = (р["вопрос_сколько"].replace("{КСК}", _кс_k(язык, i)).replace("{МН}", мн))
    делитель = "{Ц0}" if форма == "сколько_за_сумму" else "{ц}"
    return начало + " " + вопрос + " " + р["ответ_счёт"] + р["двоеточие"] + "{всего} ÷ " + делитель + " = {v}."


def страница(язык, форма, i, цена, скидка, k=0):
    ц = цена - скидка
    поля = dict(Ц=_цена(язык, цена), Цс=_цена(язык, скидка), Ц0=цена, Цс0=скидка, ц=ц)
    if форма == "цена_со_скидкой":
        поля.update(v=ц, Цv=_цена(язык, ц))
    elif форма == "счёт_со_скидкой":
        поля.update(k=k, Тk=_вещь(язык, i, k), v=k * ц, Цv=_цена(язык, k * ц))
    elif форма == "сколько_за_сумму":
        поля.update(всего=цена * k, Цвсего=_цена(язык, цена * k), v=k, Тv=_вещь(язык, i, k))
    else:
        поля.update(всего=ц * k, Цвсего=_цена(язык, ц * k), v=k, Тv=_вещь(язык, i, k))
    return рамка(язык, форма, i).format(**поля)


def _показы():
    вон = {}
    for язык in ЯЗЫКИ:
        for q, (цена, скидка) in enumerate(ЦЕНЫ):
            i = q % 2
            вон[страница(язык, "цена_со_скидкой", i, цена, скидка)] = (язык, "цена_со_скидкой")
            for k in СЧЁТ:
                вон[страница(язык, "счёт_со_скидкой", i, цена, скидка, k)] = (язык, "счёт_со_скидкой")
                вон[страница(язык, "сколько_за_сумму", i, цена, скидка, k)] = (язык, "сколько_за_сумму")
                вон[страница(язык, "сколько_со_скидкой", i, цена, скидка, k)] = (язык, "сколько_со_скидкой")
    return вон


ПОКАЗЫ = _показы()


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted({с for с in слова if с}, key=lambda с: (-len(с), с))) + ")"


def _образец(язык, шаблон, i):
    знак, сторона = ЗНАК[язык]
    цена = (re.escape(знак) + r"\d+") if сторона == "до" else (r"\d+ " + re.escape(знак))
    вещи = _альт(ТОВАРЫ[язык][i].values())
    дыры = {"Ц": цена, "Цс": цена, "Цv": цена, "Цвсего": цена, "Ц0": r"\d+", "Цс0": r"\d+",
            "ц": r"\d+", "k": r"\d+", "v": r"\d+", "всего": r"\d+", "Тk": вещи, "Тv": вещи}
    счёт, куски = {}, []
    for кусок in re.split(r"(\{[^}]+\})", шаблон):
        if кусок.startswith("{"):
            дыра = кусок[1:-1]
            счёт[дыра] = счёт.get(дыра, 0) + 1
            куски.append(f"(?P<h_{дыра}__{счёт[дыра]}>{дыры[дыра]})")
        else:
            куски.append(re.escape(кусок))
    return re.compile("^" + "".join(куски) + "$")


ОБРАЗЦЫ = [(_образец(язык, рамка(язык, форма, i), i), язык, форма, i)
           for язык in ЯЗЫКИ for форма in ФОРМЫ for i in (0, 1)]


def _значения(м):
    вон = {}
    for ключ, знач in м.groupdict().items():
        дыра, _ = ключ[2:].rsplit("__", 1)
        if дыра in вон and вон[дыра] != знач:
            return None
        вон[дыра] = знач
    return вон


def _число(с):
    м = re.search(r"\d+", с)
    return int(м.group()) if м else None


def _вердикт(язык, форма, i, зн):
    # ЦЕНА ЧИТАЕТСЯ ОТТУДА, ГДЕ ОНА СТОИТ: в леджере голым числом, а в истории — со знаком
    цена = int(зн["Ц0"]) if "Ц0" in зн else _число(зн["Ц"])
    скидка = int(зн["Цс0"]) if "Цс0" in зн else _число(зн["Цс"])
    if цена is None or скидка is None:
        return False
    if скидка < 1 or цена <= скидка:
        return False
    ц = цена - скидка
    # ЦЕНА И СКИДКА В ИСТОРИИ ПИШУТСЯ СО ЗНАКОМ, А В ЛЕДЖЕРЕ ЧИСЛОМ — и это одно число
    if _число(зн["Ц"]) != цена or _число(зн["Цс"]) != скидка:
        return False
    if форма == "цена_со_скидкой":
        v = int(зн["v"])
        return v == ц and _число(зн["Цv"]) == v
    if форма == "счёт_со_скидкой":
        k, v = int(зн["k"]), int(зн["v"])
        if k < 1 or int(зн["ц"]) != ц or v != k * ц:
            return False
        return _число(зн["Цv"]) == v and зн["Тk"] == _вещь(язык, i, k)
    всего, v = int(зн["всего"]), int(зн["v"])
    if v < 1 or _число(зн["Цвсего"]) != всего or зн["Тv"] != _вещь(язык, i, v):
        return False
    # СКОЛЬКО ВОЙДЁТ В СУММУ: делится ПОЛНАЯ цена или цена СО СКИДКОЙ — по роду показа
    делитель = цена if форма == "сколько_за_сумму" else ц
    if форма == "сколько_со_скидкой" and int(зн["ц"]) != ц:
        return False
    return всего == делитель * v


def _судить_образцом(строка):
    """(судимо, истинно): a page of a frame of the house whose money recomputes; else silence."""
    с = строка.strip()
    # ВЫХОД ПО НАБОРУ СНЯТ (21.09) — он прикрывал 864 из 2808 страниц, которые закон
    # звал ложью, судя их мерой чужого случая (см. обход ниже). НАБОР ГОВОРИТ, ЧТО ДОМ
    # СТРАНИЦУ НАПИСАЛ, А НЕ ЧТО ОНА ВЕРНА. Замер: закон судит все 2808 верно.
    # СПРАШИВАЮТСЯ ВСЕ СОВПАВШИЕ ОБРАЗЦЫ, А НЕ ПЕРВЫЙ (21.09). Образцы дома различаются
    # не рамкой, а тем, что рамка прячет в дыры, — и всякая страница совпадает с доброй
    # горстью их сразу. Обход брал первый совпавший и судил страницу мерой ЧУЖОГО случая.
    #
    #     ОБРАЗЕЦ, СОВПАВШИЙ ПЕРВЫМ, НЕ ЕСТЬ ОБРАЗЕЦ ВЕРНЫЙ, КОГДА ОБРАЗЦЫ РАЗЛИЧАЮТСЯ НЕ
    #     РАМКОЙ, А ЕЁ ДЫРАМИ. Суд обязан спросить ВСЕХ совпавших и назвать страницу ложью
    #     лишь тогда, когда СВОЕЙ её не признал никто.
    #
    # Молчал этот порок ровно потому, что выход по набору стоял впереди закона.
    совпал = False
    for образ, язык, форма, i in ОБРАЗЦЫ:
        м = образ.match(с)
        if not м:
            continue
        совпал = True
        зн = _значения(м)
        if зн is None:
            continue
        if _вердикт(язык, форма, i, зн):
            return True, True
    return (True, False) if совпал else (False, False)


def подсадки():
    """ПРЕДСТАВЛЕННОЕ «НЕТ» (М-106), ВЫВЕДЕННОЕ ИЗ ПЕРВОЙ ПАРЫ СЕТКИ (23.09), — [(род, битая)].

    Суд мира держал подсадки литералами прежней сетки («each pack costs $76. the discount is $25»
    — это задача SVAMP chal-1), и перепись сцен и сетки оставила его без единой пойманной: 0 из 8.
    Литералы «= 51.» пережили бы и следующую смену, заменяя ничто на ничто, — порча берётся у
    страницы, которую дом пишет сейчас. Одна дверь на две проверки: самопроверка и суд мира."""
    ц0, с0 = ЦЕНЫ[0]
    п0, k0 = ц0 - с0, 5
    вон = []
    for язык in ЯЗЫКИ:
        # (1) СКИДКА НЕ ВЫЧТЕНА: платят полную цену
        ц = страница(язык, "цена_со_скидкой", 0, ц0, с0)
        вон.append(("скидка не вычтена", ц, ц.replace(f"= {п0}.", f"= {ц0}.")))
        # (2) СЧЁТ ВЗЯТ ПО ПОЛНОЙ ЦЕНЕ, А НЕ ПО ЦЕНЕ СО СКИДКОЙ
        с = страница(язык, "счёт_со_скидкой", 0, ц0, с0, k0)
        вон.append(("счёт по полной цене", с,
                    с.replace(f"{k0} × {п0} = {k0 * п0}", f"{k0} × {ц0} = {k0 * ц0}")
                     .replace(_цена(язык, k0 * п0), _цена(язык, k0 * ц0))))
        # (3) СКОЛЬКО ВОЙДЁТ В СУММУ: делено не на то
        д = страница(язык, "сколько_за_сумму", 0, ц0, с0, k0)
        вон.append(("сумма делена не на ту цену", д, д.replace(f"÷ {ц0} = {k0}", f"÷ {п0} = {k0}")))
        # (4) СУММА СО СКИДКОЙ ДЕЛЕНА НА ПОЛНУЮ ЦЕНУ
        дс = страница(язык, "сколько_со_скидкой", 0, ц0, с0, k0)
        вон.append(("сумма со скидкой делена на полную цену", дс, дс.replace(f"÷ {п0} = {k0}", f"÷ {ц0} = {k0}")))
        # (5) СУММА НЕ ДЕЛИТСЯ НА ЦЕНУ, А СЧЁТ НАЗВАН ЦЕЛЫМ
        вон.append(("сумма не делится", д, д.replace(str(ц0 * k0), str(ц0 * k0 + 1))))
    for род, было, битая in вон:
        assert битая != было, (род, было)
    return [(род, битая) for род, _, битая in вон]


def _самопроверка():
    for показ in ПОКАЗЫ:
        assert судить(показ) == (True, True), показ
    ц0, с0 = ЦЕНЫ[0]
    п0, k0 = ц0 - с0, 5
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            стр = страница(язык, форма, 0, ц0, с0, k0)
            assert судить(стр) == (True, True), стр
            # ЗАЧИН ВОПРОСА ОБЪЯВЛЕН ДОМОМ ПАРЫ
            вопрос = стр[:стр.index("?") + 1].split(". ")[-1]
            assert asking.зачин_объявлен(вопрос) is not False, (язык, вопрос)
    мутанты = 0
    for род, битая in подсадки():
        assert судить(битая) == (True, False), (род, битая)
        мутанты += 1
    ц1, с1 = ЦЕНЫ[1]
    for язык in ЯЗЫКИ:
        print("  ", страница(язык, "цена_со_скидкой", 0, ц0, с0))
    for язык in ("ru", "en", "de", "pl"):
        print("  ", страница(язык, "счёт_со_скидкой", 0, ц0, с0, k0))
        print("  ", страница(язык, "сколько_за_сумму", 1, ц1, с1, 4))
        print("  ", страница(язык, "сколько_со_скидкой", 1, ц1, с1, 4))
    по_форме = {}
    for _, (язык, форма) in ПОКАЗЫ.items():
        по_форме[форма] = по_форме.get(форма, 0) + 1
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)}, образцов {len(ОБРАЗЦЫ)}): "
          + ", ".join(f"{ф} {к}" for ф, к in по_форме.items()))




import closedworld as _зк  # noqa: E402 — закон замкнутого мира читается после сборки показов
_СКЕЛЕТЫ_ЗНАКА = _зк.скелеты_знака(ПОКАЗЫ)


def судить(строка):
    """(судимо, истинно) — с ЗАКОНОМ ЗНАКА поверх образца.

    ЗНАК ДЕЙСТВИЯ СУДИТСЯ ЗАКОНОМ ЗАМКНУТОГО МИРА, А НЕ ДЫРОЙ В КАЖДОЙ РАМКЕ: строка,
    становящаяся ИСТИННОЙ при замене одного знака, есть строка ЭТОГО дома с испорченным
    знаком (М-489). Прежде такая строка получала НЕМОТУ, и палата брала истину у суда
    арифметики — у соседа (М-131).
    """
    вердикт = _судить_образцом(строка)
    if вердикт[0] is False and _зк.ложь_по_знаку(
            строка, _СКЕЛЕТЫ_ЗНАКА, ПОКАЗЫ, _судить_образцом):
        return True, False
    return вердикт
if __name__ == "__main__":
    _самопроверка()
