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
# ШЕСТОЕ ВЕЩЕСТВО КУПЛЕНО ЗАКОНОМ ПОВТОРЕНИЯ (08.09). Причастие, объявленное при вещи,
# исправило двенадцать ложных строк — и оставило португальское «feito» стоять в своде ОДИН
# раз: из пяти вещей португальского четыре женского рода. Прибор `word_once` назвал это в
# тот же час.
#
#     ПОЧИН, ВЕРНЫЙ ПО РЕЧИ, БЫВАЕТ ДОЛГОМ ПО ЗАКОНУ ПОВТОРЕНИЯ: правильная форма, стоящая
#     однажды, не показана.
#
# Шестая вещь — книга из бумаги — взята мужского рода там, где язык его даёт, и тем ставит
# вторую опору под каждое мужское причастие.
ТИПЫ = ("орудие", "место", "вещество")

ЯЗЫКИ = {
    "ru": dict(
        орудие_утв="{д} {о}.", место_утв="{д} {о}.", вещество_утв="{у} {о}.",
        орудие_воп="чем {д}? {о}.", место_воп="где {д}? {о}.", вещество_воп="из чего {д}? {о}.",
        орудие=(("пишут", "ручкой"), ("режут хлеб", "ножом"), ("едят суп", "ложкой"),
                ("рисуют", "карандашом"), ("копают землю", "лопатой")),
        место=(("покупают хлеб", "в магазине"), ("лечат больных", "в больнице"),
               ("учат детей", "в школе"), ("варят еду", "на кухне"), ("хранят книги", "в библиотеке")),
        вещество=(("сделан стол", "из дерева", "", "стол сделан"),
                  ("сделано окно", "из стекла", "", "окно сделано"),
                  ("сделан ключ", "из металла", "", "ключ сделан"),
                  ("испечён хлеб", "из муки", "", "хлеб испечён"),
                  ("связан свитер", "из шерсти", "", "свитер связан"),
                  ("сделана книга", "из бумаги", "", "книга сделана")),
    ),
    "en": dict(
        орудие_утв="people {д} {о}.", место_утв="people {д} {о}.", вещество_утв="{д} is made {о}.",
        орудие_воп="what do people {д} with? {о}.", место_воп="where do people {д}? {о}.",
        вещество_воп="what is {д} made of? {о}.",
        орудие=(("write", "with a pen"), ("cut bread", "with a knife"), ("eat soup", "with a spoon"),
                ("draw", "with a pencil"), ("dig the ground", "with a spade")),
        место=(("buy bread", "in a shop"), ("treat the sick", "in a hospital"),
               ("teach children", "in a school"), ("cook food", "in a kitchen"),
               ("keep books", "in a library")),
        вещество=(("a table", "of wood"), ("a window", "of glass"), ("a key", "of metal"),
                  ("bread", "of flour"), ("a sweater", "of wool"), ("a book", "of paper")),
    ),
    "de": dict(
        орудие_утв="{о} {д}.", место_утв="{о} {д}.", вещество_утв="{д} ist {о} gemacht.",
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
                  ("Brot", "aus Mehl"), ("ein Pullover", "aus Wolle"), ("ein Buch", "aus Papier")),
    ),
    "fr": dict(
        орудие_утв="on {д} {о}.", место_утв="on {д} {о}.", вещество_утв="{д} est {пр} {о}.",
        # ЭВФОНИЧЕСКОЕ «-T-» ОБЪЯВЛЕНО ПРИ ГЛАГОЛЕ, А НЕ ДОПИСАНО РАМКОЙ:
        # французская инверсия вставляет «-t-» лишь тогда, когда глагол кончается
        # гласной («mange-t-on», «achète-t-on»), и не вставляет при «-t» или «-d»
        # («écrit-on»). Рамка, дописывавшая «-t-on» всякому, дала «écrit-t-on» —
        # тот же род, что немецкий порядок слов: строй языка живёт в объявлении.
        орудие_воп="avec quoi {д} ? {о}.", место_воп="où {д} ? {о}.",
        вещество_воп="en quoi est {пр} {д} ? {о}.",
        орудие=(("écrit-on", "avec un stylo"), ("coupe-t-on le pain", "avec un couteau"),
                ("mange-t-on la soupe", "avec une cuillère"), ("dessine-t-on", "avec un crayon"),
                ("creuse-t-on la terre", "avec une bêche")),
        место=(("achète-t-on le pain", "dans un magasin"), ("soigne-t-on les malades", "dans un hôpital"),
               ("enseigne-t-on aux enfants", "dans une école"), ("cuisine-t-on", "dans une cuisine"),
               ("garde-t-on les livres", "dans une bibliothèque")),
        вещество=(("une table", "en bois", "faite"), ("une fenêtre", "en verre", "faite"),
                  ("une clé", "en métal", "faite"), ("le pain", "en farine", "fait"),
                  ("un pull", "en laine", "fait"), ("un livre", "en papier", "fait")),
    ),
    "es": dict(
        орудие_утв="se {д} {о}.", место_утв="se {д} {о}.", вещество_утв="{д} está {пр} {о}.",
        орудие_воп="¿con qué se {д}? {о}.", место_воп="¿dónde se {д}? {о}.",
        вещество_воп="¿de qué está {пр} {д}? {о}.",
        орудие=(("escribe", "con un bolígrafo"), ("corta el pan", "con un cuchillo"),
                ("come la sopa", "con una cuchara"), ("dibuja", "con un lápiz"),
                ("cava la tierra", "con una pala")),
        место=(("compra el pan", "en una tienda"), ("cura a los enfermos", "en un hospital"),
               ("enseña a los niños", "en una escuela"), ("cocina la comida", "en una cocina"),
               ("guardan los libros", "en una biblioteca")),
        вещество=(("una mesa", "de madera", "hecha"), ("una ventana", "de vidrio", "hecha"),
                  ("una llave", "de metal", "hecha"), ("el pan", "de harina", "hecho"),
                  ("un jersey", "de lana", "hecho"), ("un libro", "de papel", "hecho")),
    ),
    "it": dict(
        орудие_утв="si {д} {о}.", место_утв="si {д} {о}.", вещество_утв="{д} è {пр} {о}.",
        орудие_воп="con che cosa si {д}? {о}.", место_воп="dove si {д}? {о}.",
        вещество_воп="di che cosa è {пр} {д}? {о}.",
        орудие=(("scrive", "con una penna"), ("taglia il pane", "con un coltello"),
                ("mangia la zuppa", "con un cucchiaio"), ("disegna", "con una matita"),
                ("scava la terra", "con una vanga")),
        место=(("compra il pane", "in un negozio"), ("curano i malati", "in un ospedale"),
               ("insegna ai bambini", "in una scuola"), ("cucina il cibo", "in una cucina"),
               ("conservano i libri", "in una biblioteca")),
        вещество=(("un tavolo", "di legno", "fatto"), ("una finestra", "di vetro", "fatta"),
                  ("una chiave", "di metallo", "fatta"), ("il pane", "di farina", "fatto"),
                  ("un maglione", "di lana", "fatto"), ("un libro", "di carta", "fatto")),
    ),
    "pt": dict(
        орудие_утв="{д} {о}.", место_утв="{д} {о}.", вещество_утв="{д} é {пр} {о}.",
        орудие_воп="com que se {д}? {о}.", место_воп="onde se {д}? {о}.",
        вещество_воп="de que é {пр} {д}? {о}.",
        орудие=(("escreve", "com uma caneta"), ("corta o pão", "com uma faca"),
                ("come a sopa", "com uma colher"), ("desenha", "com um lápis"),
                ("cava a terra", "com uma pá")),
        место=(("compra o pão", "numa loja"), ("tratam os doentes", "num hospital"),
               ("ensina as crianças", "numa escola"), ("cozinha a comida", "numa cozinha"),
               ("guardam os livros", "numa biblioteca")),
        вещество=(("uma mesa", "de madeira", "feita"), ("uma janela", "de vidro", "feita"),
                  ("uma chave", "de metal", "feita"), ("o pão", "de farinha", "feito"),
                  ("uma camisola", "de lã", "feita"), ("um livro", "de papel", "feito")),
    ),
    "nl": dict(
        орудие_утв="{о} {д}.", место_утв="{о} {д}.", вещество_утв="{д} is {о} gemaakt.",
        орудие_воп="waarmee {д}? {о}.", место_воп="waar {д}? {о}.",
        вещество_воп="waarvan is {д} gemaakt? {о}.",
        орудие=(("schrijft men", "met een pen"), ("snijdt men brood", "met een mes"),
                ("eet men soep", "met een lepel"), ("tekent men", "met een potlood"),
                ("graaft men de grond", "met een schop")),
        место=(("koopt men brood", "in een winkel"), ("behandelt men zieken", "in een ziekenhuis"),
               ("onderwijst men kinderen", "in een school"), ("kookt men eten", "in een keuken"),
               ("bewaart men boeken", "in een bibliotheek")),
        вещество=(("een tafel", "van hout"), ("een raam", "van glas"), ("een sleutel", "van metaal"),
                  ("brood", "van meel"), ("een trui", "van wol"), ("een boek", "van papier")),
    ),
    "pl": dict(
        орудие_утв="{д} {о}.", место_утв="{д} {о}.", вещество_утв="{у} {о}.",
        орудие_воп="czym się {д}? {о}.", место_воп="gdzie się {д}? {о}.",
        вещество_воп="z czego jest {д}? {о}.",
        орудие=(("pisze", "długopisem"), ("kroi chleb", "nożem"), ("je zupę", "łyżką"),
                ("rysuje", "ołówkiem"), ("kopie ziemię", "łopatą")),
        место=(("kupuje chleb", "w sklepie"), ("leczy chorych", "w szpitalu"),
               ("uczy dzieci", "w szkole"), ("gotuje jedzenie", "w kuchni"),
               ("przechowuje książki", "w bibliotece")),
        вещество=(("zrobiony stół", "z drewna", "", "stół jest zrobiony"),
                  ("zrobione okno", "ze szkła", "", "okno jest zrobione"),
                  ("zrobiony klucz", "z metalu", "", "klucz jest zrobiony"),
                  ("upieczony chleb", "z mąki", "", "chleb jest upieczony"),
                  ("zrobiony sweter", "z wełny", "", "sweter jest zrobiony"),
                  ("zrobiona książka", "z papieru", "", "książka jest zrobiona")),
    ),
}

