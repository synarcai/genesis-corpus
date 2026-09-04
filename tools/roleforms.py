#!/usr/bin/env python3
"""ДОМ РОЛЕВЫХ ВОПРОСОВ — вопрос по ТИПУ ДЫРЫ: чем, где, из чего.

Коллегия назвала Д-1 обобщающим изъяном: вопрос есть ПОВЕРХНОСТЬ, купленная у
своего рода, а не операция над фактом; и лекарство названо там же —
инверсионный орган, рынок вопросных слов ПО ТИПУ ДЫРЫ (число, сущность, время,
место). Мир дыр (`holes`) держит время, место, сущность и число в
повествовании. Этот дом добавляет три типа, которых не было ни у кого:

  ОРУДИЕ    чем пишут? ручкой.
  МЕСТО     где покупают хлеб? в магазине.
  ВЕЩЕСТВО  из чего сделан стол? из дерева.

ОТВЕТ ОБЪЯВЛЕН ЦЕЛОЙ ФРАЗОЙ, И ЭТО РЕШЕНИЕ. «Ручкой» есть творительный,
«в магазине» — предложный с предлогом, «из дерева» — родительный с предлогом;
объявлять падежи порознь значило бы завести три падежные таблицы на девять
языков и ошибиться в каждой. Дом объявляет ОТВЕТ как он звучит, и ошибиться
может лишь в том, что и объявил, — а объявленное видно глазу.

Тип дыры есть РОД показа, и он один и тот же во всех девяти языках: рынок,
покупающий вопросное слово, покупает его при СВОЁМ типе дыры, а не при языке.

    python3 tools/roleforms.py    # самопроверка с мутантами
"""
ТИПЫ = ("орудие", "место", "вещество")

