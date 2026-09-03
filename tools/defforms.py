#!/usr/bin/env python3
"""THE HOUSE OF DEFINITIONS — a thing named by its GENUS and its DIFFERENCE.

The measure of the shelf (03.09) named «связка без числа» — a copula without a
number — as fourteen per cent of the sentences of books, and holon named both
the form and its shape: the definition must stand in ONE line, as in the world
of inquiry, «утверждение. вопрос? ответ.» — the market of the copula buys the
FACT from the statement, and the form of the ANSWER is bought only from a
question→answer show standing in the SAME line.

So every show of this house is one line with three parts:

    a pen is a tool that writes. what is a pen? a tool that writes.
    a pen is a tool that writes. is a pen a tool or an animal? a tool.
    a pen is a tool that writes. what does a pen do? a pen writes.
    a pen is a tool that writes. which tool writes? a pen.

One fact, four questions, and the four answers cover every role of the fact:
the whole predicate (genus with difference), the GENUS alone, the DIFFERENCE
alone, and the NAME alone — the last is the inversion, and it is the surface
the market of inversion buys, for the question names the difference and the
answer names the thing.

THE LEXICON IS DECLARED, NOT DERIVED. Every thing, every genus, every
difference and every tying word of every language stands in the table below;
nothing is guessed from another language.

TWO LAWS OF THE TABLE, both born of agreement and both kept by declaration:
  * the relative word ties the difference to the GENUS, so it agrees with the
    genus and is declared beside it («который» / «которое» / «которая», «das»
    / «die»); the same holds for the word of the inversion question;
  * a THING is singular, and its difference is one verb form which stands both
    after the genus and after the name («часы показывают» would need two forms
    and is therefore not declared — «будильник показывает» is).
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

ЯЗЫКИ = {
    "en": dict(
        определения=(
            ("a pen", "a tool", "writes"), ("a knife", "a tool", "cuts"),
            ("a hammer", "a tool", "strikes"), ("a spoon", "a tool", "scoops"),
            ("a bird", "an animal", "flies"), ("a fish", "an animal", "swims"),
            ("a horse", "an animal", "runs"), ("a bee", "an animal", "gathers honey"),
            ("a rose", "a plant", "blooms"), ("an oak", "a plant", "grows tall"),
            ("a cup", "a vessel", "holds water"), ("a bottle", "a vessel", "holds milk"),
            ("a chair", "a piece of furniture", "seats one person"),
            ("a table", "a piece of furniture", "holds plates"),
            ("an alarm clock", "a device", "shows the time"), ("a lamp", "a device", "gives light"),
            ("a car", "a vehicle", "carries people"), ("a boat", "a vehicle", "crosses water"),
            ("a bicycle", "a vehicle", "rolls on two wheels"),
            ("a school", "a building", "teaches children"), ("a bakery", "a building", "bakes bread"),
            ("a coat", "a garment", "keeps a person warm"), ("a hat", "a garment", "covers the head"),
            # НАУЧНЫЙ РЕГИСТР (04.09): подлежащее прозы почти всегда длиннее
            # одного слова («a prime number», «the human heart»), а род её —
            # научный. Дом, знавший только «a pen is a tool», учил бы рынок
            # определений видеть лишь короткие имена бытовых вещей.
            ("the human heart", "an organ", "pumps blood"),
            ("the lung", "an organ", "takes in air"),
            ("liquid water", "a substance", "freezes at zero"),
            ("pure iron", "a metal", "rusts in air"),
            ("a right triangle", "a figure", "has one right angle"),
            ("a prime number", "a number", "has exactly two divisors"),
            ("an even number", "a number", "divides by two"),
            ("gravity", "a force", "pulls bodies together"),
            ("a verb", "a word", "names an action"),
            ("a green plant", "an organism", "makes its own food"),
        ),
        хвост="{Р} {С} {О}",
        утв="{В} is {Хвост}.",
        имя="what is {В}? {Хвост}.",
        род="is {В} {Р} or {Р2}? {Р}.", род_справа="is {В} {Р2} or {Р}? {Р}.",
        род_один="is {В} {Р} or {Р2}? {Р}.", род_один_справа="is {В} {Р2} or {Р}? {Р}.",
        отличие="what does {В} do? {В} {О}.",
        обращение="{К} {Рб} {О}? {В}.",
        безартикля={"a tool": "tool", "an animal": "animal", "a plant": "plant",
                    "a vessel": "vessel", "a piece of furniture": "piece of furniture",
                    "a device": "device", "a vehicle": "vehicle", "a building": "building",
                    "a garment": "garment", "an organ": "organ", "a substance": "substance",
                    "a metal": "metal", "a figure": "figure", "a number": "number",
                    "a force": "force", "a word": "word", "an organism": "organism"},
        связки={"a tool": "that", "an animal": "that", "a plant": "that", "a vessel": "that",
                "a piece of furniture": "that", "a device": "that", "a vehicle": "that",
                "a building": "that", "a garment": "that", "an organ": "that",
                "a substance": "that", "a metal": "that", "a figure": "that",
                "a number": "that", "a force": "that", "a word": "that",
                "an organism": "that"},
        какой={"a tool": "which", "an animal": "which", "a plant": "which", "a vessel": "which",
               "a piece of furniture": "which", "a device": "which", "a vehicle": "which",
               "a building": "which", "a garment": "which", "an organ": "which",
               "a substance": "which", "a metal": "which", "a figure": "which",
               "a number": "which", "a force": "which", "a word": "which",
               "an organism": "which"},
    ),
    "ru": dict(
        определения=(
            ("ручка", "инструмент", "пишет"), ("нож", "инструмент", "режет"),
            ("молоток", "инструмент", "бьёт"), ("ложка", "инструмент", "черпает"),
            ("птица", "животное", "летает"), ("рыба", "животное", "плавает"),
            ("лошадь", "животное", "бегает"), ("пчела", "животное", "собирает мёд"),
            ("роза", "растение", "цветёт"), ("дуб", "растение", "растёт высоким"),
            ("чашка", "сосуд", "держит воду"), ("бутылка", "сосуд", "держит молоко"),
            ("стул", "мебель", "вмещает одного человека"), ("стол", "мебель", "держит тарелки"),
            ("будильник", "прибор", "показывает время"), ("лампа", "прибор", "даёт свет"),
            ("автомобиль", "транспорт", "везёт людей"), ("лодка", "транспорт", "плывёт по воде"),
            ("велосипед", "транспорт", "катится на двух колёсах"),
            ("школа", "здание", "учит детей"), ("пекарня", "здание", "печёт хлеб"),
            ("пальто", "одежда", "греет человека"), ("шапка", "одежда", "покрывает голову"),
            ("сердце человека", "орган", "качает кровь"),
            ("лёгкое", "орган", "принимает воздух"),
            ("жидкая вода", "вещество", "замерзает при нуле"),
            ("чистое железо", "металл", "ржавеет на воздухе"),
            ("прямоугольный треугольник", "фигура", "имеет прямой угол"),
            ("простое число", "число", "имеет ровно два делителя"),
            ("чётное число", "число", "делится на два"),
            ("тяготение", "сила", "притягивает тела"),
            ("глагол", "слово", "называет действие"),
            ("зелёное растение", "организм", "готовит себе пищу"),
        ),
        хвост="{Р}, {С} {О}",
        утв="{В} — это {Хвост}.",
        имя="что такое {В}? {Хвост}.",
        род="{В} — это {Р} или {Р2}? {Р}.", род_справа="{В} — это {Р2} или {Р}? {Р}.",
        род_один="{В} — это {Р} или {Р2}? {Р}.", род_один_справа="{В} — это {Р2} или {Р}? {Р}.",
        отличие="что делает {В}? {В} {О}.",
        обращение="{К} {Рб} {О}? {В}.",
        связки={"инструмент": "который", "животное": "которое", "растение": "которое",
                "сосуд": "который", "мебель": "которая", "прибор": "который",
                "транспорт": "который", "здание": "которое", "одежда": "которая",
                "орган": "который", "вещество": "которое", "металл": "который",
                "фигура": "которая", "число": "которое", "сила": "которая",
                "слово": "которое", "организм": "который"},
        какой={"инструмент": "какой", "животное": "какое", "растение": "какое",
               "сосуд": "какой", "мебель": "какая", "прибор": "какой",
               "транспорт": "какой", "здание": "какое", "одежда": "какая",
               "орган": "какой", "вещество": "какое", "металл": "какой",
               "фигура": "какая", "число": "какое", "сила": "какая",
               "слово": "какое", "организм": "какой"},
    ),
    "de": dict(
        определения=(
            ("ein Stift", "ein Werkzeug", "schreibt"), ("ein Messer", "ein Werkzeug", "schneidet"),
            ("ein Hammer", "ein Werkzeug", "schlägt"), ("ein Löffel", "ein Werkzeug", "schöpft"),
            ("ein Vogel", "ein Tier", "fliegt"), ("ein Fisch", "ein Tier", "schwimmt"),
            ("ein Pferd", "ein Tier", "läuft"), ("eine Biene", "ein Tier", "sammelt Honig"),
            ("eine Rose", "eine Pflanze", "blüht"), ("eine Eiche", "eine Pflanze", "wächst hoch"),
            ("eine Tasse", "ein Gefäß", "hält Wasser"), ("eine Flasche", "ein Gefäß", "hält Milch"),
            ("ein Stuhl", "ein Möbelstück", "trägt einen Menschen"),
            ("ein Tisch", "ein Möbelstück", "trägt Teller"),
            ("ein Wecker", "ein Gerät", "zeigt die Zeit"), ("eine Lampe", "ein Gerät", "gibt Licht"),
            ("ein Auto", "ein Fahrzeug", "fährt Menschen"), ("ein Boot", "ein Fahrzeug", "fährt über Wasser"),
            ("ein Fahrrad", "ein Fahrzeug", "rollt auf zwei Rädern"),
            ("eine Schule", "ein Gebäude", "lehrt Kinder"), ("eine Bäckerei", "ein Gebäude", "backt Brot"),
            ("ein Mantel", "eine Kleidung", "wärmt einen Menschen"),
            ("eine Mütze", "eine Kleidung", "bedeckt den Kopf"),
            ("das menschliche Herz", "ein Organ", "pumpt Blut"),
            ("die Lunge", "ein Organ", "nimmt Luft auf"),
            ("flüssiges Wasser", "ein Stoff", "gefriert bei null"),
            ("reines Eisen", "ein Metall", "rostet an der Luft"),
            ("ein rechtwinkliges Dreieck", "eine Figur", "hat einen rechten Winkel"),
            ("eine Primzahl", "eine Zahl", "hat genau zwei Teiler"),
            ("eine gerade Zahl", "eine Zahl", "teilt sich durch zwei"),
            ("die Schwerkraft", "eine Kraft", "zieht Körper zusammen"),
            ("ein Verb", "ein Wort", "nennt eine Handlung"),
            ("eine grüne Pflanze", "ein Organismus", "macht sich selbst Nahrung"),
        ),
        хвост="{Р}, {С} {О}",
        утв="{В} ist {Хвост}.",
        имя="was ist {В}? {Хвост}.",
        род="ist {В} {Р} oder {Р2}? {Р}.", род_справа="ist {В} {Р2} oder {Р}? {Р}.",
        род_один="ist {В} {Р} oder {Р2}? {Р}.", род_один_справа="ist {В} {Р2} oder {Р}? {Р}.",
        отличие="was macht {В}? {В} {О}.",
        обращение="{К} {Рб} {О}? {В}.",
        безартикля={"ein Werkzeug": "Werkzeug", "ein Tier": "Tier", "eine Pflanze": "Pflanze",
                    "ein Gefäß": "Gefäß", "ein Möbelstück": "Möbelstück", "ein Gerät": "Gerät",
                    "ein Fahrzeug": "Fahrzeug", "ein Gebäude": "Gebäude", "eine Kleidung": "Kleidung",
                    "ein Organ": "Organ", "ein Stoff": "Stoff", "ein Metall": "Metall",
                    "eine Figur": "Figur", "eine Zahl": "Zahl", "eine Kraft": "Kraft",
                    "ein Wort": "Wort", "ein Organismus": "Organismus"},
        связки={"ein Werkzeug": "das", "ein Tier": "das", "eine Pflanze": "die", "ein Gefäß": "das",
                "ein Möbelstück": "das", "ein Gerät": "das", "ein Fahrzeug": "das",
                "ein Gebäude": "das", "eine Kleidung": "die", "ein Organ": "das",
                "ein Stoff": "der", "ein Metall": "das", "eine Figur": "die",
                "eine Zahl": "die", "eine Kraft": "die", "ein Wort": "das",
                "ein Organismus": "der"},
        какой={"ein Werkzeug": "welches", "ein Tier": "welches", "eine Pflanze": "welche",
               "ein Gefäß": "welches", "ein Möbelstück": "welches", "ein Gerät": "welches",
               "ein Fahrzeug": "welches", "ein Gebäude": "welches", "eine Kleidung": "welche",
               "ein Organ": "welches", "ein Stoff": "welcher", "ein Metall": "welches",
               "eine Figur": "welche", "eine Zahl": "welche", "eine Kraft": "welche",
               "ein Wort": "welches", "ein Organismus": "welcher"},
    ),
}
# ВЫБОР ЧИТАЕТСЯ ОБЕИМИ СТОРОНАМИ (holon 03.09, строка 223 атаки): если
# верный род всегда стоит ПЕРВЫМ, рынок покупает не выбор, а ПОЗИЦИЮ, и
# «is a bottle an animal or a vessel?» останется немым. Половина показов
# ставит верный род справа от слова выбора.
#
# И ВОПРОС ВЫБОРА ЖИВЁТ ОТДЕЛЬНО ОТ ФАКТА: атака спрашивает его голым («is a
# bottle a vessel or an animal? a vessel.»), а мир говорил его лишь хвостом
# при утверждении; факт того же предмета стоит в мире рядом, в других показах.
ФОРМЫ = ("имя", "род", "род_справа", "отличие", "обращение",
         "род_один", "род_один_справа")
ГОЛЫЕ = ("род_один", "род_один_справа")


def роды(язык):
    """The declared genera in the order of their first thing."""
    вон = []
    for _, р, _ in ЯЗЫКИ[язык]["определения"]:
        if р not in вон:
            вон.append(р)
    return вон


def _безартикля(язык, род_):
    return (ЯЗЫКИ[язык].get("безартикля") or {}).get(род_, род_)


def _другой_род(язык, род_, сдвиг):
    """The genus of the choice question — declared, never the thing's own."""
    все = роды(язык)
    i = все.index(род_)
    return все[(i + 1 + сдвиг % (len(все) - 1)) % len(все)]


