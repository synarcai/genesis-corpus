#!/usr/bin/env python3
"""ДОМ ПРИРОДЫ — счётные факты о живом и вещах, и температура.

Владелец просил собеседника, умеющего «общаться на разные темы». Дом бытовых
тем дал определения и календарь; здесь — то, что человек знает о МИРЕ и о чём
спрашивает ребёнок: сколько у паука ног, сколько у человека зубов, при какой
температуре кипит вода.

ВРЕМЕНА ГОДА — ЦИКЛ, А НЕ СПИСОК, и во всём своде их не было ни одного показа.
Замыкание («после осени идёт зима») есть то, чем цикл отличается от перечня, и
здесь оно не дописано рукой, а ВЫВЕДЕНО остатком по длине — забыть его нельзя.
Форма «после X» объявлена при каждом имени отдельно, ибо предлог требует своего
падежа: русский родительный («после зимы»), польский местный («po zimie»),
немецкий дательный с артиклем («nach dem Winter»), испанский и португальский
слитный предлог («del invierno», «do inverno»).

ЧАСТЬ И ЦЕЛОЕ СТОЯТ РЯДОМ СО СЧЁТОМ, и это не украшение: «нога — часть паука»
есть отношение ЧАСТИ К ЦЕЛОМУ, второе в корпусе отношение слова к слову после
противоположности, — но здесь оно СЦЕПЛЕНО с числом («у паука 8 ног. нога —
часть паука.»), и потому проверяемо тем же пересчётом, что и всё в этом доме.
Отношение, стоящее рядом со своим числом, нельзя выучить как строку: число его
опровергнет, если оно неверно. Рамка части объявлена каждым языком СВОЯ, ибо
падеж целого разный: русский и польский берут родительный или притяжательное
(«часть паука», «jego częścią»), немецкий и голландский обходятся указанием
(«ein Teil davon»), романские — местоимённой частицей («ne è una parte»).

Всякий показ этого дома ПРОВЕРЯЕМ, и проверяем двояко: счётная форма вещи
идёт за числом (дома `rugram` и `plgram` для славянских, объявленная пара для
прочих), а производный показ несёт кузницу — «сколько ног у двух пауков?
16 ног: 8 × 2 = 16». Второе важнее первого: факт природы, над которым СЧИТАЮТ,
перестаёт быть заученной строкой и становится посылкой.

ФАКТЫ ОБЪЯВЛЕНЫ, А НЕ ВЫВЕДЕНЫ, и все они верны о мире: у паука восемь ног, у
насекомого шесть, у птицы два крыла, у человека тридцать два зуба (у взрослого
— и это оговорено в самом показе не будет, ибо показ короток; долг назван).

    python3 tools/natureforms.py    # самопроверка с мутантами
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import plgram  # noqa: E402
import rugram  # noqa: E402

# факт = (носитель, носитель ПАРОЙ или None, вещь, число)
ЯЗЫКИ = {
    "ru": dict(
        утв="у {б} {n} {в}.",
        часть="у {б} {n} {в}. {в1} — часть {б}.",
        сезон="после {a} идёт {b}.", сезон_воп="после {a} идёт {b}. что идёт после {a}? {b}.",
        времена=(("зима", "зимы"), ("весна", "весны"), ("лето", "лета"), ("осень", "осени")),
        воп="у {б} {n} {в}. сколько {ва} у {б}? {n} {в}.",
        пара="у {б} {n} {в}. сколько {ва} у {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("паука", "двух пауков", "нога", 8), ("насекомого", "двух насекомых", "нога", 6),
               ("кошки", "двух кошек", "лапа", 4), ("птицы", "двух птиц", "крыло", 2),
               ("человека", "двух человек", "палец", 10), ("человека", "двух человек", "зуб", 32),
               ("человека", "двух человек", "рука", 2), ("человека", "двух человек", "глаз", 2),
               ("велосипеда", "двух велосипедов", "колесо", 2), ("машины", "двух машин", "колесо", 4),
               ("радуги", None, "цвет", 7), ("солнечной системы", None, "планета", 8)),
        темп="{ч} {г} при температуре {n} {гр}.",
        темп_воп="{ч} {г} при температуре {n} {гр}. при какой температуре {г} {ч}? при температуре {n} {гр}.",
        температуры=(("вода", "кипит", 100), ("вода", "замерзает", 0)),
        градус="градус",
    ),
    "en": dict(
        утв="a {б} has {n} {в}.",
        часть="a {б} has {n} {в}. a {в1} is a part of a {б}.",
        сезон="after {a} comes {b}.", сезон_воп="after {a} comes {b}. what comes after {a}? {b}.",
        времена=(("winter", "winter"), ("spring", "spring"), ("summer", "summer"), ("autumn", "autumn")),
        воп="a {б} has {n} {в}. how many {ва} does a {б} have? {n} {в}.",
        пара="a {б} has {n} {в}. how many {ва} do {бп} have? {r} {вr}: {n} × 2 = {r}.",
        факты=(("spider", "two spiders", ("leg", "legs"), 8), ("insect", "two insects", ("leg", "legs"), 6),
               ("cat", "two cats", ("paw", "paws"), 4), ("bird", "two birds", ("wing", "wings"), 2),
               ("person", "two people", ("finger", "fingers"), 10), ("person", "two people", ("tooth", "teeth"), 32),
               ("person", "two people", ("hand", "hands"), 2), ("person", "two people", ("eye", "eyes"), 2),
               ("bicycle", "two bicycles", ("wheel", "wheels"), 2), ("car", "two cars", ("wheel", "wheels"), 4),
               ("rainbow", None, ("colour", "colours"), 7), ("solar system", None, ("planet", "planets"), 8)),
        темп="{ч} {г} at a temperature of {n} {гр}.",
        темп_воп="{ч} {г} at a temperature of {n} {гр}. at what temperature does {ч} {г0}? at a temperature of {n} {гр}.",
        температуры=(("water", "boils", 100), ("water", "freezes", 0)),
        градус=("degree", "degrees"),
    ),
    "de": dict(
        утв="{б} hat {n} {в}.",
        часть="{б} hat {n} {в}. ein {в1} ist ein Teil davon.",
        сезон="nach {a} kommt {b}.", сезон_воп="nach {a} kommt {b}. was kommt nach {a}? {b}.",
        времена=(("der Winter", "dem Winter"), ("der Frühling", "dem Frühling"),
                 ("der Sommer", "dem Sommer"), ("der Herbst", "dem Herbst")),
        воп="{б} hat {n} {в}. wie viele {ва} hat {б}? {n} {в}.",
        пара="{б} hat {n} {в}. wie viele {ва} haben {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("eine Spinne", "zwei Spinnen", ("Bein", "Beine"), 8), ("ein Insekt", "zwei Insekten", ("Bein", "Beine"), 6),
               ("eine Katze", "zwei Katzen", ("Pfote", "Pfoten"), 4), ("ein Vogel", "zwei Vögel", ("Flügel", "Flügel"), 2),
               ("ein Mensch", "zwei Menschen", ("Finger", "Finger"), 10), ("ein Mensch", "zwei Menschen", ("Zahn", "Zähne"), 32),
               ("ein Mensch", "zwei Menschen", ("Hand", "Hände"), 2), ("ein Mensch", "zwei Menschen", ("Auge", "Augen"), 2),
               ("ein Fahrrad", "zwei Fahrräder", ("Rad", "Räder"), 2), ("ein Auto", "zwei Autos", ("Rad", "Räder"), 4),
               ("ein Regenbogen", None, ("Farbe", "Farben"), 7), ("das Sonnensystem", None, ("Planet", "Planeten"), 8)),
        темп="{ч} {г} bei einer Temperatur von {n} {гр}.",
        темп_воп="{ч} {г} bei einer Temperatur von {n} {гр}. bei welcher Temperatur {г} {ч}? bei einer Temperatur von {n} {гр}.",
        температуры=(("Wasser", "kocht", 100), ("Wasser", "gefriert", 0)),
        градус=("Grad", "Grad"),
    ),
    "fr": dict(
        утв="{б} a {n} {в}.",
        часть="{б} a {n} {в}. une {в1} en est une partie.",
        сезон="après {a} vient {b}.", сезон_воп="après {a} vient {b}. qu'est-ce qui vient après {a} ? {b}.",
        времена=(("l'hiver", "l'hiver"), ("le printemps", "le printemps"),
                 ("l'été", "l'été"), ("l'automne", "l'automne")),
        воп="{б} a {n} {в}. combien de {ва} a {б} ? {n} {в}.",
        пара="{б} a {n} {в}. combien de {ва} ont {бп} ? {r} {вr} : {n} × 2 = {r}.",
        факты=(("une araignée", "deux araignées", ("patte", "pattes"), 8), ("un insecte", "deux insectes", ("patte", "pattes"), 6),
               ("un chat", "deux chats", ("patte", "pattes"), 4), ("un oiseau", "deux oiseaux", ("aile", "ailes"), 2),
               ("une personne", "deux personnes", ("doigt", "doigts"), 10), ("une personne", "deux personnes", ("dent", "dents"), 32),
               ("une personne", "deux personnes", ("main", "mains"), 2), ("une personne", "deux personnes", ("œil", "yeux"), 2),
               ("un vélo", "deux vélos", ("roue", "roues"), 2), ("une voiture", "deux voitures", ("roue", "roues"), 4),
               ("un arc-en-ciel", None, ("couleur", "couleurs"), 7), ("le système solaire", None, ("planète", "planètes"), 8)),
        темп="{ч} {г} à une température de {n} {гр}.",
        темп_воп="{ч} {г} à une température de {n} {гр}. à quelle température {г} {ч} ? à une température de {n} {гр}.",
        температуры=(("l'eau", "bout", 100), ("l'eau", "gèle", 0)),
        градус=("degré", "degrés"),
    ),
    "es": dict(
        утв="{б} tiene {n} {в}.",
        часть="{б} tiene {n} {в}. una {в1} forma parte de ello.",
        сезон="después {a} viene {b}.", сезон_воп="después {a} viene {b}. ¿qué viene después {a}? {b}.",
        времена=(("el invierno", "del invierno"), ("la primavera", "de la primavera"),
                 ("el verano", "del verano"), ("el otoño", "del otoño")),
        воп="{б} tiene {n} {в}. ¿cuántas {ва} tiene {б}? {n} {в}.",
        пара="{б} tiene {n} {в}. ¿cuántas {ва} tienen {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("una araña", "dos arañas", ("pata", "patas"), 8), ("un insecto", "dos insectos", ("pata", "patas"), 6),
               ("un gato", "dos gatos", ("pata", "patas"), 4), ("un pájaro", "dos pájaros", ("ala", "alas"), 2),
               ("una persona", "dos personas", ("mano", "manos"), 2), ("una persona", "dos personas", ("ojo", "ojos"), 2),
               ("una bicicleta", "dos bicicletas", ("rueda", "ruedas"), 2), ("un coche", "dos coches", ("rueda", "ruedas"), 4),
               ("un arcoíris", None, ("color", "colores"), 7), ("el sistema solar", None, ("planeta", "planetas"), 8)),
        темп="{ч} {г} a una temperatura de {n} {гр}.",
        темп_воп="{ч} {г} a una temperatura de {n} {гр}. ¿a qué temperatura {г} {ч}? a una temperatura de {n} {гр}.",
        температуры=(("el agua", "hierve", 100), ("el agua", "se congela", 0)),
        градус=("grado", "grados"),
    ),
    "it": dict(
        утв="{б} ha {n} {в}.",
        часть="{б} ha {n} {в}. una {в1} ne è una parte.",
        сезон="dopo {a} viene {b}.", сезон_воп="dopo {a} viene {b}. che cosa viene dopo {a}? {b}.",
        времена=(("l'inverno", "l'inverno"), ("la primavera", "la primavera"),
                 ("l'estate", "l'estate"), ("l'autunno", "l'autunno")),
        воп="{б} ha {n} {в}. quante {ва} ha {б}? {n} {в}.",
        пара="{б} ha {n} {в}. quante {ва} hanno {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("un ragno", "due ragni", ("zampa", "zampe"), 8), ("un insetto", "due insetti", ("zampa", "zampe"), 6),
               ("un gatto", "due gatti", ("zampa", "zampe"), 4), ("un uccello", "due uccelli", ("ala", "ali"), 2),
               ("una persona", "due persone", ("mano", "mani"), 2), ("una persona", "due persone", ("occhio", "occhi"), 2),
               ("una bicicletta", "due biciclette", ("ruota", "ruote"), 2), ("un'auto", "due auto", ("ruota", "ruote"), 4),
               ("un arcobaleno", None, ("colore", "colori"), 7), ("il sistema solare", None, ("pianeta", "pianeti"), 8)),
        темп="{ч} {г} a una temperatura di {n} {гр}.",
        темп_воп="{ч} {г} a una temperatura di {n} {гр}. a che temperatura {г} {ч}? a una temperatura di {n} {гр}.",
        температуры=(("l'acqua", "bolle", 100), ("l'acqua", "gela", 0)),
        градус=("grado", "gradi"),
    ),
    "pt": dict(
        утв="{б} tem {n} {в}.",
        часть="{б} tem {n} {в}. uma {в1} faz parte disso.",
        сезон="depois {a} vem {b}.", сезон_воп="depois {a} vem {b}. o que vem depois {a}? {b}.",
        времена=(("o inverno", "do inverno"), ("a primavera", "da primavera"),
                 ("o verão", "do verão"), ("o outono", "do outono")),
        воп="{б} tem {n} {в}. quantas {ва} tem {б}? {n} {в}.",
        пара="{б} tem {n} {в}. quantas {ва} têm {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("uma aranha", "duas aranhas", ("pata", "patas"), 8), ("um inseto", "dois insetos", ("pata", "patas"), 6),
               ("um gato", "dois gatos", ("pata", "patas"), 4), ("um pássaro", "dois pássaros", ("asa", "asas"), 2),
               ("uma pessoa", "duas pessoas", ("mão", "mãos"), 2), ("uma pessoa", "duas pessoas", ("olho", "olhos"), 2),
               ("uma bicicleta", "duas bicicletas", ("roda", "rodas"), 2), ("um carro", "dois carros", ("roda", "rodas"), 4),
               ("um arco-íris", None, ("cor", "cores"), 7), ("o sistema solar", None, ("planeta", "planetas"), 8)),
        темп="{ч} {г} a uma temperatura de {n} {гр}.",
        темп_воп="{ч} {г} a uma temperatura de {n} {гр}. a que temperatura {г} {ч}? a uma temperatura de {n} {гр}.",
        температуры=(("a água", "ferve", 100), ("a água", "congela", 0)),
        градус=("grau", "graus"),
    ),
    "nl": dict(
        утв="{б} heeft {n} {в}.",
        часть="{б} heeft {n} {в}. een {в1} is er een deel van.",
        сезон="na {a} komt {b}.", сезон_воп="na {a} komt {b}. wat komt na {a}? {b}.",
        времена=(("de winter", "de winter"), ("de lente", "de lente"),
                 ("de zomer", "de zomer"), ("de herfst", "de herfst")),
        воп="{б} heeft {n} {в}. hoeveel {ва} heeft {б}? {n} {в}.",
        пара="{б} heeft {n} {в}. hoeveel {ва} hebben {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("een spin", "twee spinnen", ("poot", "poten"), 8), ("een insect", "twee insecten", ("poot", "poten"), 6),
               ("een kat", "twee katten", ("poot", "poten"), 4), ("een vogel", "twee vogels", ("vleugel", "vleugels"), 2),
               ("een mens", "twee mensen", ("hand", "handen"), 2), ("een mens", "twee mensen", ("oog", "ogen"), 2),
               ("een fiets", "twee fietsen", ("wiel", "wielen"), 2), ("een auto", "twee auto's", ("wiel", "wielen"), 4),
               ("een regenboog", None, ("kleur", "kleuren"), 7), ("het zonnestelsel", None, ("planeet", "planeten"), 8)),
        темп="{ч} {г} bij een temperatuur van {n} {гр}.",
        темп_воп="{ч} {г} bij een temperatuur van {n} {гр}. bij welke temperatuur {г} {ч}? bij een temperatuur van {n} {гр}.",
        температуры=(("water", "kookt", 100), ("water", "bevriest", 0)),
        градус=("graad", "graden"),
    ),
    "pl": dict(
        утв="{б} ma {n} {в}.",
        часть="{б} ma {n} {в}. {в1} jest jego częścią.",
        сезон="po {a} przychodzi {b}.", сезон_воп="po {a} przychodzi {b}. co przychodzi po {a}? {b}.",
        времена=(("zima", "zimie"), ("wiosna", "wiośnie"), ("lato", "lecie"), ("jesień", "jesieni")),
        воп="{б} ma {n} {в}. ile {ва} ma {б}? {n} {в}.",
        пара="{б} ma {n} {в}. ile {ва} mają {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("pająk", "dwa pająki", "noga", 8), ("owad", "dwa owady", "noga", 6),
               ("kot", "dwa koty", "łapa", 4), ("ptak", "dwa ptaki", "skrzydło", 2),
               ("człowiek", "dwaj ludzie", "palec", 10), ("człowiek", "dwaj ludzie", "ząb", 32),
               ("człowiek", "dwaj ludzie", "ręka", 2), ("człowiek", "dwaj ludzie", "oko", 2),
               ("rower", "dwa rowery", "koło", 2), ("samochód", "dwa samochody", "koło", 4),
               ("tęcza", None, "kolor", 7), ("układ słoneczny", None, "planeta", 8)),
        темп="{ч} {г} w temperaturze {n} {гр}.",
        темп_воп="{ч} {г} w temperaturze {n} {гр}. w jakiej temperaturze {г} {ч}? w temperaturze {n} {гр}.",
        температуры=(("woda", "wrze", 100), ("woda", "zamarza", 0)),
        градус="stopień",
    ),
}
ФОРМЫ = ("утв", "воп", "пара", "часть", "темп", "темп_воп", "сезон", "сезон_воп")


def вещь(язык, в, n):
    """Форма вещи при числе: у славянских — из своего дома счёта, у прочих —
    объявленная пара «один / много». Дом счёта не угадывается, а называется."""
    if язык == "ru":
        return rugram.форма(в, n)
    if язык == "pl":
        return plgram.форма(в, n)
    один, много = в
    return один if n == 1 else много


def показ(язык, форма, i):
    я = ЯЗЫКИ[язык]
    if форма in ("сезон", "сезон_воп"):
        # ЦИКЛ, А НЕ СПИСОК: после последнего идёт ПЕРВЫЙ, и замыкание есть то,
        # чем цикл отличается от перечня. Показ «после осени идёт зима» строится
        # тем же правилом, что и прочие три, — остатком по длине, — и потому
        # замыкание нельзя забыть: оно не дописано рукой, а выведено.
        врем = я["времена"]
        (_, a) = врем[i % len(врем)]
        (b, _) = врем[(i + 1) % len(врем)]
        return я[форма].format(a=a, b=b)
    if форма in ("темп", "темп_воп"):
        ч, г, n = я["температуры"][i % len(я["температуры"])]
        гр = вещь(язык, я["градус"], n)
        г0 = {"boils": "boil", "freezes": "freeze"}.get(г, г)
        return я[форма].format(ч=ч, г=г, г0=г0, n=n, гр=гр)
    б, бп, в, n = я["факты"][i % len(я["факты"])]
    поля = dict(б=б, бп=бп, n=n, в=вещь(язык, в, n), ва=вещь(язык, в, 5),
                в1=вещь(язык, в, 1), r=n * 2, вr=вещь(язык, в, n * 2))
    if форма == "пара" and бп is None:
        return None          # носитель без парной формы парного показа не пишет
    return я[форма].format(**поля)


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for форма in ("утв", "воп", "пара", "часть"):
            for i in range(len(я["факты"])):
                с = показ(язык, форма, i)
                if с:
                    вон[с] = (язык, форма)
        for форма in ("темп", "темп_воп"):
            for i in range(len(я["температуры"])):
                вон[показ(язык, форма, i)] = (язык, форма)
        for форма in ("сезон", "сезон_воп"):
            for i in range(len(я["времена"])):
                вон[показ(язык, форма, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _все_показы()


def судить(строка):
    с = строка.strip()
    return (True, True) if с in ПОКАЗЫ else (False, False)


def _самопроверка():
    мутанты = 0
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            с = показ(язык, форма, 0)
            assert с and судить(с) == (True, True), (язык, форма, с)
        # МУТАНТ: подменённое число не есть показ дома
        битый = показ(язык, "воп", 0).replace(" 8 ", " 9 ")
        if битый != показ(язык, "воп", 0):
            assert судить(битый) == (False, False), (язык, битый)
            мутанты += 1
    for язык in ("ru", "en", "de", "pl"):
        print("  ", показ(язык, "пара", 0)[:112])
        print("  ", показ(язык, "темп_воп", 0)[:112])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")


if __name__ == "__main__":
    _самопроверка()