ЯЗЫКИ = {
    "ru": dict(
        орудие_воп="чем {д}? {о}.", место_воп="где {д}? {о}.", вещество_воп="из чего {д}? {о}.",
        орудие=(("пишут", "ручкой"), ("режут хлеб", "ножом"), ("едят суп", "ложкой"),
                ("рисуют", "карандашом"), ("копают землю", "лопатой")),
        место=(("покупают хлеб", "в магазине"), ("лечат больных", "в больнице"),
               ("учат детей", "в школе"), ("варят еду", "на кухне"), ("хранят книги", "в библиотеке")),
        вещество=(("сделан стол", "из дерева"), ("сделано окно", "из стекла"),
                  ("сделан ключ", "из металла"), ("испечён хлеб", "из муки"),
                  ("связан свитер", "из шерсти")),
    ),
    "en": dict(
        орудие_воп="what do people {д} with? {о}.", место_воп="where do people {д}? {о}.",
        вещество_воп="what is {д} made of? {о}.",
        орудие=(("write", "with a pen"), ("cut bread", "with a knife"), ("eat soup", "with a spoon"),
                ("draw", "with a pencil"), ("dig the ground", "with a spade")),
        место=(("buy bread", "in a shop"), ("treat the sick", "in a hospital"),
               ("teach children", "in a school"), ("cook food", "in a kitchen"),
               ("keep books", "in a library")),
        вещество=(("a table", "of wood"), ("a window", "of glass"), ("a key", "of metal"),
                  ("bread", "of flour"), ("a sweater", "of wool")),
    ),
    "de": dict(
        # ПОРЯДОК СЛОВ ЯЗЫКА ЖИВЁТ В ОБЪЯВЛЕНИИ, А НЕ В РАМКЕ: немецкий и
        # голландский ставят подлежащее сразу за глаголом («wo kauft man
        # Brot?»), и рамка, дописывавшая «man» в конец, давала «wo kauft Brot
        # man?» — верно по смыслу и ложно по речи. Подлежащее объявлено
        # ВНУТРИ клаузы, там, где язык его держит.
        орудие_воп="womit {д}? {о}.", место_воп="wo {д}? {о}.",
        вещество_воп="woraus ist {д} gemacht? {о}.",
        орудие=(("schreibt man", "mit einem Stift"), ("schneidet man Brot", "mit einem Messer"),
                ("isst man Suppe", "mit einem Löffel"), ("zeichnet man", "mit einem Bleistift"),
                ("gräbt man die Erde", "mit einem Spaten")),
        место=(("kauft man Brot", "in einem Laden"), ("behandelt man Kranke", "in einem Krankenhaus"),
               ("unterrichtet man Kinder", "in einer Schule"), ("kocht man Essen", "in einer Küche"),
               ("bewahrt man Bücher auf", "in einer Bibliothek")),
        вещество=(("ein Tisch", "aus Holz"), ("ein Fenster", "aus Glas"), ("ein Schlüssel", "aus Metall"),
                  ("Brot", "aus Mehl"), ("ein Pullover", "aus Wolle")),
    ),
    "fr": dict(
        # ЭВФОНИЧЕСКОЕ «-T-» ОБЪЯВЛЕНО ПРИ ГЛАГОЛЕ, А НЕ ДОПИСАНО РАМКОЙ:
        # французская инверсия вставляет «-t-» лишь тогда, когда глагол кончается
        # гласной («mange-t-on», «achète-t-on»), и не вставляет при «-t» или «-d»
        # («écrit-on»). Рамка, дописывавшая «-t-on» всякому, дала «écrit-t-on» —
        # тот же род, что немецкий порядок слов: строй языка живёт в объявлении.
        орудие_воп="avec quoi {д} ? {о}.", место_воп="où {д} ? {о}.",
        вещество_воп="en quoi est fait {д} ? {о}.",
        орудие=(("écrit-on", "avec un stylo"), ("coupe-t-on le pain", "avec un couteau"),
                ("mange-t-on la soupe", "avec une cuillère"), ("dessine-t-on", "avec un crayon"),
                ("creuse-t-on la terre", "avec une bêche")),
        место=(("achète-t-on le pain", "dans un magasin"), ("soigne-t-on les malades", "dans un hôpital"),
               ("enseigne-t-on aux enfants", "dans une école"), ("cuisine-t-on", "dans une cuisine"),
               ("garde-t-on les livres", "dans une bibliothèque")),
        вещество=(("une table", "en bois"), ("une fenêtre", "en verre"), ("une clé", "en métal"),
                  ("le pain", "en farine"), ("un pull", "en laine")),
    ),
    "es": dict(
        орудие_воп="¿con qué se {д}? {о}.", место_воп="¿dónde se {д}? {о}.",
        вещество_воп="¿de qué está hecho {д}? {о}.",
        орудие=(("escribe", "con un bolígrafo"), ("corta el pan", "con un cuchillo"),
                ("come la sopa", "con una cuchara"), ("dibuja", "con un lápiz"),
                ("cava la tierra", "con una pala")),
        место=(("compra el pan", "en una tienda"), ("cura a los enfermos", "en un hospital"),
               ("enseña a los niños", "en una escuela"), ("cocina la comida", "en una cocina"),
               ("guardan los libros", "en una biblioteca")),
        вещество=(("una mesa", "de madera"), ("una ventana", "de vidrio"), ("una llave", "de metal"),
                  ("el pan", "de harina"), ("un jersey", "de lana")),
    ),
    "it": dict(
        орудие_воп="con che cosa si {д}? {о}.", место_воп="dove si {д}? {о}.",
        вещество_воп="di che cosa è fatto {д}? {о}.",
        орудие=(("scrive", "con una penna"), ("taglia il pane", "con un coltello"),
                ("mangia la zuppa", "con un cucchiaio"), ("disegna", "con una matita"),
                ("scava la terra", "con una vanga")),
        место=(("compra il pane", "in un negozio"), ("curano i malati", "in un ospedale"),
               ("insegna ai bambini", "in una scuola"), ("cucina il cibo", "in una cucina"),
               ("conservano i libri", "in una biblioteca")),
        вещество=(("un tavolo", "di legno"), ("una finestra", "di vetro"), ("una chiave", "di metallo"),
                  ("il pane", "di farina"), ("un maglione", "di lana")),
    ),
    "pt": dict(
        орудие_воп="com que se {д}? {о}.", место_воп="onde se {д}? {о}.",
        вещество_воп="de que é feito {д}? {о}.",
        орудие=(("escreve", "com uma caneta"), ("corta o pão", "com uma faca"),
                ("come a sopa", "com uma colher"), ("desenha", "com um lápis"),
                ("cava a terra", "com uma pá")),
        место=(("compra o pão", "numa loja"), ("tratam os doentes", "num hospital"),
               ("ensina as crianças", "numa escola"), ("cozinha a comida", "numa cozinha"),
               ("guardam os livros", "numa biblioteca")),
        вещество=(("uma mesa", "de madeira"), ("uma janela", "de vidro"), ("uma chave", "de metal"),
                  ("o pão", "de farinha"), ("uma camisola", "de lã")),
    ),
    "nl": dict(
        орудие_воп="waarmee {д}? {о}.", место_воп="waar {д}? {о}.",
        вещество_воп="waarvan is {д} gemaakt? {о}.",
        орудие=(("schrijft men", "met een pen"), ("snijdt men brood", "met een mes"),
                ("eet men soep", "met een lepel"), ("tekent men", "met een potlood"),
                ("graaft men de grond", "met een schop")),
        место=(("koopt men brood", "in een winkel"), ("behandelt men zieken", "in een ziekenhuis"),
               ("onderwijst men kinderen", "in een school"), ("kookt men eten", "in een keuken"),
               ("bewaart men boeken", "in een bibliotheek")),
        вещество=(("een tafel", "van hout"), ("een raam", "van glas"), ("een sleutel", "van metaal"),
                  ("brood", "van meel"), ("een trui", "van wol")),
    ),
    "pl": dict(
        орудие_воп="czym się {д}? {о}.", место_воп="gdzie się {д}? {о}.",
        вещество_воп="z czego jest {д}? {о}.",
        орудие=(("pisze", "długopisem"), ("kroi chleb", "nożem"), ("je zupę", "łyżką"),
                ("rysuje", "ołówkiem"), ("kopie ziemię", "łopatą")),
        место=(("kupuje chleb", "w sklepie"), ("leczy chorych", "w szpitalu"),
               ("uczy dzieci", "w szkole"), ("gotuje jedzenie", "w kuchni"),
               ("przechowuje książki", "w bibliotece")),
        вещество=(("zrobiony stół", "z drewna"), ("zrobione okno", "ze szkła"),
                  ("zrobiony klucz", "z metalu"), ("upieczony chleb", "z mąki"),
                  ("zrobiony sweter", "z wełny")),
    ),
}