def хвост(язык, i):
    """«a tool that writes» — the whole predicate of the definition."""
    я = ЯЗЫКИ[язык]
    _, Р, О = я["определения"][i]
    return я["хвост"].format(Р=Р, С=я["связки"][Р], О=О)


def утверждение(язык, i):
    В = ЯЗЫКИ[язык]["определения"][i][0]
    return ЯЗЫКИ[язык]["утв"].format(В=В, Хвост=хвост(язык, i))


def вопрос_ответ(язык, форма, i, сдвиг=0):
    """The question and its answer — the pair that buys the form of an answer."""
    я = ЯЗЫКИ[язык]
    В, Р, О = я["определения"][i]
    if форма == "имя":
        return я["имя"].format(В=В, Хвост=хвост(язык, i))
    if форма.startswith("род"):
        return я[форма].format(В=В, Р=Р, Р2=_другой_род(язык, Р, сдвиг))
    if форма == "отличие":
        return я["отличие"].format(В=В, О=О)
    if форма == "обращение":
        return я["обращение"].format(К=я["какой"][Р], Рб=_безартикля(язык, Р), О=О, В=В)
    raise KeyError(форма)


def показ(язык, форма, i, сдвиг=0):
    """ONE LINE: statement, question, answer — holon's shape (03.09).

    Голый вопрос выбора (ГОЛЫЕ) идёт БЕЗ утверждения: так его спрашивает
    атака, и так его встретит организм в чужой речи.
    """
    вопрос = вопрос_ответ(язык, форма, i, сдвиг)
    if форма in ГОЛЫЕ:
        return вопрос
    return f"{утверждение(язык, i)} {вопрос}"