for _яз, _я in ЯЗЫКИ.items():
    for _т in ТИПЫ:
        assert _т in _я and f"{_т}_воп" in _я, (_яз, _т)
        assert len(_я[_т]) == len(ЯЗЫКИ["ru"][_т]), (_яз, _т, len(_я[_т]))


# ПРИЧАСТИЕ ОБЪЯВЛЕНО ПРИ ВЕЩИ, А НЕ В РАМКЕ (08.09).
#
# Рамка вещества четырёх романских языков держала причастие ЛИТЕРАЛОМ — «est fait», «está
# hecho», «è fatto», «é feito», — и оно не согласовывалось с родом вещи: «en quoi est fait
# une table ?», «¿de qué está hecho una mesa?», «di che cosa è fatto una finestra?», «de que
# é feito uma camisola?». Двенадцать страниц из двадцати были ложны по речи.
#
# РУССКИЙ И ПОЛЬСКИЙ БЫЛИ ПРАВЫ ВО ВСЕХ ПЯТИ, и не по удаче: они объявили причастие ВНУТРИ
# пары («сделан стол», «сделано окно», «zrobiony stół», «zrobione okno») — там, где стои́т
# вещь, чей род оно берёт.
#
#     ПРИЧАСТИЕ, ВЫНЕСЕННОЕ В РАМКУ, ПЕРЕСТАЁТ СОГЛАСОВЫВАТЬСЯ С ВЕЩЬЮ: рамка одна на все
#     вещи, а род у каждой свой.
#
# Пара, объявившая третье поле, отдаёт его дыре «{пр}»; пара из двух полей живёт как жила.
# ДЕЯНИЕ В УТВЕРЖДЕНИИ ОТЛИЧАЕТСЯ ОТ ДЕЯНИЯ В ВОПРОСЕ ТАМ, ГДЕ ЯЗЫК ЕГО ДВИГАЕТ (08.09).
#
# Дом объявлял деяние в ВОПРОСНОМ порядке — там, где инверсия и клитика стоя́т при вопросе:
# французское «écrit-on», португальское «escreve» с «se» в рамке, польское «pisze» с «się» в
# рамке. Утверждение двигает их обратно, и ход этот МЕХАНИЧЕСКИЙ и объявленный, а не рамочный:
#
#     fr: «écrit-on» → «écrit» (рамка ставит «on» впереди); «coupe-t-on le pain» → «coupe le pain»
#     pt: «escreve» → «escreve-se»; «corta o pão» → «corta-se o pão» (энклитика при ГЛАГОЛЕ)
#     pl: «pisze» → «pisze się»; «kupuje chleb» → «kupuje się chleb» (частица при ГЛАГОЛЕ)
#
# ГЛАГОЛ ЕСТЬ ПЕРВОЕ СЛОВО ДЕЯНИЯ, и это не догадка: деяние объявлено клаузой, начинающейся
# глаголом, во всех девяти языках. Немецкий и нидерландский обратного хода не требуют — их
# рамка выносит ответ вперёд, и порядок V2 остаётся верным сам собою.
def _деяние_утв(язык, тип, д):
    """Деяние в порядке утверждения — по объявленному ходу своего языка.

    ХОД КАСАЕТСЯ ЛИШЬ ТЕХ ТИПОВ, ЧЬЁ ДЕЯНИЕ ЕСТЬ КЛАУЗА. У вещества деяние есть ИМЕННАЯ
    ГРУППА («uma janela», «une table»), и клитика, поставленная в неё, дала «uma-se janela»
    — слова, которого нет. Тип назван поимённо, а не угадан по виду строки.
    """
    if тип == "вещество":
        return д
    if язык == "fr":
        глагол, _, хвост = д.partition(" ")
        for инверсия in ("-t-on", "-on"):
            if глагол.endswith(инверсия):
                глагол = глагол[:-len(инверсия)]
                break
        return (глагол + " " + хвост).strip()
    if язык in ("pt", "pl"):
        клитика = "-se" if язык == "pt" else " się"
        глагол, _, хвост = д.partition(" ")
        return (глагол + клитика + " " + хвост).strip()
    return д