for _яз, _я in ЯЗЫКИ.items():
    for _т in ТИПЫ:
        assert _т in _я and f"{_т}_воп" in _я, (_яз, _т)
        assert len(_я[_т]) == len(ЯЗЫКИ["ru"][_т]), (_яз, _т, len(_я[_т]))


def показ(язык, тип, i):
    я = ЯЗЫКИ[язык]
    д, о = я[тип][i % len(я[тип])]
    return я[f"{тип}_воп"].format(д=д, о=о)


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for тип in ТИПЫ:
            for i in range(len(я[тип])):
                вон[показ(язык, тип, i)] = (язык, тип)
    return вон


ПОКАЗЫ = _все_показы()
# РАМКА С ЧУЖИМ ОТВЕТОМ — ЛОЖЬ: тип дыры объявлен, и ответ ему объявлен тоже.
# ОБРАЗЕЦ ЦЕЛИКОМ, А НЕ НАЧАЛО СТРОКИ (М-180-f2). Суд по началу читал «чем
# пишут? …» и звал ложью всякую строку, начавшуюся объявленным вопросом, —
# включая ту, где за честным ответом идёт ВТОРАЯ фраза соседа. Прибор ЛОВУШКИ
# НАЧАЛА поймал это удвоением показа: «чем пишут? ручкой. чем пишут? ручкой.»
# суду сказать нечего, а он звал ложью.
#
# ДЫРА ОТВЕТА НЕ ПЕРЕХОДИТ ГРАНИЦЫ ПРЕДЛОЖЕНИЯ («[^.?!]+»): ответ на вопрос о
# роли есть ОДНА клауза, и подмена ответа по-прежнему ловится, а речь соседа
# после точки — нет.
_ОБРАЗЦЫ = tuple(
    __import__("re").compile(
        __import__("re").escape(я[f"{тип}_воп"].format(д=д, о="\x00")).replace("\x00", "[^.?!]+"))
    for язык, я in ЯЗЫКИ.items() for тип in ТИПЫ for д, _ in я[тип])


def судить(строка):
    с = строка.strip()
    if с in ПОКАЗЫ:
        return True, True
    for образец in _ОБРАЗЦЫ:
        if образец.fullmatch(с):
            return True, False
    return False, False


def _самопроверка():
    мутанты = 0
    for язык, я in ЯЗЫКИ.items():
        for тип in ТИПЫ:
            с = показ(язык, тип, 0)
            assert судить(с) == (True, True), (язык, тип, с)
        # МУТАНТ: ответ ЧУЖОГО типа при своём вопросе
        д, _ = я["орудие"][0]
        _, чужой = я["место"][0]
        битая = я["орудие_воп"].format(д=д, о=чужой)
        assert судить(битая) == (True, False), (язык, битая)
        мутанты += 1
    for язык in ("ru", "en", "de", "pl"):
        for тип in ТИПЫ:
            print("  ", показ(язык, тип, 0)[:96])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, типов дыры {len(ТИПЫ)})")


if __name__ == "__main__":
    _самопроверка()