# --- the court's side: the same table read back ---
def _все(язык):
    """{строка: (форма, индекс)} — every line this house can write."""
    вон = {}
    всего_родов = len(роды(язык))
    for i in range(len(ЯЗЫКИ[язык]["определения"])):
        for форма in ФОРМЫ:
            for сдвиг in range(всего_родов):
                вон[показ(язык, форма, i, сдвиг)] = (форма, i)
    return вон


ВСЕ = {язык: _все(язык) for язык in ЯЗЫКИ}


def _альт(слова):
    return "(?:" + "|".join(re.escape(с) for с in sorted(set(слова), key=len, reverse=True)) + ")"


def _образцы(язык):
    """The shapes of the house: a line of this shape that the table does not
    hold is a LIE — a wrong genus, a difference borrowed from another thing, a
    relative word that does not agree, an answer that is not the fact's part."""
    я = ЯЗЫКИ[язык]
    И = _альт(в for в, _, _ in я["определения"])
    Р = _альт(list(роды(язык)) + [_безартикля(язык, р) for р in роды(язык)])
    О = _альт(о for _, _, о in я["определения"])
    С = _альт(я["связки"].values())
    К = _альт(я["какой"].values())
    хв = rf"{Р},? {С} {О}"
    утв = rf"{И} (?:is|ist|— это) {хв}\."
    воп = [
        rf"(?:what is|was ist|что такое) {И}\? {хв}\.",
        rf"(?:is|ist) {И} {Р} (?:or|oder) {Р}\? {Р}\.|{И} — это {Р} или {Р}\? {Р}\.",
        rf"(?:what does {И} do|was macht {И}|что делает {И})\? {И} {О}\.",
        rf"{К} {Р} {О}\? {И}\.",
    ]
    return [re.compile(rf"^{утв} (?:{в})$") for в in воп]


