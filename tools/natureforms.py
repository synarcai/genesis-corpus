#!/usr/bin/env python3
"""ДОМ ПРИРОДЫ — счётные факты о живом и вещах, и температура.

Владелец просил собеседника, умеющего «общаться на разные темы». Дом бытовых
тем дал определения и календарь; здесь — то, что человек знает о МИРЕ и о чём
спрашивает ребёнок: сколько у паука ног, сколько у человека зубов, при какой
температуре кипит вода.

ЦИКЛОВ ЗДЕСЬ ТРИ — ВРЕМЕНА ГОДА, ДНИ НЕДЕЛИ И МЕСЯЦЫ, — И РАМКА У НИХ ОДНА,
ибо род у них один: замыкание по остатку. Объявлены они СПИСКОМ, а не ветвями:
первая редакция дома писала каждому циклу свою ветвь, и две ветви оказались
одинаковы буква в букву — тот самый закон, написанный дважды, который у нас
числят безымянностью рода.

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
import closedworld  # noqa: E402 — закон цифрового скелета замкнутого мира
import plgram  # noqa: E402
import plural as _plural  # noqa: E402 — английский артикль гнётся ЗВУКОМ
import rugram  # noqa: E402

# ОПРОВЕРЖЕНИЕ ПРИМЕРОМ: пары фактов, где вещь ОДНА, а число РАЗНОЕ. Общее
# утверждение берётся с первого факта, контрпример — со второго, и оба уже
# объявлены: контрпример не пишется рукой, а НАХОДИТСЯ в объявленном.
#
# ПАРЫ ВЫВОДЯТСЯ ПО ЯЗЫКУ, А НЕ ЗАДАЮТСЯ ОБЩИМИ НОМЕРАМИ. Первая редакция
# объявила их номерами (0,1) и (8,9) — и это была ложь о доме: списки фактов
# НЕ параллельны (испанский и итальянский держат десять фактов, прочие
# двенадцать), и восьмой у них оказался иным. Вышло «tutti i veicoli hanno 7
# colori? no: il sistema solare ha 8 pianeti» — вопрос о транспорте,
# опровергнутый солнечной системой. Номер есть ссылка на ПОРЯДОК, а порядок у
# каждого языка свой; ссылаться надо на СВОЙСТВО — на вещь, которая одна, и
# число, которое разное.

# ЦИКЛЫ ОБЪЯВЛЕНЫ СПИСКОМ, А НЕ ВЕТВЯМИ: имя ряда → (ключ объявления, вопросная ли)
ЦИКЛ_ФОРМЫ = {"сезон": ("времена", False), "сезон_воп": ("времена", True),
              "день": ("дни", False), "день_воп": ("дни", True),
              "месяц": ("месяцы", False), "месяц_воп": ("месяцы", True)}

# факт = (носитель, носитель ПАРОЙ или None, вещь, число)
ЯЗЫКИ = {
    "ru": dict(
        утв="у {б} {n} {в}.",
        часть="у {б} {n} {в}. {в1} — часть {б}.",
        сезон="после {a} идёт {b}.", сезон_воп="после {a} идёт {b}. что идёт после {a}? {b}.",
        времена=(("зима", "зимы"), ("весна", "весны"), ("лето", "лета"), ("осень", "осени")),
        дни=(("понедельник", "понедельника"), ("вторник", "вторника"), ("среда", "среды"),
             ("четверг", "четверга"), ("пятница", "пятницы"), ("суббота", "субботы"),
             ("воскресенье", "воскресенья")),
        месяцы=(("январь", "января"), ("февраль", "февраля"), ("март", "марта"), ("апрель", "апреля"),
                ("май", "мая"), ("июнь", "июня"), ("июль", "июля"), ("август", "августа"),
                ("сентябрь", "сентября"), ("октябрь", "октября"), ("ноябрь", "ноября"),
                ("декабрь", "декабря")),
        опроверж="{о} {n1} {в1}? нет: у {б2} {n2} {в2}.",
        общие=("у всех ли животных", "у всего ли транспорта"),
        пример="{о2} {n} {в}? у {б}.",
        общее_имя=("у какого животного", "у какого транспорта"),
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
        утв="{ба} has {n} {в}.",
        часть="{ба} has {n} {в}. {в1а} is a part of {ба}.",
        сезон="after {a} comes {b}.", сезон_воп="after {a} comes {b}. what comes after {a}? {b}.",
        времена=(("winter", "winter"), ("spring", "spring"), ("summer", "summer"), ("autumn", "autumn")),
        дни=(("monday", "monday"), ("tuesday", "tuesday"), ("wednesday", "wednesday"),
             ("thursday", "thursday"), ("friday", "friday"), ("saturday", "saturday"),
             ("sunday", "sunday")),
        месяцы=(("january", "january"), ("february", "february"), ("march", "march"), ("april", "april"),
                ("may", "may"), ("june", "june"), ("july", "july"), ("august", "august"),
                ("september", "september"), ("october", "october"), ("november", "november"),
                ("december", "december")),
        опроверж="{о} {n1} {в1}? no: {арт} {б2} has {n2} {в2}.",
        общие=("do all animals have", "do all vehicles have"),
        гласные="aeiou",
        пример="{о2} {n} {в}? a {б}.",
        общее_имя=("which animal has", "which vehicle has"),
        воп="{ба} has {n} {в}. how many {ва} does {ба} have? {n} {в}.",
        пара="{ба} has {n} {в}. how many {ва} do {бп} have? {r} {вr}: {n} × 2 = {r}.",
        факты=(("spider", "two spiders", ("leg", "legs", "a leg"), 8), ("insect", "two insects", ("leg", "legs", "a leg"), 6),
               ("cat", "two cats", ("paw", "paws", "a paw"), 4), ("bird", "two birds", ("wing", "wings", "a wing"), 2),
               ("person", "two people", ("finger", "fingers", "a finger"), 10), ("person", "two people", ("tooth", "teeth", "a tooth"), 32),
               ("person", "two people", ("hand", "hands", "a hand"), 2), ("person", "two people", ("eye", "eyes", "an eye"), 2),
               ("bicycle", "two bicycles", ("wheel", "wheels", "a wheel"), 2), ("car", "two cars", ("wheel", "wheels", "a wheel"), 4),
               ("rainbow", None, ("colour", "colours", "a colour"), 7), ("solar system", None, ("planet", "planets", "a planet"), 8)),
        темп="{ч} {г} at a temperature of {n} {гр}.",
        темп_воп="{ч} {г} at a temperature of {n} {гр}. at what temperature does {ч} {г0}? at a temperature of {n} {гр}.",
        температуры=(("water", "boils", 100), ("water", "freezes", 0)),
        градус=("degree", "degrees"),
    ),
    "de": dict(
        утв="{б} hat {n} {в}.",
        часть="{б} hat {n} {в}. {в1а} ist ein Teil davon.",
        сезон="nach {a} kommt {b}.", сезон_воп="nach {a} kommt {b}. was kommt nach {a}? {b}.",
        времена=(("der Winter", "dem Winter"), ("der Frühling", "dem Frühling"),
                 ("der Sommer", "dem Sommer"), ("der Herbst", "dem Herbst")),
        дни=(("der Montag", "dem Montag"), ("der Dienstag", "dem Dienstag"),
             ("der Mittwoch", "dem Mittwoch"), ("der Donnerstag", "dem Donnerstag"),
             ("der Freitag", "dem Freitag"), ("der Samstag", "dem Samstag"),
             ("der Sonntag", "dem Sonntag")),
        месяцы=(("der Januar", "dem Januar"), ("der Februar", "dem Februar"), ("der März", "dem März"),
                ("der April", "dem April"), ("der Mai", "dem Mai"), ("der Juni", "dem Juni"),
                ("der Juli", "dem Juli"), ("der August", "dem August"), ("der September", "dem September"),
                ("der Oktober", "dem Oktober"), ("der November", "dem November"),
                ("der Dezember", "dem Dezember")),
        опроверж="{о} {n1} {в1}? nein: {б2} hat {n2} {в2}.",
        общие=("haben alle Tiere", "haben alle Fahrzeuge"),
        пример="{о2} {n} {в}? {б}.",
        общее_имя=("welches Tier hat", "welches Fahrzeug hat"),
        воп="{б} hat {n} {в}. wie viele {ва} hat {б}? {n} {в}.",
        пара="{б} hat {n} {в}. wie viele {ва} haben {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("eine Spinne", "zwei Spinnen", ("Bein", "Beine", "ein Bein"), 8), ("ein Insekt", "zwei Insekten", ("Bein", "Beine", "ein Bein"), 6),
               ("eine Katze", "zwei Katzen", ("Pfote", "Pfoten", "eine Pfote"), 4), ("ein Vogel", "zwei Vögel", ("Flügel", "Flügel", "ein Flügel"), 2),
               ("ein Mensch", "zwei Menschen", ("Finger", "Finger", "ein Finger"), 10), ("ein Mensch", "zwei Menschen", ("Zahn", "Zähne", "ein Zahn"), 32),
               ("ein Mensch", "zwei Menschen", ("Hand", "Hände", "eine Hand"), 2), ("ein Mensch", "zwei Menschen", ("Auge", "Augen", "ein Auge"), 2),
               ("ein Fahrrad", "zwei Fahrräder", ("Rad", "Räder", "ein Rad"), 2), ("ein Auto", "zwei Autos", ("Rad", "Räder", "ein Rad"), 4),
               ("ein Regenbogen", None, ("Farbe", "Farben", "eine Farbe"), 7), ("das Sonnensystem", None, ("Planet", "Planeten", "ein Planet"), 8)),
        темп="{ч} {г} bei einer Temperatur von {n} {гр}.",
        темп_воп="{ч} {г} bei einer Temperatur von {n} {гр}. bei welcher Temperatur {г} {ч}? bei einer Temperatur von {n} {гр}.",
        температуры=(("Wasser", "kocht", 100), ("Wasser", "gefriert", 0)),
        градус=("Grad", "Grad"),
    ),
    "fr": dict(
        утв="{б} a {n} {в}.",
        часть="{б} a {n} {в}. {в1а} en est une partie.",
        сезон="après {a} vient {b}.", сезон_воп="après {a} vient {b}. qu'est-ce qui vient après {a} ? {b}.",
        времена=(("l'hiver", "l'hiver"), ("le printemps", "le printemps"),
                 ("l'été", "l'été"), ("l'automne", "l'automne")),
        дни=(("le lundi", "le lundi"), ("le mardi", "le mardi"), ("le mercredi", "le mercredi"),
             ("le jeudi", "le jeudi"), ("le vendredi", "le vendredi"), ("le samedi", "le samedi"),
             ("le dimanche", "le dimanche")),
        месяцы=(("janvier", "janvier"), ("février", "février"), ("mars", "mars"), ("avril", "avril"),
                ("mai", "mai"), ("juin", "juin"), ("juillet", "juillet"), ("août", "août"),
                ("septembre", "septembre"), ("octobre", "octobre"), ("novembre", "novembre"),
                ("décembre", "décembre")),
        опроверж="{о} {n1} {в1} ? non : {б2} a {n2} {в2}.",
        общие=("est-ce que tous les animaux ont", "est-ce que tous les véhicules ont"),
        пример="{о2} {n} {в} ? {б}.",
        общее_имя=("quel animal a", "quel véhicule a"),
        воп="{б} a {n} {в}. combien de {ва} a {б} ? {n} {в}.",
        пара="{б} a {n} {в}. combien de {ва} ont {бп} ? {r} {вr} : {n} × 2 = {r}.",
        факты=(("une araignée", "deux araignées", ("patte", "pattes", "une patte"), 8), ("un insecte", "deux insectes", ("patte", "pattes", "une patte"), 6),
               ("un chat", "deux chats", ("patte", "pattes", "une patte"), 4), ("un oiseau", "deux oiseaux", ("aile", "ailes", "une aile"), 2),
               ("une personne", "deux personnes", ("doigt", "doigts", "un doigt"), 10), ("une personne", "deux personnes", ("dent", "dents", "une dent"), 32),
               ("une personne", "deux personnes", ("main", "mains", "une main"), 2), ("une personne", "deux personnes", ("œil", "yeux", "un œil"), 2),
               ("un vélo", "deux vélos", ("roue", "roues", "une roue"), 2), ("une voiture", "deux voitures", ("roue", "roues", "une roue"), 4),
               ("un arc-en-ciel", None, ("couleur", "couleurs", "une couleur"), 7), ("le système solaire", None, ("planète", "planètes", "une planète"), 8)),
        темп="{ч} {г} à une température de {n} {гр}.",
        темп_воп="{ч} {г} à une température de {n} {гр}. à quelle température {г} {ч} ? à une température de {n} {гр}.",
        температуры=(("l'eau", "bout", 100), ("l'eau", "gèle", 0)),
        градус=("degré", "degrés"),
    ),
    "es": dict(
        утв="{б} tiene {n} {в}.",
        часть="{б} tiene {n} {в}. {в1а} forma parte de ello.",
        сезон="después {a} viene {b}.", сезон_воп="después {a} viene {b}. ¿qué viene después {a}? {b}.",
        времена=(("el invierno", "del invierno"), ("la primavera", "de la primavera"),
                 ("el verano", "del verano"), ("el otoño", "del otoño")),
        дни=(("el lunes", "del lunes"), ("el martes", "del martes"), ("el miércoles", "del miércoles"),
             ("el jueves", "del jueves"), ("el viernes", "del viernes"), ("el sábado", "del sábado"),
             ("el domingo", "del domingo")),
        месяцы=(("enero", "de enero"), ("febrero", "de febrero"), ("marzo", "de marzo"),
                ("abril", "de abril"), ("mayo", "de mayo"), ("junio", "de junio"),
                ("julio", "de julio"), ("agosto", "de agosto"), ("septiembre", "de septiembre"),
                ("octubre", "de octubre"), ("noviembre", "de noviembre"), ("diciembre", "de diciembre")),
        опроверж="{о} {n1} {в1}? no: {б2} tiene {n2} {в2}.",
        общие=("¿tienen todos los animales", "¿tienen todos los vehículos"),
        пример="{о2} {n} {в}? {б}.",
        общее_имя=("¿qué animal tiene", "¿qué vehículo tiene"),
        воп="{б} tiene {n} {в}. ¿cuántas {ва} tiene {б}? {n} {в}.",
        пара="{б} tiene {n} {в}. ¿cuántas {ва} tienen {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("una araña", "dos arañas", ("pata", "patas", "una pata"), 8), ("un insecto", "dos insectos", ("pata", "patas", "una pata"), 6),
               ("un gato", "dos gatos", ("pata", "patas", "una pata"), 4), ("un pájaro", "dos pájaros", ("ala", "alas", "un ala"), 2),
               ("una persona", "dos personas", ("mano", "manos", "una mano"), 2), ("una persona", "dos personas", ("ojo", "ojos", "un ojo"), 2),
               ("una bicicleta", "dos bicicletas", ("rueda", "ruedas", "una rueda"), 2), ("un coche", "dos coches", ("rueda", "ruedas", "una rueda"), 4),
               ("un arcoíris", None, ("color", "colores", "un color"), 7), ("el sistema solar", None, ("planeta", "planetas", "un planeta"), 8)),
        темп="{ч} {г} a una temperatura de {n} {гр}.",
        темп_воп="{ч} {г} a una temperatura de {n} {гр}. ¿a qué temperatura {г} {ч}? a una temperatura de {n} {гр}.",
        температуры=(("el agua", "hierve", 100), ("el agua", "se congela", 0)),
        градус=("grado", "grados"),
    ),
    "it": dict(
        утв="{б} ha {n} {в}.",
        часть="{б} ha {n} {в}. {в1а} ne è una parte.",
        сезон="dopo {a} viene {b}.", сезон_воп="dopo {a} viene {b}. che cosa viene dopo {a}? {b}.",
        времена=(("l'inverno", "l'inverno"), ("la primavera", "la primavera"),
                 ("l'estate", "l'estate"), ("l'autunno", "l'autunno")),
        дни=(("il lunedì", "il lunedì"), ("il martedì", "il martedì"), ("il mercoledì", "il mercoledì"),
             ("il giovedì", "il giovedì"), ("il venerdì", "il venerdì"), ("il sabato", "il sabato"),
             ("la domenica", "la domenica")),
        месяцы=(("gennaio", "gennaio"), ("febbraio", "febbraio"), ("marzo", "marzo"), ("aprile", "aprile"),
                ("maggio", "maggio"), ("giugno", "giugno"), ("luglio", "luglio"), ("agosto", "agosto"),
                ("settembre", "settembre"), ("ottobre", "ottobre"), ("novembre", "novembre"),
                ("dicembre", "dicembre")),
        опроверж="{о} {n1} {в1}? no: {б2} ha {n2} {в2}.",
        общие=("hanno tutti gli animali", "hanno tutti i veicoli"),
        пример="{о2} {n} {в}? {б}.",
        общее_имя=("quale animale ha", "quale veicolo ha"),
        воп="{б} ha {n} {в}. quante {ва} ha {б}? {n} {в}.",
        пара="{б} ha {n} {в}. quante {ва} hanno {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("un ragno", "due ragni", ("zampa", "zampe", "una zampa"), 8), ("un insetto", "due insetti", ("zampa", "zampe", "una zampa"), 6),
               ("un gatto", "due gatti", ("zampa", "zampe", "una zampa"), 4), ("un uccello", "due uccelli", ("ala", "ali", "un'ala"), 2),
               ("una persona", "due persone", ("mano", "mani", "una mano"), 2), ("una persona", "due persone", ("occhio", "occhi", "un occhio"), 2),
               ("una bicicletta", "due biciclette", ("ruota", "ruote", "una ruota"), 2), ("un'auto", "due auto", ("ruota", "ruote", "una ruota"), 4),
               ("un arcobaleno", None, ("colore", "colori", "un colore"), 7), ("il sistema solare", None, ("pianeta", "pianeti", "un pianeta"), 8)),
        темп="{ч} {г} a una temperatura di {n} {гр}.",
        темп_воп="{ч} {г} a una temperatura di {n} {гр}. a che temperatura {г} {ч}? a una temperatura di {n} {гр}.",
        температуры=(("l'acqua", "bolle", 100), ("l'acqua", "gela", 0)),
        градус=("grado", "gradi"),
    ),
    "pt": dict(
        утв="{б} tem {n} {в}.",
        часть="{б} tem {n} {в}. {в1а} faz parte disso.",
        сезон="depois {a} vem {b}.", сезон_воп="depois {a} vem {b}. o que vem depois {a}? {b}.",
        времена=(("o inverno", "do inverno"), ("a primavera", "da primavera"),
                 ("o verão", "do verão"), ("o outono", "do outono")),
        дни=(("a segunda-feira", "da segunda-feira"), ("a terça-feira", "da terça-feira"),
             ("a quarta-feira", "da quarta-feira"), ("a quinta-feira", "da quinta-feira"),
             ("a sexta-feira", "da sexta-feira"), ("o sábado", "do sábado"),
             ("o domingo", "do domingo")),
        месяцы=(("janeiro", "de janeiro"), ("fevereiro", "de fevereiro"), ("março", "de março"),
                ("abril", "de abril"), ("maio", "de maio"), ("junho", "de junho"),
                ("julho", "de julho"), ("agosto", "de agosto"), ("setembro", "de setembro"),
                ("outubro", "de outubro"), ("novembro", "de novembro"), ("dezembro", "de dezembro")),
        опроверж="{о} {n1} {в1}? não: {б2} tem {n2} {в2}.",
        общие=("todos os animais têm", "todos os veículos têm"),
        пример="{о2} {n} {в}? {б}.",
        общее_имя=("que animal tem", "que veículo tem"),
        воп="{б} tem {n} {в}. quantas {ва} tem {б}? {n} {в}.",
        пара="{б} tem {n} {в}. quantas {ва} têm {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("uma aranha", "duas aranhas", ("pata", "patas", "uma pata"), 8), ("um inseto", "dois insetos", ("pata", "patas", "uma pata"), 6),
               ("um gato", "dois gatos", ("pata", "patas", "uma pata"), 4), ("um pássaro", "dois pássaros", ("asa", "asas", "uma asa"), 2),
               ("uma pessoa", "duas pessoas", ("mão", "mãos", "uma mão"), 2), ("uma pessoa", "duas pessoas", ("olho", "olhos", "um olho"), 2),
               ("uma bicicleta", "duas bicicletas", ("roda", "rodas", "uma roda"), 2), ("um carro", "dois carros", ("roda", "rodas", "uma roda"), 4),
               ("um arco-íris", None, ("cor", "cores", "uma cor"), 7), ("o sistema solar", None, ("planeta", "planetas", "um planeta"), 8)),
        темп="{ч} {г} a uma temperatura de {n} {гр}.",
        темп_воп="{ч} {г} a uma temperatura de {n} {гр}. a que temperatura {г} {ч}? a uma temperatura de {n} {гр}.",
        температуры=(("a água", "ferve", 100), ("a água", "congela", 0)),
        градус=("grau", "graus"),
    ),
    "nl": dict(
        утв="{б} heeft {n} {в}.",
        часть="{б} heeft {n} {в}. {в1а} is er een deel van.",
        сезон="na {a} komt {b}.", сезон_воп="na {a} komt {b}. wat komt na {a}? {b}.",
        времена=(("de winter", "de winter"), ("de lente", "de lente"),
                 ("de zomer", "de zomer"), ("de herfst", "de herfst")),
        дни=(("de maandag", "de maandag"), ("de dinsdag", "de dinsdag"), ("de woensdag", "de woensdag"),
             ("de donderdag", "de donderdag"), ("de vrijdag", "de vrijdag"), ("de zaterdag", "de zaterdag"),
             ("de zondag", "de zondag")),
        месяцы=(("januari", "januari"), ("februari", "februari"), ("maart", "maart"), ("april", "april"),
                ("mei", "mei"), ("juni", "juni"), ("juli", "juli"), ("augustus", "augustus"),
                ("september", "september"), ("oktober", "oktober"), ("november", "november"),
                ("december", "december")),
        опроверж="{о} {n1} {в1}? nee: {б2} heeft {n2} {в2}.",
        общие=("hebben alle dieren", "hebben alle voertuigen"),
        пример="{о2} {n} {в}? {б}.",
        общее_имя=("welk dier heeft", "welk voertuig heeft"),
        воп="{б} heeft {n} {в}. hoeveel {ва} heeft {б}? {n} {в}.",
        пара="{б} heeft {n} {в}. hoeveel {ва} hebben {бп}? {r} {вr}: {n} × 2 = {r}.",
        факты=(("een spin", "twee spinnen", ("poot", "poten", "een poot"), 8), ("een insect", "twee insecten", ("poot", "poten", "een poot"), 6),
               ("een kat", "twee katten", ("poot", "poten", "een poot"), 4), ("een vogel", "twee vogels", ("vleugel", "vleugels", "een vleugel"), 2),
               ("een mens", "twee mensen", ("hand", "handen", "een hand"), 2), ("een mens", "twee mensen", ("oog", "ogen", "een oog"), 2),
               ("een fiets", "twee fietsen", ("wiel", "wielen", "een wiel"), 2), ("een auto", "twee auto's", ("wiel", "wielen", "een wiel"), 4),
               ("een regenboog", None, ("kleur", "kleuren", "een kleur"), 7), ("het zonnestelsel", None, ("planeet", "planeten", "een planeet"), 8)),
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
        дни=(("poniedziałek", "poniedziałku"), ("wtorek", "wtorku"), ("środa", "środzie"),
             ("czwartek", "czwartku"), ("piątek", "piątku"), ("sobota", "sobocie"),
             ("niedziela", "niedzieli")),
        месяцы=(("styczeń", "styczniu"), ("luty", "lutym"), ("marzec", "marcu"), ("kwiecień", "kwietniu"),
                ("maj", "maju"), ("czerwiec", "czerwcu"), ("lipiec", "lipcu"), ("sierpień", "sierpniu"),
                ("wrzesień", "wrześniu"), ("październik", "październiku"), ("listopad", "listopadzie"),
                ("grudzień", "grudniu")),
        опроверж="{о} {n1} {в1}? nie: {б2} ma {n2} {в2}.",
        общие=("czy wszystkie zwierzęta mają", "czy wszystkie pojazdy mają"),
        пример="{о2} {n} {в}? {б}.",
        общее_имя=("które zwierzę ma", "który pojazd ma"),
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
ФОРМЫ = ("утв", "воп", "пара", "часть", "опроверж", "пример", "темп", "темп_воп") + tuple(ЦИКЛ_ФОРМЫ)


def вещь(язык, в, n):
    """Форма вещи при числе: у славянских — из своего дома счёта, у прочих —
    объявленная пара «один / много». Дом счёта не угадывается, а называется."""
    if язык == "ru":
        return rugram.форма(в, n)
    if язык == "pl":
        return plgram.форма(в, n)
    один, много = в[0], в[1]
    return один if n == 1 else много


# АРТИКЛЬ ЧАСТИ ОБЪЯВЛЕН ПРИ ЧАСТИ, А НЕ В РАМКЕ (08.09).
#
# Рамка отношения части к целому ставила артикль ЛИТЕРАЛОМ — «a {в1}», «ein {в1}», «une {в1}»,
# «una {в1}», «uma {в1}», — и он не гнулся ни родом вещи, ни её начальным звуком:
#
#     «a eye is a part of a person»      → an eye
#     «ein Pfote», «ein Hand», «ein Farbe» → eine
#     «une œil», «une doigt»               → un
#     «una ala», «una color», «una planeta» → un ala, un color, un planeta
#     «una colore», «una pianeta», «una occhio», «una ala» → un colore, un pianeta, un occhio, un'ala
#     «uma planeta»                        → um planeta
#
# ТОТ ЖЕ РОД, ЧТО У ПРИЧАСТИЯ В ДОМЕ РОЛЕЙ: рамка одна на все вещи, а род у каждой свой.
# Русский и польский артикля не знают и потому были правы во всех.
#
# ОБЪЯВЛЕН НЕ АРТИКЛЬ, А ЕДИНСТВЕННОЕ С АРТИКЛЕМ ЦЕЛИКОМ («un'ala», «an eye»): итальянская
# элизия и английское «an» суть не приставка к слову, а иное слово, и склеивать их рамкой
# значило бы завести правило начального звука в девяти языках.
def с_артиклем(язык, в):
    """Единственное число с артиклем, как его объявил язык; без объявления — голое слово."""
    if язык in ("ru", "pl"):
        return вещь(язык, в, 1)
    return в[2] if len(в) > 2 else вещь(язык, в, 1)


def _пары_опровержения(язык):
    """Пары фактов ОДНОЙ вещи с РАЗНЫМ числом, в порядке первого появления."""
    по_вещи = {}
    for б, _, в, n in ЯЗЫКИ[язык]["факты"]:
        по_вещи.setdefault(str(в), []).append((б, в, n))
    вон = []
    for ряд in по_вещи.values():
        разные = [ф for i, ф in enumerate(ряд) if all(ф[2] != g[2] for g in ряд[:i])]
        if len(разные) >= 2:
            вон.append((разные[0], разные[1]))
    return вон


def показ(язык, форма, i):
    я = ЯЗЫКИ[язык]
    if форма == "пример":
        # ПОДТВЕРЖДЕНИЕ ПРИМЕРОМ — вторая полярность опровержения, и без неё
        # первая учила бы только отрицанию. «Есть ли животное с 8 ногами? да:
        # паук.» Пример, как и контрпример, НАХОДИТСЯ в объявленных фактах, а
        # не пишется рукой; берётся он из той же пары, что и опровержение, —
        # первая её половина, — и потому обе полярности говорят об одном ряду.
        пары = _пары_опровержения(язык)
        if not пары:
            return None
        (б, в, n), _ = пары[i % len(пары)]
        # НОСИТЕЛЬ ЗДЕСЬ ПОДЛЕЖАЩЕЕ, А В ПРОЧИХ ФОРМАХ ДОПОЛНЕНИЕ: русский и
        # польский держат его в родительном («у паука»), и для ответа нужен
        # именительный. Он берётся из ряда сравнения, если язык его объявил,
        # иначе — как есть.
        гласные = я.get("гласные")
        имя = б
        if гласные:
            имя = ("an " if б and б[0].lower() in гласные else "a ") + б
            имя = имя[2:] if я["пример"].count("a {б}") else имя
        return я["пример"].format(о2=я["общее_имя"][i % len(я["общее_имя"])],
                                  n=n, в=вещь(язык, в, n), б=имя)
    if форма == "опроверж":
        # ОПРОВЕРЖЕНИЕ ПРИМЕРОМ — первый в доме показ, где ответ есть «НЕТ» с
        # ПРИЧИНОЙ. Общее утверждение («у всех ли животных 8 ног?») опровергается
        # не мнением, а ОБЪЯВЛЕННЫМ фактом («у насекомого 6 ног»), и потому
        # проверяемо тем же счётом, что и всё в доме. Пара берётся такая, где
        # вещь одна, а число разное: контрпример НАХОДИТСЯ в объявленном, а не
        # пишется рукой, и подделать его нельзя, не подделав самого факта.
        пары = _пары_опровержения(язык)
        if not пары:
            return None
        (б1, в1, n1), (б2, в2, n2) = пары[i % len(пары)]
        о = я["общие"][i % len(я["общие"])]
        # АРТИКЛЬ ПЕРЕД ГЛАСНОЙ ОБЪЯВЛЕН ГЛАСНЫМИ, А НЕ УГАДАН: «a insect»
        # неверно, «an insect» верно, и правило это язык объявляет сам —
        # язык без объявленных гласных артикля не ставит.
        гласные = я.get("гласные")
        арт = ("an" if гласные and б2 and б2[0].lower() in гласные else "a") if гласные else ""
        return я["опроверж"].format(о=о, n1=n1, в1=вещь(язык, в1, n1), арт=арт,
                                    б2=б2, n2=n2, в2=вещь(язык, в2, n2))
    if форма in ЦИКЛ_ФОРМЫ:
        # ЦИКЛ, А НЕ СПИСОК: после последнего идёт ПЕРВЫЙ, и замыкание есть то,
        # чем цикл отличается от перечня; строится оно тем же правилом, что и
        # прочие показы — остатком по длине, — и потому забыть его нельзя: оно
        # не дописано рукой, а выведено.
        #
        # И ЦИКЛОВ ЗДЕСЬ НЕСКОЛЬКО ПРИ ОДНОЙ РАМКЕ. Первая редакция дома писала
        # каждому циклу свою ветвь, и две ветви были одинаковы буква в букву —
        # тот самый закон, написанный дважды, который у нас числят безымянностью
        # рода. Циклы объявлены списком, ветвь одна: день, когда рамки должны
        # разойтись, будет виден, ибо разойтись им придётся ОБЪЯВЛЕНИЕМ.
        имя, вопросная = ЦИКЛ_ФОРМЫ[форма]
        ряд = я[имя]
        (_, a) = ряд[i % len(ряд)]
        (b, _) = ряд[(i + 1) % len(ряд)]
        return я["сезон_воп" if вопросная else "сезон"].format(a=a, b=b)
    if форма in ("темп", "темп_воп"):
        ч, г, n = я["температуры"][i % len(я["температуры"])]
        гр = вещь(язык, я["градус"], n)
        г0 = {"boils": "boil", "freezes": "freeze"}.get(г, г)
        return я[форма].format(ч=ч, г=г, г0=г0, n=n, гр=гр)
    б, бп, в, n = я["факты"][i % len(я["факты"])]
    поля = dict(б=б, бп=бп, n=n, в=вещь(язык, в, n), ва=вещь(язык, в, 5),
                в1=вещь(язык, в, 1), в1а=с_артиклем(язык, в), r=n * 2, вr=вещь(язык, в, n * 2),
                ба=(_plural.with_article(б) if язык == "en" else б))
    if форма == "пара" and бп is None:
        return None          # носитель без парной формы парного показа не пишет
    return я[форма].format(**поля)


def _все_показы():
    вон = {}
    for язык, я in ЯЗЫКИ.items():
        for форма in ("опроверж", "пример"):
            for i in range(len(_пары_опровержения(язык))):
                с = показ(язык, форма, i)
                if с:
                    вон[с] = (язык, форма)
        for форма in ("утв", "воп", "пара", "часть"):
            for i in range(len(я["факты"])):
                с = показ(язык, форма, i)
                if с:
                    вон[с] = (язык, форма)
        for форма in ("темп", "темп_воп"):
            for i in range(len(я["температуры"])):
                вон[показ(язык, форма, i)] = (язык, форма)
        for форма, (имя, _) in ЦИКЛ_ФОРМЫ.items():
            for i in range(len(я[имя])):
                вон[показ(язык, форма, i)] = (язык, форма)
    return вон


ПОКАЗЫ = _все_показы()


def _судить_рамкой(строка):
    с = строка.strip()
    return (True, True) if с in ПОКАЗЫ else (False, False)



# ЗАКОН ЦИФРОВОГО СКЕЛЕТА (05.09, прибор мутантов: суд ОНЕМЕЛ на порче одного числа).
# Строка, отличающаяся от показа ЛИШЬ ЦИФРАМИ, есть строка этого дома и, не будучи показом,
# есть его ЛОЖЬ: мир объявлен замкнутым, а цифра формы не меняет.
_СКЕЛЕТЫ = closedworld.скелеты(ПОКАЗЫ)


def _судить_образцом(строка):
    вердикт = _судить_рамкой(строка)
    if вердикт[0] is False and closedworld.ложь_по_цифре(строка, _СКЕЛЕТЫ, ПОКАЗЫ):
        return True, False
    return вердикт

def _самопроверка():
    мутанты = 0
    for язык in ЯЗЫКИ:
        for форма in ФОРМЫ:
            с = показ(язык, форма, 0)
            assert с and судить(с) == (True, True), (язык, форма, с)
        # МУТАНТ: подменённое число не есть показ дома
        битый = показ(язык, "воп", 0).replace(" 8 ", " 9 ")
        if битый != показ(язык, "воп", 0):
            # ПОРЧА ЧИСЛА — ЛОЖЬ ДОМА, А НЕ ЧУЖАЯ СТРОКА (05.09, закон цифрового скелета):
            # прежде дом молчал на «у паука 9 ног», и молчание палата отдавала соседу
            assert судить(битый) == (True, False), (язык, битый)
            мутанты += 1
    for язык in ("ru", "en", "de", "pl"):
        print("  ", показ(язык, "пара", 0)[:112])
        print("  ", показ(язык, "темп_воп", 0)[:112])
    print(f"  мутантов поймано: {мутанты}")
    print(f"  дом пишет показов: {len(ПОКАЗЫ)} (языков {len(ЯЗЫКИ)}, форм {len(ФОРМЫ)})")




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