def показ(язык, тип, i):
    """ФАКТ СКАЗАН И ТУТ ЖЕ СПРОШЕН — одной строкой.

    ЗАКОН ПОВТОРЕНИЯ ПЛАТИТСЯ НЕ НОВЫМИ СЛОВАМИ, А НОВОЙ РОЛЬЮ ДЛЯ СТАРЫХ. Дом писал только
    вопрос, и каждое его содержательное слово жило в своде РОВНО РАЗ (98 слов, прибор
    `word_once`). Утвердительная половина показывает те же слова вторично и НА ИНОМ МЕСТЕ
    РЕЧИ — подлежащим и дополнением там, где вопрос ставил их в дыру, — и не вводит ни одного
    нового слова.
    """
    я = ЯЗЫКИ[язык]
    ряд = я[тип][i % len(я[тип])]
    д, о = ряд[0], ряд[1]
    пр = ряд[2] if len(ряд) > 2 else ""
    у = ряд[3] if len(ряд) > 3 else _деяние_утв(язык, тип, д)
    утв = я[f"{тип}_утв"].format(д=_деяние_утв(язык, тип, д), о=о, пр=пр, у=у)
    воп = я[f"{тип}_воп"].format(д=д, о=о, пр=пр)
    return f"{утв} {воп}"


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
def _скелет(язык, тип, ряд):
    """Показ с ДЫРОЙ на месте ответа — образец, ловящий подмену ответа."""
    я = ЯЗЫКИ[язык]
    д, пр = ряд[0], (ряд[2] if len(ряд) > 2 else "")
    у = ряд[3] if len(ряд) > 3 else _деяние_утв(язык, тип, д)
    утв = я[f"{тип}_утв"].format(д=_деяние_утв(язык, тип, д), о="\x00", пр=пр, у=у)
    воп = я[f"{тип}_воп"].format(д=д, о="\x00", пр=пр)
    return f"{утв} {воп}"


_ОБРАЗЦЫ = tuple(
    __import__("re").compile(
        __import__("re").escape(_скелет(язык, тип, ряд)).replace("\x00", "[^.?!]+"))
    for язык, я in ЯЗЫКИ.items() for тип in ТИПЫ for ряд in я[тип])


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
        # МУТАНТ: ответ ЧУЖОГО типа при своём вопросе — ПОРЧА ЦЕЛОГО ПОКАЗА, а не половины.
        # Показ ныне есть факт И вопрос о нём, и мутант, испортивший лишь вопрос, был бы
        # чужой строкой, а не порченой: суд читает страницу целиком.
        д = я["орудие"][0][0]
        чужой = я["место"][0][1]
        свой = показ(язык, "орудие", 0)
        битая = свой.replace(я["орудие"][0][1], чужой)
        assert битая != свой, (язык, свой)
        assert судить(битая) == (True, False), (язык, битая)
        мутанты += 1
    for язык in ("ru", "en", "de", "pl"):
        for тип in ТИПЫ:
            print("  ", показ(язык, тип, 0)[:96])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, типов дыры {len(ТИПЫ)})")


if __name__ == "__main__":
    _самопроверка()