ОБРАЗЦЫ = {язык: _образцы(язык) for язык in ЯЗЫКИ}


def судить(строка):
    """(судимо, истинно): a line of the house's shape is judged by the TABLE —
    it is exactly what the house writes, or it is a lie."""
    с = строка.strip()
    for таблица in ВСЕ.values():
        if с in таблица:
            return True, True
    for образцы in ОБРАЗЦЫ.values():
        if any(о.match(с) for о in образцы):
            return True, False
    return False, False


def _проверка():
    """The house checks itself: every show is true, every mutant is a lie."""
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            строка = показ(язык, форма, 0, 0)
            судимо, истинно = судить(строка)
            assert судимо and истинно, (язык, форма, строка)
            print(f"  {язык} {форма}: {строка}")
    # mutants: a borrowed difference, a wrong genus, a wrong relative word
    мутанты = [
        "a pen is a tool that cuts. what is a pen? a tool that cuts.",
        "a pen is an animal that writes. what is a pen? an animal that writes.",
        "ручка — это инструмент, которое пишет. что такое ручка? инструмент, которое пишет.",
        "ручка — это инструмент, который пишет. ручка — это инструмент или инструмент? инструмент.",
        "ручка — это инструмент, который пишет. какой инструмент пишет? нож.",
        "ein Stift ist ein Werkzeug, das schreibt. was macht ein Stift? ein Messer schreibt.",
    ]
    for м in мутанты:
        судимо, истинно = судить(м)
        assert судимо and not истинно, ("мутант не пойман", м)
    print(f"  мутантов поймано: {len(мутанты)}")
    всего = sum(len(т) for т in ВСЕ.values())
    print(f"  дом пишет строк: {всего} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _проверка()
